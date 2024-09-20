import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_table_row_links(soup, base_url):
    links = set()
    table_row_divs = soup.find_all('div', class_='table-row')
    for div in table_row_divs:
        for a in div.find_all('a', href=True):
            full_url = urljoin(base_url, a['href'])
            links.add(full_url)
    return links

"""
with open('../data/extracted_links.txt', 'r', encoding='utf-8') as file:
    initial_links = {line.strip() for line in file}


new_links = set()

for link in initial_links:
    print(f"Processing: {link}")
    page_content = fetch_page(link)
    if not page_content:
        continue

    soup = BeautifulSoup(page_content, 'html.parser')
    links = extract_table_row_links(soup, link)
    new_links.update(links)


with open('../data/table_row_links.txt', 'w', encoding='utf-8') as file:
    for link in sorted(new_links):
        file.write(link + '\n')

print("Links inside 'table-row' divs have been saved to table_row_links.txt")
"""
