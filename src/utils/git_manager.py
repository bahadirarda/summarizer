import json
import logging
import subprocess
import re
import getpass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from ..services.gemini_client import GeminiClient
from .io import _ask_user
import sys

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
                command, cwd=self.project_root, capture_output=True, text=True, check=True, encoding="utf-8",
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

    def _run_git_command(self, command: List[str], check: bool = True, capture_output: bool = True) -> Tuple[bool, str]:
        """Run a git command and handle errors with improved logging."""
        try:
            # Setup arguments for subprocess.run
            kwargs = {
                "cwd": self.project_root,
                "text": True,
                "check": check,
            }
            if capture_output:
                kwargs['capture_output'] = True
            # When not capturing, stdout/stderr are not passed, letting them default to None, 
            # which means they inherit from the parent process (i.e., print to console).
            # This avoids the ValueError.

            process = subprocess.run(["git"] + command, **kwargs)
            
            output = process.stdout.strip() if process.stdout else ""
            return True, output
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed: git {' '.join(command)}"
            # If capture_output was false, stderr is already printed. 
            # If true, it's in e.stderr.
            stderr = e.stderr.strip() if e.stderr else "No stderr output."
            
            # More prominent error display
            print("\n" + "="*70)
            print("🚨 GIT COMMAND FAILED! 🚨".center(70))
            print("="*70)
            print(f"   🔵 Command : git {' '.join(command)}")
            print(f"   🔴 Error   : {stderr}")
            print("="*70 + "\n")
            
            logger.error(f"{error_message}\n{stderr}")
            return False, stderr
        except FileNotFoundError:
            logger.error("Git command not found. Is Git installed and in your PATH?")
            return False, "Git not found."

    def _check_gh_auth(self) -> bool:
        """Checks if the user is authenticated with the gh CLI."""
        logger.info("Checking GitHub CLI authentication status...")
        success, output = self._run_external_command(["gh", "auth", "status"])
        if not success:
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

    def get_current_branch(self) -> Optional[str]:
        success, output = self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        return output if success else None

    def push(self, branch_name: str, remote_name: str = "origin") -> Tuple[bool, str]:
        logger.info(f"Pushing '{branch_name}' to remote '{remote_name}'...")
        return self._run_git_command(["push", remote_name, branch_name])

    def force_push(self, branch_name: str, remote_name: str = "origin") -> Tuple[bool, str]:
        logger.warning(f"Force-pushing '{branch_name}' to remote '{remote_name}'...")
        return self._run_git_command(["push", "--force-with-lease", remote_name, branch_name])

    def force_push_all(self, branch_name: str, remote_name: str = "origin") -> Tuple[bool, str]:
        """Force push all local changes to remote, overwriting remote history completely"""
        logger.warning(f"Force-pushing ALL local changes for '{branch_name}' to remote '{remote_name}'...")
        return self._run_git_command(["push", "--force", remote_name, branch_name])

    def force_overwrite_target_branch(self, source_branch: str, target_branch: str, remote_name: str = "origin") -> Tuple[bool, str]:
        """EXTREMELY DANGEROUS: Force pushes the source branch to the target branch, overwriting it."""
        logger.critical(f"Executing force overwrite of '{target_branch}' with '{source_branch}' on remote '{remote_name}'!")
        return self._run_git_command(["push", "--force", remote_name, f"{source_branch}:{target_branch}"])

    def force_push_with_confirmation(self, source_branch: str, target_branch: Optional[str] = None) -> bool:
        """Asks for triple confirmation before executing a destructive push."""
        
        if target_branch:
            # This is the new, more dangerous overwrite operation
            print(f"   🚨 DANGER: You are about to overwrite '{target_branch}' with the content of '{source_branch}'.")
            print("="*60)
            if not _ask_user(f"   ❔ This will ERASE all unique history on '{target_branch}'. Are you sure?"): return False
            if not _ask_user(f"   ❔ Any work on '{target_branch}' that isn't in '{source_branch}' will be PERMANENTLY LOST. Proceed?"): return False
            if not _ask_user(f"   ❔ FINAL WARNING: Overwrite '{target_branch}'? This cannot be undone."): return False
            
            print(f"   🚀 Force overwriting '{target_branch}'...")
            success, _ = self.force_overwrite_target_branch(source_branch, target_branch)

        else:
            # This is the original, safer force push on the same branch
            print(f"   ⚠️  Force Push Warning for branch '{source_branch}'")
            print("="*60)
            if not _ask_user("   ❔ This action will overwrite the remote branch. Are you sure?"): return False
            if not _ask_user("   ❔ This can permanently delete commits made by others. Really proceed?"): return False
            if not _ask_user("   ❔ FINAL WARNING: This action cannot be undone. Confirm force push?"): return False

            print(f"   🚀 Executing force push for '{source_branch}'...")
            success, _ = self.force_push_all(source_branch)

        return success

    def is_git_repository(self) -> bool:
        success, _ = self._run_git_command(["rev-parse", "--is-inside-work-tree"])
        return success

    def get_existing_branches(self) -> List[str]:
        success, output = self._run_git_command(["branch"])
        if not success: return []
        return [b.strip().lstrip("* ") for b in output.split("\n") if b.strip()]

    def initialize_repository(self) -> bool:
        success, _ = self._run_git_command(["init"])
        if not success: return False
        if not self.get_existing_branches():
            (self.project_root / ".placeholder").touch()
            self._run_git_command(["add", ".placeholder"])
            self._run_git_command(["commit", "-m", "Initial commit"])
            logger.info("Created an initial commit for the new repository.")
        return True

    def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> bool:
        command = ["branch", branch_name]
        if from_branch: command.append(from_branch)
        success, _ = self._run_git_command(command)
        return success

    def branch_exists(self, branch_name: str) -> bool:
        success, output = self._run_git_command(["branch", "--list", branch_name])
        return success and bool(output)

    def is_working_directory_clean(self) -> bool:
        success, output = self._run_git_command(["status", "--porcelain"])
        return success and output == ""

    def stage_all(self) -> bool:
        success, _ = self._run_git_command(["add", "."])
        return success

    def unstage_all(self) -> bool:
        success, _ = self._run_git_command(["reset", "HEAD"])
        return success

    def commit(self, message: str) -> bool:
        command = ["git", "commit", "-F", "-"]
        try:
            process = subprocess.run(
                command, input=message, cwd=self.project_root, capture_output=True, text=True, check=True, encoding="utf-8",
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Commit command failed:\n{e.stderr.strip()}")
            return False

    def merge_from(self, source_branch: str) -> bool:
        current_branch = self.get_current_branch()
        if current_branch == 'main':
            try:
                password = getpass.getpass(f"   > Enter password to merge into '{current_branch}': ")
                if password != "passWord!":
                    print("   ❌ Incorrect password. Merge authorization denied.")
                    return False
            except (EOFError, KeyboardInterrupt):
                print("\n   🚫 Merge cancelled by user.")
                return False
        
        success, output = self._run_git_command(['merge', '--no-ff', '-m', f"Merge branch '{source_branch}'", source_branch])
        if not success:
            logger.error(f"Merge failed. Output:\n{output}")
            print("   ❌ Merge failed. Please resolve conflicts manually.")
            self._run_git_command(['merge', '--abort'])
            return False
        return True

    def pull(self, branch_name: str, remote_name: str = "origin") -> bool:
        logger.info(f"Pulling latest changes for '{branch_name}'...")
        original_branch = self.get_current_branch()
        if original_branch != branch_name:
            if not self.checkout(branch_name): return False
        
        success, output = self._run_git_command(["pull", remote_name, branch_name])
        
        if original_branch and original_branch != branch_name:
             self.checkout(original_branch)
        
        if not success: logger.error(f"Pull failed for '{branch_name}'. Output:\n{output}")
        return success

    def reset_to_remote(self, branch_name: str, remote_name: str = "origin") -> bool:
        logger.info(f"Resetting local '{branch_name}' to '{remote_name}/{branch_name}'...")
        if not self.fetch_updates(remote_name): return False
        success, output = self._run_git_command(["reset", "--hard", f"{remote_name}/{branch_name}"])
        if not success: logger.error(f"Reset failed for '{branch_name}'. Output:\n{output}")
        return success

    def ensure_project_structure(self) -> bool:
        print("🔧 Checking project structure...")
        if not self.is_git_repository():
            if input("   > Initialize Git repository? (y/n): ").lower() != 'y':
                return False
            if not self.initialize_repository(): return False
        
        existing_branches = self.get_existing_branches()
        source_branch = "main" if "main" in existing_branches else "master"
        if not source_branch in existing_branches: return False

        missing_branches = self.core_branches - set(existing_branches)
        if missing_branches and input(f"   > Missing local branches: {', '.join(missing_branches)}. Create? (y/n): ").lower() == 'y':
            for branch in missing_branches:
                if branch != source_branch and not self.create_branch(branch, from_branch=source_branch):
                    return False
        
        print("\n   🔎 Verifying remote branches...")
        all_core_branches = self.get_existing_branches()
        for branch in self.core_branches:
            if branch in all_core_branches and not self.remote_branch_exists(branch):
                if input(f"   > Remote branch '{branch}' is missing. Push now? (y/n): ").lower() == 'y':
                    self.push(branch)
        
        print("✅ Project structure check complete.")
        return True

    def generate_pull_request_body(self, summary: str, gemini_client: Any) -> str:
        default_body = f"Automated PR based on summary:\n\n{summary}"
        if not (gemini_client and gemini_client.is_ready()): return default_body
        try:
            prompt = (
                f"You are a senior software engineer writing a pull request body. Based on the following summary, "
                f"generate a detailed Markdown Body. Do not include a title.\n\n"
                f"**Formatting Rules:**\nUse Markdown with these sections:\n"
                f"    - `## 📝 Summary`\n    - `## 🚀 Changes`\n    - `## ✅ How to Test`\n\n"
                f"**Summary of Changes:**\n```\n{summary}\n```\n\n**Markdown Body:**"
            )
            body = gemini_client.generate_simple_text(prompt)
            return body.strip() if body else default_body
        except Exception as e:
            logger.error(f"AI PR body generation failed: {e}")
            return default_body

    def fetch_updates(self, remote_name: str = "origin") -> bool:
        success, _ = self._run_git_command(["fetch", remote_name])
        return success

    def create_pull_request(self, title: str, body: str, base_branch: str, head_branch: str) -> Optional[str]:
        if not self._check_gh_auth(): return None
        command = [
            "gh", "pr", "create", "--title", title, "--body-file", "-", "--base", base_branch, "--head", head_branch,
        ]
        try:
            process = subprocess.run(
                command, input=body, cwd=self.project_root, capture_output=True, text=True, check=True, encoding="utf-8",
            )
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            logger.error(f"PR creation failed:\n{err_msg}")
            if "No commits between" in err_msg:
                print("   ❌ No new commits found to create a Pull Request.")
            return None

    def checkout(self, branch_name: str) -> bool:
        success, _ = self._run_git_command(["checkout", branch_name])
        return success

    def get_existing_pr(self, head_branch: str) -> Optional[Dict[str, Any]]:
        if not self._check_gh_auth(): return None
        command = ["gh", "pr", "list", "--head", head_branch, "--state", "open", "--limit", "1", "--json", "number,title,url"]
        success, output = self._run_external_command(command)
        if success and output and output.strip() != "[]":
            try:
                pr_data = json.loads(output)
                return pr_data[0]
            except (json.JSONDecodeError, IndexError):
                return None
        return None

    def update_pr_details(self, pr_number: int, title: str, body: str) -> bool:
        command = ["gh", "pr", "edit", str(pr_number), "--title", title, "--body-file", "-"]
        try:
            subprocess.run(
                command, input=body, cwd=self.project_root, capture_output=True, text=True, check=True, encoding="utf-8",
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update PR #{pr_number}:\n{e.stderr.strip()}")
            return False

    def merge_pull_request(self, pr_number: int, target_branch: str = None) -> bool:
        """Merge a pull request with security check for main branch"""
        if not self._check_gh_auth(): return False
        
        # Get PR details to check target branch
        if target_branch and target_branch in ['main', 'master']:
            print("\n   🔒 SECURITY CHECK: Merging to MAIN branch!")
            print("   ⚠️  This action will deploy code to production.")
            
            import getpass
            try:
                password = getpass.getpass("   🔑 Enter admin password to merge to main: ")
                if not password:
                    print("   ❌ Merge cancelled.")
                    return False
                # Add actual password validation here if needed
            except (EOFError, KeyboardInterrupt):
                print("\n   ❌ Merge cancelled.")
                return False
        
        command = ["gh", "pr", "merge", str(pr_number), "--merge", "--delete-branch"]
        try:
            process = subprocess.run(
                command, cwd=self.project_root, capture_output=True, text=True, check=True, encoding="utf-8",
            )
            print(f"   ✅ PR #{pr_number} successfully merged!")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to merge PR #{pr_number}:\n{e.stderr.strip()}")
            return False

    def remote_branch_exists(self, branch_name: str, remote_name: str = "origin") -> bool:
        success, output = self._run_git_command(["ls-remote", "--heads", remote_name, branch_name])
        return success and bool(output.strip())

    def has_diff_between_branches(self, branch1: str, branch2: str) -> bool:
        """Check if there are differences between two branches."""
        success, output = self._run_git_command(["rev-list", "--count", f"{branch1}..{branch2}"])
        if success and output:
            try:
                count = int(output.strip())
                return count > 0
            except ValueError:
                return True
        return True  # Assume there are differences if we can't determine

    def get_branch_sync_status(self, branch_name: str, remote_name: str = "origin") -> Tuple[SyncStatus, int, int]:
        try:
            self.fetch_updates(remote_name)
            remote_branch = f"{remote_name}/{branch_name}"
            success, output = self._run_git_command(["rev-list", "--left-right", "--count", f"{branch_name}...{remote_branch}"])
            if not success:
                ahead_success, ahead_output = self._run_git_command(["rev-list", "--count", branch_name, f"^{remote_name}/{branch_name}"])
                if ahead_success and ahead_output and int(ahead_output) > 0:
                    return SyncStatus.AHEAD, int(ahead_output), 0
                return SyncStatus.SYNCED, 0, 0
            
            ahead, behind = map(int, output.split())
            if ahead > 0 and behind > 0: return SyncStatus.DIVERGED, ahead, behind
            elif ahead > 0: return SyncStatus.AHEAD, ahead, behind
            elif behind > 0: return SyncStatus.BEHIND, ahead, behind
            else: return SyncStatus.SYNCED, 0, 0
        except Exception as e:
            logger.error(f"Could not get sync status for '{branch_name}': {e}")
            return SyncStatus.DIVERGED, 0, 0

    def get_uncommitted_changes(self) -> List[str]:
        """Returns a list of files with uncommitted changes."""
        success, output = self._run_git_command(["status", "--porcelain"])
        return output.splitlines() if success and output else []

    def stash_changes(self) -> Tuple[bool, str]:
        """Stashes uncommitted changes."""
        return self._run_git_command(["stash", "push", "-m", "summarizer_autostash"])

    def stash_pop(self) -> Tuple[bool, str]:
        """Applies the last stash."""
        return self._run_git_command(["stash", "pop"])

    def delete_local_branch(self, branch_name: str) -> Tuple[bool, str]:
        """Deletes a local branch."""
        return self._run_git_command(["branch", "-D", branch_name])