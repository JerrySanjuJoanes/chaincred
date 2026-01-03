"""
Comprehensive skill detection engine for analyzing code repositories.
Detects programming languages, frameworks, and technologies with evidence.
"""
import os
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path


class SkillDetector:
    """Detect technologies and skills from repository files."""
    
    # File extension to language/framework mapping
    FILE_EXTENSIONS = {
        '.py': ['Python'],
        '.js': ['JavaScript'],
        '.jsx': ['JavaScript', 'React'],
        '.ts': ['TypeScript'],
        '.tsx': ['TypeScript', 'React'],
        '.java': ['Java'],
        '.cpp': ['C++'],
        '.c': ['C'],
        '.cs': ['C#'],
        '.rb': ['Ruby'],
        '.go': ['Go'],
        '.rs': ['Rust'],
        '.php': ['PHP'],
        '.html': ['HTML'],
        '.css': ['CSS'],
        '.scss': ['CSS', 'SASS'],
        '.sass': ['CSS', 'SASS'],
        '.sql': ['SQL'],
        '.r': ['R'],
        '.m': ['MATLAB'],
        '.swift': ['Swift'],
        '.kt': ['Kotlin'],
        '.scala': ['Scala'],
    }
    
    # Import patterns for framework detection
    IMPORT_PATTERNS = {
        'React': [
            r'from\s+["\']react["\']',
            r'import\s+React',
            r'import\s+\{[^}]*\}\s+from\s+["\']react["\']',
        ],
        'Flask': [
            r'from\s+flask\s+import',
            r'import\s+flask',
        ],
        'Django': [
            r'from\s+django',
            r'import\s+django',
        ],
        'Express': [
            r'require\(["\']express["\']\)',
            r'from\s+["\']express["\']',
        ],
        'Vue': [
            r'from\s+["\']vue["\']',
            r'import\s+Vue',
        ],
        'Angular': [
            r'from\s+["\']@angular',
            r'import\s+\{[^}]*\}\s+from\s+["\']@angular',
        ],
        'Node.js': [
            r'require\(["\'][^"\']+["\']\)',
            r'process\.env',
        ],
        'TailwindCSS': [
            r'@tailwind',
            r'tailwindcss',
        ],
        'Bootstrap': [
            r'bootstrap',
            r'class="[^"]*\b(btn|container|row|col-)',
        ],
        'Next.js': [
            r'from\s+["\']next',
            r'import\s+\{[^}]*\}\s+from\s+["\']next',
        ],
        'FastAPI': [
            r'from\s+fastapi',
            r'import\s+FastAPI',
        ],
        'Spring': [
            r'import\s+org\.springframework',
            r'@SpringBootApplication',
        ],
    }
    
    # Package file indicators
    PACKAGE_FILES = {
        'Node.js': ['package.json', 'package-lock.json', 'yarn.lock'],
        'Python': ['requirements.txt', 'setup.py', 'Pipfile', 'pyproject.toml'],
        'Ruby': ['Gemfile', 'Gemfile.lock'],
        'Java': ['pom.xml', 'build.gradle'],
        'PHP': ['composer.json'],
        'Go': ['go.mod', 'go.sum'],
        'Rust': ['Cargo.toml', 'Cargo.lock'],
    }
    
    # Database patterns
    DATABASE_PATTERNS = {
        'SQL': [r'SELECT\s+', r'INSERT\s+INTO', r'CREATE\s+TABLE', r'UPDATE\s+'],
        'MongoDB': [r'mongoose', r'mongodb', r'\.find\(', r'\.aggregate\('],
        'PostgreSQL': [r'postgresql', r'psycopg2', r'pg\.Pool'],
        'MySQL': [r'mysql', r'pymysql'],
        'Redis': [r'redis', r'\.hset\(', r'\.get\('],
        'Firebase': [r'firebase', r'firestore'],
    }
    
    def __init__(self, repo_path: str):
        """
        Initialize skill detector for a repository.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = Path(repo_path)
        self.detected_skills = {}
        
    def detect_all_skills(self, user_files: List[str]) -> Dict[str, Dict]:
        """
        Detect all skills from repository files.
        
        Args:
            user_files: List of files modified by the user
            
        Returns:
            Dictionary mapping skill names to evidence details
        """
        skills = {}
        
        # Detect from file extensions
        ext_skills = self._detect_from_extensions(user_files)
        for skill, data in ext_skills.items():
            if skill not in skills:
                skills[skill] = {'files': [], 'imports': [], 'patterns': []}
            skills[skill]['files'].extend(data['files'])
        
        # Detect from file contents
        content_skills = self._detect_from_contents(user_files)
        for skill, data in content_skills.items():
            if skill not in skills:
                skills[skill] = {'files': [], 'imports': [], 'patterns': []}
            skills[skill]['imports'].extend(data.get('imports', []))
            skills[skill]['patterns'].extend(data.get('patterns', []))
        
        # Detect from package files
        package_skills = self._detect_from_packages()
        for skill in package_skills:
            if skill not in skills:
                skills[skill] = {'files': [], 'imports': [], 'patterns': []}
            skills[skill]['patterns'].append('Package file detected')
        
        self.detected_skills = skills
        return skills
    
    def _detect_from_extensions(self, files: List[str]) -> Dict[str, Dict]:
        """Detect skills based on file extensions."""
        skills = {}
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in self.FILE_EXTENSIONS:
                for skill in self.FILE_EXTENSIONS[ext]:
                    if skill not in skills:
                        skills[skill] = {'files': []}
                    skills[skill]['files'].append(file)
        
        return skills
    
    def _detect_from_contents(self, files: List[str]) -> Dict[str, Dict]:
        """Detect frameworks from file contents."""
        skills = {}
        
        for file in files:
            try:
                file_path = self.repo_path / file
                if not file_path.exists() or file_path.is_dir():
                    continue
                
                # Read file with error handling
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except:
                    continue
                
                # Check import patterns
                for skill, patterns in self.IMPORT_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            if skill not in skills:
                                skills[skill] = {'imports': [], 'patterns': []}
                            if 'imports' not in skills[skill]:
                                skills[skill]['imports'] = []
                            skills[skill]['imports'].append(f"{file}: {pattern}")
                            break
                
                # Check database patterns
                for db, patterns in self.DATABASE_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            if db not in skills:
                                skills[db] = {'patterns': []}
                            if 'patterns' not in skills[db]:
                                skills[db]['patterns'] = []
                            skills[db]['patterns'].append(f"{file}: {pattern}")
                            break
            
            except Exception as e:
                continue
        
        return skills
    
    def _detect_from_packages(self) -> Set[str]:
        """Detect skills from package manager files."""
        skills = set()
        
        for skill, files in self.PACKAGE_FILES.items():
            for filename in files:
                file_path = self.repo_path / filename
                if file_path.exists():
                    skills.add(skill)
                    break
        
        return skills
    
    def get_skill_evidence(self, skill: str) -> Dict:
        """
        Get detailed evidence for a specific skill.
        
        Args:
            skill: Skill name to check
            
        Returns:
            Dictionary with evidence details
        """
        if skill in self.detected_skills:
            return self.detected_skills[skill]
        
        # Check case-insensitive
        for detected_skill, evidence in self.detected_skills.items():
            if detected_skill.lower() == skill.lower():
                return evidence
        
        return {'files': [], 'imports': [], 'patterns': []}
