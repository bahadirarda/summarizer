import json
import logging
from pathlib import Path
from typing import Optional, Tuple
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
        except subprocess.CalledProcessError as e:
            logger.error(f"Could not determine git branch. Is this a git repository? Error: {e}")
            return None
        except FileNotFoundError:
            logger.error("Git command not found. Is git installed and in PATH?")
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
    
    def get_version_from_branch(self, branch_name: str) -> Optional[str]:
        """
        Extracts version from branch name if it matches release/ or hotfix/ patterns.
        Examples: release/1.2.0-rc, hotfix/1.2.1-security-patch
        """
        # Regex to capture version like X.Y.Z from branches like 'release/X.Y.Z-...' or 'hotfix/X.Y.Z-...'
        match = re.match(r"^(release|hotfix)\/(\d+\.\d+\.\d+)", branch_name)
        if match:
            version = match.group(2)
            logger.info(f"Version '{version}' extracted directly from branch name '{branch_name}'.")
            return version
        return None

    def auto_increment_based_on_branch(self) -> Tuple[str, str, str]:
        """
        Auto-increment version based on git branch name and change impact.
        Returns (new_version, old_version, increment_type)
        """
        current_version = self.get_current_version()
        branch_name = self.get_current_branch()

        if not branch_name:
            logger.warning("Could not determine git branch. Falling back to default patch increment.")
            new_version = self.increment_version(current_version, "patch")
            return new_version, current_version, "patch"

        logger.info(f"Analyzing version for branch: '{branch_name}'")

        # Priority 1: Direct version from branch name (release/ or hotfix/)
        version_from_branch = self.get_version_from_branch(branch_name)
        if version_from_branch:
            # If the version is specified in the branch, we use it directly.
            # No further increment is needed.
            return version_from_branch, current_version, "branch"

        # Priority 2: Increment based on branch type
        increment_type = "patch" # Default
        if branch_name.startswith("feature/"):
            increment_type = "minor"
        elif branch_name.startswith("bugfix/"):
            increment_type = "patch"
        elif branch_name.startswith("chore/"):
            increment_type = "patch"
        elif branch_name in ["develop", "staging"]:
             # For integration branches, a minor bump is usually appropriate
             # as they consolidate features.
            increment_type = "minor"
        elif branch_name == "main" or branch_name == "master":
            # Changes directly to main/master are rare but should be treated as patches or hotfixes.
            # Let's default to patch, but this could be configured.
            increment_type = "patch"
        
        new_version = self.increment_version(current_version, increment_type)
        
        logger.info(f"Branch-based increment determined: '{increment_type}'. New version: {new_version}")

        return new_version, current_version, increment_type

    def auto_increment(self, increment_type: str) -> Tuple[str, str]:
        """
        Increments the version based on the provided type ('major', 'minor', 'patch').
        Returns the new version and the old version.
        """
        old_version = self.get_current_version()
        new_version = self.increment_version(old_version, increment_type)
        logger.info(
            f"Incrementing version: {old_version} -> {new_version} (type: {increment_type})"
        )
        return new_version, old_version

    def auto_increment_based_on_changes(self, changed_files: list, impact_level: str) -> str:
        """Auto-increment version based on change analysis"""
        current_version_before_update = self.get_current_version() # Get version before any changes
        
        # Analyze changes to determine increment type
        if self._has_breaking_changes(changed_files, impact_level):
            increment_type = "major"
        elif self._has_new_features(changed_files, impact_level):
            increment_type = "minor"
        else:
            increment_type = "patch"
            
        new_version = self.increment_version(current_version_before_update, increment_type)
        
        logger.info(f"Attempting to update version from {current_version_before_update} to {new_version} (type: {increment_type})")

        # Actually update the version in files
        if self.update_version_in_files(new_version):
            # If update_version_in_files was successful, new_version is now the current version
            logger.info(f"Successfully auto-incremented version: {current_version_before_update} -> {new_version} ({increment_type})")
            return new_version
        else:
            logger.error(f"Failed to update version files. Version remains {current_version_before_update}")
            return current_version_before_update # Return the version as it was before attempting update
        
    def create_git_tag(self, version: str, codename: Optional[str] = None) -> tuple[bool, str]:
        """Create git tag for version, optionally with a codename in the message.
        Returns (success, final_version_used)"""
        try:
            tag_name = f"v{version}"
            
            # Check if tag already exists
            result = subprocess.run(
                ["git", "tag", "-l", tag_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                logger.warning(f"Tag {tag_name} already exists")
                
                # Ask AI for a new version suggestion
                suggested_version = self._get_ai_version_suggestion(version)
                if suggested_version and suggested_version != version:
                    logger.info(f"AI suggested new version: {suggested_version}")
                    print(f"   🤖 AI suggests using version {suggested_version} instead of {version}")
                    
                    # Update files with the new suggested version
                    if self.update_version_in_files(suggested_version):
                        logger.info(f"Updated files with new version: {suggested_version}")
                        
                        # Try to create tag with suggested version (recursive call)
                        success, final_version = self.create_git_tag(suggested_version, codename)
                        return success, final_version
                    else:
                        logger.error("Failed to update files with suggested version")
                        return False, version
                else:
                    logger.info("No valid AI suggestion received, keeping original version")
                    return False, version
                
            # Create the tag with a message
            message = f"Release {tag_name}"
            if codename:
                message += f" - Codename: {codename}"

            result = subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", message],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Created git tag: {tag_name}")
                return True, version
            else:
                logger.error(f"Failed to create git tag: {result.stderr}")
                return False, version
                
        except Exception as e:
            logger.error(f"Error creating git tag: {e}")
            return False, version
            
    def update_version_in_files(self, new_version: str) -> bool:
        """Update version in package.json and pyproject.toml."""
        updated_files = []

        # Update package.json
        if self.package_json_path.exists():
            try:
                with open(self.package_json_path, 'r+', encoding='utf-8') as f:
                    package_data = json.load(f)
                    package_data['version'] = new_version
                    f.seek(0)
                    json.dump(package_data, f, indent=2, ensure_ascii=False)
                    f.truncate()
                logger.info(f"Successfully updated version in package.json to {new_version}")
                updated_files.append("package.json")
            except Exception as e:
                logger.error(f"Failed to update package.json: {e}")
                # Continue to try other files

        # Update pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    # Use regex to replace the version to preserve comments and formatting
                    new_content, count = re.subn(
                        r'(version\s*=\s*")[^"]+(")',
                        f'\\g<1>{new_version}\\g<2>',
                        content
                    )
                    if count > 0:
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                        logger.info(f"Successfully updated version in pyproject.toml to {new_version}")
                        updated_files.append("pyproject.toml")
                    else:
                        logger.warning("Version key not found in pyproject.toml in the expected format.")
            except Exception as e:
                logger.error(f"Failed to update pyproject.toml: {e}")
        
        return len(updated_files) > 0
    
    def get_version_info(self) -> dict:
        """Get comprehensive version information"""
        current_version = self.get_current_version()
        major, minor, patch = self.parse_version(current_version)
        
        return {
            "version": current_version,
            "version_string": f"v{current_version}",
            "major": major,
            "minor": minor,
            "patch": patch,
            "release_date": datetime.now().strftime('%Y-%m-%d'),
            "framework_name": "Summarizer Framework",
        }
    
    def get_codename_from_git_tag(self, version: str) -> Optional[str]:
        """Checks a git tag's annotation for a codename."""
        try:
            tag_name = f"v{version}"
            # Use 'git tag -n' which shows the first line of the annotation
            result = subprocess.run(
                ["git", "tag", "-n1", tag_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout:
                # Output is like "v1.2.3    Release v1.2.3 - Codename: SuperNova"
                match = re.search(r"Codename:\s*(\S+)", result.stdout, re.IGNORECASE)
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
        Priority:
        1. From existing Git tag message.
        2. From AI generation if available.
        3. From a static list as a fallback.
        """
        # 1. Check existing git tag
        codename = self.get_codename_from_git_tag(new_version)
        if codename:
            return codename

        # 2. Generate with AI if available
        if gemini_client and gemini_client.is_ready():
            try:
                logger.info(f"Generating codename with AI for version {new_version}...")
                prompt = (
                    f"You are a creative product manager. "
                    f"Suggest a single, cool, and memorable codename for a software release with version number {new_version}. "
                    f"The codename should be a single word, in PascalCase. Examples: 'Odyssey', 'Phoenix', 'QuantumLeap', 'Genesis'. "
                    f"Do not add any explanation, just return the word."
                )
                ai_codename = gemini_client.generate_simple_text(prompt)
                if ai_codename:
                    logger.info(f"AI generated codename: {ai_codename}")
                    return ai_codename
            except Exception as e:
                logger.error(f"AI codename generation failed: {e}")

        # 3. Fallback to static list
        logger.info("Falling back to static codename list.")
        v2_codenames = {
            0: "Genesis", 1: "Intelligence", 2: "Synthesis",
            3: "Evolution", 4: "Transcendence", 5: "Infinity"
        }
        
        if major == 2:
            return v2_codenames.get(minor, f"V{major}M{minor}")
        elif major == 3:
            return "Quantum"
        else:
            return f"Future-{major}.{minor}"
    
    def _has_breaking_changes(self, changed_files: list, impact_level: str) -> bool:
        """Detect breaking changes"""
        
        # Critical impact usually means breaking changes
        if impact_level.lower() == "critical":
            return True
            
        # Check for breaking change indicators in files
        breaking_indicators = [
            "main.py",  # Main entry point changes
            "config.py",  # Configuration changes
            "__init__.py",  # Package structure changes
            "requirements.txt",  # Dependency changes
        ]
        
        return any(any(indicator in file for indicator in breaking_indicators) 
                  for file in changed_files)
    
    def _has_new_features(self, changed_files: list, impact_level: str) -> bool:
        """Detect new features"""
        
        # High impact often means new features
        if impact_level.lower() in ["high", "critical"]:
            return True
            
        # Check for feature indicators
        feature_indicators = [
            "feature",
            "new_",
            "add_",
            "gui/",
            "services/",
            "utils/",
        ]
        
        return any(any(indicator in file.lower() for indicator in feature_indicators) 
                  for file in changed_files)

    def _get_ai_version_suggestion(self, existing_version: str) -> Optional[str]:
        """Get AI suggestion for new version when tag already exists"""
        try:
            # Try to get AI client
            from src.core.configuration_manager import ConfigurationManager
            from src.services.gemini_client import GeminiClient
            
            config_manager = ConfigurationManager()
            if not config_manager.get_api_key():
                logger.info("No AI client available for version suggestion")
                return None
                
            gemini_client = GeminiClient(config_manager)
            if not gemini_client.is_ready():
                logger.info("AI client not ready for version suggestion")
                return None

            # Gather project context
            current_branch = self.get_current_branch()
            current_version = self.get_current_version()
            
            # Get existing tags for context
            existing_tags = self._get_existing_tags()
            
            # Get recent commits for context
            recent_commits = self._get_recent_commits()
            
            prompt = f"""
You are a semantic versioning expert. Analyze the Git tags and suggest the next logical version number.

**CURRENT SITUATION:**
- Attempted version: {existing_version} (CONFLICTS with existing tag)
- Current branch: {current_branch}
- Branch type: {self._analyze_branch_type(current_branch)}

**ALL EXISTING TAGS (sorted by version):**
{existing_tags}

**YOUR TASK:**
1. Find the HIGHEST version number from the existing tags above
2. Based on the branch type, increment appropriately:
   - Feature branch (feature/*): increment MINOR version
   - Hotfix branch (hotfix/*): increment PATCH version  
   - Release branch (release/*): use branch version or increment MINOR
   - Main branch: increment PATCH version

**EXAMPLES:**
- If highest existing tag is v8.25.0 and branch is feature/*: suggest 8.26.0
- If highest existing tag is v8.25.0 and branch is hotfix/*: suggest 8.25.1
- If highest existing tag is v8.25.0 and branch is main: suggest 8.25.1

**CRITICAL:** Look at the tag list, find the HIGHEST version number, then increment it.

**OUTPUT:** Return ONLY the version number (e.g., "8.26.0"). No explanations."""
            
            response = gemini_client.generate_simple_text(prompt)
            
            # Extract version from response
            if response:
                # Look for version pattern X.Y.Z
                import re
                version_match = re.search(r'\b(\d+\.\d+\.\d+)\b', response)
                if version_match:
                    suggested_version = version_match.group(1)
                    logger.info(f"AI suggested version: {suggested_version}")
                    return suggested_version
            
            logger.warning("Could not extract valid version from AI response")
            return None
            
        except Exception as e:
            logger.error(f"Error getting AI version suggestion: {e}")
            return None

    def _get_existing_tags(self) -> str:
        """Get list of existing git tags for context"""
        try:
            result = subprocess.run(
                ["git", "tag", "--sort=-version:refname"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                tags = result.stdout.strip().split('\n')[:10]  # Last 10 tags
                return '\n'.join(f"  - {tag}" for tag in tags if tag)
            return "  - No tags found"
            
        except Exception as e:
            logger.error(f"Error getting existing tags: {e}")
            return "  - Error reading tags"

    def _get_recent_commits(self) -> str:
        """Get recent commit messages for context"""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                return '\n'.join(f"  - {commit}" for commit in commits if commit)
            return "  - No commits found"
            
        except Exception as e:
            logger.error(f"Error getting recent commits: {e}")
            return "  - Error reading commits"

    def _analyze_branch_type(self, branch_name: Optional[str]) -> str:
        """Analyze branch type for AI context"""
        if not branch_name:
            return "unknown"
        
        if branch_name.startswith("feature/"):
            return "feature"
        elif branch_name.startswith("hotfix/"):
            return "hotfix"
        elif branch_name.startswith("release/"):
            return "release"
        elif branch_name.startswith("bugfix/"):
            return "bugfix"
        elif branch_name in ["main", "master"]:
            return "main"
        elif branch_name == "develop":
            return "develop"
        else:
            return "other"