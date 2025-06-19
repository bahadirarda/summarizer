import logging
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Optional

from .file_tracker import (
    create_file_backups,
    get_aggregate_line_stats,
    get_changed_files_since_last_run,
    get_file_line_changes,
)
from .git_manager import GitManager
from .json_changelog_manager import ChangeType, ImpactLevel, JsonChangelogManager
from .readme_generator import update_readme
from .version_manager import VersionManager

logger_changelog = logging.getLogger(__name__)


def _detect_impact_level(summary: str, changed_files: list) -> ImpactLevel:
    """Auto-detect impact level based on summary and files"""
    summary_lower = summary.lower()
    if any(keyword in summary_lower for keyword in ["critical", "hotfix", "security"]):
        return ImpactLevel.CRITICAL
    if any(keyword in summary_lower for keyword in ["major", "breaking", "api"]):
        return ImpactLevel.HIGH
    if any(keyword in summary_lower for keyword in ["typo", "docs", "readme"]):
        return ImpactLevel.LOW
    if len(changed_files) > 10:
        return ImpactLevel.HIGH
    if len(changed_files) <= 2:
        return ImpactLevel.LOW
    return ImpactLevel.MEDIUM


def update_changelog(project_root: Optional[Path] = None):
    """Update changelog with AI-generated summaries using JSON format"""
    if project_root is None:
        project_root = Path.cwd()

    json_manager = JsonChangelogManager(project_root)
    print("   🔍 Scanning for changed files...")
    changed_files = get_changed_files_since_last_run(project_root)

    if not changed_files:
        print("   📝 No file changes detected")
        return

    print(f"   ✅ Found {len(changed_files)} changed files.")

    print("   📊 Analyzing line changes...")
    line_changes = get_file_line_changes(project_root, changed_files)
    aggregate_stats = get_aggregate_line_stats(line_changes)
    total_lines_added = aggregate_stats["total_lines_added"]
    total_lines_removed = aggregate_stats["total_lines_removed"]
    print(
        f"   📈 Line changes: +{total_lines_added} added, -{total_lines_removed} removed"
    )

    print("   🤖 Generating AI analysis...")
    from ..services.request_manager import RequestManager

    request_manager = RequestManager()
    gemini_client = request_manager.get_client("GeminiClient")

    summary = "Genel güncelleme veya çalıştırma."
    impact_level = ImpactLevel.MEDIUM
    if gemini_client and gemini_client.is_ready():
        prompt = f"Değişen dosyalar: {', '.join(changed_files)}"
        ai_summary = gemini_client.generate_summary(
            text_prompt=prompt, changed_files=changed_files
        )
        summary = ai_summary
        impact_level = _detect_impact_level(ai_summary, changed_files)
        print("   ✨ AI analysis completed successfully")
    else:
        print("   ⚠️  AI client unavailable, using default summary")

    entry_id = json_manager.add_entry(
        ai_summary=summary,
        changed_files=changed_files,
        impact_level=impact_level,
        change_type=ChangeType.OTHER,
        lines_added=total_lines_added,
        lines_removed=total_lines_removed,
    )
    print(f"   ✅ Changelog entry created (ID: {entry_id[:8]}...)")

    create_file_backups(project_root, "src" if (project_root / "src").exists() else ".")
    update_readme(project_root, gemini_client)

    print("   🏷️  Analyzing changes for version management...")
    version_manager = VersionManager(project_root)
    git_manager = GitManager(project_root)

    current_version = version_manager.get_current_version()
    branch_name = version_manager.get_current_branch()
    print(f"   📋 Current version: v{current_version}, Branch: {branch_name}")

    new_version, old_version, increment_type = (
        version_manager.auto_increment_based_on_branch()
    )

    if new_version != old_version:
        print(
            f"   📈 Version update determined: {old_version} → {new_version} ({increment_type})"
        )
        if version_manager.update_version_in_files(new_version):
            major, minor, _ = version_manager.parse_version(new_version)
            codename = version_manager._get_version_codename(
                major, minor, new_version, gemini_client=gemini_client
            )
            print(f"   💫 Codename: {codename}")
            version_manager.create_git_tag(new_version, codename=codename)
            print(f"   🏷️  Git tag created: v{new_version}")

            target_branch = None
            if branch_name.startswith(("feature/", "bugfix/")):
                target_branch = "develop"
            elif branch_name == "develop":
                target_branch = "staging"
            elif branch_name.startswith("release/"):
                target_branch = "main"
            elif branch_name.startswith("hotfix/"):
                target_branch = "main"

            if branch_name == "staging":
                _handle_release_creation(project_root, git_manager, new_version)
            elif target_branch:
                _handle_pull_request_flow(
                    project_root, git_manager, branch_name, target_branch, summary
                )
            elif branch_name.startswith(("release/", "hotfix/")):
                match = re.match(r"^(release|hotfix)\/v(\d+\.\d+\.\d+)", branch_name)
                if match and match.group(2) != new_version:
                    new_branch_name = f"{match.group(1)}/v{new_version}"
                    if _ask_user(
                        f"   ❔ You're on an old branch. Create and switch to '{new_branch_name}'?"
                    ):
                        if git_manager.create_branch(new_branch_name):
                            _write_next_command(
                                project_root, f"git checkout {new_branch_name}"
                            )
                        else:
                            print(
                                f"   ⚠️  Could not create new branch '{new_branch_name}'."
                            )

    # Final cleanup and summary
    print("\n" + "=" * 50)
    print("✅ Changelog generation process completed successfully.")


