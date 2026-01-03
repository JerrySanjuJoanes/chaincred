"""
Display utilities for resume-based analysis results with skill verification.
"""
from typing import Dict, List
from skill_detector import SkillDetector
from contribution_scorer import ContributionWeightedScorer


def get_confidence_label(contribution_pct: float) -> str:
    """
    Get confidence label based on contribution percentage.
    
    Args:
        contribution_pct: Contribution percentage in repository
        
    Returns:
        Confidence label with emoji
    """
    if contribution_pct >= 70:
        return "🟢 High Confidence"
    elif contribution_pct >= 30:
        return "🟡 Medium Confidence"
    elif contribution_pct >= 5:
        return "🟠 Low Confidence"
    else:
        return "🔴 Insufficient Evidence"


def find_candidate_in_contributors(contributors: Dict, candidate_name: str, github_username: str) -> str:
    """
    Find the candidate's name in the contributor list.
    
    Args:
        contributors: Dictionary of contributors
        candidate_name: Name from resume
        github_username: GitHub username from resume
        
    Returns:
        Matched contributor name or None
    """
    # Try exact match first
    if candidate_name in contributors:
        return candidate_name
    
    # Try case-insensitive match
    for contrib_name in contributors.keys():
        if contrib_name.lower() == candidate_name.lower():
            return contrib_name
    
    # Try partial name match (first name or last name)
    name_parts = candidate_name.lower().split()
    for contrib_name in contributors.keys():
        contrib_lower = contrib_name.lower()
        if any(part in contrib_lower for part in name_parts):
            return contrib_name
    
    # Try GitHub username match
    if github_username:
        for contrib_name in contributors.keys():
            if github_username.lower() in contrib_name.lower():
                return contrib_name
    
    return None


