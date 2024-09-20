from typing import List
from main.retriever import search_similar
import os


def retrieve(query: str, k=5, index_path: str = None):
    if index_path is None:
        index_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index_all.index')

    results = search_similar(query, k, index_path)
    return results
