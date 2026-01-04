"""
Repository cloning and management utilities.
"""
import os
import shutil
from git import Repo


def clone_repo(url: str, target_dir: str = 'temp_repo') -> str:
    """
    Clone a repository to a temporary directory.
    
    Args:
        url: Repository URL to clone
        target_dir: Target directory for cloning
        
    Returns:
        Path to cloned repository
    """
    if os.path.exists(target_dir):
        print(f"Directory {target_dir} already exists. Removing...")
        shutil.rmtree(target_dir)
    
    print(f"Cloning repository: {url}")
    Repo.clone_from(url, target_dir)
    return target_dir


def cleanup_repo(target_dir: str) -> None:
    """
    Clean up temporary repository directory.
    
    Args:
        target_dir: Directory to remove
    """
    if os.path.exists(target_dir):
        print(f"🧹 Cleaning up temporary directory: {target_dir}")
        shutil.rmtree(target_dir)
        print("✅ Analysis complete!\n")
