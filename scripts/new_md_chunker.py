import os
import json
import uuid
import mistletoe
from mistletoe.block_token import Document, Heading, Paragraph, CodeFence
from mistletoe.span_token import Link
from langchain_openai import OpenAIEmbeddings
import numpy as np


class Doc:
    def __init__(self, content, id, url, content_start):
        self.content = content
        self.id = id
        self.url = url
        self.content_start = content_start


def parse_markdown_to_ast(file_path):
    with open(file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()
    return mistletoe.Document(content), content


def extract_text_from_node(node):
    if isinstance(node, Paragraph):
        return ''.join(extract_text_from_node(child) for child in node.children)
    elif isinstance(node, CodeFence):
        return f"\n```\n{node.children[0].content}\n```\n"
    elif isinstance(node, Link):
        return f"[{node.children[0].content}]({node.target})"
    elif hasattr(node, 'children') and node.children:
        return ''.join(extract_text_from_node(child) for child in node.children)
    elif hasattr(node, 'content'):
        return node.content
    return ''

def group_text_by_headings(node, current_heading, sections, file_name, content, current_pos):
    if isinstance(node, Heading):
        heading_text = extract_text_from_node(node)
        current_heading.append(heading_text)
        current_pos = content.find(heading_text, current_pos)
        sections.append((file_name, current_heading.copy(), '', current_pos))
        current_heading.pop()
    elif isinstance(node, (Paragraph, CodeFence, Link)):
        if sections:
            para_text = extract_text_from_node(node)
            sections[-1] = (sections[-1][0], sections[-1][1], sections[-1][2] + para_text, sections[-1][3])
    if hasattr(node, 'children') and node.children is not None:
        for child in node.children:
            current_pos = group_text_by_headings(child, current_heading, sections, file_name, content, current_pos)
    return current_pos


def parse_markdown_file(file_path):
    ast, content = parse_markdown_to_ast(file_path)
    sections = []
    group_text_by_headings(ast, [], sections, file_path, content, 0)

    docs = []
    file_name = os.path.basename(file_path)
    for section in sections:
        heading = section[1][-1] if section[1] else ''
        id = uuid.uuid4()
        url = f"{file_name}#{heading.replace(' ', '-').lower()}"
        url = url.replace('(', '').replace(')', '')
        content_with_headers = f"{file_name} > {' > '.join(section[1])}\n{section[2]}"
        docs.append(Doc(content=content_with_headers, id=id, url=url, content_start=section[3]))

    return docs


def write_docs_to_json(docs, json_file='../data/docs_chunks.json'):
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    for doc in docs:
        existing_data.append({
            "ID": str(doc.id),
            "URL": doc.url,
            "Content start": doc.content_start,
            "Content": doc.content
        })

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def save_vectors_to_file(vectors, metadata, file_path='../data/vectors.json'):
    data = [{"embedding": vector, "metadata": meta} for vector, meta in zip(vectors, metadata)]
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


with open('../API_key.txt', 'r') as file:
    api_key = file.read().strip()

file_path = '../kotlinx_serialisation_local/value-classes.md'
sections = parse_markdown_file(file_path)
write_docs_to_json(sections)

embeddings = OpenAIEmbeddings(api_key=api_key)
embeddings_list = [embeddings.embed_query(section.content) for section in sections]
metadata = [{"text": section.content, "id": str(section.id)} for section in sections]
save_vectors_to_file(embeddings_list, metadata)


