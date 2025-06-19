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

from .gui_installer import check_gui_availability, install_gui_components
from .parameter_checker import (
    check_required_parameters,
    print_parameter_guidance,
    setup_command,
)

# Import all features for easy access
from .screenshot import analyze_screenshot, take_app_screenshot, take_screenshot
from .terminal_commands import create_terminal_command, install_terminal_command

__all__ = [
    "take_screenshot",
    "analyze_screenshot",
    "take_app_screenshot",
    "create_terminal_command",
    "install_terminal_command",
    "install_gui_components",
    "check_gui_availability",
    "check_required_parameters",
    "print_parameter_guidance",
    "setup_command",
]
