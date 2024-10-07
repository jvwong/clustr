import sys
import argparse
import json_stream

from typing import IO, Generator, Dict, Any
from loguru import logger
from clustr.cluster import get

####################################################
#            Logging
####################################################


# logger.add("clustr_{time}.log")


####################################################
#            Command line args
####################################################

parser = argparse.ArgumentParser()
parser.add_argument("--threshold", nargs="?", type=float, default=str(0.990))
# parser.add_argument('--table', nargs='?', type=str, default='documents')
# parser.add_argument('--minyear', nargs='?', type=int, default=str(2021))


def get_opts():
    args = parser.parse_args()
    opts = {
        "threshold": args.threshold,
        # 'table': args.table,
        # 'minyear': args.minyear,
    }
    if opts["threshold"] < 0 or opts["threshold"] > 1:
        raise ValueError("threshold must be on [0, 1]")
    return opts


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
#                 __main__
####################################################

if __name__ == "__main__":
    opts = get_opts()
    logger.info("Run config: {opts}", opts=opts)

    reader = json2dict_reader(sys.stdin)
    # for item in reader:
    #     print(json.dumps(item, indent=2))
    clusters = get(reader)
    print(clusters)
