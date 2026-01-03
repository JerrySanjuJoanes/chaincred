"""
ChainCredit - Resume-Based Git Repository Skill Analyzer
Main entry point for analyzing developer skills from resume and Git repositories.
"""
import sys
import os
from pathlib import Path
import traceback

from config import REPO_SETTINGS
from repo_manager import clone_repo, cleanup_repo
from analyzer import analyze_repository
from display import display_header
from display_resume import display_resume_results
from resume_parser import parse_resume_file, classify_github_url


def main():
    """Main entry point for the ChainCredit resume analyzer."""
    display_header()
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <resume-file.pdf>")
        print("Example: python main.py resume.pdf")
        print("\nMake sure to set GEMINI_API_KEY environment variable:")
        print("  export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)
    
    resume_file = sys.argv[1]
    temp_dir = REPO_SETTINGS['temp_dir']
    
    try:
        # Stage 1: Parse resume
        print("\n" + "="*70)
        print("📄 STAGE 1: Resume Analysis")
        print("="*70)
        
        resume_data = parse_resume_file(resume_file)
        
        if not resume_data['github_repos']:
            print("\n❌ Error: No GitHub repositories found in resume")
            print("Please ensure your resume includes GitHub project URLs")
            sys.exit(1)
        
        # Stage 2: Analyze repositories
        print("\n" + "="*70)
        print("📊 STAGE 2: Repository Analysis")
        print("="*70)
        
        all_repo_results = []
        candidate_name = resume_data['candidate_name']
        github_username = resume_data['github_username']
        
        for i, repo_url in enumerate(resume_data['github_repos'], 1):
            print(f"\n[{i}/{len(resume_data['github_repos'])}] Analyzing: {repo_url}")
            print("-" * 70)
            
            # Validate URL type
            url_classification = classify_github_url(repo_url)
            
            if url_classification['type'] == 'profile':
                print(f"⏭️  Skipping GitHub profile URL – not a repository")
                print(f"   Profile URLs cannot be cloned or analyzed")
                continue
            elif url_classification['type'] == 'unknown':
                print(f"⚠️  Unknown URL format – attempting to analyze anyway")
            
            try:
                # Clone repository
                print("📥 Cloning repository...")
                repo_path = clone_repo(repo_url, temp_dir)
                
                # Analyze repository
                contributors, total_commits, all_files, file_extensions, analysis_data, warnings = analyze_repository(repo_path)
                
                # Store results
                all_repo_results.append({
                    'repo_url': repo_url,
                    'repo_path': repo_path,
                    'contributors': contributors,
                    'total_commits': total_commits,
                    'all_files': all_files,
                    'file_extensions': file_extensions,
                    'analysis_data': analysis_data,
                    'warnings': warnings
                })
                
                # Cleanup this repo
                cleanup_repo(temp_dir)
                
            except Exception as e:
                print(f"⚠️  Error analyzing {repo_url}: {e}")
                cleanup_repo(temp_dir)
                continue
        
        if not all_repo_results:
            print("\n❌ Error: Could not analyze any repositories")
            sys.exit(1)
        
        # Stage 3: Display results
        print("\n" + "="*70)
        print("📈 STAGE 3: Skill Assessment Report")
        print("="*70)
        
        display_resume_results(
            resume_data=resume_data,
            repo_results=all_repo_results
        )
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Final cleanup
        cleanup_repo(temp_dir)
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()