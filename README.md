# dockerized-elasticsearch-duplicate-finder

(try to) Use MinHash to find duplicates in an Elasticsearch index. 

Run with

```bash
docker-compose build
docker-compose up
```

The `classifier` container exposes an API that should return the ids of elements of the corpus that are near-duplicates of the query.
At least that's the idea! Code is not really working as of now...