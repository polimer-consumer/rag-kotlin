import json
import numpy as np
from typing import List
from langchain_openai import OpenAIEmbeddings
import faiss
import os
import argparse
from tqdm import tqdm


def chunked(elements: List[str], chunk_size: int) -> List[List[str]]:
    return [elements[i:i + chunk_size] for i in range(0, len(elements), chunk_size)]


def merge_json_files(file_paths, output_file_path):
    merged_data = []

    for file_path in tqdm(file_paths, desc="Merging JSON files"):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            data = json.load(file)
            merged_data.extend(data)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, ensure_ascii=False, indent=4)


def main():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '--chunks_file',
        type=str,
        nargs='+',
        required=True
    )

    argument_parser.add_argument(
        '--output_file',
        type=str,
        default=os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index.index')
    )

    args = argument_parser.parse_args()

    merged_output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'merged_output.json')
    merge_json_files(args.chunks_file, merged_output_path)

    with open(merged_output_path, 'r', encoding='utf-8') as file:
        spans = json.load(file)

    embeddings_list = []
    chunk_size = 100

    with open(os.path.join(os.path.dirname(__file__), '..', 'API_key.txt'), 'r') as file:
        api_key = file.read().strip()

    embedding_model = OpenAIEmbeddings(api_key=api_key)

    for chunk in tqdm(chunked(spans, chunk_size), desc="Generating embeddings", total=len(spans) // chunk_size + 1):
        contents = [span["Content"] for span in chunk]
        chunk_embeddings = embedding_model.embed_documents(contents)
        embeddings_list.extend(chunk_embeddings)

    d = len(embeddings_list[0])
    index = faiss.IndexFlatL2(d)

    index.add(np.array(embeddings_list))

    faiss.write_index(index, args.output_file)
    print(f"FAISS index saved to {args.output_file}")


if __name__ == "__main__":
    main()
