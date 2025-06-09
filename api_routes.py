from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess
from llm_utils import analyze_code_with_llm
from git import Repo
import tempfile

api = Blueprint('api', __name__)

@api.route('/api/chat', methods=['POST'])
def handle_chat():
    data = request.json or {}
    message = data.get('message') if data else None
    context = data.get('context') if data else None
    
    # TODO: Integrate with LLM
    response = f"Received your message about {len(context['files'])} files" if context else "Received your message"
    
    return jsonify({
        'response': response,
        'status': 'success'
    })

@api.route('/api/analyze/files', methods=['POST'])
def analyze_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
        
    results = []
    for file in request.files.getlist('files'):
        filename = secure_filename(file.filename or "uploaded_file.py")
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)
        
        # Sample analysis - replace with actual analysis logic
        loc = int(subprocess.check_output(f'wc -l {filepath}'.split()).decode().split()[0])
        complexity = len(subprocess.check_output(f'grep -c "if\\|for\\|while" {filepath}'.split()))
        
        results.append({
            'filename': filename,
            'lines': loc,
            'complexity': complexity
        })
        
    return jsonify(results)

@api.route('/api/llm-analyze', methods=['POST'])
def llm_analyze():
    data = request.json or {}
    code = data.get('code')
    prompt = data.get('prompt')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    try:
        analysis = analyze_code_with_llm(code, prompt)
        return jsonify({'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/api/clone', methods=['POST'])
def clone_repo():
    data = request.json or {}
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        # Clone to a temp directory
        temp_dir = tempfile.mkdtemp(prefix='cloned_repo_')
        Repo.clone_from(url, temp_dir)
        # List all subdirectories (paths) in the repo
        paths = []
        for root, dirs, files in os.walk(temp_dir):
            for d in dirs:
                paths.append(os.path.join(root, d))
            for f in files:
                paths.append(os.path.join(root, f))
        return jsonify({'success': True, 'paths': paths})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api.route('/api/list-paths', methods=['POST'])
def list_paths():
    data = request.json or {}
    path = data.get('path')
    if not path or not os.path.exists(path):
        return jsonify({'success': False, 'error': 'Path does not exist'}), 400
    paths = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            paths.append(os.path.join(root, d))
        for f in files:
            paths.append(os.path.join(root, f))
    return jsonify({'success': True, 'paths': paths})
