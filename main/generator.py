import os
from pprint import pprint

from openai import OpenAI
import json
import os
from openai.types.chat import ChatCompletionMessage

with open(os.path.dirname(__file__) + '\..\API_key.txt', 'r') as file:
    api_key = file.read().strip()
client = OpenAI(api_key=api_key)

# openai.api_key = os.environ['OPENAI_API_KEY']

# queries = json.load(open('../data/queries.json', 'r', encoding='utf-8'))


def query_openai_api(question, context) -> ChatCompletionMessage:
    prompt = (f"I have a question about Kotlin. Answer based on the contexts and cite the context ID. "
              f"Question: {question}\nContext: {context}")
    completion = client.chat.completions.create(
        max_tokens=150,
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are an assistant which help to answer questions about Kotlin."
                        "Do not give general broad answers - answer clear and concise on question.", },
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    print(f"{question} answered")
    return completion.choices[0].message


#
#
# results = []
#
# for query in queries:
#     chunk = query["chunk"]
#     metadata = query["metadata"]
#     question = query["question"]
#     answer = query_openai_api(question, chunk)
#
#     result = {
#         "question": question,
#         "context": chunk,
#         "metadata": metadata,
#         "answer": answer.content
#     }
#     pprint(result)
#     results.append(result)

def generate_answers(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Generate answers using the LLM API
    for i, question in enumerate(data['question']):
        context = ' '.join(data['contexts'][i])
        if question and context:
            answer = query_openai_api(question, context)
            data['answer'][i] = answer.content

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

'''
input_file = '../data/test_set_questions.json'
output_file = '../data/test_set_answers.json'
generate_answers(input_file, output_file)
'''
