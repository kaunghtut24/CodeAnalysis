
from flask import Flask, request, jsonify
from core.agent_runner import run_agent
import os

app = Flask(__name__)

@app.route("/run-agent", methods=["POST"])
def run_git_agent():
    data = request.json
    github_token = data.get("github_token")
    repo_name = data.get("repo_name")

    if not github_token or not repo_name:
        return jsonify({"error": "github_token and repo_name are required"}), 400

    os.environ["GITHUB_TOKEN"] = github_token
    result = run_agent(github_token, repo_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
