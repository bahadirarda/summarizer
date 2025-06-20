#!/usr/bin/env python3
"""
🚀 Summarizer Framework - Enhanced Entry Point

This module provides multiple ways to use the summarizer:
# Test change for file tracking - v7.0.0

Terminal Commands:
    summarizer                    # Run basic summarizer
    summarizer --setup           # Setup configuration  
    summarizer --gui             # Launch GUI configuration
    summarizer --help            # Show help
    summarizer screenshot        # Take & analyze full screenshot
    summarizer ss               # Same as screenshot
    summarizer ss chrome        # Screenshot specific application
    summarizer ss firefox       # Screenshot Firefox browser
    summarizer ss code          # Screenshot VS Code

Python Import:
    import summarizer
    summarizer()
"""

import os
import sys
import argparse
from pathlib import Path
from types import ModuleType
from types import ModuleType

# Import the main summarizer function
from src.main import summarizer as _summarizer

# Import feature modules
from features.parameter_checker import (
    setup_command,
    print_config_status
)
from features.screenshot import screenshot_command
from features.terminal_commands import (
    install_terminal_command, 
    uninstall_terminal_command,
    print_terminal_status
)
from features.gui_installer import (
    launch_gui, 
    install_full_gui_package,
    print_gui_status
)


def get_framework_version():
    """Get current framework version from package.json"""
    try:
        import json
        package_json_path = Path(__file__).parent / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('version', '2.2.0')
        return '2.2.0'
    except Exception:
        return '2.2.0'

def print_version_info():
    """Print comprehensive version information!"""
    # Get version from VersionManager for consistency
    try:
        from src.utils.version_manager import VersionManager
        from src.core.configuration_manager import ConfigurationManager
        
        project_root = Path(__file__).parent
        config_manager = ConfigurationManager(project_root)
        version_manager = VersionManager(project_root)
        
        version_info = version_manager.get_version_info()
        version = version_info.get("version", "N/A")

        # Codename should also come from the single source of truth
        major, minor, _ = version_manager.parse_version(version)
        
        # We need a gemini_client instance to potentially generate a codename
        gemini_client = None
        if not config_manager.is_config_missing():
             from src.services.request_manager import RequestManager
             try:
                request_manager = RequestManager()
                gemini_client = request_manager.get_client("GeminiClient")
             except Exception:
                pass # It's okay if it fails here, we'll fall back.
        
        codename = version_manager._get_version_codename(major, minor, version, gemini_client)

    except ImportError:
        version = get_framework_version() # Fallback
        codename = "Unavailable"

    print("🚀 Summarizer Framework")
    print("=" * 30)
    print(f"📦 Version: {version}")
    print(f"💫 Codename: {codename}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Location: {Path(__file__).parent}")
    print()
    print("✨ Features:")
    print("   🤖 AI-Powered Analysis")
    print("   📝 Automatic Changelog Generation")
    print("   🏷️  Professional Version Management")
    print("   📊 Dynamic README Updates")
    print("   🎨 Enterprise GUI Interface")
    print("   📸 Screenshot Analysis")
    print()
    print("🔗 Repository: https://github.com/bahadirarda/summarizer")
    print("📚 Documentation: Run 'summarizer --help' for usage")


