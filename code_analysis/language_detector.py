"""
Language and framework detection module.
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


# Language patterns
# Note: JSX/TSX are treated as subsets of JavaScript/TypeScript, not separate languages
LANGUAGE_EXTENSIONS = {
    'Python': ['.py', '.pyw', '.pyx'],
    'JavaScript': ['.js', '.mjs', '.cjs', '.jsx'],  # JSX is JavaScript
    'TypeScript': ['.ts', '.tsx'],  # TSX is TypeScript
    'Java': ['.java'],
    'C++': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
    'C': ['.c', '.h'],
    'Go': ['.go'],
    'Rust': ['.rs'],
    'Ruby': ['.rb'],
    'PHP': ['.php'],
    'Swift': ['.swift'],
    'Kotlin': ['.kt'],
    'HTML': ['.html', '.htm'],
    'CSS': ['.css', '.scss', '.sass', '.less']
}

# Framework detection patterns
FRAMEWORK_PATTERNS = {
    'React': {
        'dependencies': ['react', 'react-dom'],
        'dev_dependencies': ['@types/react'],
        'files': ['.jsx', '.tsx'],
        'code_patterns': ['import React', 'from "react"', "from 'react'"],
        'package_file': 'package.json'
    },
    'Django': {
        'dependencies': ['django', 'Django'],
        'files': ['manage.py', 'settings.py', 'wsgi.py'],
        'code_patterns': ['from django', 'import django', 'models.Model'],
        'package_file': 'requirements.txt'
    },
    'Flask': {
        'dependencies': ['flask', 'Flask'],
        'code_patterns': ['from flask', 'Flask(__name__)'],
        'package_file': 'requirements.txt'
    },
    'NodeJS': {
        'dependencies': ['express', 'fastify', 'koa', 'nest'],
        'files': ['server.js', 'app.js', 'index.js'],
        'code_patterns': ['require(', 'app.listen(', 'express()'],
        'package_file': 'package.json'
    },
    'Vue': {
        'dependencies': ['vue'],
        'files': ['.vue'],
        'code_patterns': ['Vue.component', 'new Vue'],
        'package_file': 'package.json'
    },
    'Angular': {
        'dependencies': ['@angular/core'],
        'files': ['angular.json'],
        'code_patterns': ['@Component', '@NgModule'],
        'package_file': 'package.json'
    },
    'FastAPI': {
        'dependencies': ['fastapi'],
        'code_patterns': ['from fastapi', 'FastAPI()'],
        'package_file': 'requirements.txt'
    },
    'Spring': {
        'files': ['pom.xml', 'build.gradle'],
        'code_patterns': ['@SpringBootApplication', '@Controller'],
        'package_file': 'pom.xml'
    },
    'TailwindCSS': {
        'dependencies': ['tailwindcss'],
        'files': ['tailwind.config.js', 'tailwind.config.ts'],
        'code_patterns': ['@tailwind', '@apply', 'tailwind'],
        'package_file': 'package.json'
    }
}


def detect_languages(repo_path: str) -> Dict[str, int]:
    """
    Detect programming languages used in the repository.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dictionary mapping language names to line counts
    """
    languages = defaultdict(int)
    
    for root, dirs, files in os.walk(repo_path):
        # Skip common ignore directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'dist', 'build'}]
        
        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()
            
            # Count lines for each language
            for lang, extensions in LANGUAGE_EXTENSIONS.items():
                if ext in extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            languages[lang] += lines
                    except Exception:
                        pass
                    break
    
    return dict(languages)


def detect_frameworks(repo_path: str) -> Dict[str, Dict]:
    """
    Detect frameworks and technologies used in the repository.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dictionary with framework detection results
    """
    detected_frameworks = {}
    
    for framework, patterns in FRAMEWORK_PATTERNS.items():
        score = 0
        signals = {
            'dependencies_found': [],
            'files_found': [],
            'patterns_found': []
        }
        
        # Check package files
        package_file = patterns.get('package_file')
        if package_file:
            package_path = Path(repo_path) / package_file
            if package_path.exists():
                deps_found = _check_dependencies(package_path, patterns.get('dependencies', []))
                signals['dependencies_found'] = deps_found
                if deps_found:
                    score += 40  # Stronger signal for dependencies
        
        # Check for specific files
        if patterns.get('files'):
            files_found = _check_files(repo_path, patterns['files'])
            signals['files_found'] = files_found
            if files_found:
                score += 30  # Stronger signal for framework files
        
        # Check code patterns
        if patterns.get('code_patterns'):
            patterns_found = _check_code_patterns(repo_path, patterns['code_patterns'])
            signals['patterns_found'] = patterns_found
            if patterns_found:
                score += 30  # Code patterns are strong indicators
        
        # Check file extensions (only if other signals present)
        if score > 0 and patterns.get('files') and any(f.startswith('.') for f in patterns['files']):
            ext_found = _check_extensions(repo_path, [f for f in patterns['files'] if f.startswith('.')])
            if ext_found:
                score += 10
        
        # Only include frameworks with confidence >= 50%
        if score >= 50:
            detected_frameworks[framework] = {
                'confidence': min(score, 100),
                'signals': signals
            }
    
    return detected_frameworks


def _check_dependencies(package_path: Path, dependencies: List[str]) -> List[str]:
    """Check if dependencies exist in package file."""
    found = []
    
    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # For package.json
            if package_path.name == 'package.json':
                try:
                    data = json.loads(content)
                    all_deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    for dep in dependencies:
                        if dep in all_deps:
                            found.append(dep)
                except json.JSONDecodeError:
                    pass
            
            # For requirements.txt
            elif package_path.name == 'requirements.txt':
                for dep in dependencies:
                    if dep.lower() in content.lower():
                        found.append(dep)
    except Exception:
        pass
    
    return found


def _check_files(repo_path: str, filenames: List[str]) -> List[str]:
    """Check if specific files exist in repository."""
    found = []
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv'}]
        
        for filename in filenames:
            if not filename.startswith('.'):  # Not an extension
                if filename in files:
                    found.append(filename)
    
    return list(set(found))


def _check_code_patterns(repo_path: str, patterns: List[str]) -> List[str]:
    """Check for code patterns in repository files."""
    found = set()
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}]
        
        for file in files:
            if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs')):
                try:
                    file_path = Path(root) / file
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for pattern in patterns:
                            if pattern in content:
                                found.add(pattern)
                except Exception:
                    pass
    
    return list(found)


def _check_extensions(repo_path: str, extensions: List[str]) -> bool:
    """Check if files with specific extensions exist."""
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv'}]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                return True
    
    return False
