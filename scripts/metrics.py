import json

import pandas as pd
import numpy as np
import matplotlib as mpl

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)

with open('../data/test_set_answers.json', 'r') as file:
    data_json = json.load(file)

data = Dataset.from_dict(data_json)
score = evaluate(data, metrics=[answer_relevancy, faithfulness, context_recall, context_precision])
df = score.to_pandas()

pure_score = df[["answer_relevancy", "faithfulness", "context_recall", "context_precision"]].mean()
markdown_content = "# Generator metrics\n\n"
for column, avg in pure_score.items():
    markdown_content += f"- **{column}**: {avg:.4f}\n"

with open("../README.md", "w") as file:
    file.write(markdown_content)

md = df.to_markdown(index=False)

file_path = '../data/metrics.md'
with open(file_path, 'w') as file:
    file.write(md)
