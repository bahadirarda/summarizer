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

    def get_current_branch(self) -> Optional[str]:
        """Get the current git branch name."""
        success, output = self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        if success:
            return output
        return None

    def push(self, branch_name: str, remote_name: str = "origin") -> Tuple[bool, str]:
        """Pushes a branch to the specified remote."""
        logger.info(f"Pushing '{branch_name}' to remote '{remote_name}'...")
        return self._run_git_command(["push", remote_name, branch_name, "--force-with-lease"])

    def has_remote(self, remote_name: str = "origin") -> bool:
        """Checks if a remote with the given name exists."""
        success, output = self._run_git_command(["remote"])
        return success and remote_name in output.split()

    def add_remote(self, remote_url: str, remote_name: str = "origin") -> bool:
        """Adds a new remote."""
        success, _ = self._run_git_command(["remote", "add", remote_name, remote_url])
        return success

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

    def has_diff_between_branches(self, base_branch: str, head_branch: str) -> bool:
        """Checks if there is a diff between two branches."""
        try:
            # Use --quiet to just get the exit code. 1 means diff exists, 0 means no diff.
            subprocess.run(
                ["git", "diff", "--quiet", f"{base_branch}..{head_branch}"],
                cwd=self.project_root,
                check=True,
                capture_output=True,
            )
            # If check=True doesn't raise an exception, it means exit code was 0 (no diff)
            return False
        except subprocess.CalledProcessError:
            # Exit code was non-zero, meaning a diff exists.
            return True
        except Exception as e:
            logger.error(f"Error checking diff between branches: {e}")
            return False # Assume no diff on other errors

    def stage_all(self) -> bool:
        """Stages all changes in the working directory.."""
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

    def generate_pull_request_details(self, summary: str, gemini_client: Any) -> Tuple[str, str]:
        """Generates a professional PR title and body from a summary using AI."""
        # Default values
        default_title = "chore: Update project based on recent changes"
        default_body = f"Automated pull request based on the following summary:\n\n---\n\n{summary}"

        if not (gemini_client and gemini_client.is_ready()):
            logger.warning("Gemini client not available for PR details generation.")
            return default_title, default_body
        
        try:
            logger.info("Generating Pull Request details with AI...")
            prompt = (
                f"You are a senior software engineer creating a pull request. Based on the following summary of changes, "
                f"generate a professional Pull Request Title and a detailed Markdown Body.\n\n"
                f"**Formatting Rules:**\n"
                f"1.  **Title:** Use conventional commit format (e.g., 'feat: ...', 'fix: ...', 'chore: ...').\n"
                f"2.  **Body:** Use Markdown. Include the following sections:\n"
                f"    - `## 📝 Summary`\n"
                f"    - `## 🚀 Changes` (use a bulleted list)\n"
                f"    - `## Impact`\n"
                f"    - `## ✅ How to Test`\n\n"
                f"**Summary of Changes:**\n```\n{summary}\n```\n\n"
                f"**Output Format (use '---' as a separator):**\n"
                f"TITLE\n"
                f"---\n"
                f"BODY"
            )
            
            response = gemini_client.generate_simple_text(prompt)
            
            if "---" in response:
                title, body = response.split("---", 1)
                return title.strip(), body.strip()
            else:
                logger.warning("AI response for PR details was not in the expected format.")
                return default_title, response # Return the full response as body
                
        except Exception as e:
            logger.error(f"AI PR detail generation failed: {e}")
            return default_title, default_body

    def fetch_updates(self, remote_name: str = "origin") -> bool:
        """Fetches the latest updates from the remote repository."""
        logger.info(f"Fetching latest updates from remote '{remote_name}'...")
        success, output = self._run_git_command(["fetch", remote_name])
        if not success:
            logger.error(f"Failed to fetch updates from remote. Output:\n{output}")
        return success

    def create_pull_request(
        self, title: str, body: str, base_branch: str, head_branch: str
    ) -> Optional[str]:
        """Creates a pull request on GitHub using the 'gh' CLI and returns the PR URL."""
        success, _ = self._run_external_command(["gh", "--version"])
        if not success:
            print("   ⚠️  GitHub CLI ('gh') not found. Cannot create pull request automatically.")
            print("   To enable, install from: https://cli.github.com")
            return None

        command = [
            "gh", "pr", "create",
            "--title", title,
            "--body-file", "-",  # Read body from stdin
            "--base", base_branch,
            "--head", head_branch,
        ]
        
        try:
            # Use subprocess.run directly to pass the body via stdin
            process = subprocess.run(
                command,
                input=body,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            logger.error(f"Failed to create pull request. Raw output:\n{err_msg}")
            # Provide more specific feedback if possible
            if "No commits between" in err_msg:
                print("   ❌ No new commits found to create a Pull Request.")
            return None

    def checkout(self, branch_name: str) -> bool:
        """Checks out the specified branch."""
        success, _ = self._run_git_command(["checkout", branch_name])
        return success

    def remote_branch_exists(self, branch_name: str, remote_name: str = "origin") -> bool:
        """Checks if a branch exists on the specified remote."""
        logger.info(f"Checking for branch '{branch_name}' on remote '{remote_name}'...")
        # This command returns a non-empty string if the branch exists
        output = self._run_git_command(["ls-remote", "--heads", remote_name, branch_name])
        return output is not None and bool(output.strip())