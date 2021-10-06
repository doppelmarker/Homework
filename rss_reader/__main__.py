import logging

from config import config
from reader import Reader

logger = logging.getLogger("rss-reader")


def main():
    reader = Reader(config)
    try:
        reader.start()
    except Exception as e:
        logger.exception(e)
        print(f"Rss reader crashed from {type(e).__name__}")
        if not config.verbose:
            print("For more details consider using --verbose")


if __name__ == "__main__":
    main()
