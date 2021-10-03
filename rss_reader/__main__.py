from reader import Reader


def main():
    reader = Reader()
    try:
        reader.start()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
