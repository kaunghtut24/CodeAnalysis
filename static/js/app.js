
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
    // Implementation for complexity metrics display
    // Would show nested depth, control structures etc.
    return '<p>Complexity metrics visualization coming soon</p>';
}

function renderDocumentationTab(data) {
    // Implementation for documentation metrics display
    // Would show docstring coverage etc.
    return '<p>Documentation metrics visualization coming soon</p>';
}

function renderChangelog(data) {
    return `<h3>Changelog</h3><pre>${data.changelog}</pre>`;
}
