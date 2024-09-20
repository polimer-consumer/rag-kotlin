import json
import os
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
import numpy as np
import faiss


def search_similar(
        query: str, k: int, index_path: str = None,
        chunks_file: str = None
) -> List[Tuple[int, str]]:
    if index_path is None:
        index_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index_all.index')
    if chunks_file is None:
        chunks_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'chunks_all.json')

    with open(os.path.join(os.path.dirname(__file__), '..', 'API_key.txt'), 'r') as file:
        api_key = file.read().strip()

    embeddings = OpenAIEmbeddings(api_key=api_key)

    query_embedding = embeddings.embed_query(query)
    query_vector = np.array(query_embedding).astype('float32').reshape(1, -1)

    index = faiss.read_index(index_path)

    distances, indices = index.search(query_vector, k)

    with open(chunks_file, 'r', encoding='utf-8') as file:
        spans = json.load(file)
        contents_list = [span["Content"] for span in spans]

    return [(i, contents_list[i]) for i in indices[0]]
