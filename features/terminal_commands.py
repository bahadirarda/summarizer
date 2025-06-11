"""
🔗 Terminal Commands Feature

This module provides terminal command creation and installation utilities.
Creates system-wide 'summarizer' command for easier access.
"""

import os
import sys
import stat
import subprocess
from pathlib import Path


def create_terminal_command():
    """Create the terminal command script"""
    
    # Get the absolute path to this project
    project_root = Path(__file__).parent.parent.absolute()
    summarizer_py = project_root / "summarizer.py"
    
    # Command script content
    if sys.platform == "win32":  # Windows
        script_content = f'''@echo off
REM Summarizer Framework Terminal Command
cd /d "{project_root}"
python "{summarizer_py}" %*
'''
        script_name = "summarizer.bat"
    else:  # Unix-like (macOS, Linux)
        script_content = f'''#!/bin/bash
# Summarizer Framework Terminal Command
cd "{project_root}"
python3 "{summarizer_py}" "$@"
'''
        script_name = "summarizer"
    
    return script_content, script_name


def install_terminal_command():
    """Install the summarizer command globally"""
    print("🔗 Installing Terminal Command")
    print("=" * 35)
    
    try:
        script_content, script_name = create_terminal_command()
        
        if sys.platform == "win32":  # Windows
            # Install to a directory in PATH
            install_paths = [
                Path.home() / "AppData" / "Local" / "Microsoft" / "WindowsApps",
                Path("C:") / "Windows" / "System32",
                Path.home() / "bin"
            ]
            
            installed = False
            for install_dir in install_paths:
                if install_dir.exists() and os.access(install_dir, os.W_OK):
                    script_path = install_dir / script_name
                    try:
                        with open(script_path, 'w') as f:
                            f.write(script_content)
                        print(f"✅ Installed to: {script_path}")
                        installed = True
                        break
                    except PermissionError:
                        continue
            
            if not installed:
                # Fallback: create in project directory and show instructions
                script_path = Path(__file__).parent.parent / script_name
                with open(script_path, 'w') as f:
                    f.write(script_content)
                
                print(f"📁 Created script: {script_path}")
                print("⚠️  To use 'summarizer' globally, add this directory to your PATH:")
                print(f"   {script_path.parent}")
        
        else:  # Unix-like (macOS, Linux)
            # Try to install to a directory in PATH
            install_paths = [
                Path.home() / ".local" / "bin",
                Path("/usr/local/bin"),
                Path.home() / "bin"
            ]
            
            # Create ~/.local/bin if it doesn't exist
            local_bin = Path.home() / ".local" / "bin"
            local_bin.mkdir(parents=True, exist_ok=True)
            
            installed = False
            for install_dir in install_paths:
                if install_dir.exists():
                    script_path = install_dir / script_name
                    try:
                        with open(script_path, 'w') as f:
                            f.write(script_content)
                        
                        # Make executable
                        script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
                        
                        print(f"✅ Installed to: {script_path}")
                        installed = True
                        break
                    except PermissionError:
                        if install_dir == Path("/usr/local/bin"):
                            # Try with sudo
                            try:
                                temp_script = Path("/tmp") / script_name
                                with open(temp_script, 'w') as f:
                                    f.write(script_content)
                                temp_script.chmod(temp_script.stat().st_mode | stat.S_IEXEC)
                                
                                result = subprocess.run([
                                    "sudo", "mv", str(temp_script), str(script_path)
                                ], capture_output=True)
                                
                                if result.returncode == 0:
                                    print(f"✅ Installed to: {script_path} (with sudo)")
                                    installed = True
                                    break
                            except Exception:
                                continue
                        continue
            
            if not installed:
                # Fallback: create in project directory
                script_path = Path(__file__).parent.parent / script_name
                with open(script_path, 'w') as f:
                    f.write(script_content)
                script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
                
                print(f"📁 Created script: {script_path}")
                print("⚠️  To use 'summarizer' globally, add this to your shell profile:")
                print(f"   export PATH=\"{script_path.parent}:$PATH\"")
        
        # Test the installation
        print()
        print("🧪 Testing installation...")
        
        try:
            result = subprocess.run(
                ["summarizer", "--help"] if sys.platform != "win32" else ["summarizer.bat", "--help"],
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ Terminal command works!")
                print()
                print("🎉 Installation complete! You can now use:")
                print("   summarizer")
                print("   summarizer --setup")
                print("   summarizer --gui")
                print("   summarizer screenshot")
                print("   summarizer ss chrome")
                return True
            else:
                print("⚠️  Command installed but test failed")
                print("   You may need to restart your terminal")
                return False
        
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Command installed but not in PATH")
            print("   You may need to restart your terminal or update PATH")
            return False
    
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False


def uninstall_terminal_command():
    """Remove the summarizer command"""
    print("🗑️  Uninstalling Terminal Command")
    print("=" * 37)
    
    script_name = "summarizer.bat" if sys.platform == "win32" else "summarizer"
    
    # Common installation locations
    if sys.platform == "win32":
        search_paths = [
            Path.home() / "AppData" / "Local" / "Microsoft" / "WindowsApps",
            Path("C:") / "Windows" / "System32",
            Path.home() / "bin"
        ]
    else:
        search_paths = [
            Path.home() / ".local" / "bin",
            Path("/usr/local/bin"),
            Path.home() / "bin"
        ]
    
    # Also check project directory
    search_paths.append(Path(__file__).parent.parent)
    
    removed = False
    for search_dir in search_paths:
        script_path = search_dir / script_name
        if script_path.exists():
            try:
                script_path.unlink()
                print(f"✅ Removed: {script_path}")
                removed = True
            except PermissionError:
                try:
                    subprocess.run(["sudo", "rm", str(script_path)], check=True)
                    print(f"✅ Removed: {script_path} (with sudo)")
                    removed = True
                except subprocess.CalledProcessError:
                    print(f"❌ Could not remove: {script_path} (permission denied)")
    
    if removed:
        print("✅ Terminal command uninstalled")
    else:
        print("⚠️  No terminal command found to remove")
    
    return removed


def check_terminal_command():
    """Check if terminal command is installed and working"""
    script_name = "summarizer" if sys.platform != "win32" else "summarizer.bat"
    
    try:
        result = subprocess.run(
            [script_name, "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def print_terminal_status():
    """Print current terminal command status"""
    print("🔗 Terminal Command Status")
    print("=" * 30)
    
    if check_terminal_command():
        print("✅ Terminal command is installed and working")
        print("   You can use: summarizer [options]")
    else:
        print("❌ Terminal command not found")
        print("   Run: summarizer --install-terminal")
        print("   Or: python summarizer.py --install-terminal")
    
    return check_terminal_command()
