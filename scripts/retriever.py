import os
import json
from langchain_openai import OpenAIEmbeddings
import numpy as np
import faiss


def load_vectors_from_file(file_path='../data/vectors.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        vectors = np.array([item["embedding"] for item in data]).astype('float32')
        metadata = [item["metadata"] for item in data]
        return vectors, metadata
    else:
        return None, None


def search_similar(query, k=5):
    query_vector = embeddings.embed_query(query)
    query_vector = np.array([query_vector]).astype('float32')

    distances, indices = index.search(query_vector, k)
    results = [documents[idx] for idx in indices[0]]
    return results


with open('../API_key.txt', 'r') as file:
    api_key = file.read().strip()

embeddings = OpenAIEmbeddings(api_key=api_key)
vectors, loaded_metadata = load_vectors_from_file()

dimension = len(vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(vectors)
documents = [{"embedding": emb, "metadata": meta} for emb, meta in zip(vectors, loaded_metadata)]



query = "How to serialize a value class?"
similar_documents = search_similar(query, k=5)
for doc in similar_documents:
    print(doc["metadata"]["text"])
