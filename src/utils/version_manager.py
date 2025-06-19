import json
import logging
from pathlib import Path
from typing import Optional, Tuple, Any
from datetime import datetime
import subprocess
import re
import toml

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

    def auto_increment(self, increment_type: str, gemini_client: Any = None) -> Tuple[str, str, str]:
        """
        Increments the version based on the provided type, generates a codename,
        and returns the new version, old version, and the codename.
        """
        old_version = self.get_current_version()
        new_version = self.increment_version(old_version, increment_type)
        
        # Generate codename as part of the atomic versioning step
        major, minor, _ = self.parse_version(new_version)
        codename = self._get_version_codename(major, minor, new_version, gemini_client)

        logger.info(
            f"Incrementing version: {old_version} -> {new_version} (type: {increment_type}, codename: {codename})"
        )
        return new_version, old_version, codename

    def create_git_tag(self, version: str, codename: Optional[str] = None) -> bool:
        """Create git tag for version, optionally with a codename in the message."""
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
                return False
                
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
                logger.info(f"Git tag {tag_name} created successfully with message: '{message}'")
                return True
            else:
                logger.error(f"Failed to create git tag: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating git tag: {e}")
            return False
            
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

        # Update pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    pyproject_data = toml.load(f)
                
                if 'project' in pyproject_data and 'version' in pyproject_data['project']:
                    pyproject_data['project']['version'] = new_version
                    with open(pyproject_path, "w", encoding="utf-8") as f:
                        toml.dump(pyproject_data, f)
                    logger.info(f"Successfully updated version in pyproject.toml to {new_version}")
                    updated_files.append("pyproject.toml")
                else:
                    logger.warning("Could not find '[project].version' in pyproject.toml")
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
                # Clean up the response to ensure it's a single word
                ai_codename = re.sub(r'[\s\W_]+', '', ai_codename)
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