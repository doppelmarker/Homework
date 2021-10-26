"""Main module, contains entry point to the rss_news_reader."""
import sys
from pathlib import Path

# add rss_news_reader package's directory path to sys.path
rss_reader_pkg_dir_path = str(Path(__file__).parent.parent.resolve())
sys.path.insert(1, rss_reader_pkg_dir_path)

import logging

from rss_news_reader.config import Config
from rss_news_reader.reader import NewsNotFoundError, Reader

logger = logging.getLogger("rss-news-reader")


def main():
    """Main function, called when running the application"""
    config = Config()
    config.setup()

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
