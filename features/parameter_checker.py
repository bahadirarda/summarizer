"""
🔧 Parameter Checker Feature

This module provides configuration validation and setup guidance.
Checks required parameters and guides users through setup process.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_required_parameters():
    """Check if required parameters are set and provide guidance"""
    missing_params = []
    guidance = []
    
    # Check for Gemini API key
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        missing_params.append('GEMINI_API_KEY')
        guidance.append("""
🔑 GEMINI_API_KEY is missing!
   
   📋 How to set it:
   
   Option 1 - Terminal (Temporary):
   export GEMINI_API_KEY="your-api-key-here"
   
   Option 2 - Environment File (Permanent):
   echo 'GEMINI_API_KEY=your-api-key-here' >> .env
   
   Option 3 - GUI Configuration (Recommended):
   summarizer --setup         # Interactive setup
   summarizer --gui           # Launch GUI configuration
   
   🔗 Get your API key from: https://makersuite.google.com/app/apikey
""")
    
    # Check .env file exists
    env_file = Path('.env')
    if not env_file.exists() and not gemini_key:
        guidance.append("""
📁 .env file not found!
   
   Creating a basic .env file for you:""")
        
        # Create basic .env template
        env_content = '''# Summarizer Framework Configuration
# Add your API keys and settings here

# Required: Gemini AI API Key
# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your-api-key-here

# Optional: Application Environment
APP_ENV=development

# Optional: Logging Level
LOG_LEVEL=INFO
'''
        try:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            guidance.append("   ✅ Created .env template file")
            guidance.append("   📝 Edit .env file and add your API key")
        except Exception as e:
            guidance.append(f"   ❌ Failed to create .env file: {e}")
    
    return missing_params, guidance


def print_parameter_guidance():
    """Print guidance for missing parameters"""
    missing_params, guidance = check_required_parameters()
    
    if missing_params:
        print("⚠️  Configuration Required")
        print("=" * 50)
        print()
        print("Some required parameters are missing:")
        for param in missing_params:
            print(f"   ❌ {param}")
        print()
        
        for guide in guidance:
            print(guide)
        
        print()
        print("📋 Quick Setup Options:")
        print()
        print("1️⃣  GUI Setup (Recommended):")
        print("   summarizer --gui")
        print()
        print("2️⃣  Interactive Setup:")
        print("   summarizer --setup")
        print()
        print("3️⃣  Manual Setup:")
        print("   export GEMINI_API_KEY='your-key-here'")
        print("   summarizer")
        print()
        
        return False
    
    return True


def setup_command():
    """Interactive setup command"""
    print("🚀 Summarizer Framework Setup")
    print("=" * 40)
    print()
    
    # Check if GUI is available
    gui_available = check_gui_availability()
    
    if not gui_available:
        print("💡 GUI setup is available for easier configuration!")
        install_gui = input("   Install GUI components? (y/n): ").lower().strip()
        if install_gui in ['y', 'yes']:
            try:
                from .gui_installer import install_gui_components
                if install_gui_components():
                    print("✅ GUI installed! You can now run: summarizer --gui")
                    return
                else:
                    print("❌ GUI installation failed, continuing with terminal setup...")
            except ImportError:
                print("❌ GUI installer not available, continuing with terminal setup...")
    
    # Terminal setup
    print()
    print("🔧 Terminal Configuration Setup")
    print("-" * 30)
    
    # Get API key
    print()
    print("🔑 Gemini API Key Setup:")
    print("   Get your key from: https://makersuite.google.com/app/apikey")
    api_key = input("   Enter your Gemini API key: ").strip()
    
    if api_key:
        # Save to .env file
        env_file = Path('.env')
        env_content = f"GEMINI_API_KEY={api_key}\n"
        
        if env_file.exists():
            # Check if key already exists
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'GEMINI_API_KEY=' in content:
                # Replace existing key
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if line.startswith('GEMINI_API_KEY='):
                        new_lines.append(f"GEMINI_API_KEY={api_key}")
                    else:
                        new_lines.append(line)
                
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
            else:
                # Append to existing file
                with open(env_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{env_content}")
        else:
            # Create new file
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write("# Summarizer Framework Configuration\n")
                f.write(env_content)
                f.write("APP_ENV=development\n")
        
        print("✅ API key saved to .env file")
        print()
        print("🎉 Setup complete! You can now use:")
        print("   summarizer")
        print("   summarizer screenshot")
        print("   summarizer ss chrome")
        
        # Test the configuration
        print()
        test_config = input("Test configuration now? (y/n): ").lower().strip()
        if test_config in ['y', 'yes']:
            from src.services.gemini_client import GeminiClient
            client = GeminiClient()
            if client.is_ready():
                print("✅ Configuration test successful!")
            else:
                print("❌ Configuration test failed. Please check your API key.")
    else:
        print("❌ No API key provided. Setup incomplete.")


def check_gui_availability():
    """Check if GUI components are available"""
    try:
        import flet
        return True
    except ImportError:
        return False


def validate_config():
    """Validate current configuration and return status"""
    missing_params, _ = check_required_parameters()
    
    if not missing_params:
        # Test Gemini connection
        try:
            from src.services.gemini_client import GeminiClient
            client = GeminiClient()
            if client.is_ready():
                return True, "✅ Configuration is complete and working!"
            else:
                return False, "❌ Gemini API key is invalid or not working"
        except Exception as e:
            return False, f"❌ Configuration error: {e}"
    else:
        return False, f"❌ Missing parameters: {', '.join(missing_params)}"


def print_config_status():
    """Print current configuration status"""
    print("🔍 Configuration Status")
    print("=" * 30)
    
    is_valid, message = validate_config()
    print(message)
    
    if not is_valid:
        print()
        print("🔧 To fix configuration:")
        print("   summarizer --setup    # Interactive setup")
        print("   summarizer --gui      # GUI configuration")
    
    return is_valid
