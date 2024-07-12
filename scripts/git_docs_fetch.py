import os
import requests


#download documentation from github
def download_file(file_url, file_path):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Failed to get file: {file_url}. Error: {e}')
        return

    try:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f'Failed to write file: {file_path}. Error: {e}')


def get_documentation_directory(docs_url, destination_dir):
    try:
        os.makedirs(destination_dir, exist_ok=True)

        response = requests.get(docs_url)
        response.raise_for_status()
        contents = response.json()

        for item in contents:
            if item['type'] == 'file':
                file_url = item['download_url']
                file_path = os.path.join(destination_dir, item['name'])
                download_file(file_url, file_path)

        print(f'Copied documentation to directory {destination_dir}')

    except requests.exceptions.RequestException as e:
        print(f'Failed to load documentation directory: {docs_url}. Error: {e}')

    except Exception as e:
        print(f': {e}')


#Example:
#documentation_url = 'https://api.github.com/repos/Kotlin/kotlinx.serialization/contents/docs'
#destination = 'kotlinx_serialisation_local'

#get_documentation_directory(documentation_url, destination)
