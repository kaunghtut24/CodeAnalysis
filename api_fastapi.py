from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from file_analysis import analyze_files
from changelog_tool import generate_changelog
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from typing import Dict

# Create FastAPI app
app = FastAPI(title="Repository Analysis API")

# Set up rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class RepoInfo(BaseModel):
    repo_path: str
    
    @validator('repo_path')
    def path_must_exist(cls, v):
        if not os.path.exists(v):
            raise ValueError("Repository path does not exist")
        if not os.path.isdir(v):
            raise ValueError("Path must be a directory")
        if not os.path.exists(os.path.join(v, '.git')):
            raise ValueError("Not a valid git repository")
        return v

class AnalysisResponse(BaseModel):
    files: Dict[str, Dict[str, int]]

class ChangelogResponse(BaseModel):
    changelog: str

@app.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("100/minute")
def analyze_repository(request: Request, repo: RepoInfo):
    try:
        analysis = analyze_files(repo.repo_path)
        return {"files": analysis}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Failed to analyze repository: " + str(e)
        )

@app.post("/changelog", response_model=ChangelogResponse)
@limiter.limit("100/minute")
def get_changelog(request: Request, repo: RepoInfo):
    try:
        changelog = generate_changelog(repo.repo_path)
        return {"changelog": changelog}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Failed to generate changelog: " + str(e)
        )

@app.get("/")
@limiter.limit("100/minute")
def read_root(request: Request):
    return {
        "message": "Welcome to the Git Repository Analysis API",
        "endpoints": {
            "/analyze": "Analyze Python files in a git repository",
            "/changelog": "Generate changelog from git commits"
        }
    }
