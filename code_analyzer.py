import ast
import os
import sys
from typing import Dict, List, Any
import re

class CodeAnalyzer:
    def __init__(self):
        self.metrics = {}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single Python file and return detailed metrics."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
        try:
            tree = ast.parse(content)
        except:
            return {
                'error': 'Could not parse file',
                'basic_metrics': self._get_basic_metrics(lines)
            }
            
        return {
            'basic_metrics': self._get_basic_metrics(lines),
            'complexity_metrics': self._get_complexity_metrics(tree),
            'documentation_metrics': self._analyze_documentation(tree),
            'imports_analysis': self._analyze_imports(tree),
            'code_style': self._analyze_code_style(lines),
            'functions': self._analyze_functions(tree)
        }
    
    def _get_basic_metrics(self, lines: List[str]) -> Dict[str, int]:
        """Calculate basic code metrics."""
        return {
            'total_lines': len(lines),
            'empty_lines': sum(1 for line in lines if not line.strip()),
            'comment_lines': sum(1 for line in lines if line.strip().startswith('#')),
            'code_lines': sum(1 for line in lines if line.strip() and not line.strip().startswith('#')),
        }
    
    def _get_complexity_metrics(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze code complexity."""
        complexity = {
            'if_statements': 0,
            'for_loops': 0,
            'while_loops': 0,
            'try_except': 0,
            'nested_depth': 0
        }
        
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
                self.max_depth = 0
            
            def generic_visit(self, node):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    if isinstance(node, ast.If):
                        complexity['if_statements'] += 1
                    elif isinstance(node, ast.For):
                        complexity['for_loops'] += 1
                    elif isinstance(node, ast.While):
                        complexity['while_loops'] += 1
                    elif isinstance(node, ast.Try):
                        complexity['try_except'] += 1
                ast.NodeVisitor.generic_visit(self, node)
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                    self.current_depth -= 1
        
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        complexity['nested_depth'] = visitor.max_depth
        return complexity
    
    def _analyze_documentation(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze documentation and comments."""
        docs = {
            'documented_functions': 0,
            'undocumented_functions': 0,
            'documented_classes': 0,
            'undocumented_classes': 0,
            'docstring_coverage': 0.0
        }
        
        class DocVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if ast.get_docstring(node):
                    docs['documented_functions'] += 1
                else:
                    docs['undocumented_functions'] += 1
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                if ast.get_docstring(node):
                    docs['documented_classes'] += 1
                else:
                    docs['undocumented_classes'] += 1
                self.generic_visit(node)
        
        visitor = DocVisitor()
        visitor.visit(tree)
        
        total_items = (docs['documented_functions'] + docs['undocumented_functions'] +
                      docs['documented_classes'] + docs['undocumented_classes'])
        if total_items > 0:
            docs['docstring_coverage'] = round(
                (docs['documented_functions'] + docs['documented_classes']) / total_items * 100, 2)
        
        return docs
    
    def _analyze_imports(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze and categorize imports."""
        imports = {
            'standard_lib': [],
            'third_party': [],
            'local': [],
            'total_imports': 0
        }
        
        stdlib_modules = set(sys.stdlib_module_names)
        
        class ImportVisitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for name in node.names:
                    imports['total_imports'] += 1
                    module = name.name.split('.')[0]
                    if module in stdlib_modules:
                        imports['standard_lib'].append(name.name)
                    elif '.' in name.name:
                        imports['local'].append(name.name)
                    else:
                        imports['third_party'].append(name.name)
            
            def visit_ImportFrom(self, node):
                imports['total_imports'] += 1
                if node.module:
                    module = node.module.split('.')[0]
                    if module in stdlib_modules:
                        imports['standard_lib'].append(f"{node.module}")
                    elif node.level > 0:
                        imports['local'].append(f"{'.'*node.level}{node.module}")
                    else:
                        imports['third_party'].append(node.module)
        
        visitor = ImportVisitor()
        visitor.visit(tree)
        return imports
    
    def _analyze_code_style(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze code style consistency."""
        style = {
            'line_length': {
                'max': 0,
                'avg': 0,
                'over_80': 0
            },
            'indentation': {
                'spaces': 0,
                'tabs': 0
            },
            'trailing_whitespace': 0,
            'blank_lines_between_functions': []
        }
        
        # Line length analysis
        lengths = [len(line) for line in lines]
        if lengths:
            style['line_length']['max'] = max(lengths)
            style['line_length']['avg'] = round(sum(lengths) / len(lengths), 2)
            style['line_length']['over_80'] = sum(1 for l in lengths if l > 80)
        
        # Indentation analysis
        for line in lines:
            if line.startswith(' '):
                style['indentation']['spaces'] += 1
            elif line.startswith('\t'):
                style['indentation']['tabs'] += 1
                
        # Trailing whitespace
        style['trailing_whitespace'] = sum(1 for line in lines if line.rstrip() != line)
        
        return style
    
    def _analyze_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze functions and their properties."""
        functions = []
        
        class FunctionVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                func = {
                    'name': node.name,
                    'args': len(node.args.args),
                    'defaults': len(node.args.defaults),
                    'has_docstring': bool(ast.get_docstring(node)),
                    'decorators': len(node.decorator_list),
                    'line_number': node.lineno
                }
                functions.append(func)
                self.generic_visit(node)
        
        visitor = FunctionVisitor()
        visitor.visit(tree)
        return functions

def analyze_repository(repo_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Analyze all Python files in a repository and return detailed metrics.
    """
    analyzer = CodeAnalyzer()
    results = {}
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    results[file] = analyzer.analyze_file(file_path)
                except Exception as e:
                    results[file] = {'error': str(e)}
    
    return results
