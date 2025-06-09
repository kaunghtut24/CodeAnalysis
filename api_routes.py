
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess

api = Blueprint('api', __name__)

@api.route('/api/chat', methods=['POST'])
def handle_chat():
    data = request.json
    message = data.get('message')
    context = data.get('context')
    
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
        filename = secure_filename(file.filename)
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
