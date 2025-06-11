# 🚀 Summarizer Framework - Quick Start Guide

**The simplest way to add AI-powered project analysis to your workflow!**

## 🌟 Super Simple Usage

```python
import summarizer
summarizer()
```

That's it! The framework automatically analyzes your project changes and generates intelligent summaries.

## 📋 First Time Setup

### Option 1: GUI Setup (Recommended) 🎨

```bash
# Install GUI components
python install_gui.py

# Launch configuration interface
python gui_launcher.py
```

- Opens in your browser
- Easy point-and-click configuration
- Visual API key management
- Folder selection for project analysis

### Option 2: Terminal Setup ⚡

```bash
# Interactive setup
python summarizer.py --setup

# Quick setup
export GEMINI_API_KEY="your-api-key-here"
python summarizer.py
```

### Option 3: Environment File 📁

Create a `.env` file:
```env
GEMINI_API_KEY=your-api-key-here
APP_ENV=development
```

## 🔑 Getting Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your preferred setup method

## 🚀 Usage Examples

### Basic Usage
```python
import summarizer
summarizer()  # Analyzes current directory
```

### Terminal Commands
```bash
# Check configuration
python summarizer.py --check

# Run interactive setup
python summarizer.py --setup

# Install GUI components
python summarizer.py --install-gui

# Get help
python summarizer.py --help
```

### Project Integration
```python
# In your project scripts
import summarizer

def deploy():
    # Your deployment code here
    summarizer()  # Auto-generate changelog entry
```

## 📁 Folder Selection

The framework intelligently detects your project structure:

- **Main Project**: Analyzes the entire framework
- **Sub-projects**: Automatically switches to current directory
- **Demo Projects**: Works in any folder with your code

## 🎯 Features

- ✅ **Zero Configuration** - Works out of the box
- 🤖 **AI-Powered Analysis** - Uses Google's Gemini AI
- 📊 **Smart Change Detection** - Tracks file modifications
- 📝 **Automatic Changelog** - Generates markdown summaries
- 🎨 **Optional GUI** - Visual configuration interface
- 🔒 **Secure** - API keys stored locally
- 📦 **Lightweight** - Minimal dependencies

## 🛠️ Advanced Configuration

### Custom Project Paths
```python
import os
os.chdir('/path/to/your/project')
import summarizer
summarizer()
```

### Environment Variables
```bash
export GEMINI_API_KEY="your-key"
export APP_ENV="production"
export LOG_LEVEL="DEBUG"
```

### Configuration Files
The framework automatically creates:
- `.env` - Environment variables
- `config/user_settings.json` - User preferences
- `changelog.json` - Change tracking data
- `CHANGELOG.md` - Human-readable summaries

## 🐛 Troubleshooting

### Missing API Key
```bash
# Check what's missing
python summarizer.py --check

# Set up interactively
python summarizer.py --setup
```

### GUI Issues
```bash
# Reinstall GUI components
python install_gui.py

# Check if Flet is installed
python -c "import flet; print(flet.__version__)"
```

### Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install dependencies
pip install -r requirements.txt
```

## 📚 What It Analyzes

- **Code Changes**: New features, bug fixes, refactoring
- **File Structure**: Added/removed files and directories
- **Dependencies**: Package updates and new installations
- **Configuration**: Settings and environment changes
- **Documentation**: README, comments, and docstring updates

## 🤝 Integration Examples

### Git Hooks
```bash
# .git/hooks/post-commit
#!/bin/bash
python -c "import summarizer; summarizer()"
```

### CI/CD Pipeline
```yaml
# GitHub Actions
- name: Generate Summary
  run: |
    export GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
    python -c "import summarizer; summarizer()"
```

### Development Workflow
```python
# development.py
import summarizer

def release():
    run_tests()
    build_project()
    summarizer()  # Document changes
    deploy()
```

## 🎉 That's It!

You're ready to use the Summarizer Framework. Start with the simple usage pattern and explore advanced features as needed.

**Happy coding! 🚀**
