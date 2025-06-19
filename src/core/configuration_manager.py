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
import getpass


class ConfigurationManager:
    """Professional configuration management system"""

    def __init__(self, config_dir: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)

        # Paths - Use .summarizer instead of config
        if config_dir is None:
            # Determine project root based on this file's location
            # (src/core/configuration_manager.py)
            # Path(__file__) is .../src/core/configuration_manager.py
            # .parent is .../src/core/
            # .parent is .../src/
            # .parent is project_root
            project_root_path = Path(__file__).resolve().parent.parent.parent
            summarizer_dir = project_root_path / ".summarizer"
            summarizer_dir.mkdir(exist_ok=True)
            self.config_dir = summarizer_dir
            self.logger.info(
                f"ConfigurationManager using project root for config: {self.config_dir}"
            )
        else:
            self.config_dir = config_dir
            self.logger.info(
                f"ConfigurationManager using provided config_dir: {self.config_dir}"
            )

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
        """Get current value for a configuration field.
        Priority:
        1. User settings (environment_variables)
        2. User settings (custom_variables)
        3. OS Environment variables (fallback)
        """
        # First check user settings environment_variables
        env_vars = self.settings.get("environment_variables", {})
        if key in env_vars and env_vars[key] is not None:
            return env_vars[key]

        # Then check user settings custom_variables
        custom_vars = self.settings.get("custom_variables", {})
        if key in custom_vars and custom_vars[key] is not None:
            return custom_vars[key]

        # Finally check OS environment variables as a fallback
        # This is useful if the key is set directly in the shell
        # or by a parent process, and not yet in user_settings.json
        return os.getenv(key)

    def set_field_value(
            self,
            key: str,
            value: str,
            is_custom: bool = False) -> None:
        """Set value for a configuration field directly in user_settings.json.
        This will be the primary source of truth.
        """
        if is_custom:
            if "custom_variables" not in self.settings:
                self.settings["custom_variables"] = {}
            self.settings["custom_variables"][key] = value
            self.logger.info(f"Custom variable \'{key}\' set in user_settings.json")
        else:
            if "environment_variables" not in self.settings:
                self.settings["environment_variables"] = {}
            self.settings["environment_variables"][key] = value
            self.logger.info(f"Environment variable \'{key}\' set in user_settings.json")
        
        # Immediately save settings after a value is set
        self._save_settings()

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
        """Export current configuration from user_settings.json to .env file.
        The .env file serves as a secondary/fallback or for external tools.
        """
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
        """Import configuration from existing .env file into user_settings.json
        if not already set in user_settings.json. This is a one-time import.
        """
        if not self.env_file.exists():
            self.logger.info(f".env file not found at {self.env_file}, skipping import.")
            return

        try:
            load_dotenv(self.env_file) # Loads .env into os.environ

            imported_something = False
            # Get all fields from schema to know what to look for
            all_schema_fields = []
            for group in self.get_configuration_groups():
                all_schema_fields.extend(field["key"] for field in group.get("fields", []))
            
            # Add common keys like GEMINI_API_KEY if not in schema
            if "GEMINI_API_KEY" not in all_schema_fields:
                all_schema_fields.append("GEMINI_API_KEY")


            for key_from_env in os.environ: # Iterate over keys loaded by load_dotenv
                # Only import keys that are part of our schema or common known keys
                if key_from_env in all_schema_fields:
                    current_value_in_settings = self.get_field_value(key_from_env)
                    
                    # If key is not in user_settings.json (get_field_value would return from os.getenv)
                    # or if it is there but None/empty, then import from .env
                    is_in_env_vars = key_from_env in self.settings.get("environment_variables", {})
                    is_in_custom_vars = key_from_env in self.settings.get("custom_variables", {})

                    if not is_in_env_vars and not is_in_custom_vars:
                        value_from_os_env = os.getenv(key_from_env)
                        if value_from_os_env: # Ensure there's a value
                            self.set_field_value(key_from_env, value_from_os_env)
                            self.logger.info(f"Imported \'{key_from_env}\' from .env into user_settings.json")
                            imported_something = True
            
            if imported_something:
                self._save_settings() # Save if any new values were imported
                self.logger.info("Configuration imported from .env file into user_settings.json where applicable.")
            else:
                self.logger.info("No new configurations to import from .env file into user_settings.json.")

        except Exception as e:
            self.logger.error(f"Error importing from .env: {e}")

    def get_api_key(self) -> Optional[str]:
        """
        Gets the GEMINI_API_KEY, prompting the user if it's not found.
        The key is then saved for future sessions.
        """
        api_key = self.get_field_value("GEMINI_API_KEY")
        if not api_key:
            print("   🔑 GEMINI_API_KEY not found in settings or environment.")
            try:
                api_key = getpass.getpass("      Please enter it now to continue (it will be saved): ")
                if api_key and len(api_key) > 10:  # Basic validation
                    self.set_api_key(api_key)
                    print("   ✅ API Key accepted and saved for future use.")
                    return api_key
                else:
                    print("   ❌ Invalid API Key entered. Please run setup or set it manually.")
                    return None
            except (EOFError, KeyboardInterrupt):
                print("\n   🚫 API key entry cancelled.")
                return None
        return api_key

    def set_api_key(self, api_key: str) -> None:
        """Convenience method to set the GEMINI_API_KEY."""
        self.set_field_value("GEMINI_API_KEY", api_key)

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

    def _load_and_validate_config(self) -> None:
        """Loads environment variables and validates required configuration."""
        self.config = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO").upper(),
            "CHANGELOG_PATH": os.getenv("CHANGELOG_PATH", "CHANGELOG.md"),
            "PROJECT_NAME": self.project_root.name,
        }

        # Interactive prompt for missing API key
        if not self.config["GEMINI_API_KEY"]:
            try:
                # Use a password-style input to hide the key
                api_key = getpass.getpass("   🔑 GEMINI_API_KEY not found. Please enter it here to continue: ")
                if api_key and len(api_key) > 10:  # Basic validation
                    self.config["GEMINI_API_KEY"] = api_key
                    os.environ["GEMINI_API_KEY"] = api_key  # Set for the current session
                else:
                    # Add to missing_params only if input is invalid
                    self.missing_params.append("GEMINI_API_KEY")
            except (EOFError, KeyboardInterrupt):
                print("\n   🚫 API key entry cancelled.")
                self.missing_params.append("GEMINI_API_KEY")

    def _validate_config(self):
        """Validates the presence of required configuration parameters."""
        # This check is now mostly for cases where user cancels the prompt
        if not self.config.get("GEMINI_API_KEY"):
             self.missing_params.append("GEMINI_API_KEY")