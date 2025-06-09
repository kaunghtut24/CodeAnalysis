
import os

def analyze_files(repo_dir):
    report = {}
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    report[file] = {
                        'line_count': len(lines),
                        'empty_lines': sum(1 for line in lines if line.strip() == ''),
                        'imports': sum(1 for line in lines if line.strip().startswith('import'))
                    }
    return report
