"""
Test detection and coverage analysis.
"""
import os
import re
from pathlib import Path
from typing import Dict, List


def detect_tests(repo_path: str) -> Dict:
    """
    Detect test files and testing frameworks.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dictionary with test metrics
    """
    metrics = {
        'has_tests': False,
        'test_files_count': 0,
        'test_frameworks': [],
        'test_files': [],
        'estimated_coverage': 0.0
    }
    
    test_patterns = {
        'pytest': r'import pytest|from pytest',
        'unittest': r'import unittest|from unittest',
        'jest': r'describe\(|test\(|it\(',
        'mocha': r'describe\(|it\(',
        'jasmine': r'describe\(|it\(',
        'django_test': r'from django.test',
        'go_test': r'func Test\w+\(t \*testing\.T\)'
    }
    
    test_file_patterns = [
        r'test_.*\.py$',
        r'.*_test\.py$',
        r'.*\.test\.(js|ts|jsx|tsx)$',
        r'.*\.spec\.(js|ts|jsx|tsx)$',
        r'.*_test\.go$'
    ]
    
    total_code_files = 0
    frameworks_found = set()
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build'}]
        
        for file in files:
            ext = Path(file).suffix
            
            # Count code files
            if ext in {'.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.java'}:
                total_code_files += 1
            
            # Check if it's a test file
            is_test_file = any(re.search(pattern, file) for pattern in test_file_patterns)
            
            if is_test_file or 'test' in root.lower():
                metrics['test_files_count'] += 1
                metrics['test_files'].append(str(Path(root) / file))
                metrics['has_tests'] = True
                
                # Analyze test file content
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        for framework, pattern in test_patterns.items():
                            if re.search(pattern, content):
                                frameworks_found.add(framework)
                
                except Exception:
                    pass
    
    metrics['test_frameworks'] = list(frameworks_found)
    
    # Estimate coverage (very rough estimate)
    if total_code_files > 0:
        coverage_ratio = metrics['test_files_count'] / total_code_files
        metrics['estimated_coverage'] = min(coverage_ratio * 100, 100)
    
    return metrics
