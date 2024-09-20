import json
import numpy as np
from typing import List
from langchain_openai import OpenAIEmbeddings
import faiss
import os
import argparse


def chunked(elements: List[str], chunk_size: int) -> List[List[str]]:
    return [elements[i:i + chunk_size] for i in range(0, len(elements), chunk_size)]


def main():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '--chunks_file',
        type=str,
        default=os.path.join(os.path.dirname(__file__), '..', 'data', 'docs_chunks.json')
        )

    argument_parser.add_argument(
        '--output_index_file',
        type=str,
        default=os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index_all.index')
        )

    args = argument_parser.parse_args()

    with open(args.chunks_file, 'r', encoding='utf-8') as file:
        spans = json.load(file)

    embeddings_list = []
    chunk_size = 100

    with open(os.path.join(os.path.dirname(__file__), '..', 'API_key.txt'), 'r') as file:
        api_key = file.read().strip()

    embedding_model = OpenAIEmbeddings(api_key=api_key)

    for chunk in chunked(spans, chunk_size):
        contents = [span["Content"] for span in chunk]
        chunk_embeddings = embedding_model.embed_documents(contents)
        embeddings_list.extend(chunk_embeddings)

    d = len(embeddings_list[0])
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings_list))

    faiss.write_index(index, args.output_index_file)


if __name__ == "__main__":
    main()
