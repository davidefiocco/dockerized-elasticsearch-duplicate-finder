def get_duplicate_documents(body, k, es):
    res = es.search(
        index="documents",
        source=["body"],
        size=k,
        query={"match": {"body": {"query": body, "analyzer": "my_analyzer"}}},
    )
    hits = res["hits"]["hits"]
    return {"id": [h["_id"] for h in hits], "score": [h["_score"] for h in hits]}
