import json
import logging
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime
import subprocess

logger = logging.getLogger(__name__)


class VersionManager:
    """Professional version management with semantic versioning"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.package_json_path = project_root / "package.json"
        
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
    
    def increment_version(self, increment_type: str = "patch") -> str:
        """Increment version based on type"""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)
        
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
            
        new_version = self.increment_version(increment_type)
        
        logger.info(f"Attempting to update version from {current_version_before_update} to {new_version} (type: {increment_type})")

        # Actually update the version in files
        if self.update_version_in_files(new_version):
            # If update_version_in_files was successful, new_version is now the current version
            logger.info(f"Successfully auto-incremented version: {current_version_before_update} -> {new_version} ({increment_type})")
            return new_version
        else:
            logger.error(f"Failed to update version files. Version remains {current_version_before_update}")
            return current_version_before_update # Return the version as it was before attempting update
        
    def create_git_tag(self, version: str) -> bool:
        """Create git tag for version"""
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
                
            # Create the tag
            result = subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Git tag {tag_name} created successfully")
                return True
            else:
                logger.error(f"Failed to create git tag: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating git tag: {e}")
            return False
            
    def update_version_in_files(self, new_version: str) -> bool:
        """Update version in package.json and other relevant files"""
        try:
            # Update package.json
            if not self.package_json_path.exists():
                logger.error(f"package.json not found at {self.package_json_path}")
                return False

            with open(self.package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                
            package_data['version'] = new_version
            
            with open(self.package_json_path, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Successfully updated version in package.json to {new_version}")
            return True
            
        except FileNotFoundError:
            logger.error(f"Error: package.json not found at {self.package_json_path} during update.")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding package.json: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while updating version in files: {e}")
            return False
    
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
            "codename": self._get_version_codename(major, minor)
        }
    
    def _get_version_codename(self, major: int, minor: int) -> str:
        """Get professional codename for version"""
        
        # v2.x series codenames (AI/Intelligence themed)
        v2_codenames = {
            0: "Genesis",      # v2.0.x - Initial v2 release
            1: "Intelligence", # v2.1.x - Enhanced AI features
            2: "Synthesis",    # v2.2.x - Integration improvements
            3: "Evolution",    # v2.3.x - Advanced evolution
            4: "Transcendence",# v2.4.x - Next level features
            5: "Infinity"      # v2.5.x - Ultimate features
        }
        
        if major == 2:
            return v2_codenames.get(minor, f"Unknown-{minor}")
        elif major == 3:
            return "Quantum"   # v3.x series
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