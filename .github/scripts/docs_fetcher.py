import requests
import os
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path


def find_git_urls(markdown_file):
    with open(markdown_file, 'r') as file:
        content = file.read()
  
    urls = list(set(re.findall(r'https://github\.com/[\w-]+/[\w-]+', content))) 
    return urls


def download_readme(url, download_folder):
    repo_name = url.split('/')[-1]
    raw_url = url.replace('github.com', 'raw.githubusercontent.com')

    # Check for main and master branches
    branches = ['main', 'master', 'develop']
    for branch in branches:
        readme_url = f'{raw_url}/{branch}/README.md'
        response = requests.get(readme_url)
        if response.status_code == 200:
            with open(os.path.join(download_folder, f'{repo_name}.md'), 'wb') as file:
                file.write(response.content)
                print(f'Downloaded README.md for {repo_name}')
                return
        else:
            print(f'Failed to download README.md for {repo_name} in {branch} branch')

    print(f'No valid README.md found for {repo_name}')


def main(markdown_file, download_folder):
    urls = find_git_urls(markdown_file)
    os.makedirs(download_folder, exist_ok=True)
    for url in urls:
        download_readme(url, download_folder)

def main():
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    markdown_file = os.path.join(project_root, "README.md")
    download_folder = os.path.join(project_root, ".github", "docs")

    urls = find_git_urls(markdown_file)
    os.makedirs(download_folder, exist_ok=True)
    for url in urls:
        download_readme(url, download_folder)

main()