
# Git Repository Analysis API

This project provides a REST API for analyzing git repositories using FastAPI/Flask. It offers tools for code analysis and changelog generation.

## Features

- **Code Analysis**: Analyze Python files in a repository
  - Line count statistics
  - Empty line detection
  - Import statement analysis
- **Changelog Generation**: Generate changelogs from git history
- **Input Validation**: Robust path and repository validation
- **Rate Limiting**: Protection against API abuse (100 requests/minute)
- **API Documentation**: Auto-generated with FastAPI/Swagger

## Requirements

- Python 3.9+
- FastAPI/Flask
- GitPython
- Uvicorn (for FastAPI)
- Additional dependencies in requirements.txt

## Installation

```powershell
# Create and activate virtual environment (Optional)
python -m venv venv
.\\venv\\Scripts\\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Running the FastAPI Server

```powershell
# Start the FastAPI server
python -m uvicorn api_fastapi:app --reload
```

## API Endpoints

### 1. Analyze Repository
```powershell
# Analyze Python files in a repository
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/analyze' `
    -Method Post `
    -Body '{"repo_path": "path/to/your/repo"}' `
    -ContentType 'application/json'
```

### 2. Generate Changelog
```powershell
# Generate changelog from git history
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/changelog' `
    -Method Post `
    -Body '{"repo_path": "path/to/your/repo"}' `
    -ContentType 'application/json'
```

## API Response Format

### Analysis Response
```json
{
    "files": {
        "example.py": {
            "line_count": 100,
            "empty_lines": 20,
            "imports": 5
        }
    }
}
```

### Changelog Response
```json
{
    "changelog": "- commit1: Description\n- commit2: Description"
}
```

## Implementation Details

- `file_analysis.py` – Analyzes Python files for metrics like line count and imports
- `changelog_tool.py` – Generates changelog from git commit history
- `api_fastapi.py` – FastAPI implementation with validation and rate limiting
- `api_flask.py` – Alternative Flask implementation

