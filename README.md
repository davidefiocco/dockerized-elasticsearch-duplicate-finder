# dockerized-elasticsearch-duplicate-finder

Use Elasticsearch implementation of MinHash to find duplicates in an Elasticsearch index, as in my StackOverflow question https://stackoverflow.com/questions/63221732/why-does-my-query-using-a-minhash-analyzer-fail-to-retrieve-duplicates and mended with advice from https://stackoverflow.com/users/5362842/lupanoide (thanks!).

Run with

```bash
docker-compose build
docker-compose up
```

The `indexer` container adds example documents to an Elasticsearch index running in the `elasticsearch` container.
The `classifier` container exposes an API that is expected to return the ids of elements of the corpus that are near-duplicates of the query.