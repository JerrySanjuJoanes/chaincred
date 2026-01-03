"""
Code complexity analysis.
"""
import os
import re
from pathlib import Path
from typing import Dict


def calculate_complexity(repo_path: str) -> Dict:
    """
    Calculate code complexity metrics.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dictionary with complexity metrics
    """
    metrics = {
        'total_lines': 0,
        'code_lines': 0,
        'comment_lines': 0,
        'blank_lines': 0,
        'avg_file_size': 0,
        'max_file_size': 0,
        'functions_count': 0,
        'classes_count': 0,
        'avg_function_length': 0
    }
    
    file_sizes = []
    function_lengths = []
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build'}]
        
        for file in files:
            ext = Path(file).suffix
            if ext in {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs', '.rb', '.php'}:
                file_path = Path(root) / file
                file_metrics = _analyze_file(file_path, ext)
                
                metrics['total_lines'] += file_metrics['total_lines']
                metrics['code_lines'] += file_metrics['code_lines']
                metrics['comment_lines'] += file_metrics['comment_lines']
                metrics['blank_lines'] += file_metrics['blank_lines']
                metrics['functions_count'] += file_metrics['functions_count']
                metrics['classes_count'] += file_metrics['classes_count']
                
                file_sizes.append(file_metrics['total_lines'])
                function_lengths.extend(file_metrics['function_lengths'])
    
    # Calculate averages
    if file_sizes:
        metrics['avg_file_size'] = sum(file_sizes) / len(file_sizes)
        metrics['max_file_size'] = max(file_sizes)
    
    if function_lengths:
        metrics['avg_function_length'] = sum(function_lengths) / len(function_lengths)
    
    return metrics


def _analyze_file(file_path: Path, ext: str) -> Dict:
    """Analyze individual file complexity."""
    metrics = {
        'total_lines': 0,
        'code_lines': 0,
        'comment_lines': 0,
        'blank_lines': 0,
        'functions_count': 0,
        'classes_count': 0,
        'function_lengths': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            metrics['total_lines'] = len(lines)
            
            in_multiline_comment = False
            current_function_lines = 0
            in_function = False
            
            for line in lines:
                stripped = line.strip()
                
                # Count blank lines
                if not stripped:
                    metrics['blank_lines'] += 1
                    continue
                
                # Handle multi-line comments
                if ext == '.py':
                    if '"""' in stripped or "'''" in stripped:
                        in_multiline_comment = not in_multiline_comment
                        metrics['comment_lines'] += 1
                        continue
                    if in_multiline_comment:
                        metrics['comment_lines'] += 1
                        continue
                    if stripped.startswith('#'):
                        metrics['comment_lines'] += 1
                        continue
                
                elif ext in {'.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs'}:
                    if '/*' in stripped:
                        in_multiline_comment = True
                        metrics['comment_lines'] += 1
                    if in_multiline_comment:
                        if '*/' in stripped:
                            in_multiline_comment = False
                        continue
                    if stripped.startswith('//'):
                        metrics['comment_lines'] += 1
                        continue
                
                # Count code lines
                metrics['code_lines'] += 1
                
                # Count functions and classes
                if ext == '.py':
                    if re.match(r'^\s*def\s+\w+', line):
                        if in_function and current_function_lines > 0:
                            metrics['function_lengths'].append(current_function_lines)
                        metrics['functions_count'] += 1
                        in_function = True
                        current_function_lines = 1
                    elif re.match(r'^\s*class\s+\w+', line):
                        if in_function and current_function_lines > 0:
                            metrics['function_lengths'].append(current_function_lines)
                        metrics['classes_count'] += 1
                        in_function = False
                        current_function_lines = 0
                    elif in_function:
                        current_function_lines += 1
                
                elif ext in {'.js', '.jsx', '.ts', '.tsx'}:
                    if re.search(r'function\s+\w+|const\s+\w+\s*=\s*\(.*\)\s*=>', line):
                        if in_function and current_function_lines > 0:
                            metrics['function_lengths'].append(current_function_lines)
                        metrics['functions_count'] += 1
                        in_function = True
                        current_function_lines = 1
                    elif re.search(r'class\s+\w+', line):
                        metrics['classes_count'] += 1
                    elif in_function:
                        current_function_lines += 1
            
            # Add last function length
            if in_function and current_function_lines > 0:
                metrics['function_lengths'].append(current_function_lines)
    
    except Exception:
        pass
    
    return metrics
