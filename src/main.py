import logging
from pathlib import Path

from src.config import setup_logging
from src.core.configuration_manager import ConfigurationManager
from src.services.gemini_client import GeminiClient
from src.services.request_manager import RequestManager
from src.utils.changelog_updater import update_changelog

logger = logging.getLogger(__name__)


def setup_configuration():
    """Konfigürasyon sistemini başlatır."""
    config_manager = ConfigurationManager()
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


def setup_gemini_client():
    """GeminiClient servisini başlatır."""
    GeminiClient()


def setup_changelog_updater():
    """Changelog güncellemesini gerçekleştirir."""
    project_root = Path(__file__).resolve().parent.parent
    update_changelog(project_root=project_root)


def summarizer():
    """Analyze and summarize current project changes"""
    print("🔍 Summarizer Framework v2.0.0 Starting...")
    print("=" * 50)
    
    try:
        print("📝 Step 1/6: Setting up configuration...")
        setup_configuration()
        print("✅ Configuration loaded successfully")
        
        print("\n🔗 Step 2/6: Initializing request manager...")
        setup_request_manager()
        print("✅ Request manager ready")
        
        print("\n🤖 Step 3/6: Connecting to Gemini AI...")
        setup_gemini_client()
        print("✅ AI client connected")

        print("\n📁 Step 4/6: Detecting project structure...")
        # Get project root path - use current working directory if different from
        # main project
        current_dir = Path.cwd()
        main_project_root = Path(__file__).resolve().parent.parent

        # If we're in a different directory (like demo_project), use that as
        # project root
        if current_dir != main_project_root and not str(
                current_dir).startswith(str(main_project_root / "src")):
            project_root = current_dir
            print(f"📂 Working directory detected: {project_root.name}")
            print(f"   Path: {project_root}")
        else:
            project_root = main_project_root
            print(f"📂 Main project root detected: {project_root.name}")
            print(f"   Path: {project_root}")

        print("\n🔎 Step 5/6: Scanning for file changes...")
        # Update changelog with current changes
        update_changelog(project_root)
        
        print("\n✨ Step 6/6: Analysis complete!")
        print("=" * 50)
        print("📊 Results saved to:")
        print(f"   • CHANGELOG.md - Human readable format")
        print(f"   • changelog.json - Structured data format")
        print(f"   • .summarizer/ - Internal tracking files")
        print("✅ Summarizer completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("💡 Try running with debug mode for more details")

    print()


def main():
    setup_logging()
    config_manager = setup_configuration()
    setup_request_manager()
    setup_gemini_client()
    setup_changelog_updater()

    logger.info("🚀 Uygulama başarıyla başlatıldı!")
    logger.info(
        f"📁 Proje kök dizini: {Path(__file__).resolve().parent.parent}")

    # Konfigürasyon durumu logla
    config_data = config_manager.settings
    logger.info(
        f"📋 Aktif konfigürasyon: {len(config_data)} parametre yüklendi")


if __name__ == "__main__":
    main()
# Debug comment Wed Jun 11 17:58:46 +03 2025
