import logging
from pathlib import Path
import re
import sys
from typing import Dict, Any, List

# Local application imports
from src.config import setup_logging
from src.core.configuration_manager import ConfigurationManager
from src.services.gemini_client import GeminiClient
from src.services.request_manager import RequestManager
from src.utils.changelog_updater import update_changelog, _ask_user
from src.utils.git_manager import GitManager
from features.parameter_checker import check_required_parameters

# Attempt to import GUI, but make it optional
try:
    from src.gui.modern_config_gui import main_gui_entry as run_gui
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    def run_gui(): # Placeholder if GUI is not available
        print("GUI is not available. Please ensure all GUI dependencies are installed.")

logger = logging.getLogger(__name__)

def _create_branch_from_issue(project_root: Path, git_manager: GitManager, issue: Dict[str, Any]):
    """Creates and switches to a new branch based on a GitHub issue."""
    issue_number = issue['number']
    title = issue['title']
    labels = [label['name'].lower() for label in issue['labels']]

    branch_prefix = "feature" # Default
    if 'bug' in labels or 'hotfix' in labels:
        branch_prefix = 'bugfix'
    elif 'documentation' in labels or 'docs' in labels:
        branch_prefix = 'docs'
    elif 'chore' in labels or 'refactor' in labels:
        branch_prefix = 'chore'

    sanitized_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    sanitized_title = re.sub(r'[\s_]+', '-', sanitized_title)
    branch_name = f"{branch_prefix}/{issue_number}-{sanitized_title[:50]}"

    next_command = f"git checkout {branch_name}"

    if git_manager.branch_exists(branch_name):
        print(f"   ✅ Branch '{branch_name}' already exists.")
        if not _ask_user("   ❔ Do you want to switch to it to continue your work?"):
            print("   OK. Staying on the current branch.")
            return
    else:
        print(f"   🌿 Creating branch '{branch_name}'...")
        if not git_manager.create_branch(branch_name, from_branch='develop'): # Always branch from develop
             print(f"   ❌ Failed to create branch '{branch_name}'.")
             return
    
    # If we are here, we either created the branch or user wants to switch to existing one.
    command_file_path = project_root / ".summarizer" / "next_command.sh"
    try:
        with open(command_file_path, "w") as f:
            f.write(f"{next_command}\n")
        print(f"   ✅ Task initiated. Your shell will now switch to '{branch_name}'.")
    except Exception as e:
        print(f"   ❌ Could not create next_command.sh file: {e}")


def _handle_issue_selection(project_root: Path, git_manager: GitManager) -> bool:
    """Checks for open GitHub issues and prompts the user to work on one."""
    open_issues = git_manager.get_open_issues()
    if not open_issues:
        return False

    print("\n" + "="*50)
    print("🎯 Open GitHub Issues Found")
    for i, issue in enumerate(open_issues):
        labels = [label['name'] for label in issue['labels']]
        print(f"  {i+1}. [#{issue['number']}] {issue['title']} ({', '.join(labels)})")
    print("="*50)

    if not _ask_user("   ❔ Found open issues. Start working on one?"):
        print("   OK. Continuing with regular summarizer flow...")
        return False
    
    # Before creating a new branch, ensure the working directory is clean or get user's permission to commit.
    if not git_manager.is_working_directory_clean():
        if not _handle_uncommitted_changes(project_root, git_manager):
            return True # Exit the assistant flow, but don't proceed to summarizer

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

def _handle_uncommitted_changes(project_root: Path, git_manager: GitManager) -> bool:
    """Asks the user if they want to auto-commit messy working directory."""
    print("\n" + "="*50)
    print("   ⚠️  Your working directory is not clean.")
    if not _ask_user("   ❔ Would you like me to create an AI-powered commit for these changes?"):
        print("   OK. Please commit or stash your changes before starting a new issue.")
        print("="*50)
        return False

    diff = git_manager.get_diff()
    if not diff:
        print("   Could not get diff of changes. Please commit manually.")
        return False

    # We need a GeminiClient instance here.
    # We can get it through the RequestManager singleton.
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

    print("\n" + "-"*50)
    print("   AI Generated Commit Message:")
    print(f"   '{commit_message}'")
    print("-"*50)

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

    print("\n🔧 Verifying Git repository structure...")
    git_manager = GitManager(project_root)
    if not git_manager.ensure_project_structure():
        return
    print("✅ Git structure verified.")

    # --- Setup Core Services FIRST ---
    # This ensures that all managers and clients are ready before any logic runs.
    config_manager = setup_configuration(project_root)
    if not check_required_parameters():
        print("\n❌ Critical parameters are missing. Please run 'summarizer --setup' to configure them.")
        return
    RequestManager()
    GeminiClient(config_manager)
    # --- End of Core Services Setup ---


    # --- GitHub Issues Integration ---
    # Now that clients are ready, we can check for issues and use AI if needed.
    if _handle_issue_selection(project_root, git_manager):
        return 

    if run_gui_mode:
        if GUI_AVAILABLE:
            print("🎨 Launching Configuration GUI...")
            run_gui()
        else:
            print("❌ Error: GUI mode requested, but GUI components could not be loaded.")
        return

    try:
        print(f"🚀 Summarizer targeting project: {project_root.name} ({project_root})")
        
        # Core services are already initialized, we just re-state the steps for the user.
        print("📝 Step 1/7: Setting up configuration... ✅")
        print("\n🔗 Step 2/7: Initializing request manager... ✅")
        print("\n🤖 Step 3/7: Connecting to Gemini AI... ✅")

        print(f"\n📁 Step 4/7: Using project root: {project_root.name}")
        print(f"   Path: {project_root}")

        print("\n🔎 Step 5/7: Scanning for file changes...")
        update_changelog(project_root=project_root)

        print("\n✨ Step 6/7: Finalizing documentation...")
        print("   📝 README.md automatically updated with current project state")

        print("\n🎉 Step 7/7: Analysis complete!")
        print("=" * 50)
        print("📊 Results saved to:")
        print(f"   • README.md - Auto-generated project documentation")
        print(f"   • CHANGELOG.md - Human readable changelog")
        print(f"   • changelog.json - Structured data format")
        print(f"   • .summarizer/ - Internal tracking files")
        print("✅ Summarizer completed successfully!")
    except Exception as e:
        logger.error(f"An unexpected error occurred in summarizer: {e}", exc_info=True)
        print(f"\n❌ An unexpected error occurred: {e}")

def main():
    """Main entry for direct script execution, not used by the CLI summarizer command."""
    setup_logging()
    logger.info("🚀 Application (main context) started successfully!")

if __name__ == "__main__":
    setup_logging()
    # This entry is for testing or direct module execution, not the primary CLI flow.
    # The CLI flow is handled by `summarizer.py` which calls the `summarizer()` function.
    parser = argparse.ArgumentParser(description="Summarizer main module.")
    parser.add_argument("--gui", action="store_true", help="Launch the configuration GUI.")
    parser.add_argument("--project_root", type=str, default=None)
    args = parser.parse_args()

    summarizer(run_gui_mode=args.gui, project_root_str=args.project_root) 