def _handle_pull_request_flow(
    project_root: Path,
    git_manager: GitManager,
    current_branch: str,
    target_branch: str,
    pr_body: str,
):
    """Guides the user through creating a Pull Request."""
    if _ask_user(f"   ❔ Create a Pull Request to '{target_branch}'?"):
        print("   ▶️  Running local CI checks...")
        if not _run_ci_checks(project_root):
            if not _ask_user("   ⚠️  CI checks failed. Do you want to proceed with the PR anyway?"):
                print("   ❌ Pull Request creation aborted by user.")
                return

        print(f"   ☁️  Pushing '{current_branch}' to remote...")
        if git_manager._run_git_command(['push', 'origin', current_branch, '--force-with-lease']):
            remote_url = git_manager.get_remote_url()
            if remote_url:
                pr_title = f"{current_branch.split('/')[0].capitalize()}: {current_branch.split('/')[1]}"
                pr_url = f"{remote_url}/compare/{target_branch}...{current_branch}?title={urllib.parse.quote(pr_title)}&body={urllib.parse.quote(pr_body)}"
                print(f"   👇 Click here to create your Pull Request:\n   {pr_url}")
                
                # The final piece of magic: switch back to the target branch.
                _write_next_command(project_root, f"git checkout {target_branch}")
        else:
            print("   ❌ Failed to push the branch to the remote repository.")


def _handle_release_creation(
    project_root: Path, git_manager: GitManager, new_version: str
):
    """Handles the CI check and creation of a release branch from staging."""
    release_branch_name = f"release/v{new_version}"
    if _ask_user(f"   ❔ Run CI checks and create release branch '{release_branch_name}'?"):
        if not _run_ci_checks(project_root):
            if not _ask_user("   ⚠️  CI checks failed. Do you want to create the release branch anyway?"):
                print("   ❌ Release branch creation aborted by user.")
                return
        
        print("   ✅ CI checks passed or were overridden by user. Proceeding with release.")
        if git_manager.create_branch(release_branch_name):
            _write_next_command(project_root, f"git checkout {release_branch_name}")
        else:
            print(f"   ⚠️  Could not create release branch '{release_branch_name}'.")


def _run_ci_checks(project_root: Path) -> bool:
    """Runs CI checks and returns True if all pass."""
    ci_script_path = project_root / "scripts" / "run_ci_checks.py"
    if not ci_script_path.exists():
        print(f"   ❌ CI script not found at {ci_script_path}")
        return False
    ci_process = subprocess.run([sys.executable, str(ci_script_path)], cwd=project_root)
    if ci_process.returncode == 0:
        print("   ✅ All CI checks passed.")
        return True
    else:
        print("   ❌ CI checks failed. Release aborted.")
        return False


def _write_next_command(project_root: Path, command: str):
    command_file_path = project_root / ".summarizer" / "next_command.sh"
    try:
        with open(command_file_path, "w") as f:
            f.write(f"{command}\n")
        print(f"   ✨ Next step command generated: {command}")
    except Exception as e:
        logger_changelog.error(f"Could not create next_command.sh file: {e}")


def _ask_user(prompt: str) -> bool:
    try:
        return input(f"{prompt} (y/n): ").lower() == "y"
    except (EOFError, KeyboardInterrupt):
        return False


def _create_initial_project_entry(json_manager, project_root: Path):
    welcome_summary = "🚀 Project initialized with Summarizer Framework."
    json_manager.add_entry(
        ai_summary=welcome_summary,
        changed_files=[],
        impact_level=ImpactLevel.LOW,
        change_type=ChangeType.CONFIG,
    )
    update_readme(project_root, None)
    print("   🎉 Project initialized successfully!")
