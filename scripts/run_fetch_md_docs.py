import os
import argparse

from main.fetch_md_docs import process_github_repo


def main(file_path, d):
    with open(file_path, 'r') as file:
        links = file.readlines()

    for link in links:
        process_github_repo(link.strip(), d)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    default_input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'md_docs_links.txt')
    default_output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'docs_local')

    parser.add_argument('--input_file', type=str, default=default_input_file)
    parser.add_argument('--output_dir', type=str, default=default_output_dir)

    args = parser.parse_args()

    main(args.input_file, args.output_dir)