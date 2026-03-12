import argparse
from backend.app.search.vector import VectorIndex


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)

    args = parser.parse_args()

    index = VectorIndex()

    print("Building vector index...")

    index.build(args.input)

    index.save(args.out)

    print("Vector index saved.")


if __name__ == "__main__":
    main()