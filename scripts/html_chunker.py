import json
import uuid
import requests
from bs4 import BeautifulSoup

def remove_unwanted_elements(soup):
    unwanted_classes = ['footer', 'copy-icon', 'breadcrumbs', 'copy-popup-wrapper', 'sample-container', 'feedback',
                        'floating-right']
    for cls in unwanted_classes:
        for element in soup.find_all(class_=cls):
            element.decompose()

def parse_single_part(block, platform=None, page_url=None, content_start=None):
    part_chunk = ""
    symbol = block.find('div', class_='symbol monospace')
    if symbol:
        part_chunk += symbol.get_text().strip() + "\n"

    paragraphs = block.find_all('p', class_='paragraph')
    for paragraph in paragraphs:
        part_chunk += paragraph.get_text().strip() + "\n"

    sample_container = block.find('div', class_='sample-container')
    if sample_container:
        code_element = sample_container.find('code')
        if code_element:
            part_chunk += f"\nexample: {code_element.get_text().strip()}\n"

    if platform:
        part_chunk += f"Platform: {platform}"

    chunk_id = str(uuid.uuid4())
    chunk_meta = {
        "ID": chunk_id,
        "URL": page_url,
        "Content start": content_start if content_start else None,
        "Content": part_chunk.strip()
    }

    return chunk_meta

def parse_functions(main_content, page_url):
    func_chunks = []
    document_text = main_content.get_text()
    content_blocks = main_content.find_all('div', class_='content sourceset-dependent-content')

    for block in content_blocks:
        platform = None
        if block.has_attr('data-togglable'):
            platform = block['data-togglable'].split('/')[-1]

        symbols = block.find_all('div', class_='symbol monospace')

        if len(symbols) == 1:
            content_start = document_text.find(symbols[0].get_text().strip())
            func_chunk = parse_single_part(block, platform, page_url, content_start)
            if func_chunk:
                func_chunks.append(func_chunk)
        else:
            content_parts = block.find_all(recursive=False)
            part_content = []
            ind = 0
            for element in content_parts:
                if element.name == 'hr':
                    if part_content:
                        part_soup = BeautifulSoup(''.join(str(e) for e in part_content), 'html.parser')
                        content_start = document_text.find(symbols[ind].get_text().strip())
                        func_chunk = parse_single_part(part_soup, platform, page_url, content_start)
                        if func_chunk:
                            func_chunks.append(func_chunk)
                        ind += 1
                    part_content = []
                else:
                    part_content.append(str(element))

            if part_content:
                part_soup = BeautifulSoup(''.join(str(e) for e in part_content), 'html.parser')
                func_chunk = parse_single_part(part_soup, platform, page_url)
                if func_chunk:
                    func_chunks.append(func_chunk)

    return func_chunks

def parse_class(main_content, klass_type="class", page_url=None):
    klass_name = main_content.find('h1', class_='cover').get_text().strip()

    klass_chunks = []

    cover_section = main_content.find('div', class_='cover')
    if cover_section:
        cover_chunks = parse_functions(cover_section, page_url)
        if cover_chunks:
            klass_chunks.extend(cover_chunks)

    tabs_section_body = main_content.find('div', class_='tabs-section-body')

    if tabs_section_body:
        toggleable_sections = tabs_section_body.find_all('div', attrs={'data-togglable': True})

        for section in toggleable_sections:
            if len(section.attrs) == 1:
                part_name = section.find('h2').get_text().strip()
                table_rows = section.find_all('div', class_='table-row')

                section_chunk = f"All {part_name} of {klass_type} {klass_name}:\n"
                section_elements = []

                for row in table_rows:
                    row_chunks = parse_functions(row, page_url)
                    if row_chunks:
                        for row_chunk in row_chunks:
                            klass_chunks.append({
                                "ID": str(uuid.uuid4()),
                                "URL": page_url,
                                "Content start": row_chunk['Content start'],
                                "Content": f"{part_name[:-1]} of {klass_type} {klass_name}:\n{row_chunk['Content']}"
                            })
                            section_elements.append(row_chunk['Content'])

                if section_elements:
                    section_chunk += "\n".join(section_elements)
                    chunk_id = str(uuid.uuid4())
                    klass_chunks.append({
                        "ID": chunk_id,
                        "URL": page_url,
                        "Content start": None,
                        "Content": section_chunk.strip()
                    })

    return klass_chunks

def parse_doc(page_content, page_url):
    soup = BeautifulSoup(page_content, 'html.parser')
    remove_unwanted_elements(soup)

    main_content = soup.find('div', class_='main-content')

    if not main_content:
        return None

    if main_content.get('data-page-type') == 'member':
        return parse_functions(main_content, page_url)

    if main_content.get('data-page-type') == 'classlike':
        if soup.find('div', class_='symbol monospace').find('span', class_='token keyword', string='class '):
            return parse_class(main_content, "class", page_url)
        elif soup.find('div', class_='symbol monospace').find('span', class_='token keyword',
                                                              string='annotation class '):
            return parse_class(main_content, "annotation class", page_url)
        elif soup.find('div', class_='symbol monospace').find('span', class_='token keyword', string='interface '):
            return parse_class(main_content, "interface", page_url)
        elif soup.find('div', class_='symbol monospace').find('span', class_='token keyword', string='typealias '):
            return parse_class(main_content, "typealias", page_url)
        elif soup.find('div', class_='symbol monospace').find('span', class_='token keyword', string='enum '):
            return parse_class(main_content, "enum", page_url)
        elif soup.find('div', class_='symbol monospace').find('span', class_='token keyword', string='object '):
            return parse_class(main_content, "object", page_url)

    return None


lines = []
line_num = 300

try:
    with open('../data/table_row_links.txt', 'r') as file:
        for i in range(line_num):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
except FileNotFoundError:
    print(f"The file does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")

chunks = []
for url in lines:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            chunk_list = parse_doc(html_content, url)
            if chunk_list:
                chunks.extend(chunk_list)
        else:
            print(f"Failed to retrieve content from {url}")
    except requests.RequestException as e:
        print(f"An error occurred while fetching {url}: {e}")

file = open("../data/chunks.json", "w")
json.dump(chunks, file, ensure_ascii=False, indent=4)