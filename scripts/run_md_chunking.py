import os
import argparse
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain_openai import OpenAIEmbeddings
from main.md_chunker import parse_markdown_file, write_docs_to_json


def main(directory_path, output_json_file):
    api_key_path = os.path.join(os.path.dirname(__file__), '..', 'API_key.txt')
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()

    markdown_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.md')]

    embeddings = OpenAIEmbeddings(api_key=api_key)

    for file_path in markdown_files:
        print(f"Processing file: {os.path.basename(file_path)}")

        sections = parse_markdown_file(file_path)
        write_docs_to_json(sections, json_file=output_json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    default_directory_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'docs_local')
    default_output_json_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'docs_chunks.json')

    parser.add_argument('--directory_path', type=str, default='../data/docs_local')

    parser.add_argument('--output_file', type=str, default='../data/md_chunks.json')

    args = parser.parse_args()

    main(args.directory_path, args.output_file)
