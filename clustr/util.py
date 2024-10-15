import json_stream
import json

from typing import Generator, Dict, Any, List

####################################################
#                  List
####################################################


def sort_descending_by(collection: List[Dict[str, Any]], k: str) -> List[Dict[str, Any]]:
    """Return a list of dictionaries sorted by key, descending"""
    return sorted(collection, key=lambda d: d[k], reverse=True)


def unique_by(collection: List[Dict[str, Any]], k: str) -> List[Dict[str, Any]]:
    """Return a list of unique dictionaries by key"""
    # TODO - is this right?
    mapp = []
    value_holder = set()
    for item in collection:
        v = item[k]
        if v not in value_holder:
            mapp.append(item)
            value_holder.add(v)
    return mapp


####################################################
#                  I/O
####################################################


def json2dict_reader(
    inpath: str,
) -> Generator[Dict[str, Any], None, None]:
    """Return a reader that streams json to list of dicts"""
    with open(inpath, "r") as f:
        data = json_stream.load(f)
        reader = json_stream.to_standard_types(data)
        yield from reader


def json2file(data: Dict[str, Any], fpath: str = "clusters.json"):
    """Write json to file"""
    with open(fpath, "w") as writer:
        json.dump(data, writer, indent=2)


def send_output(data: Dict[str, Any], fpath: str):
    """Send to stdout or write json to file"""
    if fpath:
        json2file(data, fpath)
    else:
        print(json.dumps(data, indent=2))


####################################################
#                  Clusters
####################################################


def get_article_clusters(
    clusters: List[List[int]],
    articles: List[Dict[str, Any]]
):
    """Return a dictionary of clustered articles"""
    result = {}
    for count, cluster in enumerate(clusters):
        result[count] = [articles[index] for index in cluster]
    return result
