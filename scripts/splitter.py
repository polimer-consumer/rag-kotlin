import json
from bs4 import BeautifulSoup
from langchain_text_splitters import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter

from scripts.link_fetch import fetch_page

headers_to_split_on = [
    ("h1", "Topic"),
    ("h2", "Part"),
    ("h3", "Sub-part"),
]

splits_list = []

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)

# Fot test
initial_links = {
    "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-subscription.html",
    "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/update-and-get.html",
    "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-closed-send"
    "-channel-exception/index.html",
    "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-conflated"
    "-broadcast-channel/index.html",
    "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-conflated"
    "-broadcast-channel/open-subscription.html",
    "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/-semaphore.html"
    }

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

        chunk_size = 600
        chunk_overlap = 100
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        splits = text_splitter.split_documents(html_header_splits)
        for split in splits:
            splits_list.append({"chunk": split.page_content, "metadata": split.metadata})

with open('../data/splits.json', 'w', encoding='utf-8') as file:
    json.dump(splits_list, file)
