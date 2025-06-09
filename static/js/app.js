
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
    let html = '<h3>Analysis Results</h3><table class="table"><thead><tr><th>File</th><th>Lines</th><th>Empty Lines</th><th>Imports</th></tr></thead><tbody>';
    
    for (const [file, stats] of Object.entries(data.files)) {
        html += `<tr>
            <td>${file}</td>
            <td>${stats.line_count}</td>
            <td>${stats.empty_lines}</td>
            <td>${stats.imports}</td>
        </tr>`;
    }
    
    return html + '</tbody></table>';
}

function renderChangelog(data) {
    return `<h3>Changelog</h3><pre>${data.changelog}</pre>`;
}
