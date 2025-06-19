import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from features.parameter_checker import check_required_parameters

# Local application imports
from src.config import setup_logging
from src.core.configuration_manager import ConfigurationManager
from src.services.gemini_client import GeminiClient
from src.services.request_manager import RequestManager
from src.utils.changelog_updater import _ask_user, update_changelog
from src.utils.git_manager import GitManager

# Attempt to import GUI, but make it optional
try:
    from src.gui.modern_config_gui import main_gui_entry as run_gui

    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

    def run_gui():  # Placeholder if GUI is not available
        print("GUI is not available. Please ensure all GUI dependencies are installed.")


logger = logging.getLogger(__name__)


def _create_branch_from_issue(
    project_root: Path, git_manager: GitManager, issue: Dict[str, Any]
):
    """Creates and switches to a new branch based on a GitHub issue."""
    issue_number = issue["number"]
    title = issue["title"]
    labels = [label["name"].lower() for label in issue["labels"]]

    branch_prefix = "feature"  # Default
    if "bug" in labels or "hotfix" in labels:
        branch_prefix = "bugfix"
    elif "documentation" in labels or "docs" in labels:
        branch_prefix = "docs"
    elif "chore" in labels or "refactor" in labels:
        branch_prefix = "chore"

    sanitized_title = re.sub(r"[^\w\s-]", "", title).strip().lower()
    sanitized_title = re.sub(r"[\s_]+", "-", sanitized_title)
    branch_name = f"{branch_prefix}/{issue_number}-{sanitized_title[:50]}"
    next_command = f"git checkout {branch_name}"

    if git_manager.branch_exists(branch_name):
        print(f"   ✅ Branch '{branch_name}' already exists.")
        if not _ask_user("   ❔ Do you want to switch to it to continue your work?"):
            print("   OK. Staying on the current branch.")
            return
    else:
        print(f"   🌿 Creating branch '{branch_name}'...")
        if not git_manager.create_branch(branch_name, from_branch="develop"):
            print(f"   ❌ Failed to create branch '{branch_name}'.")
            return

    command_file_path = project_root / ".summarizer" / "next_command.sh"
    try:
        with open(command_file_path, "w") as f:
            f.write(f"{next_command}\n")
        print(f"   ✅ Task initiated. Your shell will now switch to '{branch_name}'.")
    except Exception as e:
        print(f"   ❌ Could not create next_command.sh file: {e}")


def _handle_uncommitted_changes(project_root: Path, git_manager: GitManager) -> bool:
    """Asks the user if they want to auto-commit messy working directory."""
    print("\n" + "=" * 50)
    print("   ⚠️  Your working directory is not clean.")
    if not _ask_user(
        "   ❔ Would you like me to create an AI-powered commit for these changes?"
    ):
        print("   OK. Please commit or stash your changes before starting a new issue.")
        print("=" * 50)
        return False
    diff = git_manager.get_diff()
    if not diff:
        print("   Could not get diff of changes. Please commit manually.")
        return False
    try:
        request_manager = RequestManager()
        gemini_client = request_manager.get_client("GeminiClient")
        if not gemini_client or not gemini_client.is_ready():
            raise ValueError("Gemini client not ready.")
    except Exception as e:
        print(f"   ❌ Could not get AI client to generate commit message: {e}")
        return False
    print("   🤖 Generating commit message with AI...")
    prompt = f"Based on the following git diff, write a concise and conventional commit message. Start with a type (e.g., feat, fix, chore, docs) followed by a short description. Do not include anything else.\n\n--- DIFF ---\n{diff}"
    commit_message = gemini_client.generate_simple_text(prompt)
    print("\n" + "-" * 50)
    print("   AI Generated Commit Message:")
    print(f"   '{commit_message}'")
    print("-" * 50)
    if not _ask_user("   ❔ Do you approve this commit message?"):
        print("   Commit cancelled. Please commit manually.")
        return False
    print("    Committing changes...")
    if git_manager.stage_all() and git_manager.commit(commit_message):
        print("   ✅ Changes committed successfully.")
        return True
    else:
        print("   ❌ Failed to commit changes.")
        return False


def _handle_issue_selection(project_root: Path, git_manager: GitManager) -> bool:
    """Checks for open GitHub issues and prompts the user to work on one."""
    open_issues = git_manager.get_open_issues()
    if not open_issues:
        return False

    print("\n" + "=" * 50)
    print("🎯 Open GitHub Issues Found")
    for i, issue in enumerate(open_issues):
        labels = [label["name"] for label in issue["labels"]]
        print(f"  {i+1}. [#{issue['number']}] {issue['title']} ({', '.join(labels)})")
    print("=" * 50)
    if not _ask_user("   ❔ Found open issues. Start working on one?"):
        print("   OK. Continuing with regular summarizer flow...")
        return False

    if not git_manager.is_working_directory_clean():
        if not _handle_uncommitted_changes(project_root, git_manager):
            return True

    try:
        selection = input("   > Enter the number of the issue to start: ")
        issue_index = int(selection) - 1
        if not 0 <= issue_index < len(open_issues):
            raise ValueError
        selected_issue = open_issues[issue_index]
        _create_branch_from_issue(project_root, git_manager, selected_issue)
        return True
    except (ValueError, IndexError):
        print("   ❌ Invalid selection. Continuing with regular flow.")
        return False
    except (EOFError, KeyboardInterrupt):
        print("\n   Aborted. Continuing with regular flow.")
        return False


def setup_configuration(project_root: Path):
    """Initializes the configuration system for the specified project root."""
    summarizer_config_dir = project_root / ".summarizer"
    summarizer_config_dir.mkdir(exist_ok=True)
    config_manager = ConfigurationManager(config_dir=summarizer_config_dir)
    config_manager.import_from_env()
    return config_manager


def summarizer(run_gui_mode: bool = False, project_root_str: str = None):
    """Main entry point for the summarizer logic."""
    project_root = Path(project_root_str) if project_root_str else Path.cwd()

    # --- Setup Core Services FIRST ---
    config_manager = setup_configuration(project_root)
    RequestManager()
    GeminiClient(config_manager)

    # --- Git and Issue Workflow ---
    git_manager = GitManager(project_root)
    if not git_manager.ensure_project_structure():
        return

    if not check_required_parameters():
        return

    if _handle_issue_selection(project_root, git_manager):
        return

    # --- Main Analysis Flow ---
    # If we are here, it means user didn't select an issue, so we proceed with normal analysis
    print(f"\n🚀 Summarizer targeting project: {project_root.name} ({project_root})")
    print("✅ Core services initialized.")
    update_changelog(project_root=project_root)
    print("\n🎉 Analysis complete!")


def main():
    """Main entry for direct script execution, not used by the CLI summarizer command."""
    setup_logging()
    summarizer()


if __name__ == "__main__":
    main()
