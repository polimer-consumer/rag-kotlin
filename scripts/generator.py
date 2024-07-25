import os
from pprint import pprint

from openai import OpenAI
import json

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# openai.api_key = os.environ['OPENAI_API_KEY']

queries = json.load(open('../data/queries.json', 'r', encoding='utf-8'))


def query_openai_api(question, context):
    prompt = f"I have a question about Kotlin: {question}\nContext: {context}"
    completion = client.chat.completions.create(
        max_tokens=200,
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are an assistant which help to answer questions about Kotlin",},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return completion.choices[0].message


results = []

for query in queries:
    chunk = query["chunk"]
    metadata = query["metadata"]
    question = query["question"]
    answer = query_openai_api(question, chunk)

    result = {
        "question": question,
        "context": chunk,
        "metadata": metadata,
        "answer": answer.content
    }
    pprint(result)
    results.append(result)

