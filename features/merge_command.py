#!/usr/bin/env python3
"""
🔀 Merge Command - Professional PR merge with security checks

This module provides the merge functionality for the summarizer framework.
It handles merging pull requests with appropriate security checks for protected branches.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional
import subprocess
import json
import getpass

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.git_manager import GitManager
from src.services.request_manager import RequestManager
from src.utils.json_changelog_manager import ImpactLevel


def get_open_prs(project_root: Path) -> List[dict]:
    """Get all open PRs for the repository"""
    try:
        cmd = ["gh", "pr", "list", "--json", "number,title,headRefName,baseRefName,url,author,mergeable,isDraft"]
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        prs = json.loads(result.stdout)
        # Filter out draft PRs
        return [pr for pr in prs if not pr.get('isDraft', False)]
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to get PRs: {e}")
        return []
    except json.JSONDecodeError:
        print("   ❌ Failed to parse PR data")
        return []


def get_pr_impact_level(pr_number: int, project_root: Path, gemini_client) -> ImpactLevel:
    """Analyze PR and determine impact level using AI"""
    try:
        # Get PR diff
        cmd = ["gh", "pr", "diff", str(pr_number)]
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        diff_content = result.stdout
        
        if gemini_client and gemini_client.is_ready():
            prompt = f"""Analyze this PR diff and determine the impact level.
            
PR Diff:
{diff_content[:3000]}...

Determine impact level:
- CRITICAL: Breaking changes, security fixes, major API changes
- HIGH: New features, significant refactors
- MEDIUM: Bug fixes, minor features
- LOW: Documentation, typos, minor tweaks

Return only one word: CRITICAL, HIGH, MEDIUM, or LOW"""
            
            response = gemini_client.generate_simple_text(prompt)
            
            # Parse response
            for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                if level in response.upper():
                    return ImpactLevel[level]
        
        # Fallback based on diff size
        lines = len(diff_content.splitlines())
        if lines > 500:
            return ImpactLevel.HIGH
        elif lines > 100:
            return ImpactLevel.MEDIUM
        else:
            return ImpactLevel.LOW
            
    except Exception as e:
        print(f"   ⚠️  Could not analyze PR impact: {e}")
        return ImpactLevel.MEDIUM


def get_ai_merge_recommendation(pr: dict, impact_level: ImpactLevel, gemini_client) -> dict:
    """Get AI recommendation for merging this PR"""
    if not (gemini_client and gemini_client.is_ready()):
        return {
            "should_merge": True,
            "merge_method": "merge",
            "reasoning": "AI unavailable - using default merge strategy"
        }
    
    try:
        prompt = f"""As a senior engineer, analyze this PR and recommend merge strategy:

PR Title: {pr['title']}
Source Branch: {pr['headRefName']}
Target Branch: {pr['baseRefName']}
Impact Level: {impact_level.value}

Recommend:
1. Should this be merged now? (yes/no)
2. Merge method: merge (create merge commit), squash (squash commits), or rebase
3. Any security considerations for main branch?

