import json
import random
from collections import defaultdict


def generate_test_set(input_file='../data/splits.json', output_file='../data/test_set.json', noize=0.3):
    with open(input_file, 'r') as file:
        data = json.load(file)

    contexts = defaultdict(list)
    all_chunks = [item['chunk'] for item in data]

    for item in data:
        topic = item['metadata'].get('Topic')
        if topic:
            contexts[topic].append(item['chunk'])
        else:
            contexts[f"Notopic_{len(contexts)}"].append(item['chunk'])

    for key in contexts:
        num_noise_chunks = max(0, int(len(contexts[key]) * noize))
        noise_chunks = random.sample(all_chunks, num_noise_chunks)
        contexts[key].extend(noise_chunks)

    data_samples = {
        'question': [''] * len(contexts),
        'answer': [''] * len(contexts),
        'contexts': list(contexts.values()),
        'ground_truth': [''] * len(contexts)
    }

    with open(output_file, 'w') as file:
        json.dump(data_samples, file, indent=4)


generate_test_set()
