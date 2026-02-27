from elasticsearch import Elasticsearch
from fastapi import FastAPI, Query
from pydantic import BaseModel

from util import get_duplicate_documents

app = FastAPI()

es = Elasticsearch("http://elasticsearch:9200")


class ClassificationInput(BaseModel):
    text: str


@app.post("/duplicates")
def duplicates(query: ClassificationInput, k: int = Query(default=10)):
    return {"duplicates_results": get_duplicate_documents(query.text, k, es)}
