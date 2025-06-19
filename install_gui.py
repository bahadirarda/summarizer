#!/usr/bin/env python3
"""
🎨 Summarizer Framework - Complete Installer

This script installs GUI components and sets up terminal commands
for the Summarizer Framework.
"""

import sys
from pathlib import Path


def main():
    print("🚀 Summarizer Framework - Complete Installation")
    print("=" * 50)
    print()

    try:
        # Import installation features
        from features.gui_installer import install_full_gui_package
        from features.terminal_commands import install_terminal_command

        success = True

        # Step 1: Install GUI components
        print("Step 1: Installing GUI Components")
        print("-" * 40)
        if not install_full_gui_package():
            print("⚠️  GUI installation failed, but continuing...")
            success = False

        print()

        # Step 2: Install terminal command
        print("Step 2: Installing Terminal Command")
        print("-" * 40)
        if not install_terminal_command():
            print("⚠️  Terminal command installation faied.")
            success = False

        print()

        # Final status
        if success:
            print("🎉 Installation Complete!")
            print("=" * 30)
            print()
            print("✅ You can now use:")
            print("   summarizer                    # Run basic analysis")
            print("   summarizer --setup            # Setup configuration")
            print("   summarizer --gui              # Launch GUI")
            print("   summarizer screenshot         # Screenshot analysis")
            print("   summarizer ss chrome          # App-specific screenshot")
            print()
            print("🔑 Next step: Configure your API key")
            print("   summarizer --setup")

        else:
            print("⚠️  Installation completed with some issues")
            print("   Some features may not work correctly")
            print("   Try running: python summarizer.py --help")

        return success

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct directory")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False


if __name__ == "__main__":
    main()
