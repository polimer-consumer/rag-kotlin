import json
from bs4 import BeautifulSoup
from langchain_text_splitters import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter

from link_fetch import fetch_page

headers_to_split_on = [
    ("h1", "Topic"),
    ("h2", "Part"),
    ("h3", "Sub-part"),
]

splits_list = []

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)

lines = []
line_num = 16
try:
    with open('../data/test_links.txt', 'r') as file:
        for i in range(line_num):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
except FileNotFoundError:
    print(f"The file does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")

# Fot test
initial_links = lines

# Uncomment when will need to parse everything
# with open('../data/table_row_links.txt', 'r', encoding='utf-8') as file:
#     initial_links = {line.strip() for line in file}

for link in initial_links:
    print(f"Processing: {link}")
    page_content = fetch_page(link)
    if not page_content:
        continue

    soup = BeautifulSoup(page_content, 'html.parser')

    main_content = soup.find('div', id='main')
    if main_content:
        footer = main_content.find('footer')
        copy_icon = main_content.find('span', class_='copy-icon')
        breadcrumbs = main_content.find('div', class_='breadcrumbs')
        link_popup = main_content.find('div', class_='copy-popup-wrapper')
        schema_block = main_content.find('div', class_='sample-container')
        feedback = main_content.find('div', class_='feedback')
        if schema_block:
            schema_block.decompose()
        if feedback:
            feedback.decompose()
        if link_popup:
            link_popup.decompose()
        if breadcrumbs:
            breadcrumbs.decompose()
        if copy_icon:
            copy_icon.decompose()
        if footer:
            footer.decompose()

        main_html = str(main_content)

        html_header_splits = html_splitter.split_text(main_html)

        chunk_size = 150
        chunk_overlap = 40
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        splits = text_splitter.split_documents(html_header_splits)
        for split in splits:
            metadata = split.metadata
            if not metadata:
                metadata = {"Topic": link}
            splits_list.append({"chunk": split.page_content, "metadata": metadata})

with open('../data/splits.json', 'w', encoding='utf-8') as file:
    json.dump(splits_list, file)