def display_resume_results(resume_data: Dict, repo_results: List[Dict]) -> None:
    """
    Display comprehensive skill assessment with claimed vs verified separation.
    
    Args:
        resume_data: Parsed resume data
        repo_results: List of analyzed repository results
    """
    candidate_name = resume_data['candidate_name']
    github_username = resume_data['github_username']
    resume_skills = resume_data['skills']
    
    print(f"\n{'='*70}")
    print(f"{'🎓 SKILL ASSESSMENT REPORT':^70}")
    print(f"{'='*70}")
    
    print(f"\n👤 Candidate: {candidate_name}")
    if resume_data['email']:
        print(f"📧 Email: {resume_data['email']}")
    if github_username:
        print(f"🔗 GitHub: @{github_username}")
    
    print(f"\n📋 Skills Claimed in Resume ({len(resume_skills)}):")
    if resume_skills:
        for i, skill in enumerate(resume_skills, 1):
            print(f"   {i}. {skill}")
    else:
        print("   No skills listed")
    
    print(f"\n📊 Repositories Analyzed: {len(repo_results)}")
    
    # Initialize scorer
    scorer = ContributionWeightedScorer()
    
    # Process each repository
    print(f"\n{'='*70}")
    print("📈 Repository Contributions")
    print(f"{'='*70}")
    
    # Store skill scores per repository
    skill_repo_scores = {}  # skill -> [repo_score_dicts]
    
    repos_analyzed = 0
    repos_skipped = 0
    
    for idx, repo_result in enumerate(repo_results, 1):
        repo_url = repo_result['repo_url']
        contributors = repo_result['contributors']
        repo_path = repo_result['repo_path']
        all_files = repo_result['all_files']
        total_repo_commits = repo_result['total_commits']
        
        print(f"\n[{idx}] {repo_url}")
        
        # Find candidate in contributors
        matched_name = find_candidate_in_contributors(contributors, candidate_name, github_username)
        
        if not matched_name:
            print(f"   ⚠️  No contributions found (searched for: {candidate_name})")
            repos_skipped += 1
            continue
        
        if contributors[matched_name].get('is_bot', False):
            print(f"   ⚠️  Detected as bot account - skipping")
            repos_skipped += 1
            continue
        
        stats = contributors[matched_name]
        repos_analyzed += 1
        
        # Calculate contribution percentage
        contribution_pct = (stats['commits'] / max(total_repo_commits, 1)) * 100
        confidence = get_confidence_label(contribution_pct)
        
        print(f"   ✅ Contributor: {matched_name}")
        print(f"   📊 Commits: {stats['commits']}/{total_repo_commits} ({contribution_pct:.1f}%)")
        print(f"   ➕ Lines Added: {stats['lines_added']:,}")
        print(f"   ➖ Lines Deleted: {stats['lines_deleted']:,}")
        print(f"   📁 Files Modified: {len(stats['files_changed'])}")
        print(f"   🎖️  Authorship Confidence: {confidence}")
        
        # Detect skills in this repository
        detector = SkillDetector(repo_path)
        detected_skills = detector.detect_all_skills(list(stats['files_changed']))
        
        print(f"   🔍 Technologies Detected: {len(detected_skills)}")
        
        # Score each detected skill
        if detected_skills:
            print(f"   📊 Skill Scores (contribution-weighted):")
            
            for skill, evidence in detected_skills.items():
                score_data = scorer.score_skill(skill, evidence, contribution_pct)
                
                # Store for aggregation
                if skill not in skill_repo_scores:
                    skill_repo_scores[skill] = []
                skill_repo_scores[skill].append(score_data)
                
                # Display score
                if score_data['tier'] == 'insufficient':
                    print(f"      • {skill}: Insufficient Evidence")
                else:
                    print(f"      • {skill}: {score_data['final_score']:.0f}/100 " +
                          f"({score_data['files_count']} files)")
        else:
            print(f"   ⚠️  No technologies detected in modified files")
    
    # Display aggregated skill assessment
    print(f"\n{'='*70}")
    print("🎯 SKILL VERIFICATION & SCORING")
    print(f"{'='*70}")
    
    # Separate claimed vs verified skills
    print(f"\n{'='*70}")
    print("📋 CLAIMED SKILLS (from resume)")
    print(f"{'='*70}")
    
    verified_claimed_skills = []
    unverified_claimed_skills = []
    
    for skill in resume_skills:
        # Check if verified in codebase
        matched_detection = None
        for detected_skill in skill_repo_scores.keys():
            if skill.lower() == detected_skill.lower() or \
               skill.lower() in detected_skill.lower() or \
               detected_skill.lower() in skill.lower():
                matched_detection = detected_skill
                break
        
        if matched_detection:
            verified_claimed_skills.append((skill, matched_detection))
        else:
            unverified_claimed_skills.append(skill)
    
    # Display verified claimed skills
    if verified_claimed_skills:
        print(f"\n✅ VERIFIED SKILLS ({len(verified_claimed_skills)}):")
        print(f"{'='*70}")
        
        for claimed_skill, detected_skill in sorted(verified_claimed_skills):
            repo_scores = skill_repo_scores[detected_skill]
            aggregated = scorer.aggregate_scores(repo_scores)
            
            print(f"\n🔹 {claimed_skill}")
            print(f"   Verified in Code: ✅ Yes (detected as '{detected_skill}')")
            print(f"   Final Score: {aggregated['final_score']}/100")
            print(f"   Repositories: {aggregated['repos_used']} analyzed")
            if aggregated['repos_insufficient'] > 0:
                print(f"   Excluded: {aggregated['repos_insufficient']} repo(s) (insufficient contribution)")
            
            # Show evidence summary
            if 'repo_details' in aggregated and aggregated['repo_details']:
                print(f"   Evidence Summary:")
                for detail in aggregated['repo_details'][:3]:  # Show top 3
                    print(f"      • {detail['files_count']} files, " +
                          f"{detail['imports_count']} imports, " +
                          f"{detail['patterns_count']} patterns")
                    print(f"        Score: {detail['final_score']}/100 ({detail['reason']})")
    else:
        print(f"\n⚠️  No claimed skills verified in code")
    
    # Display unverified claimed skills
    if unverified_claimed_skills:
        print(f"\n{'='*70}")
        print(f"❌ UNVERIFIED SKILLS ({len(unverified_claimed_skills)}):")
        print(f"{'='*70}")
        print("These skills were claimed in resume but NOT detected in analyzed code:\n")
        
        for skill in sorted(unverified_claimed_skills):
            print(f"🔹 {skill}")
            print(f"   Verified in Code: ❌ No")
            print(f"   Score: 0/100")
            print(f"   Reason: Skill not detected in analyzed repositories")
            print(f"   Evidence: No files, imports, or patterns found")
            print()
    
    # Display additional verified skills (not claimed)
    additional_skills = []
    for detected_skill in skill_repo_scores.keys():
        is_claimed = False
        for claimed_skill in resume_skills:
            if claimed_skill.lower() == detected_skill.lower() or \
               claimed_skill.lower() in detected_skill.lower() or \
               detected_skill.lower() in claimed_skill.lower():
                is_claimed = True
                break
        
        if not is_claimed:
            additional_skills.append(detected_skill)
    
    if additional_skills:
        print(f"\n{'='*70}")
        print(f"💡 ADDITIONAL SKILLS FOUND ({len(additional_skills)}):")
        print(f"{'='*70}")
        print("These skills were detected in code but NOT claimed in resume:\n")
        
        for skill in sorted(additional_skills):
            repo_scores = skill_repo_scores[skill]
            aggregated = scorer.aggregate_scores(repo_scores)
            
            print(f"🔹 {skill}")
            print(f"   Claimed in Resume: ❌ No")
            print(f"   Verified in Code: ✅ Yes")
            print(f"   Score: {aggregated['final_score']}/100")
            print(f"   Repositories: {aggregated['repos_used']} analyzed")
            print()
    
    # Summary statistics
    print(f"\n{'='*70}")
    print("📊 SUMMARY STATISTICS")
    print(f"{'='*70}")
    
    total_commits = sum(
        repo['contributors'][find_candidate_in_contributors(
            repo['contributors'], candidate_name, github_username
        )]['commits']
        for repo in repo_results
        if find_candidate_in_contributors(repo['contributors'], candidate_name, github_username)
    )
    
    total_lines = sum(
        repo['contributors'][find_candidate_in_contributors(
            repo['contributors'], candidate_name, github_username
        )]['lines_added'] + repo['contributors'][find_candidate_in_contributors(
            repo['contributors'], candidate_name, github_username
        )]['lines_deleted']
        for repo in repo_results
        if find_candidate_in_contributors(repo['contributors'], candidate_name, github_username)
    )
    
    print(f"\n📈 Contribution Summary:")
    print(f"   • Repositories with Contributions: {repos_analyzed}/{len(repo_results)}")
    print(f"   • Repositories Skipped: {repos_skipped}")
    print(f"   • Total Commits: {total_commits}")
    print(f"   • Total Lines Modified: {total_lines:,}")
    
    print(f"\n🎯 Skill Summary:")
    print(f"   • Skills Claimed: {len(resume_skills)}")
    print(f"   • Skills Verified: {len(verified_claimed_skills)}")
    print(f"   • Skills Unverified: {len(unverified_claimed_skills)}")
    print(f"   • Additional Skills Found: {len(additional_skills)}")
    print(f"   • Total Unique Technologies: {len(skill_repo_scores)}")
    
    # Calculate verification rate
    if resume_skills:
        verification_rate = (len(verified_claimed_skills) / len(resume_skills)) * 100
        print(f"   • Verification Rate: {verification_rate:.1f}%")
    
    print(f"\n{'='*70}")
    print("✅ Assessment Complete!")
    print(f"{'='*70}")
