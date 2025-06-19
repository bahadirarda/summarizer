import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
import re
import sys
import subprocess
import urllib.parse

from .file_tracker import (
    get_changed_files_since_last_run,
    get_file_line_changes,
    get_aggregate_line_stats,
    create_file_backups,
)
from .json_changelog_manager import JsonChangelogManager, ImpactLevel, ChangeType
from .readme_generator import update_readme
from .version_manager import VersionManager
from .git_manager import GitManager

logger_changelog = logging.getLogger(__name__)


def _detect_impact_level(summary: str, changed_files: list) -> ImpactLevel:
    summary_lower = summary.lower()
    if any(keyword in summary_lower for keyword in ["critical", "hotfix", "security"]):
        return ImpactLevel.CRITICAL
    if any(keyword in summary_lower for keyword in ["major", "breaking", "api"]):
        return ImpactLevel.HIGH
    if any(keyword in summary_lower for keyword in ["typo", "docs", "readme"]):
        return ImpactLevel.LOW
    if len(changed_files) > 10:
        return ImpactLevel.HIGH
    elif len(changed_files) <= 2:
        return ImpactLevel.LOW
    return ImpactLevel.MEDIUM


def _ask_user(prompt: str) -> bool:
    try:
        return input(f"{prompt} (y/n): ").lower() == 'y'
    except (EOFError, KeyboardInterrupt):
        return False


def _run_ci_checks(project_root: Path) -> bool:
    ci_script_path = project_root / "scripts" / "run_ci_checks.py"
    if not ci_script_path.exists():
        print(f"   ❌ CI script not found at {ci_script_path}")
        return False
    ci_process = subprocess.run([sys.executable, str(ci_script_path), '-s'], cwd=project_root)
    if ci_process.returncode == 0:
        print("   ✅ All CI checks passed.")
        return True
    else:
        print("   ❌ CI checks failed.")
        return False


def _handle_pull_request_flow(project_root: Path, git_manager: GitManager, current_branch: str, target_branch: str, pr_body: str, gemini_client: Any = None):
    """
    Handles ONLY the pull request creation, assuming the branch is pushed and ready.
    """
    if not _ask_user(f"   ❔ Create a Pull Request from '{current_branch}' to '{target_branch}'?"):
        print("   ⚪️ Pull request creation skipped by user.")
        return

    print("   🤖 Generating AI-powered pull request details...")
    pr_title, new_pr_body = git_manager.generate_pull_request_details(pr_body, gemini_client)
    print(f"   📝 PR Title: {pr_title}")
    
    pr_url = git_manager.create_pull_request(
        title=pr_title, body=new_pr_body, base_branch=target_branch, head_branch=current_branch
    )

    if pr_url:
        print(f"   ✅ Successfully created Pull Request: {pr_url}")
    else:
        print("   ❌ Failed to create Pull Request.")
        print("   You may need to create it manually on GitHub.")


