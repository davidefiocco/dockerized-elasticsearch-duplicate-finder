def get_duplicate_documents(body, K, es):
    doc = {
        '_source': ['_id', 'body'],
        'size': K,
        'query': {
            "match": {
                "body": {
                    "query": body,
                    "analyzer" : "my_analyzer"
                }
            }
        }
    }

    res = es.search(index='documents', body=doc)
    top_matches = [hit['_source']['_id'] for hit in res['hits']['hits']]
    top_scores = [hit['_score'] for hit in res['hits']['hits']]
    return {'ArticleId': top_matches, 'score': top_scores}
