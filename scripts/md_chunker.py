import os

def read_files_from_directory(directory_path):
    text_content = ""
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content += file.read() + "\n"
    return text_content

def split_text(text, chunk_size=1000, overlap_size=200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap_size
    return chunks

def process_directory(directory_path):
    text_content = read_files_from_directory(directory_path)
    chunks = split_text(text_content)
    return chunks

# Example
'''directory_path = "kotlinx_serialisation_local"
chunks = process_directory(directory_path)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:")
    print(chunk)
    print(f"\n-------END OF THE CHUNK {i + 1}-------\n")
'''
