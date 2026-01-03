"""
Skill scoring calculations for contributor assessment.
"""
from typing import Dict, Set
from config import (
    WEIGHTS, CODE_QUALITY, COMMIT_MATURITY, 
    PROJECT_COMPLEXITY, AUTHORSHIP_CONFIDENCE
)
from utils import validate_score, calculate_authorship_percentage


def calculate_code_quality(contributor_data: dict) -> float:
    """
    Calculate code quality score (0-100).
    Factors: commit message quality, churn rate, file diversity
    
    Args:
        contributor_data: Dictionary containing contributor metrics
        
    Returns:
        Code quality score (0-100)
    """
    # Commit message quality (meaningful commits)
    messages = contributor_data['commit_messages']
    meaningful_commits = sum(
        1 for msg in messages 
        if len(msg.split()) > CODE_QUALITY['min_meaningful_words']
    )
    message_quality = (meaningful_commits / max(len(messages), 1)) * CODE_QUALITY['message_quality_weight']
    
    # Low churn rate is better (less code deletion)
    churn_score = (1 - contributor_data['churn_rate']) * CODE_QUALITY['churn_rate_weight']
    
    # File diversity (working on multiple file types)
    file_diversity = min(
        len(contributor_data['file_types']) * CODE_QUALITY['diversity_multiplier'], 
        CODE_QUALITY['file_diversity_weight']
    )
    
    return min(message_quality + churn_score + file_diversity, 100)


def calculate_authorship_confidence(contributor_data: dict, total_commits: int) -> float:
    """
    Calculate authorship confidence (0-100).
    
    GLOBAL FORMULA:
    authorship_confidence = (lines_modified_by_author / total_lines_modified_in_repo) × 100
    
    This represents what percentage of all code changes in the repository 
    were made by this contributor.
    
    Args:
        contributor_data: Dictionary containing contributor metrics
        total_commits: Total number of commits in repository (excluding bots)
        
    Returns:
        Authorship confidence score (0-100)
    """
    # Use the global authorship formula
    author_lines = contributor_data['lines_added'] + contributor_data['lines_deleted']
    total_lines = contributor_data.get('total_lines_modified_in_repo', author_lines)
    
    # Calculate raw authorship percentage
    authorship_pct = calculate_authorship_percentage(author_lines, total_lines)
    
    # This is already a 0-100 value representing true authorship
    # No additional weighting needed - this IS the authorship confidence
    return min(authorship_pct, 100.0)


def calculate_commit_maturity(contributor_data: dict) -> float:
    """
    Calculate commit maturity (0-100).
    Factors: commit patterns, complexity trends
    
    Args:
        contributor_data: Dictionary containing contributor metrics
        
    Returns:
        Commit maturity score (0-100)
    """
    # Average commit size (smaller, frequent commits are more mature)
    avg_complexity = sum(contributor_data['complexity_metrics']) / max(
        len(contributor_data['complexity_metrics']), 1
    )
    
    # Prefer moderate complexity (50-200 lines per commit)
    min_complexity = COMMIT_MATURITY['optimal_min_complexity']
    max_complexity = COMMIT_MATURITY['optimal_max_complexity']
    
    if min_complexity <= avg_complexity <= max_complexity:
        complexity_score = 60
    elif avg_complexity < min_complexity:
        complexity_score = 40
    else:
        complexity_score = max(20, 60 - (avg_complexity - max_complexity) / 10)
    
    # Commit frequency consistency
    timestamps = contributor_data['commit_timestamps']
    if len(timestamps) > 1:
        timestamps_sorted = sorted(timestamps)
        intervals = [
            (timestamps_sorted[i+1] - timestamps_sorted[i]).days 
            for i in range(len(timestamps_sorted)-1)
        ]
        avg_interval = sum(intervals) / len(intervals)
        
        # Prefer commits every 1-7 days
        min_interval = COMMIT_MATURITY['optimal_min_interval_days']
        max_interval = COMMIT_MATURITY['optimal_max_interval_days']
        center = COMMIT_MATURITY['optimal_interval_center']
        
        if min_interval <= avg_interval <= max_interval:
            consistency_score = 40
        else:
            consistency_score = max(10, 40 - abs(avg_interval - center) * 2)
    else:
        consistency_score = 20
    
    return min(complexity_score + consistency_score, 100)


def calculate_project_complexity(
    contributor_data: dict, 
    all_files: Set[str], 
    file_extensions: dict
) -> float:
    """
    Calculate project complexity contribution (0-100).
    Factors: file count, diverse technologies, code volume
    
    Args:
        contributor_data: Dictionary containing contributor metrics
        all_files: Set of all files in repository
        file_extensions: Dictionary of file extension counts
        
    Returns:
        Project complexity score (0-100)
    """
    # Files touched percentage
    files_touched = len(contributor_data['files_changed']) / max(len(all_files), 1)
    file_coverage = min(
        files_touched * 100, 
        PROJECT_COMPLEXITY['file_coverage_weight']
    )
    
    # Technology diversity
    tech_diversity = min(
        len(contributor_data['file_types']) * PROJECT_COMPLEXITY['diversity_multiplier'], 
        PROJECT_COMPLEXITY['tech_diversity_weight']
    )
    
    # Code volume
    total_lines = contributor_data['lines_added']
    volume_score = min(
        total_lines / PROJECT_COMPLEXITY['volume_divisor'], 
        PROJECT_COMPLEXITY['volume_weight']
    )
    
    return min(file_coverage + tech_diversity + volume_score, 100)


def calculate_skill_score(
    contributor_data: dict, 
    total_commits: int, 
    all_files: Set[str], 
    file_extensions: dict
) -> Dict[str, float]:
    """
    Calculate final skill score using weighted formula:
    Skill Score = 0.35 * Code Quality + 0.25 * Authorship Confidence 
                + 0.20 * Commit Maturity + 0.10 * Project Complexity
    
    All sub-scores are validated to be in [0, 100] range.
    
    Args:
        contributor_data: Dictionary containing contributor metrics
        total_commits: Total number of commits in repository (excluding bots)
        all_files: Set of all files in repository
        file_extensions: Dictionary of file extension counts
        
    Returns:
        Dictionary containing all scores and breakdown
        
    Raises:
        ValueError: If any score is out of [0, 100] bounds
    """
    # Calculate all sub-scores
    code_quality = calculate_code_quality(contributor_data)
    authorship_confidence = calculate_authorship_confidence(contributor_data, total_commits)
    commit_maturity = calculate_commit_maturity(contributor_data)
    project_complexity = calculate_project_complexity(
        contributor_data, all_files, file_extensions
    )
    
    # Validate all scores are in [0, 100]
    code_quality = validate_score(code_quality, "Code Quality")
    authorship_confidence = validate_score(authorship_confidence, "Authorship Confidence")
    commit_maturity = validate_score(commit_maturity, "Commit Maturity")
    project_complexity = validate_score(project_complexity, "Project Complexity")
    
    # Apply weighted formula
    skill_score = (
        WEIGHTS['code_quality'] * code_quality +
        WEIGHTS['authorship_confidence'] * authorship_confidence +
        WEIGHTS['commit_maturity'] * commit_maturity +
        WEIGHTS['project_complexity'] * project_complexity
    )
    
    # Validate final score
    skill_score = validate_score(skill_score, "Final Skill Score")
    
    return {
        'skill_score': round(skill_score, 2),
        'code_quality': round(code_quality, 2),
        'authorship_confidence': round(authorship_confidence, 2),
        'commit_maturity': round(commit_maturity, 2),
        'project_complexity': round(project_complexity, 2)
    }
