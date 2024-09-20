import json
from typing import List, Tuple
from main.retriever import search_similar
import os


class RecallMetric:
    def __init__(self):
        self.correct = 0
        self.total = 0
        self.mrr_total = 0.0

    def update(self, is_correct: bool, rank: int = None):
        self.total += 1
        if is_correct:
            self.correct += 1
            if rank is not None:
                self.mrr_total += 1 / (rank + 1)

    @property
    def recall(self):
        return self.correct / self.total if self.total > 0 else 0.0

    @property
    def mrr(self):
        return self.mrr_total / self.total if self.total > 0 else 0.0


def load_splits(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        splits = json.load(file)
    return splits


def calculate_metrics(questions_and_answers: List[tuple], top_k: int, splits: List[dict]):
    metric = RecallMetric()

    for q, answer_urls in questions_and_answers:
        print(f"Answering question: {q}")
        docs = search_similar(q, top_k)
        doc_indices = [d[0] for d in docs]

        found_urls = []
        for idx in doc_indices:
            if 0 <= idx < len(splits):
                doc_id = splits[idx]["ID"]
                url = splits[idx]["URL"]
                found_urls.append(url)

        found = False
        for rank, found_url in enumerate(found_urls):
            if found_url in answer_urls:
                print("Found, rank:", rank)
                metric.update(is_correct=True, rank=rank)
                found = True
                break

        if not found:
            metric.update(is_correct=False)

    print(f"Recall@{top_k}: {metric.recall}")
    print(f"MRR@{top_k}: {metric.mrr}")


with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'test_set_questions.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

questions = data['question']
answers = data['answer']

questions_and_answers = list(zip(questions, [[answer] for answer in answers]))

splits = load_splits(os.path.join(os.path.dirname(__file__), '..', 'data', 'chunks_all.json'))

calculate_metrics(questions_and_answers, top_k=35, splits=splits)
