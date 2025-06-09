
# Git Automation Agent with Multi-Model Support

This project implements a Git automation agent using LangGraph and Python. It supports:

- Cloning repositories
- File analysis
- Automated code generation and testing using LLMs (OpenAI, Anthropic, Gemini, HuggingFace, etc.)
- Commit and PR creation
- API access via FastAPI or Flask

## Requirements

- Python 3.9+
- GitPython
- LangGraph
- FastAPI / Flask
- HuggingFace Transformers (optional)

## Running the Flask API

```bash
pip install -r requirements.txt
python api_flask.py
```

## Running the Agent

```bash
curl -X POST http://localhost:5000/run-agent \
    -H "Content-Type: application/json" \
    -d '{"github_token": "your_token", "repo_name": "user/repo"}'
```

## Extending

You can extend the system with tools like:
- `file_analysis.py` – Basic file reading and metadata analysis
- `changelog_tool.py` – Generates a simple changelog from diffs

