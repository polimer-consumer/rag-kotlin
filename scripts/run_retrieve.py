import os
import argparse
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from main.retriever import search_similar


def retrieve(query: str, k=5, index_path: str = None):
    if index_path is None:
        index_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index_all.index')

    results = search_similar(query, k, index_path)
    return results


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--query', type=str, required=True)

    parser.add_argument('--k', type=int, default=5)

    parser.add_argument('--index_path', type=str,
                        default=os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index.index'))

    args = parser.parse_args()

    results = retrieve(query=args.query, k=args.k, index_path=args.index_path)

    for i, result in enumerate(results, 1):
        print(f"Result {i}: {result}")


if __name__ == "__main__":
    main()
