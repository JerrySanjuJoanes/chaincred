"""
Code quality and linting metrics.
"""
import os
import re
from pathlib import Path
from typing import Dict


def analyze_code_quality(repo_path: str) -> Dict:
    """
    Analyze code quality indicators.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dictionary with quality metrics
    """
    metrics = {
        'has_linter_config': False,
        'has_formatter_config': False,
        'has_type_checking': False,
        'documentation_ratio': 0.0,
        'naming_conventions_score': 0.0,
        'config_files_found': []
    }
    
    # Check for configuration files
    config_files = {
        '.eslintrc', '.eslintrc.js', '.eslintrc.json',
        '.prettierrc', '.prettierrc.json',
        'pylint.rc', '.pylintrc', 'setup.cfg',
        'tslint.json', 'tsconfig.json',
        '.flake8', 'pyproject.toml'
    }
    
    for root, dirs, files in os.walk(repo_path):
        if root == repo_path:  # Only check root level
            for config in config_files:
                if config in files:
                    metrics['config_files_found'].append(config)
                    
                    if config in {'.eslintrc', '.eslintrc.js', '.eslintrc.json', '.pylintrc', 'pylint.rc', '.flake8'}:
                        metrics['has_linter_config'] = True
                    
                    if config in {'.prettierrc', '.prettierrc.json'}:
                        metrics['has_formatter_config'] = True
                    
                    if config in {'tsconfig.json', 'mypy.ini'}:
                        metrics['has_type_checking'] = True
    
    # Analyze documentation
    metrics['documentation_ratio'] = _calculate_documentation_ratio(repo_path)
    
    # Analyze naming conventions
    metrics['naming_conventions_score'] = _analyze_naming_conventions(repo_path)
    
    return metrics


def _calculate_documentation_ratio(repo_path: str) -> float:
    """Calculate ratio of documented code."""
    total_functions = 0
    documented_functions = 0
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}]
        
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                funcs, docs = _count_python_docstrings(file_path)
                total_functions += funcs
                documented_functions += docs
            
            elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                file_path = Path(root) / file
                funcs, docs = _count_js_comments(file_path)
                total_functions += funcs
                documented_functions += docs
    
    if total_functions == 0:
        return 0.0
    
    return (documented_functions / total_functions) * 100


def _count_python_docstrings(file_path: Path) -> tuple:
    """Count Python functions and their docstrings."""
    functions = 0
    documented = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if re.match(r'^\s*def\s+\w+', lines[i]):
                    functions += 1
                    # Check next line for docstring
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line.startswith('"""') or next_line.startswith("'''"):
                            documented += 1
                
                i += 1
    
    except Exception:
        pass
    
    return functions, documented


def _count_js_comments(file_path: Path) -> tuple:
    """Count JavaScript functions and their JSDoc comments."""
    functions = 0
    documented = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if re.search(r'function\s+\w+|const\s+\w+\s*=.*=>|export\s+function', lines[i]):
                    functions += 1
                    # Check previous lines for JSDoc
                    if i > 0:
                        prev_line = lines[i - 1].strip()
                        if prev_line.startswith('/**') or '*/' in prev_line:
                            documented += 1
                
                i += 1
    
    except Exception:
        pass
    
    return functions, documented


def _analyze_naming_conventions(repo_path: str) -> float:
    """Analyze adherence to naming conventions."""
    score = 0.0
    checks = 0
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}]
        
        for file in files:
            if file.endswith('.py'):
                # Python should use snake_case
                if '_' in file or file.islower():
                    score += 1
                checks += 1
            
            elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                # JavaScript/TypeScript often use camelCase or PascalCase
                if file[0].isupper() or file[0].islower():
                    score += 1
                checks += 1
    
    if checks == 0:
        return 0.0
    
    return (score / checks) * 100
