#!/usr/bin/env python3
"""
🚀 Summarizer Framework - Enhanced Entry Point

This module provides multiple ways to use the summarizer:

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
        
        return _summarizer(*args, **kwargs)

    def main(self):
        """Entry point when running as script"""
        # Handle simple commands without argparse for better UX
        args = sys.argv[1:]
        
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
        
        # Check parameters and run if OK
        if print_parameter_guidance():
            return _summarizer()
        else:
            print()
            print("🔧 Quick setup options:")
            print("   summarizer --setup    # Interactive setup")
            print("   summarizer --gui      # GUI configuration")
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
