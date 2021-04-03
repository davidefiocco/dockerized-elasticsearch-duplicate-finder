import pandas as pd
import json
import sys
import os
import time
import csv
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from elasticsearch.exceptions import ConnectionError

# start ES server
corpus_filename = sys.argv[1]


def get_client():
    # wait for ES yellow status
    es = Elasticsearch(hosts=[{"host": "elasticsearch"}], retry_on_timeout=True)

    for _ in range(100):
        try:
            es.cluster.health(wait_for_status="yellow")
            return es
        except ConnectionError:
            time.sleep(2)


def create_index(client):
    client.indices.create(
        index="documents",
        body={
            "settings": {
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
                            "bucket_count": 512,
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
            },
            "mappings": {
                "properties": {"body": {"type": "text", "analyzer": "my_analyzer"}}
            },
        },
        ignore=400,
    )


def generate_actions(corpus):

    for i in range(len(corpus)):
        doc = {"_id": corpus.iloc[i]["id"], "body": corpus.iloc[i]["text"]}

        yield doc


def main():

    corpus = pd.read_json(corpus_filename, lines=True)

    es = get_client()

    # delete index if it exists already
    if es.indices.exists(index="documents"):
        es.indices.delete(index="documents", ignore=[400, 404])

    create_index(es)

    print("Indexing documents...")

    progress = tqdm.tqdm(unit="docs", total=len(corpus))
    successes = 0
    for ok, action in streaming_bulk(
        client=es,
        index="documents",
        actions=generate_actions(corpus),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, len(corpus)))


if __name__ == "__main__":
    main()
