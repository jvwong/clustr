import sys
import argparse

from loguru import logger

####################################################
#            Logging
####################################################


logger.add("cron_{time}.log")


####################################################
#            Command line args
####################################################

parser = argparse.ArgumentParser()
parser.add_argument('--threshold', nargs='?', type=float, default=str(0.990))
# parser.add_argument('--table', nargs='?', type=str, default='documents')
# parser.add_argument('--minyear', nargs='?', type=int, default=str(2021))


def get_opts():
    args = parser.parse_args()
    opts = {
        'threshold': args.threshold,
        # 'table': args.table,
        # 'minyear': args.minyear,
    }
    if opts['threshold'] < 0 or opts['threshold'] > 1:
        raise ValueError('threshold must be on [0, 1]')
    return opts

####################################################
#                  Extract
####################################################

def csv2dict_reader(stream: IO) -> Callable[[None], Generator[Dict[str, Any], None, None]]:
    """Return a reader that streams csv to dicts"""

    def _csv2dict_reader():
        reader = csv.DictReader(stream)
        yield from reader

    return _csv2dict_reader()

####################################################
#                 __main__
####################################################

if __name__ == '__main__':
    opts = get_opts()
    logger.info('Run config: {opts}', opts=opts)

    pipeline = as_pipeline(
        [
            csv2dict_reader(sys.stdin)
        ]
    )