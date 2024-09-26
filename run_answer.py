import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from main.generator import query_openai_api
from scripts.run_retrieve import retrieve


def generate_answer(question: str, k: int = 5, index_path: str = '../data/faiss_index_all.index'):
    contexts = retrieve(question, k, index_path)
    contexts = [f"ID: {id}\nTEXT: {text}" for id, text in contexts]
    combined_context = '\n\n'.join(contexts)
    answer = query_openai_api(question, combined_context)

    return answer


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--query",
        type=str,
        default="What does invoke do?"
    )
    argument_parser.add_argument(
        "--top_k",
        type=int,
        default=30
    )
    argument_parser.add_argument(
        "--index_path",
        type=str,
        required=True
    )

    arguments = argument_parser.parse_args()
    query = arguments.query
    k = arguments.top_k
    answer = generate_answer(query, k, index_path=arguments.index_path)
    print(answer.content)


if __name__ == "__main__":
    main()
