from config import config
from reader import Reader


def main():
    reader = Reader(config)
    try:
        reader.start()
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
