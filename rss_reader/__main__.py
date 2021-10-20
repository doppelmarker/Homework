"""
Main module, contains entry point to the rss_reader.
"""
import sys
from pathlib import Path

# add rss_reader package path to sys.path
rss_reader_pkg_path = str(Path(__file__).parent.parent.resolve())
sys.path.insert(0, rss_reader_pkg_path)


import logging

from rss_reader.config import config
from rss_reader.reader import NewsNotFoundError, Reader

logger = logging.getLogger("rss-reader")


def main():
    """Main function, called when running the exported CLI utility or straightforwardly this module."""
    reader = Reader(config)
    try:
        reader.start()
    except NewsNotFoundError as e:
        logger.info(e)
    except Exception as e:
        # logger.exception(e)
        print(f"Rss reader crashed from {type(e).__name__}")
    finally:
        if not config.verbose:
            print("For more details consider using --verbose")


if __name__ == "__main__":
    main()
