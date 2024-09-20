import os
import argparse
from langchain_openai import OpenAIEmbeddings
from main.md_chunker import parse_markdown_file, write_docs_to_json


def main(directory_path, output_json_file):
    with open('../API_key.txt', 'r') as file:
        api_key = file.read().strip()

    markdown_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.md')]

    embeddings = OpenAIEmbeddings(api_key=api_key)

    for file_path in markdown_files:
        print(f"Processing file: {os.path.basename(file_path)}")

        sections = parse_markdown_file(file_path)
        write_docs_to_json(sections, json_file=output_json_file)

        #embeddings_list = [embeddings.embed_query(section.content) for section in sections]
        #metadata = [{"text": section.content, "id": str(section.id)} for section in sections]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown files and save sections to JSON")

    parser.add_argument('--directory_path', type=str, default='../data/docs_local')

    parser.add_argument('--output_json_file', type=str, default='../data/docs_chunks.json')

    args = parser.parse_args()

    main(args.directory_path, args.output_json_file)