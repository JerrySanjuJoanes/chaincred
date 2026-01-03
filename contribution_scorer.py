"""
Contribution-weighted skill scoring engine.
Applies strict authorship constraints to skill scores.
"""
from typing import Dict, List, Tuple


class ContributionWeightedScorer:
    """
    Score skills based on code evidence with contribution-based capping.
    
    Scoring Rules:
    - Contribution < 5%: "Insufficient Evidence"
    - Contribution < 10%: Max score = 40/100
    - Contribution < 30%: Max score = 60/100
    - Contribution >= 70%: Full scoring (0-100)
    """
    
    # Contribution thresholds and caps
    THRESHOLDS = {
        'insufficient': 5.0,   # Below this = insufficient evidence
        'low': 10.0,          # Below this = capped at 40
        'medium': 30.0,       # Below this = capped at 60
        'high': 70.0,         # Above this = full scoring
    }
    
    CAPS = {
        'insufficient': 0,
        'low': 40,
        'medium': 60,
        'high': 100,
    }
    
    def __init__(self):
        """Initialize the scorer."""
        pass
    
    def get_contribution_tier(self, contribution_pct: float) -> str:
        """
        Determine contribution tier based on percentage.
        
        Args:
            contribution_pct: Percentage of total repository commits
            
        Returns:
            Tier name: 'insufficient', 'low', 'medium', or 'high'
        """
        if contribution_pct < self.THRESHOLDS['insufficient']:
            return 'insufficient'
        elif contribution_pct < self.THRESHOLDS['low']:
            return 'low'
        elif contribution_pct < self.THRESHOLDS['medium']:
            return 'medium'
        else:
            return 'high'
    
    def calculate_base_score(self, evidence: Dict) -> float:
        """
        Calculate base skill score from evidence.
        
        Args:
            evidence: Dictionary with 'files', 'imports', 'patterns'
            
        Returns:
            Base score (0-100) before contribution capping
        """
        score = 0.0
        
        # Files using the technology (up to 40 points)
        num_files = len(evidence.get('files', []))
        if num_files > 0:
            score += min(40, num_files * 5)
        
        # Import statements found (up to 30 points)
        num_imports = len(evidence.get('imports', []))
        if num_imports > 0:
            score += min(30, num_imports * 10)
        
        # Pattern matches (up to 30 points)
        num_patterns = len(evidence.get('patterns', []))
        if num_patterns > 0:
            score += min(30, num_patterns * 10)
        
        return min(100, score)
    
    def apply_contribution_cap(self, base_score: float, contribution_pct: float) -> Tuple[float, str, str]:
        """
        Apply contribution-based capping to skill score.
        
        Args:
            base_score: Uncapped score based on evidence
            contribution_pct: User's contribution percentage in repository
            
        Returns:
            Tuple of (capped_score, tier, reason)
        """
        tier = self.get_contribution_tier(contribution_pct)
        cap = self.CAPS[tier]
        
        if tier == 'insufficient':
            return 0, tier, f"Contribution too low ({contribution_pct:.1f}% < {self.THRESHOLDS['insufficient']}%)"
        
        capped_score = min(base_score, cap)
        
        if capped_score < base_score:
            reason = f"Capped due to {contribution_pct:.1f}% contribution (max {cap})"
        else:
            reason = f"Full score applied ({contribution_pct:.1f}% contribution)"
        
        return capped_score, tier, reason
    
    def score_skill(self, skill: str, evidence: Dict, contribution_pct: float) -> Dict:
        """
        Calculate complete skill score with evidence and explanation.
        
        Args:
            skill: Skill name
            evidence: Evidence dictionary
            contribution_pct: User's contribution percentage
            
        Returns:
            Dictionary with score, evidence, tier, and explanation
        """
        # Calculate base score
        base_score = self.calculate_base_score(evidence)
        
        # Apply contribution cap
        final_score, tier, reason = self.apply_contribution_cap(base_score, contribution_pct)
        
        # Determine if verified
        verified = len(evidence.get('files', [])) > 0 or \
                   len(evidence.get('imports', [])) > 0 or \
                   len(evidence.get('patterns', [])) > 0
        
        return {
            'skill': skill,
            'verified': verified,
            'base_score': base_score,
            'final_score': final_score,
            'tier': tier,
            'contribution_pct': contribution_pct,
            'reason': reason,
            'evidence': evidence,
            'files_count': len(evidence.get('files', [])),
            'imports_count': len(evidence.get('imports', [])),
            'patterns_count': len(evidence.get('patterns', []))
        }
    
    def aggregate_scores(self, repo_scores: List[Dict]) -> Dict:
        """
        Aggregate skill scores across multiple repositories.
        
        Args:
            repo_scores: List of score dictionaries from different repositories
            
        Returns:
            Aggregated score with weighted averaging
        """
        if not repo_scores:
            return {
                'final_score': 0,
                'verified': False,
                'repos_used': 0,
                'repos_insufficient': 0,
                'weighted_avg': 0,
                'reason': 'No evidence found in any repository'
            }
        
        # Filter out insufficient evidence repos
        valid_scores = [s for s in repo_scores if s['tier'] != 'insufficient']
        insufficient_count = len(repo_scores) - len(valid_scores)
        
        if not valid_scores:
            return {
                'final_score': 0,
                'verified': False,
                'repos_used': 0,
                'repos_insufficient': insufficient_count,
                'weighted_avg': 0,
                'reason': 'Insufficient contribution in all repositories'
            }
        
        # Weighted average by contribution percentage
        total_weight = sum(s['contribution_pct'] for s in valid_scores)
        if total_weight == 0:
            weighted_avg = sum(s['final_score'] for s in valid_scores) / len(valid_scores)
        else:
            weighted_avg = sum(
                s['final_score'] * s['contribution_pct'] 
                for s in valid_scores
            ) / total_weight
        
        return {
            'final_score': round(weighted_avg, 1),
            'verified': any(s['verified'] for s in valid_scores),
            'repos_used': len(valid_scores),
            'repos_insufficient': insufficient_count,
            'weighted_avg': round(weighted_avg, 1),
            'repo_details': valid_scores,
            'reason': f'Aggregated from {len(valid_scores)} repo(s)'
        }
