
from git import Repo

def generate_changelog(repo_path):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits('main', max_count=10))
    changelog = []
    for commit in commits:
        changelog.append(f"- {commit.hexsha[:7]}: {commit.summary} ({commit.author.name})")
    return "\n".join(changelog)
