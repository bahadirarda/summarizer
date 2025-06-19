import subprocess
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

class GitManager:
    """Manages Git repository structure and initialization."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.core_branches = {'main', 'develop', 'staging'}

    def _run_git_command(self, command: List[str]) -> Optional[str]:
        """Helper to run a git command and return its output."""
        try:
            process = subprocess.run(
                ['git'] + command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            return process.stdout.strip()
        except FileNotFoundError:
            logger.error("Git command not found. Please ensure Git is installed and in your system's PATH.")
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)}\nError: {e.stderr.strip()}")
            return None

    def is_git_repository(self) -> bool:
        """Check if the project is a Git repository."""
        # A more reliable check than just .git existence
        return self._run_git_command(['rev-parse', '--is-inside-work-tree']) == 'true'

    def get_existing_branches(self) -> List[str]:
        """Get a list of all local branches."""
        output = self._run_git_command(['branch'])
        if not output:
            return []
        return [b.strip().lstrip('* ') for b in output.split('\n')]

    def initialize_repository(self) -> bool:
        """Initializes a new Git repository and makes an initial commit."""
        if self._run_git_command(['init']) is None:
            return False
        
        # Create an initial commit to have a HEAD to branch from
        # Check if there are any staged files, if not, create an empty commit
        status_output = self._run_git_command(['status', '--porcelain'])
        if not self.get_existing_branches():
             # An initial commit is required to create branches
            (self.project_root / '.placeholder').touch()
            self._run_git_command(['add', '.placeholder'])
            self._run_git_command(['commit', '-m', 'Initial commit'])
            logger.info("Created an initial commit for the new repository.")
        return True

    def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> bool:
        """Creates a new branch, optionally from another branch."""
        command = ['branch', branch_name]
        if from_branch:
            command.append(from_branch)
        return self._run_git_command(command) is not None

    def switch_to_branch(self, branch_name: str) -> bool:
        """Checks out a branch. A simple alias for clarity."""
        logger.info(f"Switching to branch '{branch_name}'...")
        return self._run_git_command(['checkout', branch_name]) is not None

    def merge_from(self, source_branch: str) -> bool:
        """Merges from a source branch into the current branch."""
        logger.info(f"Merging from '{source_branch}' into current branch...")
        # Using --no-ff creates a merge commit, which is good for tracking history
        merge_output = self._run_git_command(['merge', '--no-ff', '-m', f"Merge branch '{source_branch}'", source_branch])
        
        if merge_output is None: # _run_git_command returns None on error
            logger.error(f"Merge command failed. This may be due to merge conflicts.")
            print("   ❌ Merge failed. Please resolve conflicts manually in another terminal and then commit.")
            self._run_git_command(['merge', '--abort']) # Attempt to clean up
            return False
        
        logger.info(f"Successfully merged from '{source_branch}'.")
        return True

    def ensure_project_structure(self) -> bool:
        """
        Interactively ensures the git repository and branch structure are set up correctly.
        """
        print("🔧 Checking project structure...")

        if not self.is_git_repository():
            print("⚠️ This project is not a Git repository.")
            choice = input("   > Would you like to initialize a new Git repository here? (y/n): ").lower()
            if choice == 'y':
                print("   > Initializing Git repository...")
                if not self.initialize_repository():
                    print("   ❌ Failed to initialize Git repository. Aborting.")
                    return False
                print("   ✅ Git repository initialized successfully.")
            else:
                print("   ℹ️ Git setup skipped. Summarizer cannot proceed without a Git repository.")
                return False

        # Now, check for branches
        existing_branches = self.get_existing_branches()
        
        # Determine the main branch (master or main)
        source_branch = None
        if 'main' in existing_branches:
            source_branch = 'main'
        elif 'master' in existing_branches:
            source_branch = 'master'
        
        if not source_branch:
             print("   ❌ Critical error: No 'main' or 'master' branch found after initialization.")
             return False

        missing_branches = self.core_branches - set(existing_branches)

        if missing_branches:
            print(f"⚠️ Some standard branches are missing: {', '.join(missing_branches)}")
            choice = input(f"   > Would you like to create them from '{source_branch}'? (y/n): ").lower()
            if choice == 'y':
                for branch in missing_branches:
                    if branch == source_branch: continue # Don't try to create main/master
                    print(f"   > Creating branch '{branch}'...")
                    if self.create_branch(branch, from_branch=source_branch):
                        print(f"   ✅ Branch '{branch}' created successfully.")
                    else:
                        print(f"   ❌ Failed to create branch '{branch}'.")
                        # You might want to decide if this is a fatal error
            else:
                print("   ℹ️ Branch setup skipped. Proceeding with existing structure.")
        
        print("✅ Project structure check complete.")
        return True 