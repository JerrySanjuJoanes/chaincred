"""
Display and formatting utilities for analysis results.
"""
from typing import Dict, Set
from scoring import calculate_skill_score
from skill_scorer import SkillScorer
from config import SKILL_LEVELS
from utils import AnalysisWarnings


def get_skill_level(score: float) -> str:
    """
    Determine skill level based on score.
    
    Args:
        score: Skill score (0-100)
        
    Returns:
        Skill level string with emoji
    """
    if score >= SKILL_LEVELS['expert']:
        return "🌟 Expert"
    elif score >= SKILL_LEVELS['advanced']:
        return "⭐ Advanced"
    elif score >= SKILL_LEVELS['intermediate']:
        return "💫 Intermediate"
    else:
        return "✨ Beginner"


def display_header() -> None:
    """Display the ChainCredit header."""
    print(f"\n{'='*70}")
    print(f"{'⛓️  CHAINCREDIT - Git Repository Skill Analyzer':^70}")
    print(f"{'='*70}\n")


def display_results(
    contributors: Dict,
    total_commits: int,
    all_files: Set,
    file_extensions: Dict,
    analysis_data: Dict,
    repo_path: str,
    warnings: AnalysisWarnings
) -> None:
    """
    Display analysis results with skill scores.
    
    Args:
        contributors: Dictionary of contributor data
        total_commits: Total number of commits (excluding bots)
        all_files: Set of all files
        file_extensions: Dictionary of file extension counts
        analysis_data: Additional analysis data (languages, frameworks, etc.)
        repo_path: Path to the repository
        warnings: Analysis warnings and assumptions
    """
    print(f"\n{'='*70}")
    print(f"{'🎯 CHAINCREDIT - Repository Analysis Results':^70}")
    print(f"{'='*70}")
    
    # Display repository overview
    _display_repository_overview(total_commits, contributors, all_files, file_extensions, analysis_data)
    
    # Display technology detection
    _display_technology_stack(analysis_data)
    
    # Sort contributors by skill score (exclude bots from ranking)
    contributors_with_scores = []
    for author, stats in contributors.items():
        # Skip bot contributors in skill scoring
        if stats.get('is_bot', False):
            continue
        
        try:
            scores = calculate_skill_score(stats, total_commits, all_files, file_extensions)
            contributors_with_scores.append((author, stats, scores))
        except ValueError as e:
            print(f"\n⚠️ Validation error for {author}: {e}")
            continue
    
    contributors_with_scores.sort(key=lambda x: x[2]['skill_score'], reverse=True)
    
    print(f"\n{'='*70}")
    print(f"{'💯 SKILL-WISE SCORING':^70}")
    print(f"{'='*70}")
    
    for author, stats, scores in contributors_with_scores:
        _display_contributor_details(author, stats, scores, total_commits)
        
        # Display technology-specific skill scores
        _display_technology_skills(author, stats, repo_path, analysis_data)
    
    # Display bot contributors separately
    _display_bot_contributors(contributors)
    
    print(f"\n{'='*70}")
    print(f"{'Formula: 0.35×CodeQ + 0.25×Auth + 0.20×Maturity + 0.10×Complexity':^70}")
    print(f"{'='*70}\n")
    
    # Display warnings and assumptions
    warnings.display()


def _display_repository_overview(total_commits, contributors, all_files, file_extensions, analysis_data):
    """Display repository overview section."""
    print(f"\n📊 Repository Overview:")
    print(f"  • Total Commits: {total_commits}")
    print(f"  • Total Contributors: {len(contributors)}")
    print(f"  • Total Files: {len(all_files)}")
    print(f"  • File Types: {', '.join(list(file_extensions.keys())[:5])}")
    
    # Display code metrics
    complexity = analysis_data.get('complexity', {})
    print(f"  • Total Lines of Code: {complexity.get('code_lines', 0):,}")
    print(f"  • Functions/Methods: {complexity.get('functions_count', 0)}")
    print(f"  • Classes: {complexity.get('classes_count', 0)}")


def _display_technology_stack(analysis_data):
    """Display detected technologies."""
    print(f"\n🔧 Technology Stack:")
    
    # Languages
    languages = analysis_data.get('languages', {})
    if languages:
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        print(f"  Languages:")
        for lang, lines in sorted_langs[:5]:
            percentage = (lines / sum(languages.values())) * 100 if languages else 0
            print(f"    • {lang}: {lines:,} lines ({percentage:.1f}%)")
    
    # Frameworks
    frameworks = analysis_data.get('frameworks', {})
    if frameworks:
        print(f"  Frameworks:")
        for fw, info in frameworks.items():
            confidence = info.get('confidence', 0)
            print(f"    • {fw} (confidence: {confidence}%)")
    
    # Tests
    tests = analysis_data.get('tests', {})
    if tests.get('has_tests'):
        print(f"  Testing:")
        print(f"    • Test Files: {tests.get('test_files_count', 0)}")
        if tests.get('test_frameworks'):
            print(f"    • Frameworks: {', '.join(tests['test_frameworks'])}")


