import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class GitManager:
    """Manages Git repository structure, initialization, and interactions..."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.core_branches = {"main", "develop", "staging"}

    def _run_external_command(self, command: List[str]) -> Tuple[bool, str]:
        """Helper to run any external command. Returns (success, output/error string)."""
        try:
            process = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            return True, process.stdout.strip()
        except FileNotFoundError:
            tool = command[0]
            err_msg = f"Command '{tool}' not found. Please ensure it is installed and in your system's PATH."
            logger.error(err_msg)
            return False, err_msg
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            logger.error(f"Command failed: {' '.join(command)}\nError: {err_msg}")
            return False, err_msg

    def _run_git_command(self, command: List[str]) -> Tuple[bool, str]:
        """Helper to run a git command. Returns (success, output/error string)."""
        return self._run_external_command(["git"] + command)

    def has_remote(self, remote_name: str = "origin") -> bool:
        """Checks if a remote with the given name exists."""
        success, output = self._run_git_command(["remote"])
        return success and remote_name in output.split()

    def add_remote(self, remote_url: str, remote_name: str = "origin") -> bool:
        """Adds a new remote."""
        success, _ = self._run_git_command(["remote", "add", remote_name, remote_url])
        return success

    def push(self, branch_name: str, remote_name: str = "origin") -> Tuple[bool, str]:
        """Pushes a branch to the specified remote."""
        logger.info(f"Pushing '{branch_name}' to remote '{remote_name}'...")
        return self._run_git_command(["push", remote_name, branch_name, "--force-with-lease"])

    def is_git_repository(self) -> bool:
        """Check if the project is a Git repository."""
        success, _ = self._run_git_command(["rev-parse", "--is-inside-work-tree"])
        return success

    def get_existing_branches(self) -> List[str]:
        """Get a list of all local branches."""
        success, output = self._run_git_command(["branch"])
        if not success:
            return []
        return [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]

    def initialize_repository(self) -> bool:
        """Initializes a new Git repository and makes an initial commit."""
        success, _ = self._run_git_command(["init"])
        if not success:
            return False
        if not self.get_existing_branches():
            (self.project_root / ".placeholder").touch()
            self._run_git_command(["add", ".placeholder"])
            self._run_git_command(["commit", "-m", "Initial commit"])
            logger.info("Created an initial commit for the new repository.")
        return True

    def create_branch(
        self, branch_name: str, from_branch: Optional[str] = None
    ) -> bool:
        """Creates a new branch, optionally from another branch."""
        command = ["branch", branch_name]
        if from_branch:
            command.append(from_branch)
        success, _ = self._run_git_command(command)
        return success

    def branch_exists(self, branch_name: str) -> bool:
        """Checks if a branch with the given name already exists."""
        success, output = self._run_git_command(["branch", "--list", branch_name])
        return success and bool(output)

    def get_remote_url(self) -> Optional[str]:
        """Gets the GitHub repository URL from the git remote configuration."""
        success, raw_url = self._run_git_command(["config", "--get", "remote.origin.url"])
        if not success or not raw_url:
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
        success, _ = self._run_external_command(["gh", "--version"])
        if not success:
            print("   ⚠️  GitHub CLI ('gh') not found. Skipping issue check. To enable, install from: https://cli.github.com")
            return None
        
        success, issues_json = self._run_external_command(
            ["gh", "issue", "list", "--state", "open", "--json", "number,title,labels"]
        )
        if not success:
            return None
        try:
            return json.loads(issues_json)
        except json.JSONDecodeError:
            return None

    def is_working_directory_clean(self) -> bool:
        """Checks if the git working directory is clean."""
        success, output = self._run_git_command(["status", "--porcelain"])
        return success and output == ""

    def get_diff(self) -> Optional[str]:
        """Gets the diff of the current uncommitted changes."""
        success_staged, diff_staged = self._run_git_command(["diff", "--staged"])
        if success_staged and diff_staged:
            return diff_staged
        
        success_unstaged, diff_unstaged = self._run_git_command(["diff"])
        if success_unstaged and diff_unstaged:
            return diff_unstaged

        return None

    def stage_all(self) -> bool:
        """Stages all changes in the working directory."""
        success, _ = self._run_git_command(["add", "."])
        return success

    def commit(self, message: str) -> bool:
        """Commits the staged changes with the given message."""
        success, _ = self._run_git_command(["commit", "-m", message])
        return success

    def ensure_project_structure(self) -> bool:
        """Interactively ensures the git repository and branch structure are set up correctly."""
        if not self.is_git_repository():
            choice = input(
                "   > This project is not a Git repository. Initialize now? (y/n): "
            ).lower()
            if choice == "y":
                if not self.initialize_repository():
                    return False
            else:
                return False

        existing_branches = self.get_existing_branches()
        source_branch = "main" if "main" in existing_branches else "master"
        missing_branches = self.core_branches - set(existing_branches)

        if missing_branches:
            choice = input(
                f"   > Missing standard branches: {', '.join(missing_branches)}. Create them from '{source_branch}'? (y/n): "
            ).lower()
            if choice == "y":
                for branch in missing_branches:
                    if branch != source_branch:
                        self.create_branch(branch, from_branch=source_branch)
        return True