def update_changelog(project_root: Optional[Path] = None):
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent
    
    git_manager = GitManager(project_root)
    json_manager = JsonChangelogManager(project_root)
    
    changed_files = get_changed_files_since_last_run(project_root)
    if not changed_files:
        print("   📝 No file changes detected")
        return

    print(f"   ✅ Found {len(changed_files)} changed files.")
    
    line_changes = get_file_line_changes(project_root, changed_files)
    aggregate_stats = get_aggregate_line_stats(line_changes)
    total_lines_added = aggregate_stats["total_lines_added"]
    total_lines_removed = aggregate_stats["total_lines_removed"]
    print(f"   📈 Line changes: +{total_lines_added} added, -{total_lines_removed} removed")

    gemini_client = None
    try:
        from ..services.request_manager import RequestManager
        request_manager = RequestManager()
        gemini_client = request_manager.get_client("GeminiClient")
    except ValueError:
        logger_changelog.warning("GeminiClient not found.")

    summary = "Default update summary."
    if gemini_client and gemini_client.is_ready():
        try:
            prompt = f"Değişen dosyalar: {', '.join(changed_files)}"
            summary = gemini_client.generate_summary(text_prompt=prompt, changed_files=changed_files)
            print("   ✨ AI analysis completed successfully")
        except Exception as e:
            logger_changelog.error(f"AI summary failed: {e}")
            summary = "AI summary failed. Changes have been applied."
    
    impact_level = _detect_impact_level(summary, changed_files)
    print(f"   🎯 Impact level: {impact_level.value}")

    current_branch = git_manager.get_current_branch()
    if current_branch in ['main', 'master']:
        print(f"\n   ⚠️  You are on the protected '{current_branch}' branch.")
        suggested_branch = git_manager.suggest_branch_name(summary, gemini_client)
        prompt_text = f"'{suggested_branch}'" if suggested_branch else "a new branch"
        
        if _ask_user(f"   ❔ Create and switch to {prompt_text} to continue?"):
            new_branch_name = suggested_branch or input("   > Enter the new branch name: ").strip()
            if new_branch_name and git_manager.create_branch(new_branch_name) and git_manager.checkout(new_branch_name):
                print(f"   ✅ Switched to new branch: '{new_branch_name}'")
            else:
                print("   ❌ Aborting. No changes have been made.")
                return
        else:
            print("   ⚪️ Operation aborted. No changes have been made.")
            return

    entry_id = json_manager.add_entry(
        ai_summary=summary, changed_files=changed_files, impact_level=impact_level,
        change_type=ChangeType.OTHER, lines_added=total_lines_added, lines_removed=total_lines_removed,
    )
    print(f"   ✅ Changelog entry created (ID: {entry_id[:8]}...)")
    create_file_backups(project_root, "src")
    update_readme(project_root, gemini_client)
    
    try:
        version_manager = VersionManager(project_root)
        increment_type = "patch"
        if impact_level == ImpactLevel.CRITICAL: increment_type = "major"
        elif impact_level == ImpactLevel.HIGH: increment_type = "minor"
        elif impact_level == ImpactLevel.MEDIUM: increment_type = "minor"

        new_version, old_version, codename = version_manager.auto_increment(increment_type, gemini_client)

        if new_version != old_version and version_manager.update_version_in_files(new_version):
            print(f"   📈 Version updated: {old_version} → {new_version}")
            if codename: print(f"   💫 Codename: {codename}")
            
            version_manager.create_git_tag(new_version, codename=codename)
            
            # Pre-commit CI checks for all branches
            current_branch_name = git_manager.get_current_branch()
            print(f"\n   🔬 Running pre-push CI checks for '{current_branch_name}'...")
            if not _run_ci_checks(project_root):
                if not _ask_user("   ⚠️  CI checks failed. Continue with push/PR anyway?"):
                    print("   ⚪️ Operation aborted due to CI failure.")
                    # Revert version bump if commit is aborted
                    version_manager.update_version_in_files(old_version)
                    print(f"   ⏪ Version reverted to {old_version}.")
                    return
                print("   ⚪️ CI checks failed, but proceeding as requested.")
            else:
                print("   ✅ Pre-push CI checks passed.")

            # Commit changes to git
            if not git_manager.is_working_directory_clean():
                prompt_message = f"   ❔ Summarizer updated project files. Commit these maintenance changes to '{current_branch_name}'?"
                if _ask_user(prompt_message):
                    commit_message = f"chore(summarizer): Auto-update to v{new_version}\n\n{summary}"
                    if not (git_manager.stage_all() and git_manager.commit(commit_message)):
                        print("   ❌ Failed to commit maintenance changes. Aborting.")
                        return
                    print("   ✅ Maintenance changes committed.")
                else:
                    print("   ⚪️ Commit skipped by user.")


            # --- DECOUPLED PUSH AND PULL REQUEST FLOW ---
            
            # Step 1: Always ask to push the current branch
            if _ask_user(f"   ❔ Push the changes on '{current_branch_name}' to remote?"):
                print(f"   🚀 Pushing changes to '{current_branch_name}'...")
                push_success, push_output = git_manager.push(current_branch_name)

                if not push_success:
                    # If it's a real error (not just 'up-to-date'), stop.
                    if "already up-to-date" not in push_output and "up to date" not in push_output:
                        print(f"   ❌ Push failed. Git Error:\n{push_output}")
                        return
                
                print(f"   ✅ Branch '{current_branch_name}' is up-to-date on remote.")

                # Step 2: AFTER a push, check if a PR is logical for this branch
                pr_target_map = {
                    'feature/': 'develop',
                    'bugfix/': 'develop',
                    'develop': 'staging', # The missing link
                    'release/': 'main',
                    'hotfix/': 'main'
                }
                
                pr_target = pr_target_map.get(current_branch_name)
                if not pr_target:
                    pr_target = next((target for prefix, target in pr_target_map.items() if current_branch_name.startswith(prefix)), None)

                if pr_target:
                    _handle_pull_request_flow(project_root, git_manager, current_branch_name, pr_target, summary, gemini_client)
                else:
                    print(f"   ⚪️ No standard Pull Request action defined for branch '{current_branch_name}'.")
            else:
                print("   ⚪️ Push skipped by user.")

    except Exception as e:
        logger_changelog.error(f"Version management failed: {e}", exc_info=True)
