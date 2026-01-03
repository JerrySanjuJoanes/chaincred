"""
Project structure and architecture analysis.
"""
import os
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def analyze_structure(repo_path: str) -> Dict:
    """
    Analyze folder structure and architectural patterns.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dictionary with structure metrics
    """
    structure = {
        'total_files': 0,
        'total_directories': 0,
        'max_depth': 0,
        'file_types': defaultdict(int),
        'architecture_patterns': [],
        'modular_structure': False
    }
    
    # Walk directory tree
    for root, dirs, files in os.walk(repo_path):
        # Filter out common ignore directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build'}]
        
        depth = root[len(repo_path):].count(os.sep)
        structure['max_depth'] = max(structure['max_depth'], depth)
        structure['total_directories'] += len(dirs)
        structure['total_files'] += len(files)
        
        # Count file types
        for file in files:
            ext = Path(file).suffix or 'no_ext'
            structure['file_types'][ext] += 1
    
    # Detect architectural patterns
    structure['architecture_patterns'] = _detect_architecture_patterns(repo_path)
    structure['modular_structure'] = len(structure['architecture_patterns']) > 0
    
    # Convert defaultdict to regular dict
    structure['file_types'] = dict(structure['file_types'])
    
    return structure


def _detect_architecture_patterns(repo_path: str) -> List[str]:
    """Detect common architectural patterns."""
    patterns = []
    
    # Check for MVC pattern
    if _has_mvc_structure(repo_path):
        patterns.append('MVC')
    
    # Check for microservices
    if _has_microservices_structure(repo_path):
        patterns.append('Microservices')
    
    # Check for layered architecture
    if _has_layered_structure(repo_path):
        patterns.append('Layered')
    
    # Check for modular structure
    if _has_modular_structure(repo_path):
        patterns.append('Modular')
    
    return patterns


def _has_mvc_structure(repo_path: str) -> bool:
    """Check if repository follows MVC pattern."""
    mvc_dirs = {'models', 'views', 'controllers'}
    found_dirs = set()
    
    for root, dirs, _ in os.walk(repo_path):
        for d in dirs:
            if d.lower() in mvc_dirs:
                found_dirs.add(d.lower())
    
    return len(found_dirs) >= 2


def _has_microservices_structure(repo_path: str) -> bool:
    """Check for microservices architecture indicators."""
    service_indicators = {'services', 'api', 'gateway'}
    
    for root, dirs, files in os.walk(repo_path):
        # Look for docker-compose or multiple service directories
        if 'docker-compose.yml' in files or 'docker-compose.yaml' in files:
            return True
        
        for d in dirs:
            if d.lower() in service_indicators:
                return True
    
    return False


def _has_layered_structure(repo_path: str) -> bool:
    """Check for layered architecture."""
    layer_dirs = {'api', 'business', 'data', 'domain', 'infrastructure', 'application'}
    found_layers = set()
    
    for root, dirs, _ in os.walk(repo_path):
        for d in dirs:
            if d.lower() in layer_dirs:
                found_layers.add(d.lower())
    
    return len(found_layers) >= 2


def _has_modular_structure(repo_path: str) -> bool:
    """Check for modular organization."""
    # Check for multiple subdirectories with similar structure
    subdirs_with_files = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Count subdirectories that have code files
        if len(files) > 0:
            code_files = [f for f in files if Path(f).suffix in {'.py', '.js', '.ts', '.java', '.go'}]
            if len(code_files) > 0:
                subdirs_with_files += 1
    
    return subdirs_with_files > 3


def count_django_apps(repo_path: str) -> int:
    """Count Django app modules."""
    app_count = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Django app has models.py, views.py, or apps.py
        django_files = {'models.py', 'views.py', 'apps.py'}
        if any(f in files for f in django_files):
            app_count += 1
    
    return app_count
