#!/usr/bin/env python3
"""
🧪 Force Push Test

Test script to check if force push functionality works properly.
"""

from pathlib import Path
from src.utils.git_manager import GitManager

def test_force_push():
    print("🧪 Force Push Test")
    print("=" * 30)
    
    # Initialize git manager
    project_root = Path.cwd()
    git_manager = GitManager(project_root)
    
    # Get current branch
    current_branch = git_manager.get_current_branch()
    print(f"   📍 Current branch: {current_branch}")
    
    # Make a simple change
    print("   📝 Making a test change...")
    with open("force_push_test.txt", "w") as f:
        f.write("Force push test file - this is a test!\n")
    
    # Stage and commit
    print("   💾 Staging and committing...")
    if not git_manager.stage_all():
        print("   ❌ Failed to stage files")
        return False
    
    if not git_manager.commit("test: Force push test commit"):
        print("   ❌ Failed to commit")
        return False
    
    print("   ✅ Test commit created")
    
    # Ask user if they want to force push
    if input("   ❔ Test force push? (y/n): ").lower() == 'y':
        print("   🚀 Executing force push...")
        success, output = git_manager.force_push_all(current_branch)
        
        if success:
            print("   ✅ Force push successful!")
            print(f"   📤 Output: {output}")
        else:
            print("   ❌ Force push failed!")
            print(f"   💥 Error: {output}")
    else:
        print("   ⚪️ Force push test skipped")
    
    # Clean up test file
    print("   🧹 Cleaning up...")
    try:
        Path("force_push_test.txt").unlink()
        git_manager.stage_all()
        git_manager.commit("chore: Remove force push test file")
        print("   ✅ Cleanup complete")
    except:
        print("   ⚠️  Cleanup failed (file may not exist)")
    
    return True

if __name__ == "__main__":
    test_force_push() 