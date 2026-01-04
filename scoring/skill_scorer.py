"""
Rule-based skill evaluation using repository analysis signals.
"""
from typing import Dict, List
from pathlib import Path
from code_analysis.language_detector import detect_frameworks
from code_analysis.structure import count_django_apps
from code_analysis.complexity import calculate_complexity
from shared.utils import calculate_authorship_percentage, validate_skill_breakdown
import os
import re


class SkillScorer:
    """Evaluates developer skills based on repository analysis."""
    
    def __init__(self, repo_path: str, contributor_data: dict):
        self.repo_path = repo_path
        self.contributor_data = contributor_data
        self.frameworks = detect_frameworks(repo_path)
        self.complexity_metrics = calculate_complexity(repo_path)
        
        # Calculate authorship ratio using global formula
        author_lines = contributor_data['lines_added'] + contributor_data['lines_deleted']
        total_lines = contributor_data.get('total_lines_modified_in_repo', author_lines)
        self.authorship_percentage = calculate_authorship_percentage(author_lines, total_lines)
    
    def evaluate_all_skills(self) -> Dict[str, Dict]:
        """
        Evaluate all detected frameworks/technologies.
        
        Returns zero scores for undetected skills to make it explicit.
        
        Returns:
            Dictionary mapping skill names to scores
        """
        skill_scores = {}
        
        # Check React - only if confidence >= 60%
        if 'React' in self.frameworks and self.frameworks['React']['confidence'] >= 60:
            skill_scores['React'] = self._evaluate_react()
        elif 'React' in self.frameworks:
            # Detected but not confident enough
            skill_scores['React'] = {
                'total_score': 0,
                'max_score': 100,
                'percentage': 0,
                'breakdown': [{'criterion': 'react_presence', 'score': 0, 
                              'reason': f"React detected but confidence too low ({self.frameworks['React']['confidence']}% < 60%)"}]
            }
        
        # Check Django - only if confidence >= 60%
        if 'Django' in self.frameworks and self.frameworks['Django']['confidence'] >= 60:
            skill_scores['Django'] = self._evaluate_django()
        elif 'Django' in self.frameworks:
            skill_scores['Django'] = {
                'total_score': 0,
                'max_score': 100,
                'percentage': 0,
                'breakdown': [{'criterion': 'django_presence', 'score': 0, 
                              'reason': f"Django detected but confidence too low ({self.frameworks['Django']['confidence']}% < 60%)"}]
            }
        
        # Check NodeJS - only if confidence >= 60%
        if 'NodeJS' in self.frameworks and self.frameworks['NodeJS']['confidence'] >= 60:
            skill_scores['NodeJS'] = self._evaluate_nodejs()
        elif 'NodeJS' in self.frameworks:
            skill_scores['NodeJS'] = {
                'total_score': 0,
                'max_score': 100,
                'percentage': 0,
                'breakdown': [{'criterion': 'node_presence', 'score': 0, 
                              'reason': f"Node.js detected but confidence too low ({self.frameworks['NodeJS']['confidence']}% < 60%)"}]
            }
        
        # Check TailwindCSS - only if confidence >= 60%
        if 'TailwindCSS' in self.frameworks and self.frameworks['TailwindCSS']['confidence'] >= 60:
            skill_scores['TailwindCSS'] = self._evaluate_tailwind()
        elif 'TailwindCSS' in self.frameworks:
            skill_scores['TailwindCSS'] = {
                'total_score': 0,
                'max_score': 100,
                'percentage': 0,
                'breakdown': [{'criterion': 'tailwind_presence', 'score': 0, 
                              'reason': f"TailwindCSS detected but confidence too low ({self.frameworks['TailwindCSS']['confidence']}% < 60%)"}]
            }
        
        # Evaluate programming languages based on presence
        languages_data = self._get_language_stats()
        
        if languages_data.get('Python', {}).get('file_count', 0) > 0:
            skill_scores['Python'] = self._evaluate_python(languages_data['Python'])
        
        if languages_data.get('JavaScript', {}).get('file_count', 0) > 0:
            skill_scores['JavaScript'] = self._evaluate_javascript(languages_data['JavaScript'])
        
        if languages_data.get('TypeScript', {}).get('file_count', 0) > 0:
            skill_scores['TypeScript'] = self._evaluate_typescript(languages_data['TypeScript'])
        
        if languages_data.get('C', {}).get('file_count', 0) > 0:
            skill_scores['C'] = self._evaluate_c(languages_data['C'])
        
        if languages_data.get('C++', {}).get('file_count', 0) > 0:
            skill_scores['C++'] = self._evaluate_cpp(languages_data['C++'])
        
        return skill_scores
    
    def _evaluate_react(self) -> Dict:
        """Evaluate React skill level."""
        score = 0
        breakdown = []
        
        # Criterion 1: React presence (20 points)
        has_react = 'React' in self.frameworks and self.frameworks['React'].get('confidence', 0) >= 60
        if has_react and self.frameworks['React']['signals'].get('dependencies_found'):
            score += 20
            breakdown.append({'criterion': 'react_presence', 'score': 20, 'reason': 'React dependencies found'})
        else:
            breakdown.append({'criterion': 'react_presence', 'score': 0, 'reason': 'React not detected'})
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: Hooks usage (20 points)
        hooks_count = self._count_code_patterns(['useState(', 'useEffect(', 'useContext(', 'useReducer('])
        if hooks_count >= 10:
            hook_score = 20
        elif hooks_count >= 5:
            hook_score = 12
        elif hooks_count >= 1:
            hook_score = 6
        else:
            hook_score = 0
        
        score += hook_score
        breakdown.append({'criterion': 'hooks_usage', 'score': hook_score, 'reason': f'{hooks_count} hook usages found'})
        
        # Criterion 3: Project size (20 points)
        loc = self.complexity_metrics.get('code_lines', 0)
        if loc >= 3000:
            size_score = 20
        elif loc >= 1500:
            size_score = 12
        elif loc >= 500:
            size_score = 6
        else:
            size_score = 0
        
        score += size_score
        breakdown.append({'criterion': 'project_size', 'score': size_score, 'reason': f'{loc} lines of code'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 30:
            maturity_score = 20
        elif commits >= 15:
            maturity_score = 12
        elif commits >= 5:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_django(self) -> Dict:
        """Evaluate Django skill level."""
        score = 0
        breakdown = []
        
        # Criterion 1: Django presence (20 points)
        has_django = 'Django' in self.frameworks and self.frameworks['Django'].get('confidence', 0) >= 60
        if has_django and self.frameworks['Django']['signals'].get('dependencies_found'):
            score += 20
            breakdown.append({'criterion': 'django_presence', 'score': 20, 'reason': 'Django framework detected'})
        else:
            breakdown.append({'criterion': 'django_presence', 'score': 0, 'reason': 'Django not detected'})
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: App structure (20 points)
        app_count = count_django_apps(self.repo_path)
        if app_count >= 3:
            app_score = 20
        elif app_count >= 2:
            app_score = 12
        elif app_count >= 1:
            app_score = 6
        else:
            app_score = 0
        
        score += app_score
        breakdown.append({'criterion': 'app_structure', 'score': app_score, 'reason': f'{app_count} Django apps found'})
        
        # Criterion 3: ORM usage (20 points)
        orm_count = self._count_code_patterns(['models.Model', '.objects.', '.filter(', '.get('])
        if orm_count >= 10:
            orm_score = 20
        elif orm_count >= 5:
            orm_score = 12
        elif orm_count >= 1:
            orm_score = 6
        else:
            orm_score = 0
        
        score += orm_score
        breakdown.append({'criterion': 'orm_usage', 'score': orm_score, 'reason': f'{orm_count} ORM patterns found'})
        
        # Criterion 4: REST practices (20 points)
        rest_count = self._count_code_patterns(['APIView', 'Serializer', 'status.HTTP_', 'ViewSet'])
        if rest_count >= 8:
            rest_score = 20
        elif rest_count >= 4:
            rest_score = 12
        elif rest_count >= 1:
            rest_score = 6
        else:
            rest_score = 0
        
        score += rest_score
        breakdown.append({'criterion': 'rest_practices', 'score': rest_score, 'reason': f'{rest_count} REST patterns found'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_nodejs(self) -> Dict:
        """Evaluate Node.js skill level."""
        score = 0
        breakdown = []
        
        # Criterion 1: Node presence (20 points)
        has_nodejs = 'NodeJS' in self.frameworks and self.frameworks['NodeJS'].get('confidence', 0) >= 60
        if has_nodejs and self.frameworks['NodeJS']['signals'].get('dependencies_found'):
            score += 20
            breakdown.append({'criterion': 'node_presence', 'score': 20, 'reason': 'Node.js framework detected'})
        else:
            breakdown.append({'criterion': 'node_presence', 'score': 0, 'reason': 'Node.js not detected'})
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: API design (20 points)
        api_count = self._count_code_patterns(['app.get(', 'app.post(', 'app.put(', 'app.delete(', 'router.'])
        if api_count >= 15:
            api_score = 20
        elif api_count >= 8:
            api_score = 12
        elif api_count >= 3:
            api_score = 6
        else:
            api_score = 0
        
        score += api_score
        breakdown.append({'criterion': 'api_design', 'score': api_score, 'reason': f'{api_count} API endpoints found'})
        
        # Criterion 3: Middleware usage (20 points)
        middleware_count = self._count_code_patterns(['app.use(', 'next(', 'middleware'])
        if middleware_count >= 10:
            mw_score = 20
        elif middleware_count >= 5:
            mw_score = 12
        elif middleware_count >= 1:
            mw_score = 6
        else:
            mw_score = 0
        
        score += mw_score
        breakdown.append({'criterion': 'middleware_usage', 'score': mw_score, 'reason': f'{middleware_count} middleware patterns found'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 25:
            maturity_score = 20
        elif commits >= 12:
            maturity_score = 12
        elif commits >= 5:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _get_language_stats(self) -> Dict:
        """Get statistics for each programming language."""
        stats = {}
        
        language_extensions = {
            'Python': ['.py'],
            'JavaScript': ['.js', '.mjs', '.cjs'],
            'TypeScript': ['.ts', '.tsx'],
            'C': ['.c', '.h'],
            'C++': ['.cpp', '.hpp', '.cc', '.cxx']
        }
        
        for lang, extensions in language_extensions.items():
            stats[lang] = {
                'file_count': 0,
                'files': []
            }
            
            for root, dirs, files in os.walk(self.repo_path):
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}]
                
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        stats[lang]['file_count'] += 1
                        stats[lang]['files'].append(Path(root) / file)
        
        return stats
    
    def _evaluate_python(self, lang_stats: Dict) -> Dict:
        """Evaluate Python skill level."""
        score = 0
        breakdown = []
        
        file_count = lang_stats['file_count']
        
        # Criterion 1: Python presence (20 points)
        if file_count >= 10:
            presence_score = 20
        elif file_count >= 5:
            presence_score = 12
        elif file_count >= 1:
            presence_score = 6
        else:
            presence_score = 0
        
        score += presence_score
        breakdown.append({'criterion': 'python_presence', 'score': presence_score, 'reason': f'{file_count} Python files'})
        
        if presence_score == 0:
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: Python structure (20 points)
        structure_patterns = ['__init__.py', 'setup.py', 'pyproject.toml', 'requirements.txt']
        patterns_found = len(self._check_file_patterns(structure_patterns))
        
        if patterns_found >= 3:
            struct_score = 20
        elif patterns_found >= 2:
            struct_score = 12
        elif patterns_found >= 1:
            struct_score = 6
        else:
            struct_score = 0
        
        score += struct_score
        breakdown.append({'criterion': 'python_structure', 'score': struct_score, 'reason': f'{patterns_found} structure files found'})
        
        # Criterion 3: Function complexity (20 points)
        avg_func_len = self.complexity_metrics.get('avg_function_length', 0)
        if avg_func_len > 0 and avg_func_len <= 40:
            complex_score = 20
        elif avg_func_len <= 70:
            complex_score = 12
        else:
            complex_score = 6
        
        score += complex_score
        breakdown.append({'criterion': 'function_complexity', 'score': complex_score, 'reason': f'Avg function length: {avg_func_len:.1f} lines'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 25:
            maturity_score = 20
        elif commits >= 12:
            maturity_score = 12
        elif commits >= 5:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_javascript(self, lang_stats: Dict) -> Dict:
        """Evaluate JavaScript skill level."""
        score = 0
        breakdown = []
        
        file_count = lang_stats['file_count']
        
        # Criterion 1: JS presence (20 points)
        if file_count >= 15:
            presence_score = 20
        elif file_count >= 8:
            presence_score = 12
        elif file_count >= 3:
            presence_score = 6
        else:
            presence_score = 0
        
        score += presence_score
        breakdown.append({'criterion': 'js_presence', 'score': presence_score, 'reason': f'{file_count} JS files'})
        
        if presence_score == 0:
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: Modern JS usage (20 points)
        modern_patterns = ['=>', 'async ', 'await ', 'import ', 'export ']
        modern_count = self._count_code_patterns(modern_patterns)
        
        if modern_count >= 20:
            modern_score = 20
        elif modern_count >= 10:
            modern_score = 12
        elif modern_count >= 3:
            modern_score = 6
        else:
            modern_score = 0
        
        score += modern_score
        breakdown.append({'criterion': 'modern_js_usage', 'score': modern_score, 'reason': f'{modern_count} modern JS patterns'})
        
        # Criterion 3: Modularity (20 points)
        if file_count >= 20:
            mod_score = 20
        elif file_count >= 10:
            mod_score = 12
        else:
            mod_score = 6
        
        score += mod_score
        breakdown.append({'criterion': 'modularity', 'score': mod_score, 'reason': f'{file_count} modular files'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 30:
            maturity_score = 20
        elif commits >= 15:
            maturity_score = 12
        elif commits >= 6:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_typescript(self, lang_stats: Dict) -> Dict:
        """Evaluate TypeScript skill level."""
        score = 0
        breakdown = []
        
        file_count = lang_stats['file_count']
        
        # Criterion 1: TS presence (20 points)
        if file_count >= 10:
            presence_score = 20
        elif file_count >= 5:
            presence_score = 12
        elif file_count >= 1:
            presence_score = 6
        else:
            presence_score = 0
        
        score += presence_score
        breakdown.append({'criterion': 'ts_presence', 'score': presence_score, 'reason': f'{file_count} TS files'})
        
        if presence_score == 0:
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: Type safety (20 points)
        type_patterns = [': string', ': number', 'interface ', 'type ', ': boolean']
        type_count = self._count_code_patterns(type_patterns)
        
        if type_count >= 20:
            type_score = 20
        elif type_count >= 10:
            type_score = 12
        elif type_count >= 3:
            type_score = 6
        else:
            type_score = 0
        
        score += type_score
        breakdown.append({'criterion': 'type_safety', 'score': type_score, 'reason': f'{type_count} type annotations'})
        
        # Criterion 3: Config quality (20 points)
        has_tsconfig = len(self._check_file_patterns(['tsconfig.json'])) > 0
        config_score = 20 if has_tsconfig else 0
        
        score += config_score
        breakdown.append({'criterion': 'config_quality', 'score': config_score, 'reason': 'tsconfig.json found' if has_tsconfig else 'No tsconfig.json'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 25:
            maturity_score = 20
        elif commits >= 12:
            maturity_score = 12
        elif commits >= 5:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_c(self, lang_stats: Dict) -> Dict:
        """Evaluate C skill level."""
        score = 0
        breakdown = []
        
        file_count = lang_stats['file_count']
        
        # Criterion 1: C presence (20 points)
        if file_count >= 10:
            presence_score = 20
        elif file_count >= 5:
            presence_score = 12
        elif file_count >= 1:
            presence_score = 6
        else:
            presence_score = 0
        
        score += presence_score
        breakdown.append({'criterion': 'c_presence', 'score': presence_score, 'reason': f'{file_count} C files'})
        
        if presence_score == 0:
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: Pointer usage (20 points)
        pointer_patterns = ['malloc(', 'free(', 'calloc(', 'realloc(']
        pointer_count = self._count_code_patterns(pointer_patterns)
        
        if pointer_count >= 15:
            pointer_score = 20
        elif pointer_count >= 7:
            pointer_score = 12
        elif pointer_count >= 3:
            pointer_score = 6
        else:
            pointer_score = 0
        
        score += pointer_score
        breakdown.append({'criterion': 'pointer_usage', 'score': pointer_score, 'reason': f'{pointer_count} memory operations'})
        
        # Criterion 3: Modular design (20 points)
        # Count .c and .h file pairs
        c_files = sum(1 for f in lang_stats['files'] if str(f).endswith('.c'))
        h_files = sum(1 for f in lang_stats['files'] if str(f).endswith('.h'))
        pairs = min(c_files, h_files)
        
        if pairs >= 5:
            mod_score = 20
        elif pairs >= 3:
            mod_score = 12
        else:
            mod_score = 6
        
        score += mod_score
        breakdown.append({'criterion': 'modular_design', 'score': mod_score, 'reason': f'{pairs} header/source pairs'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 20:
            maturity_score = 20
        elif commits >= 10:
            maturity_score = 12
        elif commits >= 4:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_cpp(self, lang_stats: Dict) -> Dict:
        """Evaluate C++ skill level."""
        score = 0
        breakdown = []
        
        file_count = lang_stats['file_count']
        
        # Criterion 1: C++ presence (20 points)
        if file_count >= 10:
            presence_score = 20
        elif file_count >= 5:
            presence_score = 12
        elif file_count >= 1:
            presence_score = 6
        else:
            presence_score = 0
        
        score += presence_score
        breakdown.append({'criterion': 'cpp_presence', 'score': presence_score, 'reason': f'{file_count} C++ files'})
        
        if presence_score == 0:
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: OOP usage (20 points)
        oop_patterns = ['class ', 'public:', 'private:', 'protected:', 'virtual ']
        oop_count = self._count_code_patterns(oop_patterns)
        
        if oop_count >= 15:
            oop_score = 20
        elif oop_count >= 7:
            oop_score = 12
        elif oop_count >= 3:
            oop_score = 6
        else:
            oop_score = 0
        
        score += oop_score
        breakdown.append({'criterion': 'oop_usage', 'score': oop_score, 'reason': f'{oop_count} OOP patterns'})
        
        # Criterion 3: Memory management (20 points)
        mem_patterns = ['new ', 'delete ', 'unique_ptr', 'shared_ptr', 'make_unique', 'make_shared']
        mem_count = self._count_code_patterns(mem_patterns)
        
        if mem_count >= 10:
            mem_score = 20
        elif mem_count >= 5:
            mem_score = 12
        elif mem_count >= 2:
            mem_score = 6
        else:
            mem_score = 0
        
        score += mem_score
        breakdown.append({'criterion': 'memory_management', 'score': mem_score, 'reason': f'{mem_count} memory operations'})
        
        # Criterion 4: Git maturity (20 points)
        commits = self.contributor_data.get('commits', 0)
        if commits >= 25:
            maturity_score = 20
        elif commits >= 12:
            maturity_score = 12
        elif commits >= 5:
            maturity_score = 6
        else:
            maturity_score = 0
        
        score += maturity_score
        breakdown.append({'criterion': 'git_maturity', 'score': maturity_score, 'reason': f'{commits} commits'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _evaluate_tailwind(self) -> Dict:
        """Evaluate TailwindCSS skill level."""
        score = 0
        breakdown = []
        
        # Criterion 1: Tailwind presence (20 points)
        has_tailwind = 'TailwindCSS' in self.frameworks
        if has_tailwind:
            score += 20
            breakdown.append({'criterion': 'tailwind_presence', 'score': 20, 'reason': 'TailwindCSS detected'})
        else:
            breakdown.append({'criterion': 'tailwind_presence', 'score': 0, 'reason': 'TailwindCSS not detected'})
            return {'total_score': 0, 'max_score': 100, 'percentage': 0, 'breakdown': breakdown}
        
        # Criterion 2: Utility usage (20 points)
        utility_patterns = ['class="', 'className="', 'flex', 'grid', 'bg-', 'text-']
        utility_count = self._count_code_patterns(utility_patterns)
        
        if utility_count >= 50:
            util_score = 20
        elif utility_count >= 25:
            util_score = 12
        elif utility_count >= 10:
            util_score = 6
        else:
            util_score = 0
        
        score += util_score
        breakdown.append({'criterion': 'utility_usage', 'score': util_score, 'reason': f'{utility_count} utility classes'})
        
        # Criterion 3: Config customization (20 points)
        has_config = len(self._check_file_patterns(['tailwind.config.js', 'tailwind.config.ts'])) > 0
        config_score = 20 if has_config else 0
        
        score += config_score
        breakdown.append({'criterion': 'config_customization', 'score': config_score, 'reason': 'Config file found' if has_config else 'No config file'})
        
        # Criterion 4: Project scale (20 points)
        loc = self.complexity_metrics.get('code_lines', 0)
        if loc >= 2000:
            scale_score = 20
        elif loc >= 1000:
            scale_score = 12
        elif loc >= 300:
            scale_score = 6
        else:
            scale_score = 0
        
        score += scale_score
        breakdown.append({'criterion': 'project_scale', 'score': scale_score, 'reason': f'{loc} lines of code'})
        
        # Criterion 5: Authorship confidence (20 points)
        # Use global formula: (author_lines / total_lines) × 100
        if self.authorship_percentage >= 70:
            auth_score = 20
        elif self.authorship_percentage >= 50:
            auth_score = 12
        elif self.authorship_percentage >= 30:
            auth_score = 6
        else:
            auth_score = 0
        
        score += auth_score
        breakdown.append({'criterion': 'authorship_confidence', 'score': auth_score, 'reason': f'{self.authorship_percentage:.1f}% of repository changes'})
        
        # Validate breakdown
        validate_skill_breakdown(breakdown)
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': score,
            'breakdown': breakdown
        }
    
    def _check_file_patterns(self, patterns: List[str]) -> List[str]:
        """Check if specific file patterns exist."""
        found = []
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}]
            
            for pattern in patterns:
                if pattern in files:
                    found.append(pattern)
        
        return list(set(found))
    
    def _count_code_patterns(self, patterns: List[str]) -> int:
        """Count occurrences of code patterns in repository."""
        count = 0
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', '__pycache__'}]
            
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                    try:
                        file_path = Path(root) / file
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in patterns:
                                count += content.count(pattern)
                    except Exception:
                        pass
        
        return count
