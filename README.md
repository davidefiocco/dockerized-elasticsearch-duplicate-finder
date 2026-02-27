# dockerized-elasticsearch-duplicate-finder

Find near-duplicate documents using Elasticsearch's [MinHash](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-minhash-tokenfilter.html) token filter, running in Docker containers.

Based on [this StackOverflow question](https://stackoverflow.com/questions/63221732/why-does-my-query-using-a-minhash-analyzer-fail-to-retrieve-duplicates).

## Quick start

```bash
docker compose build
docker compose up
```

This indexes the example corpus at `data/mydocs.jsonl` and starts the API on port 8000.

## Query for duplicates

```bash
curl -X POST "http://localhost:8000/duplicates?k=5" \
  -H "Content-Type: application/json" \
  -d '{"text": "your text here"}'
```

## Using a custom corpus

Provide any JSONL file with `id` and `text` fields:

```jsonl
{"id": 1, "text": "First document"}
{"id": 2, "text": "Second document"}
```

Mount it by editing the indexer volume in `docker-compose.yml`:

```yaml
indexer:
  volumes:
    - ./path/to/your/corpus.jsonl:/data/corpus.jsonl:ro
```

Then `docker compose up` (add `--build` if the images haven't been built yet).

A download script for [HuggingFace's AG News dataset](https://huggingface.co/datasets/fancyzhx/ag_news) (120k articles) is included:

```bash
pip install datasets
python scripts/download_corpus.py 120000  # writes corpus.jsonl
```

## Stack

- **Elasticsearch 8.17** — MinHash analyzer (5-gram shingles, 256 hash buckets)
- **Indexer** — Python 3.12, bulk-indexes JSONL into ES
- **Classifier** — Python 3.12, FastAPI, exposes `/duplicates` endpoint
