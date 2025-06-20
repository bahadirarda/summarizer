import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import re
import getpass
from enum import Enum

logger = logging.getLogger(__name__)

class SyncStatus(Enum):
    SYNCED = "synced"
    AHEAD = "ahead"
    BEHIND = "behind"
    DIVERGED = "diverged"

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
            if "unexpected EOF" in err_msg:
                print("   ❌ A network error occurred while communicating with GitHub.")
                print("      Please check your connection and try again.")
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
        """Commits the staged changes with the given message.."""
        success, _ = self._run_git_command(["commit", "-m", message])
        return success

    def merge_from(self, source_branch: str) -> bool:
        """Merges from a source branch into the current branch, with protection for 'main'."""
        current_branch = self.get_current_branch()
        
        # --- PASSWORD PROTECTION FOR MAIN BRANCH ---
        if current_branch == 'main':
            print(f"   ⚠️  You are about to merge changes into the '{current_branch}' branch.")
            try:
                password = getpass.getpass("      Please enter the merge authorization password: ")
                if password != "passWord!":
                    print("   ❌ Incorrect password. Merge authorization denied.")
                    return False
                print("   ✅ Password accepted. Proceeding with merge.")
            except (EOFError, KeyboardInterrupt):
                print("\n   🚫 Merge cancelled by user.")
                return False

        logger.info(f"Merging from '{source_branch}' into '{current_branch}'...")
        # Using --no-ff creates a merge commit, which is good for tracking history
        success, output = self._run_git_command(['merge', '--no-ff', '-m', f"Merge branch '{source_branch}'", source_branch])
        
        if not success:
            logger.error(f"Merge command failed. This may be due to merge conflicts. Output:\n{output}")
            print("   ❌ Merge failed. Please resolve conflicts manually and then commit.")
            # Attempt to clean up on failure
            self._run_git_command(['merge', '--abort'])
            return False
        
        logger.info(f"Successfully merged from '{source_branch}'.")
        return True

    def pull(self, branch_name: str, remote_name: str = "origin") -> bool:
        """Pulls the latest changes for a specific branch from the remote."""
        logger.info(f"Pulling latest changes for '{branch_name}' from remote '{remote_name}'...")
        
        # It's safer to checkout the branch first, then pull.
        original_branch = self.get_current_branch()
        if original_branch != branch_name:
            if not self.checkout(branch_name):
                return False # Failed to switch to the branch to be pulled

        success, output = self._run_git_command(["pull", remote_name, branch_name])
        
        if original_branch and original_branch != branch_name:
             self.checkout(original_branch) # Switch back if we changed branch

        if not success:
            logger.error(f"Failed to pull changes for '{branch_name}'. Output:\n{output}")
        
        return success

    def reset_to_remote(self, branch_name: str, remote_name: str = "origin") -> bool:
        """
        Forcefully resets the local branch to match the remote branch. 
        This is a destructive operation for local changes on that branch.
        """
        logger.info(f"Resetting local branch '{branch_name}' to '{remote_name}/{branch_name}'...")
        
        # First, fetch the latest updates
        if not self.fetch_updates(remote_name):
            return False

        # Then, perform the reset
        success, output = self._run_git_command(["reset", "--hard", f"{remote_name}/{branch_name}"])
        
        if not success:
            logger.error(f"Failed to reset branch '{branch_name}'. Output:\n{output}")

        return success

    def ensure_project_structure(self) -> bool:
        """Interactively ensures the git repository and branch structure are set up correctly on local and remote."""
        print("🔧 Checking project structure...")

        if not self.is_git_repository():
            if input("   > This project is not a Git repository. Initialize now? (y/n): ").lower() != 'y':
                print("   ⚪️ Git setup skipped. Summarizer cannot proceed without a Git repository.")
                return False
            if not self.initialize_repository():
                print("   ❌ Failed to initialize Git repository. Aborting.")
                return False
            print("   ✅ Git repository initialized.")

        existing_branches = self.get_existing_branches()
        source_branch = "main" if "main" in existing_branches else "master"

        if not source_branch in existing_branches:
             print(f"   ❌ Critical error: No '{source_branch}' branch found.")
             return False

        missing_branches = self.core_branches - set(existing_branches)
        if missing_branches:
            if input(f"   > Missing local branches: {', '.join(missing_branches)}. Create them from '{source_branch}'? (y/n): ").lower() == 'y':
                for branch in missing_branches:
                    if branch != source_branch:
                        print(f"   > Creating local branch '{branch}'...")
                        if self.create_branch(branch, from_branch=source_branch):
                            print(f"   ✅ Branch '{branch}' created.")
                        else:
                            print(f"   ❌ Failed to create branch '{branch}'.")
                            return False
            else:
                print("   ⚪️ Branch setup skipped.")
                return False

        # Now, ensure all core branches exist on the remote
        print("\n   🔎 Verifying remote branches on 'origin'...")
        pushed_any = False
        all_core_branches = self.get_existing_branches() # Re-check after creation
        for branch in self.core_branches:
            if branch in all_core_branches and not self.remote_branch_exists(branch):
                if input(f"   > Branch '{branch}' is missing on the remote. Push it now? (y/n): ").lower() == 'y':
                    print(f"   🚀 Pushing branch '{branch}' to remote...")
                    success, _ = self.push(branch)
                    if success:
                        print(f"   ✅ Branch '{branch}' pushed successfully.")
                        pushed_any = True
                    else:
                        print(f"   ❌ Failed to push branch '{branch}'.")
        
        if pushed_any:
            self.fetch_updates()

        print("✅ Project structure check complete.")
        return True

    def generate_pull_request_body(self, summary: str, gemini_client: Any) -> str:
        """Generates a professional Markdown PR body from a summary using AI."""
        default_body = f"Automated pull request based on the following summary:\n\n---\n\n{summary}"

        if not (gemini_client and gemini_client.is_ready()):
            logger.warning("Gemini client not available for PR body generation.")
            return default_body
        
        try:
            logger.info("Generating Pull Request body with AI...")
            prompt = (
                f"You are a senior software engineer writing a pull request body. Based on the following summary of changes, "
                f"generate a detailed Markdown Body. Do not include a title.\n\n"
                f"**Formatting Rules:**\n"
                f"Use Markdown. Include the following sections:\n"
                f"    - `## 📝 Summary`\n"
                f"    - `## 🚀 Changes` (use a bulleted list)\n"
                f"    - `## Impact`\n"
                f"    - `## ✅ How to Test`\n\n"
                f"**Summary of Changes:**\n```\n{summary}\n```\n\n"
                f"**Markdown Body:**"
            )
            
            body = gemini_client.generate_simple_text(prompt)
            return body.strip() if body else default_body
                
        except Exception as e:
            logger.error(f"AI PR body generation failed: {e}")
            return default_body

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
        if not self._check_gh_auth():
            return None

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

    def get_existing_pr(self, head_branch: str) -> Optional[Dict[str, Any]]:
        """
        Checks if an open PR already exists for the given head branch.
        Returns a dict with 'number', 'title', 'url' if found, otherwise None.
        """
        if not self._check_gh_auth():
            return None
        
        logger.info(f"Checking for existing PR for branch '{head_branch}'...")
        command = [
            "gh", "pr", "list",
            "--head", head_branch,
            "--state", "open",
            "--limit", "1",
            "--json", "number,title,url"
        ]
        success, output = self._run_external_command(command)
        if success and output and output.strip() != "[]":
            try:
                pr_data = json.loads(output)
                if pr_data and isinstance(pr_data, list) and all(k in pr_data[0] for k in ['number', 'title', 'url']):
                    pr_info = pr_data[0]
                    logger.info(f"Found existing PR #{pr_info['number']}: {pr_info['title']}")
                    return pr_info
            except (json.JSONDecodeError, IndexError) as e:
                logger.error(f"Failed to parse JSON from gh CLI output: {output}. Error: {e}")
                return None
        return None

    def update_pr_details(self, pr_number: int, title: str, body: str) -> bool:
        """Updates the title and body of an existing pull request."""
        logger.info(f"Updating PR #{pr_number} with new details...")
        command = [
            "gh", "pr", "edit", str(pr_number),
            "--title", title,
            "--body-file", "-" # Read body from stdin
        ]
        try:
            subprocess.run(
                command,
                input=body,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            logger.info(f"Successfully updated PR #{pr_number}.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update PR #{pr_number}. Error:\n{e.stderr.strip()}")
            return False

    def remote_branch_exists(self, branch_name: str, remote_name: str = "origin") -> bool:
        """Checks if a branch exists on the specified remote."""
        logger.info(f"Checking for branch '{branch_name}' on remote '{remote_name}'...")
        # This command returns a non-empty string if the branch exists
        success, output = self._run_git_command(["ls-remote", "--heads", remote_name, branch_name])
        return success and bool(output.strip())

    def _check_gh_auth(self) -> bool:
        """Checks if the user is authenticated with the gh CLI."""
        logger.info("Checking GitHub CLI authentication status...")
        success, output = self._run_external_command(["gh", "auth", "status"])
        if not success:
            # The error from _run_external_command is already printed.
            # We add context for the user here.
            print("   💡 To fix this, please run 'gh auth login' in your terminal.")
            return False
        
        if "Logged in to github.com" in output:
            logger.info("GitHub CLI is authenticated.")
            return True
        else:
            print("   ❌ GitHub CLI ('gh') is not authenticated.")
            print(f"      Auth status output:\n{output}")
            print("\n      Please run 'gh auth login' in your terminal and follow the prompts.")
            return False

    def get_branch_sync_status(self, branch_name: str, remote_name: str = "origin") -> Tuple[SyncStatus, int, int]:
        """
        Compares a local branch with its remote counterpart.
        Returns a SyncStatus enum and the number of ahead/behind commits.
        """
        try:
            # Ensure remote info is up-to-date
            self.fetch_updates(remote_name)
            
            remote_branch = f"{remote_name}/{branch_name}"
            # This command counts commits that are unique to each branch
            output = self._run_git_command(["rev-list", "--left-right", "--count", f"{branch_name}...{remote_branch}"])
            
            if output is None:
                # This can happen if the remote branch doesn't exist
                # Check if local branch is unpushed
                local_commits_output = self._run_git_command(["rev-list", "--count", branch_name, f"^{remote_name}/{branch_name}"])
                if local_commits_output is not None:
                    ahead_count = int(local_commits_output)
                    if ahead_count > 0:
                        return SyncStatus.AHEAD, ahead_count, 0
                return SyncStatus.SYNCED, 0, 0 # Assume synced if remote doesn't exist and local isn't ahead.

            ahead, behind = map(int, output.split())
            
            if ahead > 0 and behind > 0:
                return SyncStatus.DIVERGED, ahead, behind
            elif ahead > 0:
                return SyncStatus.AHEAD, ahead, behind
            elif behind > 0:
                return SyncStatus.BEHIND, ahead, behind
            else:
                return SyncStatus.SYNCED, 0, 0
                
        except Exception as e:
            logger.error(f"Could not get sync status for branch '{branch_name}': {e}")
            # In case of error, assume diverged to be safe
            return SyncStatus.DIVERGED, 0, 0