import logging
from pathlib import Path

from src.config import setup_logging
from src.core.configuration_manager import ConfigurationManager
from src.services.gemini_client import GeminiClient
from src.services.request_manager import RequestManager
from src.utils.changelog_updater import update_changelog

logger = logging.getLogger(__name__)


def setup_configuration(project_root: Path):  # Added project_root parameter
    """Konfigürasyon sistemini başlatır ve belirtilen proje kökünü kullanır."""
    # ConfigurationManager'ı proje kökündeki .summarizer diziniyle başlat
    summarizer_config_dir = project_root / ".summarizer"
    summarizer_config_dir.mkdir(exist_ok=True)  # Ensure .summarizer directory exists

    config_manager = ConfigurationManager(config_dir=summarizer_config_dir)
    # Attempt to import from .env on initial setup if settings are sparse
    config_manager.import_from_env()
    config_data = config_manager.settings

    # Konfigürasyon verilerini environment'a yükle
    import os

    # Load environment variables
    env_vars = config_data.get("environment_variables", {})
    for key, value in env_vars.items():
        if value:  # Only set non-empty values
            os.environ[str(key)] = str(value)

    # Load custom variables
    custom_vars = config_data.get("custom_variables", {})
    for key, value in custom_vars.items():
        if value:  # Only set non-empty values
            os.environ[str(key)] = str(value)

    logger.info(
        f"Konfigürasyon sistemi başlatıldı. "
        f"{len(env_vars)} environment ve "
        f"{len(custom_vars)} özel değişken yüklendi."
    )
    return config_manager


def setup_request_manager():
    """RequestManager servisini başlatır."""
    RequestManager()


def setup_gemini_client(config_manager: ConfigurationManager):  # Added config_manager parameter
    """GeminiClient servisini başlatır."""
    GeminiClient(config_manager=config_manager)  # Pass config_manager


def setup_changelog_updater(project_root: Path):  # Added project_root parameter
    """Changelog güncellemesini gerçekleştirir."""
    update_changelog(project_root=project_root)


def summarizer():
    """Analyze and summarize current project changes based on the current working directory."""
    # Version display is handled by the entry point script (summarizer.py)

    project_root = Path.cwd()

    # Validate if project_root is a valid project directory
    # (e.g., contains package.json or .git)
    # This is a basic check; more sophisticated checks can be added if needed.
    if not (project_root / "package.json").exists() and \
       not (project_root / ".git").is_dir() and \
       not (project_root / ".summarizer").is_dir(): # Also check for existing .summarizer
        print(f"❌ Error: The current directory ({project_root}) does not appear to be a valid project.")
        print("   Please run 'summarizer' from the root directory of your project.")
        print("   A project should typically contain a 'package.json' file or a '.git' directory.")
        return

    try:
        print(f"🚀 Summarizer targeting project: {project_root.name} ({project_root})")
        print("📝 Step 1/7: Setting up configuration...")
        config_manager = setup_configuration(project_root)  # Pass determined project_root
        print("✅ Configuration loaded successfully")

        print("\n🔗 Step 2/7: Initializing request manager...")
        setup_request_manager()
        print("✅ Request manager ready")

        print("\n🤖 Step 3/7: Connecting to Gemini AI...")
        setup_gemini_client(config_manager)  # Pass config_manager
        print("✅ AI client connected")

        # project_root is already determined as Path.cwd()
        print(f"\n📁 Step 4/7: Using project root: {project_root.name}")
        print(f"   Path: {project_root}")

        print("\n🔎 Step 5/7: Scanning for file changes...")
        # Update changelog with current changes, using the determined project_root
        setup_changelog_updater(project_root) # Pass determined project_root

        print("\n✨ Step 6/7: Finalizing documentation...")
        print("   📝 README.md automatically updated with current project state")

        print("\n🎉 Step 7/7: Analysis complete!")
        print("=" * 50)
        print("📊 Results saved to:")
        print(f"   • README.md - Auto-generated project documentation")
        print(f"   • CHANGELOG.md - Human readable changelog")
        print(f"   • changelog.json - Structured data format")
        print(f"   • .summarizer/ - Internal tracking files")
        print("✅ Summarizer completed successfully!")
        print(f"   • .summarizer/ - Internal tracking files")
        print("✅ Summarizer completed successfully!")

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("💡 Try running with debug mode for more details")

    print()


def main():
    setup_logging()

    # Determine project_root for main execution context (e.g. if module is run directly)
    # However, for the 'summarizer' command, project_root is Path.cwd()
    # This main() function might be for a different purpose (e.g. API server setup)
    # For now, let's assume it uses its own installation's config if run directly.
    # If main() is part of the CLI flow, it needs consistent project_root handling.
    # For the purpose of the `summarizer` CLI command, `summarizer()` function is the key entry.

    # If this main() is for a global/non-project-specific context:
    script_installation_root = Path(__file__).resolve().parent.parent
    config_manager_for_main = setup_configuration(script_installation_root) # or ConfigurationManager() for default

    setup_request_manager()
    setup_gemini_client(config_manager=config_manager_for_main)
    # setup_changelog_updater(script_installation_root) # This might not make sense here

    logger.info("🚀 Uygulama (main context) başarıyla başlatıldı!")
    logger.info(
        f"📁 Betik kurulum kök dizini: {script_installation_root}")

    # Konfigürasyon durumu logla
    config_data = config_manager_for_main.settings
    logger.info(
        f"📋 Aktif konfigürasyon: {len(config_data)} parametre yüklendi")


if __name__ == "__main__":
    main()
# Debug comment Wed Jun 11 17:58:46 +03 2025
# Version v2.0.3 test
