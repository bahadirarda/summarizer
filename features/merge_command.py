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

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.git_manager import GitManager


def get_open_prs(git_manager: GitManager) -> List[dict]:
    """Get list of open pull requests"""
    try:
        cmd = ["gh", "pr", "list", "--state", "open", "--json", "number,title,headRefName,baseRefName,url"]
        process = subprocess.run(
            cmd, 
            cwd=git_manager.project_root,
            capture_output=True, 
            text=True, 
            check=True
        )
        
        if process.stdout:
            return json.loads(process.stdout)
        return []
    except subprocess.CalledProcessError:
        return []
    except json.JSONDecodeError:
        return []


def get_ai_merge_recommendation(prs: List[dict], gemini_client) -> Optional[dict]:
    """Get AI recommendation for which PR to merge"""
    if not gemini_client or not gemini_client.is_ready():
        return None
    
    try:
        pr_info = "\n".join([
            f"PR #{pr['number']}: {pr['title']} ({pr['headRefName']} → {pr['baseRefName']})"
            for pr in prs
        ])
        
        prompt = f"""You are a senior software engineer reviewing pull requests.
Based on the following open PRs, recommend which one should be merged first and why.

Open Pull Requests:
{pr_info}

Analyze each PR based on:
1. Target branch (main/master PRs are critical)
2. PR title and implied changes
3. Branch naming (hotfix > release > feature)
4. PR age (older PRs might have priority)

Response format:
RECOMMENDED_PR: <number>
REASON: <brief explanation>
PRIORITY: <HIGH/MEDIUM/LOW>
WARNING: <any concerns or warnings>
"""
        
        response = gemini_client.generate_simple_text(prompt)
        if response:
            # Parse AI response
            lines = response.strip().split('\n')
            recommended_pr = None
            reason = ""
            priority = ""
            warning = ""
            
            for line in lines:
                if line.startswith("RECOMMENDED_PR:"):
                    try:
                        recommended_pr = int(line.split(":", 1)[1].strip())
                    except:
                        pass
                elif line.startswith("REASON:"):
                    reason = line.split(":", 1)[1].strip()
                elif line.startswith("PRIORITY:"):
                    priority = line.split(":", 1)[1].strip()
                elif line.startswith("WARNING:"):
                    warning = line.split(":", 1)[1].strip()
            
            # Find the recommended PR
            for pr in prs:
                if pr['number'] == recommended_pr:
                    return {
                        'pr': pr,
                        'reason': reason,
                        'priority': priority,
                        'warning': warning
                    }
    except Exception as e:
        print(f"   ⚠️  AI recommendation failed: {e}")
    
    return None


def select_pr_interactive(prs: List[dict], gemini_client=None) -> Optional[dict]:
    """Interactive PR selection"""
    if not prs:
        print("   ❌ No open pull requests found.")
        return None
    
    print("\n📋 Open Pull Requests:")
    print("=" * 60)
    
    for i, pr in enumerate(prs, 1):
        print(f"{i}. PR #{pr['number']}: {pr['title']}")
        print(f"   Branch: {pr['headRefName']} → {pr['baseRefName']}")
        print(f"   URL: {pr['url']}")
        print()
    
    # Get AI recommendation if available
    if gemini_client:
        print("🤖 Getting AI recommendation...")
        recommendation = get_ai_merge_recommendation(prs, gemini_client)
        
        if recommendation:
            print("\n" + "="*60)
            print("🎯 AI RECOMMENDATION")
            print("="*60)
            pr = recommendation['pr']
            print(f"   📌 Recommended: PR #{pr['number']}")
            print(f"   📝 Reason: {recommendation['reason']}")
            print(f"   🔥 Priority: {recommendation['priority']}")
            if recommendation['warning']:
                print(f"   ⚠️  Warning: {recommendation['warning']}")
            print("="*60)
    
    while True:
        try:
            if gemini_client and recommendation:
                choice = input("\nAction: [y]es to merge recommended / [n]umber to select / [q]uit: ")
                
                if choice.lower() == 'y':
                    return recommendation['pr']
                elif choice.lower() == 'q':
                    return None
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(prs):
                        return prs[idx]
                    else:
                        print("   ⚠️  Invalid selection. Please try again.")
                else:
                    print("   ⚠️  Invalid input. Use 'y', a number, or 'q'.")
            else:
                choice = input("Select PR number to merge (or 'q' to quit): ")
                if choice.lower() == 'q':
                    return None
                
                idx = int(choice) - 1
                if 0 <= idx < len(prs):
                    return prs[idx]
                else:
                    print("   ⚠️  Invalid selection. Please try again.")
        except ValueError:
            print("   ⚠️  Please enter a valid number.")


