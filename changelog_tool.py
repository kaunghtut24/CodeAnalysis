
from git import Repo

def generate_changelog(repo_url):
    import os
    import tempfile
    from urllib.parse import urlparse
    
    def get_repo(path_or_url):
        """Handle both local paths and GitHub URLs"""
        if path_or_url.startswith(('http://', 'https://')):
            parsed = urlparse(path_or_url)
            if 'github.com' not in parsed.netloc:
                raise ValueError("Only GitHub repositories are currently supported")
                
            repo_name = parsed.path.strip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
                
            clone_path = os.path.join(tempfile.gettempdir(), repo_name)
            
            if not os.path.exists(clone_path):
                Repo.clone_from(path_or_url, clone_path)
                
            return Repo(clone_path)
            
        cleaned_path = os.path.normpath(path_or_url)
        if not os.path.exists(cleaned_path):
            raise ValueError(f"Invalid repository path: {cleaned_path}")
        return Repo(cleaned_path)

    repo = get_repo(repo_url)
    commits = list(repo.iter_commits(repo.active_branch.name, max_count=10))
    changelog = []
    for commit in commits:
        changelog.append(f"- {commit.hexsha[:7]}: {commit.summary} ({commit.author.name})")
    return "\n".join(changelog)