def _display_contributor_details(
    author: str,
    stats: Dict,
    scores: Dict,
    total_commits: int
) -> None:
    """
    Display detailed statistics for a single contributor.
    
    Args:
        author: Contributor name
        stats: Contributor statistics
        scores: Calculated scores
        total_commits: Total commits in repository
    """
    print(f"\n👤 {author}")
    print(f"   {'-'*66}")
    
    # Basic stats
    print(f"   📈 Contribution Stats:")
    print(f"      • Commits: {stats['commits']}")
    print(f"      • Lines Added: {stats['lines_added']}")
    print(f"      • Lines Deleted: {stats['lines_deleted']}")
    print(f"      • Files Modified: {len(stats['files_changed'])}")
    contribution_pct = (stats['commits'] / total_commits) * 100
    print(f"      • Contribution: {contribution_pct:.2f}%")
    
    # Skill breakdown
    print(f"\n   🎯 Skill Score Breakdown:")
    print(f"      ┌─────────────────────────────────────────┬─────────┐")
    print(f"      │ Metric                                  │  Score  │")
    print(f"      ├─────────────────────────────────────────┼─────────┤")
    print(f"      │ Code Quality (35%)                      │ {scores['code_quality']:6.2f}  │")
    print(f"      │ Authorship Confidence (25%)             │ {scores['authorship_confidence']:6.2f}  │")
    print(f"      │ Commit Maturity (20%)                   │ {scores['commit_maturity']:6.2f}  │")
    print(f"      │ Project Complexity (10%)                │ {scores['project_complexity']:6.2f}  │")
    print(f"      ├─────────────────────────────────────────┼─────────┤")
    print(f"      │ FINAL SKILL SCORE                       │ {scores['skill_score']:6.2f}  │")
    print(f"      └─────────────────────────────────────────┴─────────┘")
    
    # Skill level
    skill_level = get_skill_level(scores['skill_score'])
    print(f"\n   🏆 Skill Level: {skill_level}")


def _display_technology_skills(author: str, stats: Dict, repo_path: str, analysis_data: Dict) -> None:
    """Display technology-specific skill scores."""
    # Initialize skill scorer
    scorer = SkillScorer(repo_path, stats)
    skill_scores = scorer.evaluate_all_skills()
    
    if skill_scores:
        print(f"\n   🎓 Technology-Specific Skills:")
        
        for tech, score_data in skill_scores.items():
            total = score_data['total_score']
            percentage = score_data['percentage']
            level = get_skill_level(percentage)
            
            # Display all skills, including zero scores
            if total == 0:
                print(f"\n      {tech}: {total}/100 ({percentage}%) - Not Detected")
                # Show reason if available
                if score_data['breakdown'] and len(score_data['breakdown']) > 0:
                    reason = score_data['breakdown'][0].get('reason', '')
                    if reason:
                        print(f"        • {reason}")
            else:
                print(f"\n      {tech}: {total}/100 ({percentage}%) - {level}")
                
                # Show breakdown (only non-zero scores)
                for criterion in score_data['breakdown']:
                    crit_score = criterion['score']
                    if crit_score > 0:  # Only show criteria with actual scores
                        crit_name = criterion['criterion'].replace('_', ' ').title()
                        reason = criterion['reason']
                        print(f"        • {crit_name}: {crit_score}/20 - {reason}")


def _display_bot_contributors(contributors: Dict) -> None:
    """Display bot/automated contributors separately."""
    bots = [(name, stats) for name, stats in contributors.items() if stats.get('is_bot', False)]
    
    if not bots:
        return
    
    print(f"\n{'='*70}")
    print(f"{'🤖 AUTOMATED CONTRIBUTORS (Excluded from Scoring)':^70}")
    print(f"{'='*70}")
    
    for bot_name, bot_stats in bots:
        print(f"\n   🤖 {bot_name} [AUTOMATED]")
        print(f"      • Commits: {bot_stats['commits']}")
        print(f"      • Lines Added: {bot_stats['lines_added']}")
        print(f"      • Lines Deleted: {bot_stats['lines_deleted']}")

