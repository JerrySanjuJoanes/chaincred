"""
Utility functions for validation and bot detection.
"""
from typing import Dict, List, Set
import re


# Bot detection patterns
BOT_PATTERNS = [
    'bot',
    'dependabot',
    'github-actions',
    'renovate',
    '[bot]',
    'semantic-release',
    'greenkeeper',
    'snyk-bot',
    'codecov',
    'travis',
    'circleci',
]


def is_bot_user(author_name: str, author_email: str = '') -> bool:
    """
    Detect if a user is a bot based on name or email.
    
    Args:
        author_name: Git author name
        author_email: Git author email
        
    Returns:
        True if the user appears to be a bot
    """
    author_lower = author_name.lower()
    email_lower = author_email.lower() if author_email else ''
    
    for pattern in BOT_PATTERNS:
        if pattern in author_lower or pattern in email_lower:
            return True
    
    # Check for email patterns like noreply@github.com
    if 'noreply' in email_lower or 'no-reply' in email_lower:
        return True
    
    return False


def validate_score(score: float, name: str = "Score") -> float:
    """
    Validate that a score is within [0, 100] range.
    
    Args:
        score: The score to validate
        name: Name of the score for error messages
        
    Returns:
        Validated score
        
    Raises:
        ValueError: If score is out of bounds
    """
    if not 0 <= score <= 100:
        raise ValueError(
            f"{name} out of bounds: {score:.2f}. "
            f"All scores must be in range [0, 100]"
        )
    return score


def validate_skill_breakdown(breakdown: List[Dict], max_per_criterion: int = 20) -> None:
    """
    Validate skill breakdown criteria scores.
    
    Args:
        breakdown: List of criterion dictionaries
        max_per_criterion: Maximum score per criterion
        
    Raises:
        ValueError: If any criterion score is out of bounds
    """
    for criterion in breakdown:
        score = criterion.get('score', 0)
        crit_name = criterion.get('criterion', 'Unknown')
        
        if not 0 <= score <= max_per_criterion:
            raise ValueError(
                f"Criterion '{crit_name}' score out of bounds: {score}. "
                f"Must be in range [0, {max_per_criterion}]"
            )


def calculate_authorship_percentage(
    author_lines_modified: int,
    total_lines_modified: int
) -> float:
    """
    Calculate authorship percentage using the global formula:
    authorship_confidence = (lines_modified_by_author / total_lines_modified) × 100
    
    Args:
        author_lines_modified: Total lines (added + deleted) by author
        total_lines_modified: Total lines (added + deleted) in repository
        
    Returns:
        Authorship percentage (0-100)
    """
    if total_lines_modified == 0:
        return 0.0
    
    percentage = (author_lines_modified / total_lines_modified) * 100
    return min(percentage, 100.0)


def calculate_file_attribution_ratio(
    author_files: Set[str],
    all_files: Set[str]
) -> float:
    """
    Calculate what percentage of files an author contributed to.
    
    Args:
        author_files: Set of files modified by author
        all_files: Set of all files in repository
        
    Returns:
        Attribution ratio (0.0 to 1.0)
    """
    if not all_files:
        return 0.0
    
    return len(author_files) / len(all_files)


class AnalysisWarnings:
    """Collect and manage warnings during analysis."""
    
    def __init__(self):
        self.warnings: List[str] = []
        self.assumptions: List[str] = []
    
    def add_warning(self, warning: str) -> None:
        """Add a warning message."""
        self.warnings.append(warning)
    
    def add_assumption(self, assumption: str) -> None:
        """Add an assumption made during analysis."""
        self.assumptions.append(assumption)
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0 or len(self.assumptions) > 0
    
    def display(self) -> None:
        """Display all warnings and assumptions."""
        if not self.has_warnings():
            return
        
        print(f"\n{'='*70}")
        print(f"{'⚠️  WARNINGS & ASSUMPTIONS':^70}")
        print(f"{'='*70}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if self.assumptions:
            print(f"\n📝 Assumptions:")
            for i, assumption in enumerate(self.assumptions, 1):
                print(f"  {i}. {assumption}")
        
        print(f"\n{'='*70}\n")
