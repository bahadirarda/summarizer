"""
🎨 GUI Installer Feature

This module provides GUI component installation and management.
Handles flet GUI dependencies and configuration interface.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_gui_availability():
    """Check if GUI components are available"""
    try:
        import flet
        return True
    except ImportError:
        return False


def install_gui_components():
    """Install GUI components (flet and dependencies)"""
    print("🎨 Installing GUI Components")
    print("=" * 35)
    
    required_packages = [
        "flet>=0.10.0",
        "flet-core>=0.10.0"
    ]
    
    print("📦 Installing required packages:")
    for package in required_packages:
        print(f"   • {package}")
    
    try:
        # Install packages
        cmd = [sys.executable, "-m", "pip", "install"] + required_packages
        
        print("\n⏳ Installing...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ GUI components installed successfully!")
            
            # Test import
            try:
                import flet
                print("✅ GUI components are working!")
                return True
            except ImportError as e:
                print(f"❌ GUI import test failed: {e}")
                return False
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False


def launch_gui():
    """Launch the GUI configuration interface"""
    print("🎨 Launching GUI Configuration")
    print("=" * 40)
    
    if not check_gui_availability():
        print("❌ GUI components not available")
        print("   Run: summarizer --install-gui")
        return False
    
    try:
        # Import and run GUI
        import sys
        from pathlib import Path
        
        # Add project root to path if not already there
        project_root = Path(__file__).parent.parent.absolute()
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from src.gui.modern_config_gui import run_configuration_gui
        
        print("🚀 Starting GUI...")
        run_configuration_gui()
        return True
        
    except ImportError as e:
        print(f"❌ GUI import failed: {e}")
        print("   The GUI module may need to be updated")
        return False
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        return False


def create_gui_launcher():
    """Create a standalone GUI launcher script"""
    project_root = Path(__file__).parent.parent.absolute()
    
    launcher_content = f'''#!/usr/bin/env python3
"""
🎨 Summarizer GUI Launcher
Standalone launcher for the configuration GUI
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path("{project_root}")
sys.path.insert(0, str(project_root))

def main():
    try:
        # Check GUI availability
        try:
            import flet
        except ImportError:
            print("❌ GUI components not installed")
            print("   Run: python install_gui.py")
            return False
        
        # Import and launch GUI
        from src.gui.modern_config_gui import run_configuration_gui
        
        print("🎨 Launching Summarizer Configuration GUI...")
        run_configuration_gui()
        
    except KeyboardInterrupt:
        print("\\n👋 GUI closed by user")
    except Exception as e:
        print(f"❌ GUI error: {{e}}")
        return False

if __name__ == "__main__":
    main()
'''
    
    launcher_path = project_root / "gui_launcher.py"
    
    try:
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        # Make executable on Unix-like systems
        if sys.platform != "win32":
            import stat
            launcher_path.chmod(launcher_path.stat().st_mode | stat.S_IEXEC)
        
        print(f"✅ GUI launcher created: {launcher_path}")
        return str(launcher_path)
    
    except Exception as e:
        print(f"❌ Failed to create GUI launcher: {e}")
        return None


def update_gui_components():
    """Update GUI components to latest version"""
    print("🔄 Updating GUI Components")
    print("=" * 35)
    
    packages = ["flet", "flet-core"]
    
    try:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages
        
        print("⏳ Updating packages...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ GUI components updated successfully!")
            return True
        else:
            print(f"❌ Update failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Update error: {e}")
        return False


def uninstall_gui_components():
    """Uninstall GUI components"""
    print("🗑️  Uninstalling GUI Components")
    print("=" * 40)
    
    packages = ["flet", "flet-core"]
    
    try:
        cmd = [sys.executable, "-m", "pip", "uninstall", "-y"] + packages
        
        print("⏳ Removing packages...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ GUI components uninstalled successfully!")
            return True
        else:
            print(f"❌ Uninstall failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Uninstall error: {e}")
        return False


def print_gui_status():
    """Print current GUI status"""
    print("🎨 GUI Status")
    print("=" * 20)
    
    if check_gui_availability():
        print("✅ GUI components are installed")
        print("   You can use: summarizer --gui")
        
        # Check for GUI launcher
        launcher_path = Path(__file__).parent.parent / "gui_launcher.py"
        if launcher_path.exists():
            print(f"✅ GUI launcher available: {launcher_path}")
        else:
            print("⚠️  GUI launcher not found")
            print("   Creating launcher...")
            create_gui_launcher()
    else:
        print("❌ GUI components not installed")
        print("   Run: summarizer --install-gui")
    
    return check_gui_availability()


def install_full_gui_package():
    """Install complete GUI package with all dependencies"""
    print("🎨 Installing Complete GUI Package")
    print("=" * 45)
    
    success = True
    
    # Step 1: Install GUI components
    if not install_gui_components():
        success = False
    
    # Step 2: Create GUI launcher
    if success:
        if not create_gui_launcher():
            print("⚠️  GUI launcher creation failed (non-critical)")
    
    # Step 3: Test GUI
    if success:
        print("\n🧪 Testing GUI...")
        if check_gui_availability():
            print("✅ GUI package installation complete!")
            print()
            print("🎉 You can now use:")
            print("   summarizer --gui")
            print("   python gui_launcher.py")
        else:
            print("❌ GUI test failed")
            success = False
    
    return success
