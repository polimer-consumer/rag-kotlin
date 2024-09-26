import json
import os
import sys

import requests
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from main.html_chunker import parse_doc


def main(links_file, output_file):
    lines = []
    try:
        with open(links_file, 'r') as file:
            for line in file.readlines():
                if not line:
                    break
                lines.append(line.strip())
    except FileNotFoundError:
        print(f"The file {links_file} does not exist.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    chunks = []
    for url in lines:
        print(f"Processing URL: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                chunk_list = parse_doc(html_content, url)
                if chunk_list:
                    chunks.extend(chunk_list)
            else:
                print(f"Failed to retrieve content from {url}")
        except requests.RequestException as e:
            print(f"An error occurred while fetching {url}: {e}")

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(chunks, file, ensure_ascii=False, indent=4)
        print(f"Chunks successfully saved to {output_file}")
    except Exception as e:
        print(f"Failed to save chunks to {output_file}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--links_file', type=str, default='../data/table_row_links.txt')
    parser.add_argument('--output_file', type=str, default='../data/html_chunks.json')

    args = parser.parse_args()

    main(args.links_file, args.output_file)
