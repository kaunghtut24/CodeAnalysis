
document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const repoPath = document.getElementById('repoPath').value;
    const analysisType = document.getElementById('analysisType').value;
    const resultsDiv = document.getElementById('results');
    
    resultsDiv.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';
    
    try {
        const endpoint = analysisType === 'code' ? '/analyze' : '/changelog';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ repo_path: repoPath })
        });
        
        const data = await response.json();
        
        if (analysisType === 'code') {
            resultsDiv.innerHTML = renderCodeAnalysis(data);
        } else {
            resultsDiv.innerHTML = renderChangelog(data);
        }
    } catch (error) {
        resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
});

function renderCodeAnalysis(data) {
    let html = `
        <div class="analysis-container">
            <h3>Analysis Results</h3>
            <ul class="nav nav-tabs" id="analysisTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#summary" type="button">Summary</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#complexity" type="button">Complexity</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#documentation" type="button">Documentation</button>
                </li>
            </ul>
            <div class="tab-content p-3 border border-top-0 rounded-bottom">
                <div class="tab-pane fade show active" id="summary" role="tabpanel">
                    ${renderSummaryTab(data)}
                </div>
                <div class="tab-pane fade" id="complexity" role="tabpanel">
                    ${renderComplexityTab(data)}
                </div>
                <div class="tab-pane fade" id="documentation" role="tabpanel">
                    ${renderDocumentationTab(data)}
                </div>
            </div>
        </div>
    `;
    return html;
}

function renderSummaryTab(data) {
    let html = '<table class="table"><thead><tr><th>File</th><th>Lines</th><th>Code</th><th>Imports</th><th>Functions</th></tr></thead><tbody>';
    
    for (const [file, stats] of Object.entries(data)) {
        if (stats.error) {
            html += `<tr><td colspan="5" class="text-danger">${file}: ${stats.error}</td></tr>`;
            continue;
        }
        
        const basic = stats.basic_metrics || {};
        const functions = stats.functions || [];
        const imports = stats.imports_analysis || {};
        
        html += `<tr>
            <td>${file}</td>
            <td>${basic.total_lines || 0}</td>
            <td>${basic.code_lines || 0}</td>
            <td>${imports.total_imports || 0}</td>
            <td>${functions.length || 0}</td>
        </tr>`;
    }
    
    return html + '</tbody></table>';
}

function renderComplexityTab(data) {
    let html = `
        <div class="complexity-container">
            <h4>Code Complexity Metrics</h4>
            <table class="table table-striped">
                <thead class="thead-dark">
                    <tr>
                        <th>File</th>
                        <th>If</th>
                        <th>For</th>
                        <th>While</th>
                        <th>Try</th>
                        <th>Max Depth</th>
                        <th>Complexity Score</th>
                    </tr>
                </thead>
                <tbody>`;
    
    for (const [file, stats] of Object.entries(data)) {
        if (!stats.complexity_metrics) continue;
        const cm = stats.complexity_metrics;
        const score = (cm.if_statements || 0) + (cm.for_loops || 0) + 
                     (cm.while_loops || 0) + (cm.try_except || 0) + 
                     (cm.nested_depth || 0);
        html += `<tr>
            <td>${file}</td>
            <td>${cm.if_statements || 0}</td>
            <td>${cm.for_loops || 0}</td>
            <td>${cm.while_loops || 0}</td>
            <td>${cm.try_except || 0}</td>
            <td>${cm.nested_depth || 0}</td>
            <td>${score}</td>
        </tr>`;
    }
    
    return html + '</tbody></table>';
}

function renderDocumentationTab(data) {
    let html = `
        <div class="documentation-container">
            <h4>Documentation Metrics</h4>
            <table class="table table-striped">
                <thead class="thead-dark">
                    <tr>
                        <th>File</th>
                        <th>Documented</th>
                        <th>Undocumented</th>
                        <th>Coverage %</th>
                    </tr>
                </thead>
                <tbody>`;
    
    for (const [file, stats] of Object.entries(data)) {
        if (!stats.documentation_metrics) continue;
        const dm = stats.documentation_metrics;
        html += `
            <tr>
                <td>${file}</td>
                <td>${dm.documented_functions + dm.documented_classes}</td>
                <td>${dm.undocumented_functions + dm.undocumented_classes}</td>
                <td class="${dm.docstring_coverage >= 80 ? 'text-success' : dm.docstring_coverage >= 50 ? 'text-warning' : 'text-danger'}">
                    ${dm.docstring_coverage || 0}%
                </td>
            </tr>`;
    }
    
    return html + '</tbody></table>';
}

function renderChangelog(data) {
    return `<h3>Changelog</h3><pre>${data.changelog}</pre>`;
}

// Chat Interface Handlers
document.getElementById('send-chat').addEventListener('click', handleChatSubmit);
document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChatSubmit();
});

async function handleChatSubmit() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    addChatMessage('user', message);
    input.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message,
                context: window.analysisResults || null 
            })
        });
        const data = await response.json();
        addChatMessage('assistant', data.response);
    } catch (error) {
        addChatMessage('system', 'Error connecting to assistant');
        console.error('Chat error:', error);
    }
}

function addChatMessage(role, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert ${role === 'user' ? 'alert-primary' : 'alert-secondary'}`;
    messageDiv.innerHTML = `
        <strong>${role.toUpperCase()}:</strong>
        <div>${content}</div>
    `;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// File Analysis Handlers
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.multiple = true;
    fileInput.style.display = 'none';
    fileInput.addEventListener('change', handleFileUpload);
    document.body.appendChild(fileInput);

    document.getElementById('file-analysis-results').addEventListener('click', () => {
        fileInput.click();
    });
});

async function handleFileUpload(e) {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
        const response = await fetch('/api/analyze/files', {
            method: 'POST',
            body: formData
        });
        const results = await response.json();
        displayFileAnalysis(results);
    } catch (error) {
        console.error('File analysis error:', error);
    }
}

function displayFileAnalysis(results) {
    const container = document.getElementById('file-analysis-results');
    container.innerHTML = results.map(file => `
        <div class="file-result mb-3">
            <h6>${file.filename}</h6>
            <div>Lines: ${file.lines}</div>
            <div>Complexity: ${file.complexity}</div>
        </div>
    `).join('');
}
