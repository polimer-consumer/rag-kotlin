import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from main.link_fetch import run


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--links_file', type=str, default='../data/extracted_links.txt')

    parser.add_argument('--output_file', type=str, default='../data/table_row_links.txt')

    args = parser.parse_args()

    run(args.links_file, args.output_file)