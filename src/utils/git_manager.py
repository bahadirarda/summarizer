import subprocess
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

logger = logging.getLogger(__name__)

class GitManager:
    """Manages Git repository structure, initialization, and interactions."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.core_branches = {'main', 'develop', 'staging'}

    def _run_external_command(self, command: List[str]) -> Optional[str]:
        """Helper to run any external command and return its output."""
        try:
            process = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            return process.stdout.strip()
        except FileNotFoundError:
            tool = command[0]
            logger.error(f"Command '{tool}' not found. Please ensure it is installed and in your system's PATH.")
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}\nError: {e.stderr.strip()}")
            return None

    def _run_git_command(self, command: List[str]) -> Optional[str]:
        """Helper to run a git command and return its output."""
        return self._run_external_command(['git'] + command)

    def is_git_repository(self) -> bool:
        """Check if the project is a Git repository."""
        return self._run_git_command(['rev-parse', '--is-inside-work-tree']) == 'true'

    def get_existing_branches(self) -> List[str]:
        """Get a list of all local branches."""
        output = self._run_git_command(['branch'])
        if not output:
            return []
        return [b.strip().lstrip('* ') for b in output.split('\n')]

    def initialize_repository(self) -> bool:
        """Initializes a new Git repository and makes an initial commit."""
        if self._run_git_command(['init']) is None: return False
        if not self.get_existing_branches():
            (self.project_root / '.placeholder').touch()
            self._run_git_command(['add', '.placeholder'])
            self._run_git_command(['commit', '-m', 'Initial commit'])
            logger.info("Created an initial commit for the new repository.")
        return True

    def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> bool:
        """Creates a new branch, optionally from another branch."""
        command = ['branch', branch_name]
        if from_branch: command.append(from_branch)
        return self._run_git_command(command) is not None

    def branch_exists(self, branch_name: str) -> bool:
        """Checks if a branch with the given name already exists."""
        output = self._run_git_command(['branch', '--list', branch_name])
        return bool(output)
        
    def get_remote_url(self) -> Optional[str]:
        """Gets the GitHub repository URL from the git remote configuration."""
        raw_url = self._run_git_command(['config', '--get', 'remote.origin.url'])
        if not raw_url:
            return None
        if raw_url.startswith("git@"):
            http_url = raw_url.replace(":", "/").replace("git@", "https://")
        else:
            http_url = raw_url
        if http_url.endswith(".git"):
            http_url = http_url[:-4]
        return http_url

    def get_open_issues(self) -> Optional[List[Dict[str, Any]]]:
        """Fetches open issues from the GitHub repository using the 'gh' CLI."""
        try:
            if not self._run_external_command(['gh', '--version']):
                return None
        except Exception:
             print("   ⚠️  GitHub CLI ('gh') not found. Skipping issue check.")
             return None
        issues_json = self._run_external_command(['gh', 'issue', 'list', '--state', 'open', '--json', 'number,title,labels'])
        if issues_json is None: return None
        try:
            return json.loads(issues_json)
        except json.JSONDecodeError:
            return None

    def is_working_directory_clean(self) -> bool:
        """Checks if the git working directory is clean."""
        status_output = self._run_git_command(['status', '--porcelain'])
        return status_output == ''

    def get_diff(self) -> Optional[str]:
        """Gets the diff of the current uncommitted changes."""
        return self._run_git_command(['diff', '--staged']) or self._run_git_command(['diff'])

    def stage_all(self) -> bool:
        """Stages all changes in the working directory."""
        return self._run_git_command(['add', '.']) is not None

    def commit(self, message: str) -> bool:
        """Commits the staged changes with the given message."""
        return self._run_git_command(['commit', '-m', message]) is not None

    def ensure_project_structure(self) -> bool:
        """Interactively ensures the git repository and branch structure are set up correctly."""
        if not self.is_git_repository():
            choice = input("   > This project is not a Git repository. Initialize now? (y/n): ").lower()
            if choice == 'y':
                if not self.initialize_repository(): return False
            else:
                return False
        
        existing_branches = self.get_existing_branches()
        source_branch = 'main' if 'main' in existing_branches else 'master'
        missing_branches = self.core_branches - set(existing_branches)

        if missing_branches:
            choice = input(f"   > Missing standard branches: {', '.join(missing_branches)}. Create them from '{source_branch}'? (y/n): ").lower()
            if choice == 'y':
                for branch in missing_branches:
                    if branch != source_branch: self.create_branch(branch, from_branch=source_branch)
        return True 