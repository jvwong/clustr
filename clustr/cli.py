import sys
import argparse

from typing import IO, Generator, Dict, Any
from loguru import logger
from clustr import cluster
import util

####################################################
#            Logging
####################################################


# logger.add("clustr_{time}.log")


####################################################
#            Command line args
####################################################

parser = argparse.ArgumentParser()
parser.add_argument("--threshold", nargs="?", type=float, default=str(0.990))
parser.add_argument('--filepath', nargs='?', type=str, default='data/clusters.json')


def get_opts():
    args = parser.parse_args()
    opts = {
        "threshold": args.threshold,
        'filepath': args.filepath
    }
    if opts["threshold"] < 0 or opts["threshold"] > 1:
        raise ValueError("threshold must be on [0, 1]")
    return opts


####################################################
#                 __main__
####################################################

if __name__ == "__main__":
    opts = get_opts()
    logger.info("Run config: {opts}", opts=opts)

    # Stream in json data from stdin
    reader = util.json2dict_reader(sys.stdin)

    # Cluster the data
    clusters, articles = cluster.get(reader)
    result = util.get_article_clusters(clusters, articles)

    # Write to file
    util.json2file(result, opts.filepath)
