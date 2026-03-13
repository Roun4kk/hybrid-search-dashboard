import argparse
import json
import os
from datetime import datetime


def read_documents(input_dir):
    docs = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt") or filename.endswith(".md"):
            path = os.path.join(input_dir, filename)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            doc = {
                "doc_id": filename,
                "title": filename.replace(".txt", "").replace(".md", ""),
                "text": text.strip(),
                "source": "local",
                "created_at": datetime.utcnow().isoformat()
            }

            docs.append(doc)

    return docs


def write_jsonl(docs, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)

    args = parser.parse_args()

    docs = read_documents(args.input)
    if not docs:
        raise ValueError("No documents found in input directory")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    output_file = args.out

    write_jsonl(docs, output_file)

    print(f"Ingested {len(docs)} documents")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()