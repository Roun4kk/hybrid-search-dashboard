import os
import random

topics = [
    "machine learning", "artificial intelligence", "data science",
    "deep learning", "neural networks", "natural language processing",
    "computer vision", "reinforcement learning", "statistics",
    "data engineering", "big data", "cloud computing"
]

sentences = [
    "This document discusses concepts in {}.",
    "Modern systems rely heavily on {} techniques.",
    "{} is widely used in modern software systems.",
    "Researchers continue to improve methods in {}.",
    "Applications of {} are expanding rapidly."
]

os.makedirs("data/raw", exist_ok=True)

for i in range(1, 301):
    topic = random.choice(topics)

    text = "\n".join(
        [random.choice(sentences).format(topic) for _ in range(10)]
    )

    with open(f"data/raw/doc_{i}.txt", "w", encoding="utf-8") as f:
        f.write(text)

print("Generated 300 documents in data/raw/")