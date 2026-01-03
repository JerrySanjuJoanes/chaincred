"""
Configuration constants for ChainCredit analyzer.
"""

# Skill score weights
WEIGHTS = {
    'code_quality': 0.35,
    'authorship_confidence': 0.25,
    'commit_maturity': 0.20,
    'project_complexity': 0.10
}

# Skill level thresholds
SKILL_LEVELS = {
    'expert': 70,
    'advanced': 50,
    'intermediate': 30,
    'beginner': 0
}

# Code quality parameters
CODE_QUALITY = {
    'message_quality_weight': 40,
    'churn_rate_weight': 30,
    'file_diversity_weight': 30,
    'min_meaningful_words': 3,
    'diversity_multiplier': 10
}

# Commit maturity parameters
COMMIT_MATURITY = {
    'optimal_min_complexity': 50,
    'optimal_max_complexity': 200,
    'optimal_min_interval_days': 1,
    'optimal_max_interval_days': 7,
    'optimal_interval_center': 4
}

# Project complexity parameters
PROJECT_COMPLEXITY = {
    'file_coverage_weight': 40,
    'tech_diversity_weight': 30,
    'volume_weight': 30,
    'diversity_multiplier': 15,
    'volume_divisor': 50
}

# Authorship confidence parameters
AUTHORSHIP_CONFIDENCE = {
    'commit_ratio_multiplier': 200,
    'max_commit_score': 50,
    'volume_divisor': 100,
    'max_volume_score': 50
}

# Repository settings
REPO_SETTINGS = {
    'temp_dir': 'temp_repo'
}
