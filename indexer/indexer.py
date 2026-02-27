import json
import sys
import time

import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

corpus_filename = sys.argv[1]

INDEX_SETTINGS = {
    "analysis": {
        "filter": {
            "my_shingle_filter": {
                "type": "shingle",
                "min_shingle_size": 5,
                "max_shingle_size": 5,
                "output_unigrams": False,
            },
            "my_minhash_filter": {
                "type": "min_hash",
                "hash_count": 10,
                "bucket_count": 256,
                "hash_set_size": 1,
                "with_rotation": True,
            },
        },
        "analyzer": {
            "my_analyzer": {
                "tokenizer": "standard",
                "filter": ["my_shingle_filter", "my_minhash_filter"],
            }
        },
    }
}

INDEX_MAPPINGS = {"properties": {"body": {"type": "text", "analyzer": "my_analyzer"}}}


def load_corpus(filename):
    with open(filename) as f:
        return [json.loads(line) for line in f]


def get_client():
    es = Elasticsearch("http://elasticsearch:9200", request_timeout=120)
    for _ in range(100):
        try:
            es.cluster.health(wait_for_status="yellow")
            return es
        except Exception:
            time.sleep(2)
    raise RuntimeError("Could not connect to Elasticsearch")


def create_index(client):
    client.indices.create(
        index="documents",
        settings=INDEX_SETTINGS,
        mappings=INDEX_MAPPINGS,
    )


def generate_actions(corpus):
    for doc in corpus:
        yield {"_id": doc["id"], "body": doc["text"]}


def main():
    corpus = load_corpus(corpus_filename)
    es = get_client()

    if es.indices.exists(index="documents"):
        es.indices.delete(index="documents")

    create_index(es)

    total = len(corpus)
    print(f"Indexing {total} documents...")
    successes = 0
    for ok, _ in tqdm.tqdm(
        streaming_bulk(
            client=es, index="documents", actions=generate_actions(corpus), chunk_size=200
        ),
        total=total,
        unit="docs",
        miniters=max(1, total // 100),
    ):
        successes += ok
    print(f"Indexed {successes}/{total} documents")


if __name__ == "__main__":
    main()
