import json_stream
import json

from typing import IO, Generator, Dict, Any, List

####################################################
#                  Configuration
####################################################


####################################################
#                  Extract
####################################################

def json2dict_reader(
    stream: IO,
) -> Generator[Dict[str, Any], None, None]:
    """Return a reader that streams json to list of dicts"""
    data = json_stream.load(stream)
    reader = json_stream.to_standard_types(data)
    yield from reader


####################################################
#                  I/O
####################################################

def json2file(
    data: Dict[str, Any],
    fpath: str = "clusters.json"
):
    """Write json to file"""
    with open(fpath, "w") as writer:
        json.dump(data, writer, indent=2)


####################################################
#                  Clusters
####################################################

def get_article_clusters(
    clusters: List[List[int]],
    articles: List[Dict[str, Any]],
):
    """Return a dictionary of clustered articles"""
    result = {}
    for count, cluster in enumerate(clusters):
        result[count] = [articles[index] for index in cluster]
    return result
