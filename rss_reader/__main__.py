import logging

from rss_reader.config import config
from rss_reader.reader import NewsNotFoundError, Reader

logger = logging.getLogger("rss-reader")


def main():
    reader = Reader(config)
    try:
        reader.start()
    except NewsNotFoundError as e:
        logger.info(e)
    except Exception as e:
        logger.exception(e)
        print(f"Rss reader crashed from {type(e).__name__}")
    finally:
        if not config.verbose:
            print("For more details consider using --verbose")


if __name__ == "__main__":
    main()
