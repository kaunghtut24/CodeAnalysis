
from flask import Flask, request, jsonify, render_template
from code_analyzer import analyze_repository
from changelog_tool import generate_changelog
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/analyze", methods=["POST"])
def analyze_repo():
    data = request.json
    repo_path = data.get("repo_path")
    if not repo_path:
        return jsonify({"error": "repo_path is required"}), 400
    return jsonify(analyze_repository(repo_path))

@app.route("/changelog", methods=["POST"])
def get_changelog():
    data = request.json
    repo_path = data.get("repo_path")
    if not repo_path:
        return jsonify({"error": "repo_path is required"}), 400
    return jsonify({"changelog": generate_changelog(repo_path)})

if __name__ == "__main__":
    app.run(debug=True)
