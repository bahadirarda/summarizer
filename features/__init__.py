"""
🚀 Summarizer Framework Features

This package contains modular features for the summarizer framework.
Each feature is self-contained and can be imported independently.

Available Features:
- screenshot: Screenshot capture and analysis
- terminal_commands: Terminal command utilities
- gui_installer: GUI installation helpers
- parameter_checker: Configuration validation
"""

# Import all features for easy access
from .screenshot import take_screenshot, analyze_screenshot, take_app_screenshot
from .terminal_commands import (
    install_terminal_command,
    uninstall_terminal_command,
    print_terminal_status,
)
from .gui_installer import (
    install_full_gui_package,
    launch_gui,
    print_gui_status,
)
from .parameter_checker import (
    setup_command,
    print_config_status,
    validate_config,
)
from .screenshot import (
    screenshot_command
)

__all__ = [
    'take_screenshot',
    'analyze_screenshot', 
    'take_app_screenshot',
    'install_terminal_command',
    'uninstall_terminal_command',
    'print_terminal_status',
    'install_full_gui_package',
    'launch_gui',
    'print_gui_status',
    'setup_command',
    'print_config_status',
    'validate_config',
    'screenshot_command'
]
