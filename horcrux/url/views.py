from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import re
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def parse_github_url(url):
    pattern = r"https://github.com/(?P<owner>[\w\-]+)/(?P<repo>[\w\-]+)(/tree/(?P<branch>[\w\-]+))?"
    match = re.match(pattern, url)
    
    if match:
        owner = match.group('owner')
        repo = match.group('repo')
        branch = match.group('branch')
        
        if not branch:
            branch = get_default_branch(owner, repo)
        
        return owner, repo, branch
    return None, None, None

def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('default_branch', 'main')
    return 'main'

def get_github_files(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=true"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return [file for file in data.get('tree', []) if file['path'].endswith('.py')]

    return []

def get_file_content(owner, repo, sha):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        content = base64.b64decode(data['content']).decode('utf-8')
        return content
    
    return None

def format_file_output(file_contents):
    output = []
    
    for file_name, content in file_contents.items():
        formatted_content = f"""
    <file name="{file_name}">
        <content><![CDATA[{content}]]></content>
    </file>
        """
        output.append(formatted_content.strip())

    return '\n'.join(output)

@api_view(['POST'])
def index(request):
    repo_url = request.data.get('url', '')
    print("token")
    print(GITHUB_TOKEN)
    
    owner, repo, branch = parse_github_url(repo_url)
    
    if not owner or not repo:
        return Response({"error": "Invalid GitHub URL"}, status=400)
    
    files = get_github_files(owner, repo, branch)
    
    if not files:
        return Response({"error": "Unable to fetch files or no Python files in the repository"}, status=400)
    
    result = {}
    
    for file in files:
        file_path = file['path']
        file_sha = file['sha']
        content = get_file_content(owner, repo, file_sha)
        
        if content is not None:
            result[file_path] = content
    
    if not result:
        return Response({"error": "Unable to fetch file contents"}, status=400)
    
    formatted_output = format_file_output(result)

    return Response(formatted_output)
