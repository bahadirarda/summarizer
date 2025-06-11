# 🚀 Summarizer Framework v2.0

> **AI-Powered Project Summarizer with Enterprise GUI and Terminal Commands**

A powerful, modular framework that automatically analyzes your project changes, generates intelligent summaries using AI, and provides both GUI and terminal interfaces for easy configuration and usage.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Smart Change Detection**: Automatically tracks file modifications and generates meaningful summaries
- **Gemini AI Integration**: Uses Google's Gemini AI for intelligent code analysis and summary generation
- **Multi-format Output**: JSON changelog and Markdown documentation

### 🎨 Enterprise GUI
- **Modern Flat Design**: Professional, Microsoft-inspired interface
- **Easy Configuration**: Visual setup for API keys and settings
- **Real-time Validation**: Instant feedback on configuration changes
- **Profile Management**: Save and load different configuration profiles

### 💻 Terminal Commands
- **Global Commands**: Use `summarizer` from anywhere in your terminal
- **Screenshot Analysis**: AI-powered screenshot analysis with `summarizer ss`
- **Interactive Setup**: Step-by-step configuration with `summarizer --setup`

### 📸 Screenshot Analysis
- **Full Screen Capture**: `summarizer screenshot` for complete desktop analysis
- **App-Specific Capture**: `summarizer ss chrome` for specific application analysis
- **AI Commentary**: Detailed analysis of what's happening on screen

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bahadirarda/summarizer-framework
cd summarizer-framework

# Install dependencies
pip install -r requirements.txt

# Install GUI and terminal commands
python install_gui.py
```

### Setup

```bash
# Interactive setup (recommended)
summarizer --setup

# Or use GUI setup
summarizer --gui

# Check configuration
summarizer --check
```

### Usage

#### Python Import (Simplest)
```python
import summarizer
summarizer()  # Analyzes current project
```

#### Terminal Commands
```bash
# Basic analysis
summarizer

# Screenshot analysis
summarizer screenshot
summarizer ss chrome
summarizer ss firefox

# Configuration
summarizer --setup
summarizer --gui
summarizer --status
```

## 📋 Detailed Usage

### 1. Python Integration
The framework is designed for the simplest possible usage pattern:

```python
import summarizer
summarizer()
```

This will:
- ✅ Detect project changes automatically
- ✅ Generate AI-powered summaries
- ✅ Update changelog files
- ✅ Show helpful guidance if configuration is missing

### 2. Terminal Commands

#### Global Command Installation
After running `python install_gui.py`, you can use `summarizer` globally:

```bash
summarizer --help              # Show all options
summarizer --setup             # Interactive configuration
summarizer --gui               # Launch GUI interface
summarizer --status            # Show system status
summarizer --check             # Validate configuration
```

#### Screenshot Analysis
```bash
# Full screen analysis
summarizer screenshot
summarizer ss

# Application-specific analysis
summarizer ss chrome           # Capture Chrome window
summarizer ss firefox          # Capture Firefox window
summarizer ss code             # Capture VS Code window
summarizer ss terminal         # Capture Terminal window
```

### 3. GUI Interface

Launch the enterprise-grade configuration GUI:

```bash
summarizer --gui
# Or
python gui_launcher.py
```

The GUI provides:
- 🔑 **API Key Management**: Secure storage of Gemini API keys
- ⚙️ **Configuration Profiles**: Save different setups for different projects
- 🎯 **Real-time Validation**: Instant feedback on settings
- 📁 **Environment Variables**: Easy management of project settings

## 🛠️ Configuration

### API Key Setup

You need a Google Gemini API key for AI features:

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Setup Options**:
   - **GUI**: `summarizer --gui` (recommended)
   - **Interactive**: `summarizer --setup`
   - **Manual**: Add `GEMINI_API_KEY=your-key` to `.env` file

### Environment Variables

Create a `.env` file in your project root:

```env
# Required: Gemini AI API Key
GEMINI_API_KEY=your-api-key-here

# Optional: Application Environment
APP_ENV=development

