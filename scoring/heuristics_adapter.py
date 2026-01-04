"""Adapter to reuse detailed heuristics from skill_scorer inside the
contribution-capped scoring flow.
"""
from typing import Dict, Optional

from scoring.skill_scorer import SkillScorer

# Mapping from detector skill names to SkillScorer keys
SKILL_KEY_MAP = {
    'react': 'React',
    'django': 'Django',
    'node.js': 'NodeJS',
    'nodejs': 'NodeJS',
    'tailwindcss': 'TailwindCSS',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'python': 'Python',
    'c': 'C',
    'c++': 'C++',
}


def get_heuristic_score(skill: str, repo_path: str, contributor_data: dict) -> Optional[Dict]:
    """
    Return detailed heuristic score for a skill if supported by SkillScorer.
    Falls back to None when the skill is not covered by SkillScorer.
    """
    key = SKILL_KEY_MAP.get(skill.lower())
    if not key:
        return None

    scorer = SkillScorer(repo_path, contributor_data)
    scores = scorer.evaluate_all_skills()
    if key not in scores:
        return None

    score_data = scores[key]
    return {
        'base_score': score_data.get('total_score', 0),
        'breakdown': score_data.get('breakdown', []),
        'max_score': score_data.get('max_score', 100),
        'source': 'heuristic'
    }