def main():
    """Entry point for script execution"""
    # Handle simple commands without argparse for better UX
    args = sys.argv[1:]
    
    # Handle version commands first
    if args and args[0] in ['--version', '--v', '-v', 'version']:
        print_version_info()
        return True
    
    # Handle screenshot commands
    if args and args[0] in ['screenshot', 'ss']:
        return screenshot_command(args[1:])
    
    # Handle merge command
    if args and args[0] == 'merge':
        from features.merge_command import merge_command
        merge_command(Path.cwd())
        return True
    
    # Handle setup and configuration commands
    if args and args[0] == '--setup':
        return setup_command()
    
    if args and args[0] == '--gui':
        return launch_gui()
    
    if args and args[0] == '--check':
        return print_config_status()
    
    if args and args[0] == '--install-gui':
        return install_full_gui_package()
    
    if args and args[0] == '--install-terminal':
        return install_terminal_command()
    
    if args and args[0] == '--uninstall-terminal':
        return uninstall_terminal_command()
    
    if args and args[0] == '--status':
        print("📊 Summarizer Framework Status")
        print("=" * 40)
        print()
        print_config_status()
        print()
        print_gui_status()
        print()
        print_terminal_status()
        return
    
    # Use argparse for help and other commands
    parser = argparse.ArgumentParser(
        description="🚀 Summarizer Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  summarizer                    # Run basic analysis
  summarizer --version          # Show version information
  summarizer --setup            # Interactive setup
  summarizer --gui              # Launch GUI configuration
  summarizer --check            # Check configuration
  summarizer screenshot         # Full screen analysis
  summarizer ss chrome          # Chrome window analysis
  summarizer merge              # Merge PR with security checks
  
  # Python usage:
  import summarizer
  summarizer()                  # Analyze current project
            """
    )
    
    parser.add_argument(
        '--setup', 
        action='store_true',
        help='Interactive setup for API keys and configuration'
    )
    
    parser.add_argument(
        '--version', '--v', '-v',
        action='store_true',
        help='Show version information and features'
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true',
        help='Launch GUI configuration interface'
    )
    
    parser.add_argument(
        '--check', 
        action='store_true',
        help='Check current configuration status'
    )
    
    parser.add_argument(
        '--install-gui', 
        action='store_true',
        help='Install GUI components'
    )
    
    parser.add_argument(
        '--install-terminal', 
        action='store_true',
        help='Install global terminal command'
    )
    
    parser.add_argument(
        '--uninstall-terminal', 
        action='store_true',
        help='Remove global terminal command'
    )
    
    parser.add_argument(
        '--status', 
        action='store_true',
        help='Show complete system status'
    )
    
    parser.add_argument(
        'command', 
        nargs='?',
        help='Command to run (screenshot, ss)'
    )
    
    parser.add_argument(
        'args', 
        nargs='*',
        help='Additional arguments for commands'
    )
    
    parsed_args = parser.parse_args()
    
    # Handle parsed arguments
    if parsed_args.setup:
        return setup_command()
    
    if parsed_args.version:
        return print_version_info()
    
    if parsed_args.gui:
        return launch_gui()
    
    if parsed_args.check:
        return print_config_status()
    
    if parsed_args.install_gui:
        return install_full_gui_package()
    
    if parsed_args.install_terminal:
        return install_terminal_command()
    
    if parsed_args.uninstall_terminal:
        return uninstall_terminal_command()
    
    if parsed_args.status:
        print("📊 Summarizer Framework Status")
        print("=" * 40)
        print()
        print_config_status()
        print()
        print_gui_status()
        print()
        print_terminal_status()
        return
    
    # Handle command argument
    if parsed_args.command in ['screenshot', 'ss']:
        return screenshot_command(parsed_args.args)
    
    # Default behavior - run summarizer
    print("🚀 Summarizer Framework")
    print("=" * 30)
    
    # The __call__ method will handle the check and execution
    return _summarizer()


# Entry point for script execution
if __name__ == "__main__":
    main()


# TODO: Her pushtan sonra otomatik olarak release boyutunda olabilecek bir güncelleme ise release olduğunu anlasın vs. geliştir kanka.
# TODO: Kişisel know-how havuzu oluşturabilmek için lazım. Ya login oluşturulmuş olacak ya da summerizer edilmiş olacak. Dökümantasyon, VSCode Extension, using style: Page -> Write just Login than snippet tarzı veri gelişi.
# BiG TODO: Summarizer Eye: bir göz gibi çalışacak, sürekli kodu analiz edecek, değişiklikleri takip edecek, yeni özellikler önericek, kodu optimize edecek. AI destekli bir göz.
# TODO:  Add to new option in context menu to run summarizer on current file or selection
# TODO: summarizer ss <comment> - screenshot with comment özelliği ekle (Commente göre yorumlasın.)
# BiG TODO: Summarizer Enter: sesli komut sistemiyle terminal kullanımı. Cihaz ile tam erişim halinde iletişime geçme konusunda ilk versiyon.
# TODO: Summarizer Updater : otomatik olarak güncellemeleri kontrol etme ve yükleme. Yeni sürüm çıktığında kullanıcıyı bilgilendir.