# Optional: Logging Level
LOG_LEVEL=INFO
```

## 📁 Project Structure

```
summarizer-framework/
├── 🐍 summarizer.py              # Main entry point
├── 🎨 gui_launcher.py            # GUI launcher
├── 📦 install_gui.py             # Installation script
├── 📄 requirements.txt           # Dependencies
├── 🔧 src/                       # Core framework
│   ├── 🎛️ config.py              # Configuration
│   ├── 🚀 main.py                # Main application
│   ├── 🏗️ core/                  # Core components
│   ├── 🎨 gui/                   # GUI interface
│   ├── 🔌 services/              # AI and API services
│   └── 🛠️ utils/                 # Utilities
├── ✨ features/                  # Modular features
│   ├── 📸 screenshot.py          # Screenshot analysis
│   ├── 🔧 parameter_checker.py   # Configuration validation
│   ├── 💻 terminal_commands.py   # Terminal integration
│   └── 🎨 gui_installer.py       # GUI installation
└── 📚 demo_project/              # Example usage
```

## 🔧 Advanced Usage

### Custom Project Analysis

```python
import summarizer

# Analyze specific directory
import os
os.chdir('/path/to/your/project')
summarizer()

# Or from any Python script
from pathlib import Path
from src.main import summarizer as analyze_project

project_root = Path('/path/to/project')
os.chdir(project_root)
analyze_project()
```

### Screenshot Analysis with Custom Prompts

```bash
# Basic screenshot analysis
summarizer ss

# Application-specific with context
summarizer ss chrome "analyze the website design"
summarizer ss code "review the code quality"
```

### API Integration

```python
from src.services.gemini_client import GeminiClient
from src.utils.changelog_updater import update_changelog

# Direct AI client usage
client = GeminiClient()
summary = client.generate_summary("Describe these changes", ["file1.py", "file2.js"])

# Direct changelog update
update_changelog(project_root=Path.cwd())
```

## 🎯 Use Cases

### 1. Development Workflow
```bash
# Start coding session
git pull
summarizer --check

# After making changes
summarizer  # Auto-generates changelog

# Before commit
git add .
git commit -m "$(summarizer --summary)"  # AI-generated commit message
```

### 2. Code Review Process
```bash
# Analyze changes for review
summarizer ss code "review code quality and suggest improvements"

# Generate review summary
summarizer --review
```

### 3. Documentation Generation
```bash
# Auto-update project documentation
summarizer --docs

# Generate release notes
summarizer --release-notes
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "Configuration Required" Message
```bash
# Solution: Set up your API key
summarizer --setup
```

#### 2. "GUI components not installed"
```bash
# Solution: Install GUI
python install_gui.py
```

#### 3. "Terminal command not found"
```bash
# Solution: Install and update PATH
python summarizer.py --install-terminal
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### 4. Import Errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Getting Help

```bash
summarizer --help              # Show all commands
summarizer --status            # Show system status
summarizer --check             # Validate configuration
```

## 📈 Version Information

- **Current Version**: v2.0.0
- **Release Date**: June 11, 2025
- **Compatibility**: Python 3.8+
- **Dependencies**: See `requirements.txt`

### What's New in v2.0

- ✨ **Modular Architecture**: Feature-based organization
- 🎨 **Enterprise GUI**: Professional flat design interface
- 💻 **Global Commands**: Terminal integration with `summarizer` command
- 📸 **Screenshot Analysis**: AI-powered visual analysis
- 🔧 **Improved Setup**: Interactive configuration wizard
- 🚀 **Better Performance**: Optimized imports and faster startup
- 🔒 **Enhanced Security**: Better API key management

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/bahadirarda/summarizer-framework
cd summarizer-framework
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/

# Code formatting
black src/ features/
flake8 src/ features/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Documentation**: [Wiki](https://github.com/bahadirarda/summarizer-framework/wiki)
- **Issues**: [GitHub Issues](https://github.com/bahadirarda/summarizer-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bahadirarda/summarizer-framework/discussions)

## 💡 Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting issues
- 💬 Starting discussions
- 📝 Contributing improvements

---

**Made with ❤️ by [Bahadir Arda](https://github.com/bahadirarda)**

> *"Simplifying project analysis with the power of AI"*
