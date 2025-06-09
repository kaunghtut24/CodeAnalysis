
from git import Repo

def generate_changelog(repo_path):
    import os
    cleaned_path = os.path.normpath(repo_path.replace('https:\\', '').replace(':', ''))
    if not os.path.exists(cleaned_path):
        raise ValueError(f"Invalid repository path: {cleaned_path}")
    repo = Repo(cleaned_path)
    commits = list(repo.iter_commits(repo.active_branch.name, max_count=10))
    changelog = []
    for commit in commits:
        changelog.append(f"- {commit.hexsha[:7]}: {commit.summary} ({commit.author.name})")
    return "\n".join(changelog)