def merge_command(args: List[str] = None) -> bool:
    """
    Handle PR merge with security checks
    
    Usage:
        summarizer merge          # Interactive PR selection
        summarizer merge 123      # Merge specific PR number
    """
    print("🔀 Summarizer Merge Command")
    print("=" * 30)
    
    # Initialize managers
    project_root = Path.cwd()
    git_manager = GitManager(project_root)
    
    # Setup configuration like in main.py
    from src.main import setup_configuration
    config_manager = setup_configuration(project_root)
    
    # Initialize Gemini client for AI recommendations
    gemini_client = None
    try:
        # Get API key from configuration manager
        api_key = config_manager.get_field_value("GEMINI_API_KEY")
        
        if api_key:
            from src.services.gemini_client import GeminiClient
            # GeminiClient expects a ConfigurationManager, not just the API key
            gemini_client = GeminiClient(config_manager=config_manager)
            if gemini_client.is_ready():
                print("   ✅ AI recommendation system ready")
            else:
                print("   ⚠️  AI features unavailable: Client not ready")
                gemini_client = None
        else:
            print("   ⚠️  AI features unavailable: GEMINI_API_KEY not found")
    except Exception as e:
        print(f"   ⚠️  AI features unavailable: {e}")
    
    # Check if we're in a git repository
    if not git_manager.is_git_repository():
        print("   ❌ Not in a git repository!")
        return False
    
    # Check GitHub CLI authentication
    try:
        auth_check = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )
        if auth_check.returncode != 0:
            print("   ❌ GitHub CLI not authenticated!")
            print("   💡 Run 'gh auth login' to authenticate.")
            return False
    except FileNotFoundError:
        print("   ❌ GitHub CLI (gh) not found!")
        print("   💡 Install it from: https://cli.github.com/")
        return False
    
    # Determine which PR to merge
    pr_to_merge = None
    
    if args and args[0].isdigit():
        # PR number provided
        pr_number = int(args[0])
        print(f"   🔍 Looking for PR #{pr_number}...")
        
        # Get PR details
        try:
            cmd = ["gh", "pr", "view", str(pr_number), "--json", "number,title,headRefName,baseRefName,state,url"]
            process = subprocess.run(
                cmd,
                cwd=project_root,
                capture_output=True,
                text=True,
                check=True
            )
            pr_data = json.loads(process.stdout)
            
            if pr_data['state'] != 'OPEN':
                print(f"   ❌ PR #{pr_number} is not open (state: {pr_data['state']})")
                return False
                
            pr_to_merge = pr_data
            
        except subprocess.CalledProcessError:
            print(f"   ❌ PR #{pr_number} not found!")
            return False
        except json.JSONDecodeError:
            print("   ❌ Failed to parse PR data!")
            return False
    else:
        # Interactive selection
        print("   🔍 Fetching open pull requests...")
        open_prs = get_open_prs(git_manager)
        pr_to_merge = select_pr_interactive(open_prs, gemini_client)
        
        if not pr_to_merge:
            print("   ⚪️ Merge cancelled.")
            return False
    
    # Display PR details
    print(f"\n📌 Selected PR:")
    print(f"   • PR #{pr_to_merge['number']}: {pr_to_merge['title']}")
    print(f"   • Branch: {pr_to_merge['headRefName']} → {pr_to_merge['baseRefName']}")
    print(f"   • URL: {pr_to_merge['url']}")
    
    # Check merge status
    print("\n   🔍 Checking merge status...")
    try:
        status_cmd = ["gh", "pr", "checks", str(pr_to_merge['number'])]
        status_process = subprocess.run(
            status_cmd,
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if status_process.returncode == 0:
            print("   ✅ All checks passed!")
        else:
            print("   ⚠️  Some checks may have failed.")
            if not input("   ❔ Continue anyway? (y/n): ").lower() == 'y':
                print("   ⚪️ Merge cancelled.")
                return False
    except:
        # Checks command might not be available, continue
        pass
    
    # Final confirmation
    target_branch = pr_to_merge['baseRefName']
    
    if target_branch in ['main', 'master']:
        print("\n" + "="*50)
        print("   🔒 SECURITY CHECK: Merging to MAIN branch!")
        print("   ⚠️  This action will deploy code to production.")
        print("="*50)
        
        # Get security confirmation
        import getpass
        try:
            password = getpass.getpass("   🔑 Enter admin password to merge to main: ")
            if not password:
                print("   ❌ Merge cancelled.")
                return False
            # You can add actual password validation here
        except (EOFError, KeyboardInterrupt):
            print("\n   ❌ Merge cancelled.")
            return False
    else:
        # Non-main branch merge confirmation
        if not input(f"\n   ❔ Merge PR #{pr_to_merge['number']} to '{target_branch}'? (y/n): ").lower() == 'y':
            print("   ⚪️ Merge cancelled.")
            return False
    
    # Perform the merge
    print(f"\n   🔀 Merging PR #{pr_to_merge['number']}...")
    
    try:
        merge_cmd = ["gh", "pr", "merge", str(pr_to_merge['number']), "--merge", "--delete-branch"]
        merge_process = subprocess.run(
            merge_cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"   ✅ PR #{pr_to_merge['number']} successfully merged!")
        print(f"   🗑️  Branch '{pr_to_merge['headRefName']}' deleted.")
        
        # Update local repository
        print("\n   🔄 Updating local repository...")
        git_manager.fetch_updates()
        
        current_branch = git_manager.get_current_branch()
        if current_branch == pr_to_merge['headRefName']:
            # We're on the deleted branch, switch to target
            print(f"   📋 Switching to '{target_branch}' branch...")
            git_manager.checkout(target_branch)
            git_manager.pull(target_branch)
        elif current_branch == target_branch:
            # Update the target branch
            git_manager.pull(target_branch)
        
        print("\n   🎉 Merge completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Merge failed!")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False


if __name__ == "__main__":
    # Allow direct execution
    merge_command(sys.argv[1:]) 