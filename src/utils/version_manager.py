import json
import logging
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import datetime
import subprocess
import re

logger = logging.getLogger(__name__)


class VersionManager:
    """Professional version management with semantic versioning and branch awareness"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.package_json_path = project_root / "package.json"
        
    def get_current_branch(self) -> Optional[str]:
        """Get the current git branch name."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Could not determine git branch. Is this a git repository?")
            return None

    def get_current_version(self) -> str:
        """Get current version from package.json"""
        try:
            if self.package_json_path.exists():
                with open(self.package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    return package_data.get('version', '2.0.3')
            return '2.0.3'
        except Exception as e:
            logger.error(f"Error reading version: {e}")
            return '2.0.3'
    
    def parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parse semantic version string"""
        try:
            # Remove 'v' prefix if exists
            version = version.lstrip('v')
            major, minor, patch = map(int, version.split('.'))
            return major, minor, patch
        except:
            return 2, 0, 3
    
    def format_version(self, major: int, minor: int, patch: int) -> str:
        """Format version tuple as string"""
        return f"{major}.{minor}.{patch}"
    
    def increment_version(self, current_version: str, increment_type: str = "patch") -> str:
        """Increment version based on type"""
        major, minor, patch = self.parse_version(current_version)
        
        if increment_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif increment_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
            
        return self.format_version(major, minor, patch)
    
    def auto_increment_based_on_branch(self) -> Tuple[str, str, str]:
        """
        Auto-increment version based on git branch name.
        Returns (new_version, old_version, increment_type)
        """
        current_version = self.get_current_version()
        branch_name = self.get_current_branch()

        if not branch_name:
            logger.warning("Could not determine git branch. Falling back to default patch increment.")
            new_version = self.increment_version(current_version, "patch")
            return new_version, current_version, "patch"

        logger.info(f"Analyzing version for branch: '{branch_name}'")

        increment_type = "patch" # Default
        if branch_name.startswith(('feature/', 'release/', 'hotfix/')):
            increment_type = "minor"
        elif branch_name in ["develop", "staging"]:
            increment_type = "minor"
        
        new_version = self.increment_version(current_version, increment_type)
        logger.info(f"Branch-based increment determined: '{increment_type}'. New version: {new_version}")

        return new_version, current_version, increment_type
    
    def create_git_tag(self, version: str, codename: Optional[str] = None) -> bool:
        """Create git tag for version, optionally with a codename in the message."""
        try:
            tag_name = f"v{version}"
            
            if self._run_git_command(["tag", "-l", tag_name]):
                logger.warning(f"Tag {tag_name} already exists")
                return False
                
            message = f"Release {tag_name}"
            if codename:
                message += f" - Codename: {codename}"

            result = self._run_git_command(["tag", "-a", tag_name, "-m", message], capture_output=True)
            
            if result:
                logger.info(f"Git tag {tag_name} created successfully with message: '{message}'")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error creating git tag: {e}")
            return False
            
    def update_version_in_files(self, new_version: str) -> bool:
        """Update version in package.json and other relevant files"""
        try:
            if not self.package_json_path.exists():
                logger.error(f"package.json not found at {self.package_json_path}")
                return False

            with open(self.package_json_path, 'r+', encoding='utf-8') as f:
                package_data = json.load(f)
                package_data['version'] = new_version
                f.seek(0)
                json.dump(package_data, f, indent=2, ensure_ascii=False)
                f.truncate()
                
            logger.info(f"Successfully updated version in package.json to {new_version}")
            return True
            
        except Exception as e:
            logger.error(f"An unexpected error occurred while updating version in files: {e}")
            return False
    
    def get_codename_from_git_tag(self, version: str) -> Optional[str]:
        """Checks a git tag's annotation for a codename."""
        try:
            tag_name = f"v{version}"
            output = self._run_git_command(["tag", "-n1", tag_name])
            if output:
                match = re.search(r"Codename:\s*(\S+)", output, re.IGNORECASE)
                if match:
                    codename = match.group(1)
                    logger.info(f"Found codename '{codename}' in git tag for version {version}.")
                    return codename
        except Exception as e:
            logger.error(f"Error checking git tag for codename: {e}")
        return None
    
    def _get_version_codename(self, major: int, minor: int, new_version: str, gemini_client=None) -> str:
        """
        Get a professional codename for the version.
        """
        codename = self.get_codename_from_git_tag(new_version)
        if codename:
            return codename

        if gemini_client and gemini_client.is_ready():
            try:
                logger.info(f"Generating codename with AI for version {new_version}...")
                prompt = (
                    f"Suggest a single, cool, and memorable codename for a software release with version number {new_version}. "
                    f"The codename should be a single word, in PascalCase. Examples: 'Odyssey', 'Phoenix'. "
                    f"Just return the word."
                )
                ai_codename = gemini_client.generate_simple_text(prompt)
                ai_codename = re.sub(r'[\s\W_]+', '', ai_codename)
                if ai_codename:
                    logger.info(f"AI generated codename: {ai_codename}")
                    return ai_codename
            except Exception as e:
                logger.error(f"AI codename generation failed: {e}")

        logger.info("Falling back to static codename list.")
        v2_codenames = {0: "Genesis", 1: "Intelligence", 2: "Synthesis", 3: "Evolution", 4: "Transcendence", 5: "Infinity"}
        if major == 2: return v2_codenames.get(minor, f"V{major}M{minor}")
        elif major == 3: return "Quantum"
        else: return f"Future-{major}.{minor}"

    def _run_git_command(self, command: List[str], capture_output: bool = False) -> Optional[str]:
        """Helper to run a git command."""
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Git command failed: {' '.join(command)} - {e}")
            return None

def auto_version_management(project_root: Path, changed_files: list, 
                          impact_level: str, ai_summary: str) -> Optional[str]:
    """Automatic version management workflow"""
    
    try:
        print("   🔖 Managing version automatically...")
        
        version_manager = VersionManager(project_root)
        
        # Get current version
        current_version_str = version_manager.get_current_version()
        print(f"   📋 Current version: v{current_version_str}")
        
        # auto_increment_based_on_changes attempts to update files and returns 
        # the new version string if successful, or the original version string if not.
        new_version_str = version_manager.auto_increment_based_on_changes(
            changed_files, impact_level
        )
        
        if new_version_str != current_version_str:
            # This means auto_increment_based_on_changes succeeded in determining AND applying a new version.
            # The update_version_in_files call was handled within auto_increment_based_on_changes.
            print(f"   ⬆️ Version updated: v{current_version_str} → v{new_version_str}")
            return new_version_str
        else:
            # This means either no version change was needed, 
            # or auto_increment_based_on_changes failed to update the files 
            # (it would have logged an error and returned current_version_str).
            print(f"   ✅ Version unchanged or update failed for v{current_version_str}")
            return current_version_str
            
    except Exception as e:
        print(f"   ⚠️ Version management error: {e}")
        logger.error(f"Auto version management error: {e}")
        return None