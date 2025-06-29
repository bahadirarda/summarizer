import logging
from pathlib import Path

from src.config import setup_logging
from src.core.configuration_manager import ConfigurationManager
from src.services.gemini_client import GeminiClient
from src.services.request_manager import RequestManager
from src.utils.changelog_updater import update_changelog

# Attempt to import GUI, but make it optional
try:
    from src.gui.modern_config_gui import main_gui_entry as run_gui
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    def run_gui(): # Placeholder if GUI is not available
        print("GUI is not available. Please ensure all GUI dependencies are installed.")

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


def summarizer(run_gui_mode: bool = False, project_root_str: str = None):
    """Analyze and summarize current project changes or run the configuration GUI."""

    if run_gui_mode:
        if GUI_AVAILABLE:
            print("🎨 Launching Configuration GUI...")
            # Pass project_root to the GUI if provided, otherwise it will use cwd
            # The GUI's main_gui_entry should handle receiving this or using cwd.
            # For now, we assume the GUI's entry point can be called directly
            # and it will parse its own arguments if necessary or use cwd.
            # We need to ensure modern_config_gui.py's entry point is compatible.
            
            # If project_root_str is provided (e.g. from CLI args to summarizer), pass it.
            # The GUI's entry point (main_gui_entry) will need to accept this.
            if project_root_str:
                # This assumes run_gui (main_gui_entry) can accept project_root
                # We might need to adjust how arguments are passed if not.
                # For example, by setting an environment variable or modifying sys.argv
                # before calling it if it uses argparse directly without expecting a direct arg.
                
                # Simplest approach: if main_gui_entry uses argparse, it will pick up --project_root
                # if we construct sys.argv appropriately. Or, modify main_gui_entry to accept it.
                # Given the previous change to modern_config_gui.py, it should now accept --project_root.
                
                # We will call it and let its argparse handle the --project_root if present in sys.argv
                # or we can explicitly pass it if the function signature allows.
                # The updated modern_config_gui.py's main_gui_entry uses argparse.
                # So, we ensure the argument is available for it.
                
                # To be safe and explicit, let's modify sys.argv for the GUI's argparse
                import sys
                original_argv = sys.argv
                sys.argv = [sys.argv[0], "--project_root", project_root_str]
                try:
                    run_gui() # This will now use the project_root_str via its own argparse
                finally:
                    sys.argv = original_argv # Restore original sys.argv
            else:
                run_gui() # Run GUI in the context of current working directory
        else:
            print("❌ Error: GUI mode requested, but GUI components could not be loaded.")
            print("   Please check your installation and ensure all dependencies for the GUI are met.")
        return

    # Determine project_root: use provided string or default to Path.cwd()
    project_root = Path(project_root_str) if project_root_str else Path.cwd()

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
    # This part is typically for when main.py is run directly (e.g., python -m src.main)
    # The CLI entry point (summarizer.py) will call summarizer() function directly.
    
    # Basic argument parsing for direct execution (e.g., for testing GUI launch)
    import argparse
    parser = argparse.ArgumentParser(description="Summarizer main module.")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the configuration GUI."
    )
    parser.add_argument(
        "--project_root",
        type=str,
        default=None,
        help="Specify the project root directory. Defaults to current working directory if not in GUI mode."
    )
    args = parser.parse_args()

    setup_logging() # Setup logging first

    if args.gui:
        summarizer(run_gui_mode=True, project_root_str=args.project_root)
    else:
        # If not running GUI, and main.py is run directly, 
        # it implies a direct call to the summarizer logic for the specified/current project.
        summarizer(run_gui_mode=False, project_root_str=args.project_root)

# Debug comment Wed Jun 11 17:58:46 +03 2025
# Version v2.0.3 test
