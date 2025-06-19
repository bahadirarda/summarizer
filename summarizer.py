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
import logging

# Import the main summarizer function
from src.main import summarizer as _summarizer

# Import feature modules
from features.parameter_checker import (
    check_required_parameters, 
    print_parameter_guidance, 
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

def get_version_codename(version):
    """Get professional codename for version"""
    try:
        major, minor = map(int, version.split('.')[:2])
        if major == 2:
            codenames = {
                0: "Genesis",      # v2.0.x - Initial v2 release
                1: "Intelligence", # v2.1.x - Enhanced AI features
                2: "Synthesis",    # v2.2.x - Integration improvements
                3: "Evolution",    # v2.3.x - Advanced evolution
                4: "Transcendence",# v2.4.x - Next level features
                5: "Infinity"      # v2.5.x - Ultimate features
            }
            return codenames.get(minor, f"Unknown-{minor}")
        elif major == 3:
            return "Quantum"   # v3.x series
        else:
            return f"Future-{major}.{minor}"
    except:
        return "Genesis"

def print_version_info():
    """Print comprehensive version information"""
    version = get_framework_version()
    codename = get_version_codename(version)
    
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


class CallableModule(ModuleType):
    """A module that can be called like a function"""

    def __call__(self, *args, **kwargs):
        """Make the module callable with parameter checking"""
        # Check required parameters first
        if not print_parameter_guidance():
            print()
            print("🔧 Run setup to configure missing parameters:")
            print("   summarizer --setup")
            return False
        
        # Pass the current working directory to the main logic
        project_root_str = str(Path.cwd())
        return _summarizer(project_root_str=project_root_str, *args, **kwargs)

    def main(self):
        """Entry point when running as script"""
        # Handle simple commands without argparse for better UX
        args = sys.argv[1:]
        
        # Handle version commands first
        if args and args[0] in ['--version', '--v', '-v', 'version']:
            print_version_info()
            return True
        
        # Handle screenshot commands
        if args and args[0] in ['screenshot', 'ss']:
            return screenshot_command(args[1:])
        
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
        # This is the main entry point for the core logic
        if print_parameter_guidance():
            # Pass the current working directory to the main logic
            project_root_str = str(Path.cwd())
            return _summarizer(project_root_str=project_root_str)
        else:
            print()
            print("🔧 Quick setup options:")
            print("   summarizer --setup    # Interactive setup.")
            print("   summarizer --gui      # GUI configuration.")
            return False


# Replace the module in sys.modules with our callable version
old_module = sys.modules[__name__]
new_module = CallableModule(__name__)

# Copy attributes from old module to new module
for attr in dir(old_module):
    if not attr.startswith('__'):
        setattr(new_module, attr, getattr(old_module, attr))

# Set the docstring
new_module.__doc__ = old_module.__doc__
new_module.__file__ = old_module.__file__

# Replace the module
sys.modules[__name__] = new_module

# Entry point for script execution
if __name__ == "__main__":
    new_module.main() 