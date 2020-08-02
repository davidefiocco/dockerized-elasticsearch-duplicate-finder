from fastapi import FastAPI, Query
import json
from elasticsearch import Elasticsearch
import numpy as np
from util import get_duplicate_documents
from pydantic import BaseModel
import uvicorn

class ClassificationInput(BaseModel):
    text: str


app = FastAPI()

# connect to ES server
es = Elasticsearch(hosts=[{"host": "elasticsearch"}])
print("connected to ES server")


@app.post("/duplicates")
def duplicates(query: ClassificationInput, K: int):

    duplicates_results = get_duplicate_documents(query.text, K, es)
        
    return {"duplicates_results": duplicates_results}  # return duplicates, ideally


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

