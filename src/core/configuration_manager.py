"""
Professional Configuration Manager
Dynamic configuration system with JSON schema support
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import logging


class ConfigurationManager:
    """Professional configuration management system"""

    def __init__(self, config_dir: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)

        # Paths
        self.config_dir = config_dir or Path.cwd() / "config"
        self.schema_file = self.config_dir / "configuration_schema.json"
        self.settings_file = self.config_dir / "user_settings.json"
        self.env_file = Path.cwd() / ".env"

        # Data
        self.schema: Dict[str, Any] = {}
        self.settings: Dict[str, Any] = {}

        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)

        # Load configurations
        self._load_schema()
        self._load_settings()

    def _load_schema(self) -> None:
        """Load configuration schema from JSON file"""
        try:
            if self.schema_file.exists():
                with open(self.schema_file, "r", encoding="utf-8") as f:
                    self.schema = json.load(f)
                self.logger.info("Configuration schema loaded successfully")
            else:
                self.logger.warning(
                    f"Schema file not found: {self.schema_file}")
                self.schema = {"configuration_groups": [], "profiles": {}}
        except Exception as e:
            self.logger.error(f"Error loading schema: {e}")
            self.schema = {"configuration_groups": [], "profiles": {}}

    def _load_settings(self) -> None:
        """Load user settings from JSON file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
                self.logger.info("User settings loaded successfully")
            else:
                # Create default settings
                self.settings = {
                    "user_settings": {
                        "last_modified": datetime.now().isoformat(),
                        "created_by": "Configuration Manager v1.0",
                        "profile": "development",
                    },
                    "environment_variables": {},
                    "custom_variables": {},
                    "backup_count": 5,
                    "export_format": "env",
                }
                self._save_settings()
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            self.settings = {}

    def _save_settings(self) -> None:
        """Save user settings to JSON file"""
        try:
            self.settings["user_settings"]["last_modified"] = datetime.now(
            ).isoformat()
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            self.logger.info("User settings saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")

    def get_configuration_groups(self) -> List[Dict[str, Any]]:
        """Get all configuration groups from schema"""
        return self.schema.get("configuration_groups", [])

    def get_field_value(self, key: str) -> Optional[str]:
        """Get current value for a configuration field"""
        # First check user settings
        env_vars = self.settings.get("environment_variables", {})
        if key in env_vars:
            return env_vars[key]

        # Then check custom variables
        custom_vars = self.settings.get("custom_variables", {})
        if key in custom_vars:
            return custom_vars[key]

        # Finally check environment variables
        return os.getenv(key)

    def set_field_value(
            self,
            key: str,
            value: str,
            is_custom: bool = False) -> None:
        """Set value for a configuration field"""
        if is_custom:
            if "custom_variables" not in self.settings:
                self.settings["custom_variables"] = {}
            self.settings["custom_variables"][key] = value
        else:
            if "environment_variables" not in self.settings:
                self.settings["environment_variables"] = {}
            self.settings["environment_variables"][key] = value

    def validate_field(
        self, field_config: Dict[str, Any], value: str
    ) -> tuple[bool, str]:
        """Validate field value against schema rules"""
        field_type = field_config.get("type", "text")
        validation = field_config.get("validation", {})
        required = field_config.get("required", False)

        # Check if required and empty
        if required and not value.strip():
            return False, f"Field '{field_config.get('label', 'Unknown')}' is required"

        # Skip validation if empty and not required
        if not value.strip() and not required:
            return True, ""

        # Type-specific validation
        if field_type == "number":
            try:
                num_value = float(value)
                if "min" in validation and num_value < validation["min"]:
                    return False, f"Value must be at least {validation['min']}"
                if "max" in validation and num_value > validation["max"]:
                    return False, f"Value must be at most {validation['max']}"
            except ValueError:
                return False, "Value must be a valid number"

        elif field_type in ["text", "password"]:
            if "min_length" in validation and len(value) < validation["min_length"]:
                return (
                    False, f"Value must be at least {validation['min_length']} characters",
                )
            if "max_length" in validation and len(value) > validation["max_length"]:
                return (
                    False, f"Value must be at most {validation['max_length']} characters",
                )
            if "pattern" in validation:
                if not re.match(validation["pattern"], value):
                    return False, "Value format is invalid"

        return True, ""

    def apply_profile(self, profile_name: str) -> bool:
        """Apply a predefined configuration profile"""
        profiles = self.schema.get("profiles", {})
        if profile_name not in profiles:
            return False

        profile = profiles[profile_name]
        profile_values = profile.get("values", {})

        for key, value in profile_values.items():
            self.set_field_value(key, value)

        self.settings["user_settings"]["profile"] = profile_name
        return True

    def export_to_env(self) -> None:
        """Export current configuration to .env file"""
        try:
            # Create new .env content
            new_lines = [
                "# Environment Configuration\n",
                f"# Generated by Configuration Manager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                "# DO NOT EDIT MANUALLY - Use Configuration Manager\n",
                "\n",
            ]

            # Add environment variables
            env_vars = self.settings.get("environment_variables", {})
            if env_vars:
                new_lines.append("# Application Environment Variables\n")
                for key, value in env_vars.items():
                    if value:  # Only export non-empty values
                        new_lines.append(f"{key}={value}\n")
                new_lines.append("\n")

            # Add custom variables
            custom_vars = self.settings.get("custom_variables", {})
            if custom_vars:
                new_lines.append("# Custom Variables\n")
                for key, value in custom_vars.items():
                    if value:  # Only export non-empty values
                        new_lines.append(f"{key}={value}\n")

            # Write to file
            with open(self.env_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            self.logger.info(f"Configuration exported to {self.env_file}")

        except Exception as e:
            self.logger.error(f"Error exporting to .env: {e}")
            raise

    def import_from_env(self) -> None:
        """Import configuration from existing .env file"""
        if not self.env_file.exists():
            return

        try:
            load_dotenv(self.env_file)

            # Get all fields from schema
            all_fields = []
            for group in self.get_configuration_groups():
                all_fields.extend(group.get("fields", []))

            # Import known fields
            env_vars = {}
            for field in all_fields:
                key = field["key"]
                value = os.getenv(key)
                if value:
                    env_vars[key] = value

            if env_vars:
                self.settings["environment_variables"] = env_vars
                self._save_settings()
                self.logger.info("Configuration imported from .env file")

        except Exception as e:
            self.logger.error(f"Error importing from .env: {e}")

    def save_configuration(self) -> None:
        """Save current configuration"""
        try:
            self._save_settings()
            self.export_to_env()
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            raise

    def get_profiles(self) -> Dict[str, Any]:
        """Get available configuration profiles"""
        return self.schema.get("profiles", {})

    def get_current_profile(self) -> str:
        """Get currently active profile"""
        return self.settings.get(
            "user_settings",
            {}).get(
            "profile",
            "development")

    def add_custom_field(
            self,
            key: str,
            value: str,
            description: str = "") -> None:
        """Add a custom configuration field"""
        if "custom_variables" not in self.settings:
            self.settings["custom_variables"] = {}

        self.settings["custom_variables"][key] = value

        # You could extend this to store metadata about custom fields
        # in a separate structure if needed

    def remove_custom_field(self, key: str) -> bool:
        """Remove a custom configuration field"""
        custom_vars = self.settings.get("custom_variables", {})
        if key in custom_vars:
            del custom_vars[key]
            return True
        return False
