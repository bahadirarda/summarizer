import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
import re
import sys
import subprocess
import urllib.parse
import time

from .file_tracker import (  # Import for getting changed files
    get_changed_files_since_last_run,
    get_file_line_changes,
    get_aggregate_line_stats,
    create_file_backups,
)
from .json_changelog_manager import JsonChangelogManager, ImpactLevel, ChangeType
from .readme_generator import update_readme
from .version_manager import VersionManager
from .git_manager import GitManager, SyncStatus, _ask_user

logger_changelog = logging.getLogger(__name__)


def _prompt_for_issue(issues: list) -> Optional[dict]:
    """Displays a list of issues and prompts the user to select one."""
    if not issues:
        return None
        
    print("\n   🔗 Link to an open GitHub Issue?")
    print("   " + "="*40)
    for i, issue in enumerate(issues):
        print(f"      {i+1}. #{issue['number']}: {issue['title']}")
    print("      0. None of these / Skip")
    print("   " + "="*40)
    
    while True:
        try:
            choice = input("   Enter your choice (number): ").strip()
            if not choice: # User just pressed enter
                print("   ⚪️ Skipping issue linking.")
                return None
            
            choice_num = int(choice)
            
            if choice_num == 0:
                print("   ⚪️ Skipping issue linking.")
                return None
            if 1 <= choice_num <= len(issues):
                selected = issues[choice_num - 1]
                print(f"   ✅ Linking to Issue #{selected['number']}: {selected['title']}")
                return selected
            else:
                print(f"   ⚠️  Invalid selection. Please try again.")
        except ValueError:
            print(f"   ⚠️  Invalid input. Please enter a number from the list.")
        except (EOFError, KeyboardInterrupt):
            print("\n   ⚪️ Operation cancelled by user.")
            return None


def _detect_impact_level(summary: str, changed_files: list) -> ImpactLevel:
    """Auto-detect impact level based on summary and files"""
    summary_lower = summary.lower()

    # Critical indicators
    critical_keywords = [
        "critical",
        "hotfix",
        "security"]
    if any(keyword in summary_lower for keyword in critical_keywords):
        return ImpactLevel.CRITICAL

    # High impact indicators
    high_keywords = ["major", "breaking", "api"]
    if any(keyword in summary_lower for keyword in high_keywords):
        return ImpactLevel.HIGH

    # Low impact indicators
    low_keywords = ["typo", "docs", "readme"]
    if any(keyword in summary_lower for keyword in low_keywords):
        return ImpactLevel.LOW

    # Based on file count
    if len(changed_files) > 10:
        return ImpactLevel.HIGH
    elif len(changed_files) <= 2:
        return ImpactLevel.LOW

    return ImpactLevel.MEDIUM


def _run_ci_checks(project_root: Path) -> bool:
    ci_script_path = project_root / "scripts" / "run_ci_checks.py"
    if not ci_script_path.exists():
        print(f"   ❌ CI script not found at {ci_script_path}")
        return False
    # Pass '-s' to pytest to disable output capture, allowing interactive prompts if necessary for testing
    ci_process = subprocess.run([sys.executable, str(ci_script_path), '-s'], cwd=project_root)
    if ci_process.returncode == 0:
        print("   ✅ All CI checks passed.")
        return True
    else:
        print("   ❌ CI checks failed.")
        return False


def _write_next_command(project_root: Path, command: str):
    command_file_path = project_root / ".summarizer" / "next_command.sh"
    try:
        with open(command_file_path, "w") as f: f.write(f"{command}\n")
        print(f"   ✨ Next step command generated: {command}")
    except Exception as e:
        logger_changelog.error(f"Could not create next_command.sh file: {e}")


def _extract_pr_number(pr_url: str) -> Optional[int]:
    """Extract PR number from GitHub PR URL"""
    try:
        # URL format: https://github.com/owner/repo/pull/123
        parts = pr_url.strip().split('/')
        if 'pull' in parts:
            pr_number = int(parts[-1])
            return pr_number
    except:
        pass
    return None


