"""Download a text corpus from HuggingFace and save it as JSONL.

Usage: python scripts/download_corpus.py [NUM_DOCS]

Requires: pip install datasets
"""

import json
import sys

from datasets import load_dataset

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
ds = load_dataset("fancyzhx/ag_news", split=f"train[:{n}]")

with open("corpus.jsonl", "w") as f:
    for i, row in enumerate(ds):
        json.dump({"id": i, "text": row["text"]}, f)
        f.write("\n")

print(f"Wrote {n} documents to corpus.jsonl")
