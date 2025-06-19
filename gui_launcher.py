#!/usr/bin/env python3
"""
🎨 Summarizer GUI Launcher
Standalone launcher for the configuration GUI
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(
    "/Users/bahadirarda/Documents/bahadirarda96@icloud.com/project.110620251156"
)
sys.path.insert(0, str(project_root))


def main():
    try:
        # Check GUI availability
        try:
            import flet
        except ImportError:
            print(
                "❌ GUI components not installed. Please install the dependencies first."
            )
            print("   Run: python install_gui.py")
            return False

        # Import and launch GUI
        from src.gui.modern_config_gui import run_configuration_gui

        print("🎨 Launching Summarizer Configuration GUI..")
        run_configuration_gui()

    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")
    except Exception as e:
        print(f"❌ GUI error: {e}")
        return False


if __name__ == "__main__":
    main()
