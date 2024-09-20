import requests
import os


def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Saved: {save_path}")
    else:
        print(f"Failed to save: {url}")


def process_github_repo(link, directory):
    parts = link.strip().split('/')
    owner, repo = parts[3], parts[4]

    docs_url = f"https://api.github.com/repos/{owner}/{repo}/contents/docs"
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"

    os.makedirs(directory, exist_ok=True)

    response = requests.get(docs_url)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith('.md'):
                file_url = item['download_url']
                file_name = f"{repo}_{item['name']}"
                save_path = os.path.join(directory, file_name)
                download_file(file_url, save_path)

    elif response.status_code == 404:
        response = requests.get(readme_url)
        if response.status_code == 200:
            readme_info = response.json()
            file_url = readme_info['download_url']
            file_name = f"{repo}_README.md"
            save_path = os.path.join(directory, file_name)
            download_file(file_url, save_path)
        else:
            print(f"Could not find README for repo: {repo}")
    else:
        print(f"Error for repo {repo}: {response.status_code}")
