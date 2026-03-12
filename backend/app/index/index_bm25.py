import argparse
from backend.app.search.bm25 import BM25Index


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True
    )

    parser.add_argument(
        "--out",
        required=True
    )

    args = parser.parse_args()

    index = BM25Index()

    print("Building BM25 index...")

    index.build(args.input)

    index.save(args.out)

    print("BM25 index saved.")


if __name__ == "__main__":
    main()