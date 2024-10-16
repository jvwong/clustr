import argparse

from loguru import logger
from clustr import cluster
from clustr import util

####################################################
#            Logging
####################################################


# logger.add("clustr_{time}.log")


####################################################
#            Command line args
####################################################

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str)
parser.add_argument("--threshold", nargs="?", type=float, default=str(0.96))
parser.add_argument("--outpath", nargs="?", type=str)


def get_args():
    args = parser.parse_args()
    if args.threshold < 0 or args.threshold > 1:
        raise ValueError("threshold must be on [0, 1]")
    return args


####################################################
#                 __main__
####################################################

if __name__ == "__main__":
    args = get_args()
    logger.info(vars(args))

    # Stream in json data from stdin
    reader = util.json2dict_reader(args.filename)

    # Cluster the data
    articles = [article for article in reader]
    articles = util.sort_descending_by(articles, "date")
    articles = util.unique_by(articles, "doi")
    clusters = cluster.get(articles, args.threshold)
    result = util.get_article_clusters(clusters, articles)

    # Write to file
    util.send_output(result, args.outpath)
