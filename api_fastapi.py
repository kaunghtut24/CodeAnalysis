
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from file_analysis import analyze_files
from changelog_tool import generate_changelog

app = FastAPI()

class RepoInfo(BaseModel):
    repo_path: str

@app.post("/analyze")
def analyze_repository(repo: RepoInfo):
    try:
        analysis = analyze_files(repo.repo_path)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/changelog")
def get_changelog(repo: RepoInfo):
    try:
        changelog = generate_changelog(repo.repo_path)
        return {"changelog": changelog}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Git Repository Analysis API"}