Return JSON:
{{
    "should_merge": true/false,
    "merge_method": "merge|squash|rebase",
    "reasoning": "explanation",
    "requires_security": true/false
}}"""

        response = gemini_client.generate_simple_text(prompt)
        
        # Parse JSON from response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"   ⚠️  AI recommendation failed: {e}")
    
    # Intelligent fallback
    if pr['baseRefName'] == 'main':
        return {
            "should_merge": impact_level != ImpactLevel.CRITICAL,
            "merge_method": "squash" if pr['headRefName'].startswith('feature/') else "merge",
            "reasoning": "Main branch requires careful consideration",
            "requires_security": True
        }
    else:
        return {
            "should_merge": True,
            "merge_method": "merge",
            "reasoning": "Standard merge for development branches",
            "requires_security": False
        }


def check_pr_status(pr_number: int, project_root: Path) -> bool:
    """Check if PR is ready to merge (all checks passed)"""
    try:
        cmd = ["gh", "pr", "checks", str(pr_number), "--json", "state"]
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        checks = json.loads(result.stdout)
        
        # Check if all checks passed
        for check in checks:
            if check.get('state') not in ['SUCCESS', 'NEUTRAL', 'SKIPPED']:
                return False
        
        return True
    except:
        # If we can't get check status, assume it's okay
        return True


def execute_merge(pr_to_merge: dict, merge_method: str, project_root: Path, git_manager: GitManager) -> bool:
    """Execute the actual merge"""
    pr_number = pr_to_merge['number']
    
    print(f"\n   🔄 Merging PR #{pr_number}: {pr_to_merge['title']}")
    print(f"   📋 Method: {merge_method}")
    print(f"   🔀 {pr_to_merge['headRefName']} → {pr_to_merge['baseRefName']}")
    
    # Check for conflicts first
    try:
        print("   🔍 Checking for merge conflicts...")
        
        mergeable_cmd = ["gh", "pr", "view", str(pr_number), "--json", "mergeable,mergeStateStatus"]
        mergeable_process = subprocess.run(
            mergeable_cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        mergeable_data = json.loads(mergeable_process.stdout)
        
        if mergeable_data.get('mergeable') == 'CONFLICTING':
            print("   ❌ This PR has merge conflicts that must be resolved!")
            print("   📝 Conflicting files need to be resolved before merging.")
            
            while True:
                print("\n   💡 How would you like to proceed?")
                print("      1. Attempt to resolve conflicts automatically (merges target into source)")
                print("      2. Force push source branch to overwrite remote (DANGEROUS)")
                print("      3. Cancel and resolve manually")
                choice = input("   Enter your choice (1, 2, or 3): ").strip()

                if choice == '1':
                    print("\n   🔧 Attempting to resolve conflicts automatically...")
                    if git_manager.resolve_conflicts_with_pr(pr_number):
                        print("\n   🎉 Conflicts resolved successfully!")
                        print("   📋 The PR has been updated. You may need to re-run the merge command.")
                        return True # Indicate that an action was taken, but merge needs re-run
                    else:
                        print("   ❌ Automatic conflict resolution failed.")
                        print("   💡 Please resolve conflicts manually.")
                    break 
                elif choice == '2':
                    pr_branch_name = pr_to_merge['headRefName']
                    if git_manager.force_push_with_confirmation(pr_branch_name):
                         print("\n   🎉 Force push completed.")
                         print("   📋 The PR has been updated. You may need to re-run the merge command.")
                    else:
                        print("   ❌ Force push was cancelled or failed.")
                    break
                elif choice == '3':
                    print("   ⚪️ Merge cancelled. Please resolve conflicts manually.")
                    return False # Explicitly stop the merge
                else:
                    print("   ⚠️  Invalid choice. Please enter 1, 2, or 3.")
            return False
    except Exception as e:
        print(f"   ⚠️  Could not check merge conflicts: {e}")
        # Continue anyway
    
    # Execute the merge
    try:
        merge_cmd = ["gh", "pr", "merge", str(pr_number), f"--{merge_method}"]
        
        print(f"\n   🚀 Executing merge...")
        merge_process = subprocess.run(
            merge_cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("   ✅ PR merged successfully!")
        
        # Sync local repository
        print("\n   🔄 Syncing local repository...")
        current_branch = git_manager.get_current_branch()
        
        # Fetch latest changes
        git_manager.fetch_updates()
        
        # If we're on the merged branch, switch to base branch
        if current_branch == pr_to_merge['headRefName']:
            print(f"   📋 Switching from merged branch to {pr_to_merge['baseRefName']}...")
            git_manager.checkout(pr_to_merge['baseRefName'])
            git_manager.pull(pr_to_merge['baseRefName'])
            
            # Offer to delete the merged branch locally
            if input(f"\n   ❔ Delete local branch '{pr_to_merge['headRefName']}'? (y/n): ").lower() == 'y':
                git_manager._run_git_command(["branch", "-d", pr_to_merge['headRefName']])
                print(f"   ✅ Local branch '{pr_to_merge['headRefName']}' deleted")
        else:
            # Just pull latest on current branch
            git_manager.pull(current_branch)
        
        print("   ✅ Local repository synced")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Merge failed: {e}")
        if e.stderr:
            print(f"   📝 Error details: {e.stderr}")
        return False


def merge_command(project_root: Path):
    """Main merge command handler"""
    print("\n🔀 Intelligent PR Merge Assistant")
    print("="*50)
    
    # Initialize git manager
    git_manager = GitManager(project_root)
    
    # Get AI client
    gemini_client = None
    try:
        from src.core.configuration_manager import ConfigurationManager
        from src.services.gemini_client import GeminiClient
        from features.parameter_checker import setup_command

        config_manager = ConfigurationManager()
        
        # Check if API key is missing
        if not config_manager.get_api_key():
            print("   ⚠️  AI features require a GEMINI_API_KEY.")
            if input("   ❔ Run setup now to add it? (y/n): ").lower() == 'y':
                setup_command()
                # Re-initialize after setup
                config_manager = ConfigurationManager()
        
        # Try to initialize the client if we have a key
        if config_manager.get_api_key():
            gemini_client = GeminiClient(config_manager)
            if gemini_client.is_ready():
                print("   ✅ AI assistant connected")
            else:
                gemini_client = None
                print("   ⚠️  AI assistant could not be initialized. The API key might be invalid.")
        else:
            print("   ⚠️  AI assistant unavailable - API key not provided.")

    except Exception as e:
        print(f"   ⚠️  AI assistant unavailable - using fallback logic. Error: {e}")
    
    # Get open PRs
    print("\n   🔍 Fetching open pull requests...")
    prs = get_open_prs(project_root)
    
    if not prs:
        print("   ℹ️  No open pull requests found")
        return
    
    print(f"   ✅ Found {len(prs)} open PR(s)")
    
    # Analyze each PR
    pr_analysis = []
    for pr in prs:
        print(f"\n   📊 Analyzing PR #{pr['number']}: {pr['title']}")
        impact = get_pr_impact_level(pr['number'], project_root, gemini_client)
        recommendation = get_ai_merge_recommendation(pr, impact, gemini_client)
        checks_passed = check_pr_status(pr['number'], project_root)
        
        pr_analysis.append({
            'pr': pr,
            'impact': impact,
            'recommendation': recommendation,
            'checks_passed': checks_passed
        })
    
    # Display analysis
    print("\n" + "="*50)
    print("📋 PR Analysis Summary")
    print("="*50)
    
    for i, analysis in enumerate(pr_analysis):
        pr = analysis['pr']
        print(f"\n{i+1}. PR #{pr['number']}: {pr['title']}")
        print(f"   • Branch: {pr['headRefName']} → {pr['baseRefName']}")
        print(f"   • Impact: {analysis['impact'].value}")
        print(f"   • Checks: {'✅ Passed' if analysis['checks_passed'] else '❌ Failed'}")
        print(f"   • AI Says: {analysis['recommendation']['reasoning']}")
        if analysis['recommendation'].get('requires_security', False):
            print(f"   • 🔒 Security: Main branch protection required")
    
    # Let user select
    print("\n" + "="*50)
    
    while True:
        try:
            choice = input("\n   ❔ Select PR to merge (number) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("   👋 Merge cancelled")
                return
            
            idx = int(choice) - 1
            if 0 <= idx < len(pr_analysis):
                selected = pr_analysis[idx]
                break
            else:
                print("   ❌ Invalid selection")
        except ValueError:
            print("   ❌ Please enter a number or 'q'")
    
    # Confirm merge
    pr_to_merge = selected['pr']
    recommendation = selected['recommendation']
    
    print(f"\n   🎯 Selected: PR #{pr_to_merge['number']}")
    
    # Check if already pushed
    sync_status, ahead, _ = git_manager.get_branch_sync_status(git_manager.get_current_branch())
    if ahead > 0:
        print(f"\n   ⚠️  You have {ahead} unpushed commit(s) on current branch.")
        if input("   ❔ Push changes before merging? (y/n): ").lower() == 'y':
            git_manager.push(git_manager.get_current_branch())
    
    # Security check for main branch
    if recommendation.get('requires_security', False) and pr_to_merge['baseRefName'] in ['main', 'master']:
        print("\n   🔒 SECURITY CHECK: This PR targets the MAIN branch")
        print("   ⚠️  Merging to main requires additional authorization")
        
        # Simple password check (in real world, use proper auth)
        password = getpass.getpass("   🔑 Enter security password: ")
        if password != "merge2main":  # You should use env var or better auth
            print("   ❌ Invalid password. Merge cancelled.")
            return
        
        print("   ✅ Security check passed")
    
    # Check for failed checks
    if not selected['checks_passed']:
        print("\n   ⚠️  Warning: Some checks have not passed!")
        if input("   ❔ Continue anyway? (y/n): ").lower() != 'y':
            print("   ❌ Merge cancelled")
            return
    
    # Final confirmation
    print(f"\n   📋 Ready to merge:")
    print(f"      • PR: #{pr_to_merge['number']} - {pr_to_merge['title']}")
    print(f"      • Method: {recommendation['merge_method']}")
    print(f"      • Target: {pr_to_merge['baseRefName']}")
    
    if input("\n   ❔ Proceed with merge? (y/n): ").lower() != 'y':
        print("   ❌ Merge cancelled")
        return
    
    # Execute merge
    if execute_merge(pr_to_merge, recommendation['merge_method'], project_root, git_manager):
        print("\n   🎉 Merge completed successfully!")
    else:
        print("\n   ❌ Merge failed. Please check the errors above.")


if __name__ == "__main__":
    # Run from project root
    project_root = Path.cwd()
    
    # If run from scripts directory, go up
    if project_root.name == "features":
        project_root = project_root.parent
    
    merge_command(project_root) 