def _handle_pull_request_flow(project_root: Path, git_manager: GitManager, current_branch: str, target_branch: str, summary: str, gemini_client: Any = None, auto_create: bool = True):
    """Handles the pull request creation/update process intelligently and offers next steps."""
    print("   ⏱️  Checking for existing PRs and remote branches...")
    if not git_manager.remote_branch_exists(target_branch):
        print(f"   ❌ Target branch '{target_branch}' does not exist on the remote. Please push it first.")
        return
    
    git_manager.fetch_updates()
    
    existing_pr = git_manager.get_existing_pr(current_branch)
    current_version = VersionManager(project_root).get_current_version()
    
    # Better PR title based on branch type
    branch_type = current_branch.split('/')[0] if '/' in current_branch else 'update'
    pr_title = f"{branch_type}: v{current_version} - {current_branch.split('/')[-1] if '/' in current_branch else 'update'}"
    
    if existing_pr:
        print(f"   ✅ An open pull request already exists: {existing_pr['url']}")
        
        # Check if there are new commits to push
        sync_status, ahead, behind = git_manager.get_branch_sync_status(current_branch)
        
        if sync_status == SyncStatus.AHEAD:
            # Only push if we have unpushed commits
            if _ask_user(f"   ❔ Push {ahead} new commit(s) to the existing PR?"):
                print(f"   🚀 Pushing new commits to '{current_branch}'...")
                push_success, _ = git_manager.push(current_branch)
                if push_success:
                    print("   ✅ Successfully pushed new commits to the existing PR.")
                    print(f"   📎 PR URL: {existing_pr['url']}")
                else:
                    print("   ❌ Failed to push updates to the PR branch.")
        else:
            print(f"   ⚪️ No new commits since last push. PR is up to date.")
            print(f"   📎 PR URL: {existing_pr['url']}")
    else:
        # Check if branch has been pushed
        if not git_manager.remote_branch_exists(current_branch):
            print(f"   ⚠️  Branch '{current_branch}' has not been pushed to remote yet.")
            return
        
        # If auto_create is True (from AI workflow), create PR automatically
        # Otherwise ask the user
        should_create = auto_create or _ask_user(f"   ❔ Create a new Pull Request from '{current_branch}' to '{target_branch}'?")
        
        if should_create:
            print("   🤖 Generating AI-powered pull request details...")
            new_body = git_manager.generate_pull_request_body(summary, gemini_client)
            print(f"   📝 PR Title: {pr_title}")
            pr_url = git_manager.create_pull_request(title=pr_title, body=new_body, base_branch=target_branch, head_branch=current_branch)
            if pr_url:
                print(f"   ✅ Successfully created Pull Request: {pr_url}")
                
                # Check if PR has conflicts after creation
                print("   🔍 Checking for potential conflicts...")
                pr_number = _extract_pr_number(pr_url)
                if pr_number:
                    try:
                        import subprocess
                        import json
                        conflict_cmd = ["gh", "pr", "view", str(pr_number), "--json", "mergeable,mergeStateStatus"]
                        conflict_process = subprocess.run(
                            conflict_cmd,
                            cwd=project_root,
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        
                        conflict_data = json.loads(conflict_process.stdout)
                        
                        if conflict_data.get('mergeable') == 'CONFLICTING':
                            print("   ⚠️  WARNING: This PR has merge conflicts!")
                            print("   📝 Conflicts need to be resolved before merging.")
                            
                            while True:
                                print("\n   💡 How would you like to proceed?")
                                print("      1. Attempt to resolve conflicts automatically (merges target into source)")
                                print("      2. Force push your branch to overwrite remote (DANGEROUS)")
                                print("      3. Cancel and resolve manually")
                                choice = input("   Enter your choice (1, 2, or 3): ").strip()

                                if choice == '1':
                                    if git_manager.resolve_conflicts_with_pr(pr_number):
                                        print("\n   🎉 Conflicts resolved successfully!")
                                        print("   📋 The PR has been updated and is ready for review.")
                                    else:
                                        print("   ❌ Automatic conflict resolution failed.")
                                        print("   💡 Please resolve conflicts manually.")
                                    break
                                elif choice == '2':
                                    if git_manager.force_push_with_confirmation(current_branch):
                                        print("\n   🎉 Force push completed.")
                                        print("   📋 The PR has been updated and should now be conflict-free.")
                                    else:
                                        print("   ❌ Force push was cancelled or failed.")
                                    break
                                elif choice == '3':
                                    print("   ⚪️ Action cancelled. Please resolve conflicts manually.")
                                    break
                                else:
                                    print("   ⚠️  Invalid choice. Please enter 1, 2, or 3.")
                        elif conflict_data.get('mergeStateStatus') == 'BLOCKED':
                            print("   ⚠️  PR is blocked (required checks not passed)")
                    except Exception as e:
                        # Don't fail if conflict check fails
                        print(f"   ⚠️  Could not check PR status: {e}")
            else:
                print("   ❌ Failed to create Pull Request.")


def _handle_release_creation(project_root: Path, git_manager: GitManager, new_version: str):
    release_branch_name = f"release/v{new_version}"
    if _ask_user(f"   ❔ Run CI checks and create release branch '{release_branch_name}'?"):
        if not _run_ci_checks(project_root):
            if not _ask_user("   ⚠️  CI checks failed. Create branch anyway?"):
                return
        if git_manager.create_branch(release_branch_name):
            _write_next_command(project_root, f"git checkout {release_branch_name}")
        else:
            print(f"   ⚠️  Could not create release branch '{release_branch_name}'.")


def _post_workflow_sync(git_manager: GitManager):
    """After a workflow, offers a safe, professional, and context-aware way to sync the local repo."""
    print("\n" + "="*50 + "\n   🚀 Workflow Complete\n" + "="*50)
    
    # Just sync current branch, don't offer dangerous merges
    current_branch = git_manager.get_current_branch()
    print(f"\n   🔎 Checking sync status for current branch '{current_branch}'...")
    
    status, ahead, behind = git_manager.get_branch_sync_status(current_branch)
    if status == SyncStatus.SYNCED:
        print(f"   ✅ Branch '{current_branch}' is in sync with remote.")
    elif status == SyncStatus.AHEAD:
        if _ask_user(f"   ❔ Your branch is {ahead} commit(s) ahead. Push remaining changes?"):
            git_manager.push(current_branch)
    elif status == SyncStatus.BEHIND:
        if _ask_user(f"   ❔ Your branch is {behind} commit(s) behind. Pull latest changes?"):
            git_manager.pull(current_branch)
    elif status == SyncStatus.DIVERGED:
        print(f"   ⚠️  Branch '{current_branch}' has diverged from the remote. You have unique local and remote commits.")
        print("   💡 This requires manual intervention. Your options:")
        print("      1. 'git pull' - to merge remote changes into your local branch (may cause conflicts).")
        print("      2. Force push - to overwrite the remote branch with your local changes (DANGEROUS).")
        
        if _ask_user("\n   ❔ Do you want to attempt a force push to resolve the divergence?"):
            git_manager.force_push_with_confirmation(current_branch)
    
    print("\n   📋 Workflow Summary:")
    print(f"   • Current branch: {current_branch}")
    print("   • All changes have been processed")
    print("   • Remember: Use PRs for merging to protected branches")


def _handle_git_workflow(project_root: Path, git_manager: GitManager, new_version: str, summary: str, gemini_client: Any):
    """Handle additional git workflow after main processing - simplified version"""
    current_branch_name = git_manager.get_current_branch()
    
    # Only handle if there are uncommitted changes (edge case)
    if not git_manager.is_working_directory_clean():
        print(f"\n   📂 Additional changes detected on '{current_branch_name}'...")
        if _ask_user("   ❔ Stage and commit these additional changes?"):
            git_manager.stage_all()
            commit_message = f"feat(summarizer): Additional changes for v{new_version}"
            if git_manager.commit(commit_message):
                print("   ✅ Additional changes committed.")
                if _ask_user("   ❔ Push these additional changes?"):
                    git_manager.push(current_branch_name)
    
    # Show final sync status
    _post_workflow_sync(git_manager)


def update_changelog(project_root: Optional[Path] = None):
    """Update changelog with AI-generated summaries using JSON format"""
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        logger_changelog.warning(
            f"project_root not provided to update_changelog, guessed as {project_root}")

    # Initialize JSON changelog manager
    json_manager = JsonChangelogManager(project_root)

    # Get changed files - check for different possible source directories
    changed_files = []
    try:
        print("   🔍 Scanning for changed files...")
        # Use dynamic directory discovery (no manual directory specification needed)
        changed_files = get_changed_files_since_last_run(project_root)
        print(f"   📂 Dynamically scanning all Python directories")

        if changed_files:
            print(f"   ✅ Found {len(changed_files)} changed files:")
            for file in changed_files:
                print(f"      • {file}")
            logger_changelog.info(
                f"Detected changed files since last run: {changed_files}"
            )
        else:
            print("   📝 No file changes detected")
            logger_changelog.info("No file changes detected since last run.")
            # Check if this is a new project that needs initialization
            changelog_file = project_root / "CHANGELOG.md"
            json_file = project_root / "changelog.json"
            
            if not changelog_file.exists() or not json_file.exists():
                print("   🎉 Initializing new project...")
                logger_changelog.info("Initializing new project with welcome entry.")
                _create_initial_project_entry(json_manager, project_root)
                return
            else:
                print("   ✅ Project up to date - no changes to track")
                # No changes in existing project
                return
    except Exception as e:
        logger_changelog.error(
            f"Error detecting changed files for changelog: {e}", exc_info=True
        )
        # Return if there's an error, don't create fake entries
        return

    # Analyze line changes
    line_changes = {}
    total_lines_added = 0
    total_lines_removed = 0

    try:
        print("   📊 Analyzing line changes...")
        line_changes = get_file_line_changes(project_root, changed_files)
        aggregate_stats = get_aggregate_line_stats(line_changes)
        total_lines_added = aggregate_stats["total_lines_added"]
        total_lines_removed = aggregate_stats["total_lines_removed"]

        print(f"   📈 Line changes: +{total_lines_added} added, -{total_lines_removed} removed")

        logger_changelog.info(
            f"Line changes analysis: +{total_lines_added} -{total_lines_removed} "
            f"across {len(changed_files)} files"
        )

    except Exception as e:
        print("   ⚠️  Could not analyze line changes")
        logger_changelog.error(
            f"Error analyzing line changes: {e}",
            exc_info=True)

    # Get AI summary using RequestManager
    try:
        print("   🤖 Generating AI analysis...")
        from ..services.request_manager import RequestManager

        request_manager = RequestManager()
        gemini_client = request_manager.get_client("GeminiClient")
    except ValueError:
        print("   ⚠️  AI client not available")
        logger_changelog.warning("GeminiClient not found in RequestManager.")
        gemini_client = None

    summary = "Genel güncelleme."
    impact_level = ImpactLevel.MEDIUM
    change_type = ChangeType.OTHER

    if gemini_client and gemini_client.is_ready():
        try:
            prompt = f"Değişen dosyalar: {', '.join(changed_files)}"
            ai_summary = gemini_client.generate_summary(
                text_prompt=prompt, changed_files=changed_files
            )
            summary = ai_summary
            print("   ✨ AI analysis completed successfully")
            print(f"   📝 Summary: {summary[:100]}{'...' if len(summary) > 100 else ''}")
            logger_changelog.info(f"AI tarafından oluşturulan özet: {summary}")

            # Auto-detect impact level based on summary and files
            impact_level = _detect_impact_level(ai_summary, changed_files)
            print(f"   🎯 Impact level: {impact_level.value}")

            # Ask user to link to a GitHub issue
            selected_issue = None
            try:
                git_manager = GitManager(project_root)
                open_issues = git_manager.get_open_issues()
                if open_issues:
                    selected_issue = _prompt_for_issue(open_issues)
            except Exception as e:
                logger_changelog.warning(f"Could not check for GitHub issues: {e}")

        except Exception as e:
            print("   ⚠️  AI analysis failed, using fallback")
            logger_changelog.error(
                f"GeminiClient'tan özet alınırken hata oluştu: {e}",
                exc_info=True)
            summary = "AI özeti alınamadı. Değişiklikler uygulandı."
    else:
        print("   ⚠️  AI client unavailable, using default summary")
        logger_changelog.warning(
            "GeminiClient kullanılamıyor. Varsayılan özet kullanılıyor."
        )

    # Add entry to JSON changelog
    print("   💾 Saving changelog entry...")
    entry_id = json_manager.add_entry(
        ai_summary=summary,
        changed_files=changed_files,
        impact_level=impact_level,
        change_type=change_type,
        lines_added=total_lines_added,
        lines_removed=total_lines_removed,
    )

    print(f"   ✅ Changelog entry created (ID: {entry_id[:8]}...)")
    logger_changelog.info(f"Changelog entry added with ID: {entry_id}")

    # Create backups for next run comparison
    try:
        print("   🔄 Creating backup files for future comparison...")
        create_file_backups(project_root, "src" if (project_root / "src").exists() else ".")
        print("   ✅ Backup files created")
        logger_changelog.debug("File backups created for future line analysis")
    except Exception as e:
        print("   ⚠️  Could not create backup files")
        logger_changelog.error(
            f"Error creating file backups: {e}",
            exc_info=True)

    # Update README.md automatically with AI enhancement
    try:
        print("   📝 Updating README.md with current project state...")
        
        # Get AI client for README enhancement
        ai_client = None
        try:
            from ..services.request_manager import RequestManager
            request_manager = RequestManager()
            ai_client = request_manager.get_client("GeminiClient")
        except:
            pass  # Continue without AI enhancement
            
        readme_updated = update_readme(project_root, ai_client)
        if readme_updated:
            print("   ✅ README.md automatically updated")
        else:
            print("   ⚠️  README.md update skipped")
            
    except Exception as e:
        print(f"   ⚠️  Could not update README.md: {e}")
        logger_changelog.error(f"Error updating README.md: {e}", exc_info=True)

    # Professional Version Management
    try:
        print("   🏷️  Analyzing changes for version management...")
        version_manager = VersionManager(project_root)
        git_manager = GitManager(project_root)

        # Determine increment type based on impact level ONLY. This is the single source of truth.
        increment_type = "patch"
        if impact_level == ImpactLevel.CRITICAL:
            increment_type = "major"
        elif impact_level == ImpactLevel.HIGH:
            increment_type = "minor"
        elif impact_level == ImpactLevel.MEDIUM:
            increment_type = "minor"

        # Use the new centralized incrementer
        new_version, old_version = version_manager.auto_increment(increment_type)

        if new_version != old_version and version_manager.update_version_in_files(new_version):
            print(f"   📈 Version updated: {old_version} → {new_version}")
            print(f"   🎯 Change Impact: {impact_level.value} ({increment_type} increment)")

            # Get version codename
            major, minor, _ = version_manager.parse_version(new_version)
            codename = version_manager._get_version_codename(major, minor, new_version, gemini_client)
            if codename:
                print(f"   💫 Codename: {codename}")
                
            # Create git tag for new version
            try:
                version_manager.create_git_tag(new_version, codename=codename)
                print(f"   🏷️  Git tag created: v{new_version}")
            except Exception as tag_error:
                print(f"   ⚠️  Could not create git tag: {tag_error}")

            # Get AI workflow decision
            current_branch_name = git_manager.get_current_branch()
            print("\n   🤖 Consulting AI for workflow optimization...")
            workflow_decision = _get_ai_workflow_decision(gemini_client, current_branch_name, summary, impact_level, changed_files)
            
            print(f"   🎯 AI Recommendation: {workflow_decision['reasoning']}")
            
            # Handle branch creation if recommended
            if workflow_decision['recommended_branch'] != 'current' and workflow_decision['recommended_branch'] != current_branch_name:
                recommended_branch = workflow_decision['recommended_branch']
                if _ask_user(f"   ❔ AI suggests creating branch '{recommended_branch}'. Create it?"):
                    if git_manager.create_branch(recommended_branch):
                        git_manager.checkout(recommended_branch)
                        current_branch_name = recommended_branch
                        print(f"   ✅ Switched to recommended branch: {recommended_branch}")
                    else:
                        print(f"   ⚠️  Could not create recommended branch. Continuing on {current_branch_name}")
            
            # Pre-commit CI checks for main/develop branches
            if current_branch_name in ['main', 'develop', 'staging']:
                print(f"\n   🔬 Running pre-commit CI checks for '{current_branch_name}' branch...")
                if not _run_ci_checks(project_root):
                    if not _ask_user("   ⚠️  CI checks failed. Continue with commit anyway?"):
                        print("   ⚪️ Commit aborted by user.")
                        # Revert version bump if commit is aborted
                        version_manager.update_version_in_files(old_version)
                        print(f"   ⏪ Version reverted to {old_version}.")
                        return
                    print("   ⚪️ CI checks failed, but proceeding with commit as requested.")
                else:
                    print("   ✅ Pre-commit CI checks passed.")

            # Commit changes to git
            if not git_manager.is_working_directory_clean():
                prompt_message = f"   ❔ Commit changes to '{current_branch_name}'?"
                if _ask_user(prompt_message):
                    commit_body = summary
                    if selected_issue:
                        commit_body += f"\n\nCloses #{selected_issue['number']}"
                    
                    commit_message = f"chore(summarizer): Auto-update to v{new_version}\n\n{commit_body}"
                    if not (git_manager.stage_all() and git_manager.commit(commit_message)):
                        print("   ❌ Failed to commit changes. Aborting.")
                        return

            # Follow AI-recommended workflow
            if workflow_decision['workflow'] == 'pr':
                # Create PR to target branch
                target_branch = workflow_decision.get('target_branch', 'develop')
                
                if _ask_user(f"   ❔ Push '{current_branch_name}' to GitHub and create PR to '{target_branch}'?"):
                    success, output = git_manager.push(current_branch_name)
                    if success:
                        print("   ✅ Branch pushed to GitHub successfully.")
                        # Now handle PR creation/update
                        _handle_pull_request_flow(project_root, git_manager, current_branch_name, target_branch, summary, gemini_client)
                        
                        # Info about main branch protection
                        if target_branch in ['main', 'master']:
                            print("\n   🔒 Note: This PR targets the MAIN branch.")
                            print("   📋 The PR will need to be reviewed and approved before merging.")
                            print("   💡 Merge protection is enforced on the main branch.")
                    else:
                        print(f"   ❌ Push failed: {output}")
            elif workflow_decision['workflow'] == 'direct':
                # Direct push (only for non-protected branches)
                if current_branch_name not in ['main', 'master']:
                    if _ask_user(f"   ❔ Push changes directly to '{current_branch_name}' on GitHub (no PR)?"):
                        success, output = git_manager.push(current_branch_name)
                        if success:
                            print("   ✅ Changes pushed directly to GitHub.")
                        else:
                            print(f"   ❌ Push failed: {output}")
                else:
                    print("   ❌ Direct push to main/master branch is not allowed!")
                    print("   💡 Please create a release or hotfix branch instead.")
            elif workflow_decision['workflow'] == 'release':
                # Special release workflow
                print("   📦 Following release workflow...")
                if _ask_user(f"   ❔ Push '{current_branch_name}' to GitHub and create release PR to 'main'?"):
                    success, output = git_manager.push(current_branch_name)
                    if success:
                        print("   ✅ Release branch pushed to GitHub.")
                        # Now handle PR creation for release
                        _handle_pull_request_flow(project_root, git_manager, current_branch_name, 'main', summary, gemini_client)
                    else:
                        print(f"   ❌ Push failed: {output}")

    except Exception as e:
        print(f"   ⚠️  Version management failed: {e}")
        logger_changelog.error(f"Error in version management: {e}", exc_info=True)

    # Hand off to the master Git workflow handler
    _handle_git_workflow(project_root, git_manager, new_version, summary, gemini_client)


def _create_initial_project_entry(json_manager, project_root: Path):
    """Create professional initial project entry for new projects"""
    
    # Create hidden project structure
    summarizer_dir = project_root / ".summarizer"
    summarizer_dir.mkdir(exist_ok=True)
    
    # Detect project type
    project_type = _detect_project_type(project_root)
    project_name = project_root.name
    
    # Professional welcome message based on project type
    if project_type == "python":
        welcome_summary = f"""🚀 **{project_name} Projesi Başlatıldı**

**Proje Türü**: Python Projesi  
**Başlatılma Tarihi**: {datetime.now().strftime('%d %B %Y')}  
**Summarizer Framework**: v2.0.0

**📋 Proje Özeti:**
Bu proje, Summarizer Framework ile otomatik değişiklik takibi ve AI destekli analiz için yapılandırıldı. Artık kod değişiklikleriniz otomatik olarak tespit edilecek ve akıllı özetler oluşturulacak.

**🔧 Aktif Özellikler:**
- ✅ Otomatik dosya değişiklik takibi
- ✅ AI destekli kod analizi (Gemini AI)
- ✅ JSON ve Markdown changelog oluşturma
- ✅ Etki seviyesi ve değişiklik tipi otomatik tespiti
- ✅ Satır bazında değişiklik analizi

**📁 Oluşturulan Dosyalar:**
- `CHANGELOG.md` - İnsan okunabilir değişiklik günlüğü
- `changelog.json` - Yapılandırılmış değişiklik verisi
- `.summarizer/` - Gizli sistem dosyaları

**🎯 Sonraki Adımlar:**
1. Python dosyalarınızda değişiklik yapın
2. `summarizer` komutunu tekrar çalıştırın
3. Otomatik oluşturulan değişiklik analizini inceleyin

**💡 İpucu:** `summarizer --help` komutuyla tüm özellikleri keşfedin!"""

    elif project_type == "web":
        welcome_summary = f"""🌐 **{project_name} Web Projesi Başlatıldı**

**Proje Türü**: Web Geliştirme Projesi  
**Başlatılma Tarihi**: {datetime.now().strftime('%d %B %Y')}  
**Summarizer Framework**: v2.0.0

**📋 Proje Özeti:**
Web geliştirme projeniz Summarizer Framework ile entegre edildi. Frontend ve backend değişiklikleriniz otomatik olarak takip edilecek ve profesyonel değişiklik raporları oluşturulacak.

**🔧 Desteklenen Dosya Türleri:**
- ✅ JavaScript/TypeScript dosyaları (.js, .ts, .jsx, .tsx)
- ✅ HTML/CSS dosyaları (.html, .css, .scss)
- ✅ Python backend dosyaları (.py)
- ✅ Konfigürasyon dosyaları (package.json, requirements.txt)

**📁 Proje Yapısı Hazırlandı:**
- `CHANGELOG.md` - Geliştirme günlüğü
- `changelog.json` - API entegrasyonu için JSON verisi
- `.summarizer/` - Gizli sistem dosyaları

**🚀 Web Projesi Özellikleri:**
- Frontend/Backend değişiklik ayrımı
- Component bazında analiz
- Dependencies değişiklik takibi
- Performance impact analizi

Bu projede değişiklik yaptığınızda, otomatik olarak akıllı analizler oluşturulacak!"""

    else:
        welcome_summary = f"""📁 **{project_name} Projesi Başlatıldı**

**Proje Türü**: Genel Yazılım Projesi  
**Başlatılma Tarihi**: {datetime.now().strftime('%d %B %Y')}  
**Summarizer Framework**: v2.0.0

**📋 Hoş Geldiniz!**
Projeniz başarıyla Summarizer Framework ile entegre edildi. Artık tüm kod değişiklikleriniz otomatik olarak takip edilecek ve yapay zeka destekli analizler oluşturulacak.

**🔧 Sistem Özellikleri:**
- ✅ Dosya değişiklik takibi (.py, .js, .ts, .html, .css ve daha fazlası)
- ✅ Gemini AI ile kod analizi
- ✅ Otomatik impact level tespiti (Low/Medium/High/Critical)
- ✅ Değişiklik tipi kategorilendirmesi (Feature/Bug Fix/Refactor/Config)
- ✅ Markdown ve JSON format desteği

**📊 Tracking Bilgileri:**
- **Toplam Dosya**: 0 (henüz değişiklik yok)
- **Son Güncelleme**: {datetime.now().strftime('%H:%M:%S')}
- **Durum**: Aktif ve hazır ✅

**🎯 İlk Kullanım:**
1. Herhangi bir dosyada değişiklik yapın
2. `summarizer` komutunu tekrar çalıştırın  
3. Otomatik oluşturulan analizi görüntüleyin

**💡 Komutlar:**
- `summarizer --gui` - Görsel arayüz
- `summarizer --status` - Sistem durumu
- `summarizer screenshot` - Ekran analizi

Projenizde her değişiklik yaptığınızda, akıllı özetler otomatik oluşturulacak!"""

    # Add the initial entry
    print("   🎉 Creating welcome entry for new project...")
    entry_id = json_manager.add_entry(
        ai_summary=welcome_summary,
        changed_files=[],
        impact_level=ImpactLevel.LOW,
        change_type=ChangeType.CONFIG,
        lines_added=0,
        lines_removed=0,
    )
    
    print("   📁 Project structure initialized:")
    print("      • CHANGELOG.md - Human readable changelog")  
    print("      • changelog.json - Structured data format")
    print("      • .summarizer/ - Internal tracking files")
    
    # Create initial README.md for new project
    try:
        print("      • README.md - Auto-generated project documentation")
        
        # Get AI client for enhanced README
        ai_client = None
        try:
            from ..services.request_manager import RequestManager
            request_manager = RequestManager()
            ai_client = request_manager.get_client("GeminiClient")
        except:
            pass  # Continue without AI enhancement
            
        readme_created = update_readme(project_root, ai_client)
        if readme_created:
            print("   📝 Professional README.md created")
        else:
            print("   ⚠️  README.md creation skipped")
            
    except Exception as e:
        print(f"   ⚠️  Could not create README.md: {e}")
        logger_changelog.warning(f"Error creating initial README.md: {e}")
    
    logger_changelog.info(f"Initial project entry created: {entry_id}")
    print(f"   ✅ Project initialized successfully!")


def _detect_project_type(project_root: Path) -> str:
    """Detect project type based on files in directory"""
    
    # Check for web project indicators
    web_files = ["package.json", "index.html", "main.js", "app.js", "webpack.config.js"]
    if any((project_root / f).exists() for f in web_files):
        return "web"
    
    # Check for Python project indicators
    python_files = ["requirements.txt", "setup.py", "pyproject.toml", "main.py"]
    py_files = list(project_root.glob("*.py"))
    if any((project_root / f).exists() for f in python_files) or len(py_files) > 0:
        return "python"
    
    # Default to general project
    return "general"


def get_recent_changelog_entries(project_root: Path, count: int = 5) -> list:
    """Get the most recent changelog entries from JSON format"""
    try:
        json_manager = JsonChangelogManager(project_root)
        entries = json_manager.get_entries(limit=count)
        return [entry.__dict__ for entry in entries]
    except Exception as e:
        logger_changelog.error(f"Error reading changelog entries: {e}")
        return []


def get_changelog_stats(project_root: Path) -> dict:
    """Get changelog statistics"""
    try:
        json_manager = JsonChangelogManager(project_root)
        return json_manager.get_stats()
    except Exception as e:
        logger_changelog.error(f"Error getting changelog stats: {e}")
        return {}


def export_changelog(project_root: Path, format_type: str = "json") -> str:
    """Export changelog in specified format"""
    try:
        json_manager = JsonChangelogManager(project_root)
        return json_manager.export_to_format(format_type)
    except Exception as e:
        logger_changelog.error(f"Error exporting changelog: {e}")
        return ""


def _get_ai_workflow_decision(gemini_client: Any, current_branch: str, summary: str, impact_level: ImpactLevel, changed_files: list) -> dict:
    """Use AI to decide the best workflow, branch strategy, and version management"""
    
    if not (gemini_client and gemini_client.is_ready()):
        # Fallback to rule-based decision
        return {
            "recommended_branch": "feature/auto-update" if current_branch == "main" else "current",
            "workflow": "standard",
            "reasoning": "AI unavailable, using standard workflow"
        }
    
    try:
        prompt = f"""As a senior DevOps engineer, analyze this Git workflow situation and recommend the best approach:

Current Branch: {current_branch}
Impact Level: {impact_level.value}
Changed Files: {', '.join(changed_files[:10])}
Summary: {summary[:200]}...

CRITICAL CONTEXT:
- If already on a feature/bugfix/hotfix/release branch, consider staying on it for continued development
- Only suggest a new branch if the current work is unrelated to the existing branch's purpose

Based on GitFlow best practices, determine:
1. Should we stay on current branch or create a new one?
2. If new branch needed, what type (feature/bugfix/release/hotfix)?
3. The recommended workflow to follow
4. Whether this change should go through PR or direct push

IMPORTANT RULES:
- NEVER allow direct commits to main branch
- If on feature/bugfix/hotfix/release branch, usually stay on it unless work is unrelated
- Critical changes should use hotfix branches
- High/Medium changes should use feature or release branches
- Low impact changes can use existing branches if appropriate
- Branch names MUST be in English, use descriptive English words based on the changed files
- For example: hotfix/git-workflow-fix, feature/ai-integration, release/version-update

Return a JSON object with:
{{
    "recommended_branch": "branch name in ENGLISH or 'current' to stay on {current_branch}",
    "branch_type": "feature|bugfix|release|hotfix|none",
    "workflow": "pr|direct|release",
    "target_branch": "where to merge (if PR workflow)",
    "reasoning": "brief explanation of your decision"
}}"""

        response = gemini_client.generate_simple_text(prompt)
        # Parse JSON from response
        import json
        import re
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            decision = json.loads(json_match.group())
            
            # Validate and sanitize the decision
            if current_branch == "main" and decision.get("recommended_branch") == "current":
                # Override AI if it suggests staying on main
                decision["recommended_branch"] = f"release/v{VersionManager(Path.cwd()).get_current_version()}"
                decision["branch_type"] = "release"
                decision["workflow"] = "pr"
                decision["reasoning"] = "Overriding to prevent direct commits to main branch"
            
            return decision
        else:
            raise ValueError("Could not parse AI response")
            
    except Exception as e:
        logger_changelog.error(f"AI workflow decision failed: {e}")
        # Intelligent fallback based on current situation
        if current_branch == "main":
            # Generate English branch name based on changed files
            if changed_files:
                # Extract meaningful name from first changed file
                first_file = changed_files[0].replace('/', '-').replace('.py', '').replace('_', '-')
                branch_suffix = first_file.split('-')[-1] if '-' in first_file else 'update'
            else:
                branch_suffix = 'update'
                
            return {
                "recommended_branch": f"release/{branch_suffix}-{datetime.now().strftime('%Y%m%d')}",
                "branch_type": "release",
                "workflow": "pr",
                "target_branch": "main",
                "reasoning": "Protecting main branch from direct commits"
            }
        elif current_branch.startswith("feature/"):
            return {
                "recommended_branch": "current",
                "branch_type": "none",
                "workflow": "pr",
                "target_branch": "develop",
                "reasoning": "Standard feature branch workflow"
            }
        else:
            return {
                "recommended_branch": "current",
                "branch_type": "none", 
                "workflow": "direct",
                "reasoning": "Standard workflow for this branch type"
            }


# Test comment
