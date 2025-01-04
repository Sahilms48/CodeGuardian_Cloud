import os
import tiktoken
import base64
import re
import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

file_extensions = {
    ".c", ".cpp", ".cc", ".h", ".hpp", ".cs",  # C, C++, C#
    ".java",                                   # Java
    ".py",                                     # Python
    ".js", ".jsx", ".ts", ".tsx",              # JavaScript and TypeScript
    ".rb", ".php", ".pl", ".pm",               # Ruby, PHP, Perl
    ".go", ".rs", ".kt", ".kts",               # Go, Rust, Kotlin
    ".swift", ".html", ".htm", ".xhtml", ".xml",  # Swift, HTML, XML
    ".css", ".json", ".yaml", ".yml", ".ini",  # CSS, JSON, YAML, INI
    ".toml", ".env", ".sh", ".bash",           # TOML, Env, Bash
    ".ps1", ".bat", ".cmd",                    # PowerShell, Batch
    "package.json", "package-lock.json",       # Node.js
    "requirements.txt", "Pipfile", "Pipfile.lock", "pyproject.toml",  # Python
    "pom.xml", "build.gradle", "build.gradle.kts",  # Java
    ".csproj", ".vbproj", ".sln", "packages.config",  # .NET
    "Gemfile", "Gemfile.lock",                 # Ruby
    "composer.json", "composer.lock",         # PHP
    "go.mod", "go.sum",                        # Go
    ".jinja", ".jinja2", ".hbs", ".ejs", ".tpl",  # Templates
    ".tf", ".tfvars", ".dockerignore", "Dockerfile",  # Terraform, Docker
    ".log", ".sql", ".proto"                   # Miscellaneous
}

def matches_extension(filename):
    extension = os.path.splitext(filename)[-1]
    
    # If the file has no extension (e.g., Dockerfile)
    if extension == "":
        base_name = os.path.basename(filename)
        return base_name in file_extensions
    
    # Check if the extension matches
    return extension in file_extensions

def build_tree(folder_path):
    tree = {"name": os.path.basename(folder_path), "type": "folder", "children": []}

    try:
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)

            if os.path.isdir(entry_path) and entry != ".git":
                tree["children"].append(build_tree(entry_path))
            elif os.path.isfile(entry_path) and matches_extension(entry):
                tree["children"].append({"name": entry, "type": "file"})
        
    except Exception as e:
        print(f"An error occurred while accessing {folder_path}: {e}")

    return tree

def build_tree_from_github_files(files, repo):
    root = {"name": repo, "type": "folder", "children": []}

    for file in files:
        path_parts = file['path'].split('/')
        current_node = root

        for i, part in enumerate(path_parts):
            # Check if this part already exists in the tree
            existing_node = next((node for node in current_node['children'] if node['name'] == part), None)
            
            if existing_node:
                current_node = existing_node
            else:
                # If not found, create a new node
                new_node = {
                    "name": part,
                    "type": "folder" if i < len(path_parts) - 1 else "file",  # Last part is a file, others are folders
                    "children": []
                }
                current_node['children'].append(new_node)
                current_node = new_node

    return root

def print_tree(tree, prefix=""):
    try:
        # Print the current node
        if "children" in tree:  # It's a folder
            connector = "├── "  # Default connector for folders
            print(prefix + connector + tree['name'])
            # Recursively print its children
            for i, child in enumerate(tree['children']):
                is_last = i == len(tree['children']) - 1  # Check if it's the last child
                new_prefix = prefix + ("│   " if not is_last else "    ")
                print_tree(child, new_prefix)
        else:  # It's a file
            print(prefix + "└── " + tree['name'])  # Use "└──" for the last file

    except Exception as e:
        print(f"An error occurred: {e}")

def tree_to_string(tree, prefix=""):
    try:
        result = []
        # Append the current node
        if "children" in tree:  # It's a folder
            connector = "├── "  # Default connector for folders
            result.append(prefix + connector + tree['name'])
            # Recursively process its children
            for i, child in enumerate(tree['children']):
                is_last = i == len(tree['children']) - 1  # Check if it's the last child
                new_prefix = prefix + ("│   " if not is_last else "    ")
                result.append(tree_to_string(child, new_prefix))
        else:  # It's a file
            result.append(prefix + "└── " + tree['name'])  # Use "└──" for the last file

        return "\n".join(result)

    except Exception as e:
        return f"An error occurred: {e}"

def count_tokens(string: str, model: str = "gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))


def write_folder_structure_to_file(output_path, folder_structure):
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            # Write the folder structure
            output_file.write("Folder Structure:\n")
            output_file.write(folder_structure + "\n\n")
        print(f"Output successfully written to {output_path}")
    except Exception as e:
        print(f"An error occurred while writing to {output_path}: {e}")

def write_content_to_file(output_path, file_path, content):
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"File Path: {file_path}\n")
            output_file.write("Content:\n")
            output_file.write(content + "\n")
            output_file.write("\n" + "="*80 + "\n\n")
            
        print(f"Output successfully written to {output_path}")
    except Exception as e:
        print(f"An error occurred while writing to {output_path}: {e}")

def build_file_content_dict(folder_path):
    file_content_dict = {}

    try:
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)

            if os.path.isdir(entry_path) and entry != ".git":
                # Recursively process subdirectories
                file_content_dict.update(build_file_content_dict(entry_path))
            elif os.path.isfile(entry_path) and matches_extension(entry):
                # Read and store the file content
                try:
                    with open(entry_path, 'r', encoding='utf-8') as file:
                        file_content_dict[entry_path] = file.read()
                except Exception as e:
                    print(f"An error occurred while reading {entry_path}: {e}")

    except Exception as e:
        print(f"An error occurred while accessing {folder_path}: {e}")

    return file_content_dict



import os

def build_file_content_dict_local(folder_path):
    file_content_dict = {}

    try:
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)

            if os.path.isdir(entry_path) and entry != ".git":
                # Recursively process subdirectories
                file_content_dict.update(build_file_content_dict_local(entry_path))
            elif os.path.isfile(entry_path) and matches_extension(entry):
                # Read and store the file content with only the file name as the key
                try:
                    with open(entry_path, 'r', encoding='utf-8') as file:
                        file_name = os.path.basename(entry_path)
                        file_content_dict[file_name] = file.read()
                except Exception as e:
                    print(f"An error occurred while reading {entry_path}: {e}")

    except Exception as e:
        print(f"An error occurred while accessing {folder_path}: {e}")

    return file_content_dict


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
        return [
            file for file in data.get('tree', [])
            if any(file['path'].endswith(ext) for ext in file_extensions)
        ]


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


def determine_severity(content):
    """Extract severity from report content"""
    content = content.lower()
    if 'high' in content:
        return 'high'
    elif 'medium' in content:
        return 'medium'
    elif 'low' in content:
        return 'low'
    return 'medium'  # default severity