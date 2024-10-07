import torch

from adapters import AutoAdapterModel
from loguru import logger
from typing import Generator, Any

from more_itertools import chunked
from sentence_transformers import util as sbert_util
from transformers import AutoTokenizer

####################################################
#                  Configuration
####################################################

SPECTER_MODEL = "allenai/specter2_aug2023refresh_base"  # base model for embedding
SPECTER_ADAPTOR = "allenai/specter2_aug2023refresh"  # adaptor to use with chosen specter model
ENCODER_MAX_LEN = 512  # Maximum number of tokens to pass to the encoder
MIN_ARTICLES_TO_CLUSTER = 100  # If there are less than this number of articles, skip clustering
MIN_ARTICLES_TO_AVOID_BACKOFF = 2  # If there are less than this number of clusters, perform backoff
BACKOFF_THRESHOLD = 0.02  # The amount to reduce the cosine similarity by during backoff


####################################################
#                  Parameters
####################################################

min_community_size = 2  # Minimum number of articles in a cluster
threshold = 0.96  # Cosine similarity threshold for clustering

####################################################
#                  Cluster
####################################################


def load_encoder():
    """Load an SPECTER-based text encoder for embedding titles and abstracts."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoAdapterModel.from_pretrained(SPECTER_MODEL)
    _ = model.load_adapter(SPECTER_ADAPTOR, source="hf", set_active=True)
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained(SPECTER_MODEL)
    return model, tokenizer


def embed_evidence(articles: list[str], model: str, _batch_size: int = 32):
    """Jointly embed the titles and abstracts in articles for the given encoder."""
    encoder, tokenizer = load_encoder()
    embeddings = []
    for batch in chunked(articles, _batch_size):
        text_batch = [f"{example['title']} {tokenizer.sep_token} {example['abstract']}" for example in batch]
        inputs = tokenizer(
            text_batch,
            padding=True,
            truncation=True,
            return_tensors="pt",
            return_token_type_ids=False,
            max_length=ENCODER_MAX_LEN,
        )
        inputs = inputs.to(encoder.device)
        output = encoder(**inputs)
        embeddings.append(output.last_hidden_state[:, 0, :])
        # Clear the cache to avoid OOM errors
        torch.cuda.empty_cache()
    return torch.cat(embeddings, dim=0)


def get(reader: Generator[Any, None, None]) -> None:
    print("Hello from get() in cluster.py")
    # temporarily read in the articles
    articles = [article for article in reader]
    num_articles = len(articles)

    # Default clusters are no clusters
    clusters = None

    if not num_articles >= MIN_ARTICLES_TO_CLUSTER:
        msg = f"Insufficient numbers of articles to cluster ({num_articles})"
        logger.error(msg)
        raise Exception(msg)

    logger.info("Clustering evidence")
    embeddings = embed_evidence(articles, model=SPECTER_MODEL)
    clusters = sbert_util.community_detection(embeddings, min_community_size=min_community_size, threshold=threshold)

    #                 # Try lowering the threshold if no clusters are found
    #                 backoff_threshold = threshold
    #                 while len(clusters) < MIN_ARTICLES_TO_AVOID_BACKOFF and backoff_threshold > 0.9:
    #                     backoff_threshold -= BACKOFF_THRESHOLD
    #                     st.warning(
    #                         f"No clusters found with threshold {threshold},"
    #                         f" trying a lower threshold ({backoff_threshold:.2f})...",
    #                         icon="⚠️",
    #                     )
    #                     clusters = sbert_util.community_detection(
    #                         embeddings, min_community_size=min_community_size, threshold=backoff_threshold
    #                     )

    if not clusters:
        logger.warning("No clusters found for your query. Randomly sampling articles instead")

    #                 max_cluster_size = len(max(clusters, key=len))
    #                 min_cluster_size = len(min(clusters, key=len))
    #                 avg_cluster_size = sum(len(cluster) for cluster in clusters) / len(clusters)
    #                 st.success(
    #                     f"Found {len(clusters)} clusters (max size: {max_cluster_size}, min size:"
    #                     f" {min_cluster_size}, mean size: {avg_cluster_size:.1f}) matching your query",
    #                     icon="✅",
    #                 )

    #                 if debug:
    #                     st.info(
    #                         f"The first {DEBUG_CLUSTER_SIZE} titles of the first {DEBUG_NUM_CLUSTERS} clusters, useful for"
    #                         " spot checking the clustering. Clusters are sorted by decreasing size. The first"
    #                         " element of each cluster is its centroid.\n"
    #                         + "\n".join(
    #                             f"\n__Cluster {i + 1}__ (size: {len(cluster)}):\n"
    #                             + "\n".join(f"- {articles[idx]['title']}" for idx in cluster[:DEBUG_CLUSTER_SIZE])
    #                             for i, cluster in enumerate(clusters[:DEBUG_NUM_CLUSTERS])
    #                         )
    #                     )
    #             else:
    #                 st.warning(
    #                     f"Less than {MIN_ARTICLES_TO_CLUSTER} total publications found, skipping clustering...", icon="⚠️"
    #                 )

    #             clusters = clusters or [[i] for i in range(len(articles))]
    return clusters
