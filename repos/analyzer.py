"""
Repository analysis module for extracting contributor metrics.
"""
from pathlib import Path
from pydriller import Repository
from collections import defaultdict
from typing import Dict, Set, Tuple

from code_analysis.language_detector import detect_languages, detect_frameworks
from code_analysis.structure import analyze_structure
from code_analysis.complexity import calculate_complexity
from code_analysis.lint_metrics import analyze_code_quality
from code_analysis.test_detector import detect_tests
from shared.utils import is_bot_user, AnalysisWarnings


def analyze_repository(repo_path: str) -> Tuple[Dict, int, Set, Dict, Dict, AnalysisWarnings]:
    """
    Analyze repository commits and contributors with advanced metrics.
    
    Args:
        repo_path: Path to the cloned repository
        
    Returns:
        Tuple of (contributors_data, total_commits, all_files, file_extensions, analysis_data, warnings)
    """
    warnings = AnalysisWarnings()
    print("\n🔍 Stage 1: Static Analysis")
    
    # Detect languages and frameworks
    languages = detect_languages(repo_path)
    frameworks = detect_frameworks(repo_path)
    
    print("🔍 Stage 2: Commit Analysis")
    print("🔍 Stage 3: Authorship Analysis")
    print("🔍 Stage 4: Code Intelligence Engine\n")
    
    contributors = defaultdict(lambda: {
        'commits': 0,
        'lines_added': 0,
        'lines_deleted': 0,
        'files_changed': set(),
        'commit_messages': [],
        'file_types': defaultdict(int),
        'commit_timestamps': [],
        'complexity_metrics': [],
        'churn_rate': 0,
        'is_bot': False
    })
    
    total_commits = 0
    total_commits_excluding_bots = 0
    all_files = set()
    file_extensions = defaultdict(int)
    total_lines_modified = 0  # Global total for authorship calculation
    bot_count = 0
    
    for commit in Repository(repo_path).traverse_commits():
        total_commits += 1
        author = commit.author.name
        email = commit.author.email
        
        # Detect if author is a bot
        is_bot = is_bot_user(author, email)
        contributors[author]['is_bot'] = is_bot
        
        if is_bot:
            bot_count += 1
        else:
            total_commits_excluding_bots += 1
        
        contributors[author]['commits'] += 1
        contributors[author]['lines_added'] += commit.insertions
        contributors[author]['lines_deleted'] += commit.deletions
        contributors[author]['commit_messages'].append(commit.msg)
        contributors[author]['commit_timestamps'].append(commit.committer_date)
        
        # Track total lines modified globally (for authorship percentage)
        total_lines_modified += (commit.insertions + commit.deletions)
        
        # Calculate complexity per commit (lines changed)
        complexity = commit.insertions + commit.deletions
        contributors[author]['complexity_metrics'].append(complexity)
        
        for modified_file in commit.modified_files:
            filename = modified_file.filename
            contributors[author]['files_changed'].add(filename)
            all_files.add(filename)
            
            # Track file types
            ext = Path(filename).suffix or 'no_ext'
            contributors[author]['file_types'][ext] += 1
            file_extensions[ext] += 1
    
    # Calculate churn rate and authorship for each contributor
    for author in contributors:
        total_changes = contributors[author]['lines_added'] + contributors[author]['lines_deleted']
        contributors[author]['churn_rate'] = contributors[author]['lines_deleted'] / max(total_changes, 1)
        
        # Store total_lines_modified globally for authorship calculation
        contributors[author]['total_lines_modified_in_repo'] = total_lines_modified
    
    # Add warnings
    if bot_count > 0:
        warnings.add_warning(
            f"Detected {bot_count} bot/automated contributor(s). "
            f"Bot commits excluded from skill scoring."
        )
    
    if total_commits < 10:
        warnings.add_warning(
            f"Small repository ({total_commits} commits). "
            f"Skill scores may not be representative."
        )
    
    if len(contributors) == 1:
        warnings.add_assumption(
            "Single contributor detected. Authorship confidence set to 100%."
        )
    
    # Perform additional code analysis
    print("📊 Analyzing project structure...")
    structure = analyze_structure(repo_path)
    
    print("📊 Calculating complexity metrics...")
    complexity = calculate_complexity(repo_path)
    
    print("📊 Analyzing code quality...")
    quality = analyze_code_quality(repo_path)
    
    print("📊 Detecting tests...")
    tests = detect_tests(repo_path)
    
    # Package analysis data
    analysis_data = {
        'languages': languages,
        'frameworks': frameworks,
        'structure': structure,
        'complexity': complexity,
        'quality': quality,
        'tests': tests
    }
    
    return contributors, total_commits_excluding_bots, all_files, file_extensions, analysis_data, warnings
