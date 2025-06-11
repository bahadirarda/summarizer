# 🚀 Summarizer Framework v2.0

> **AI-Powered Project Summarizer with Step-by-Step Feedback and Hidden File Management**

A powerful, modular framework that automatically analyzes your project changes, generates intelligent summaries using AI, and provides detailed step-by-step feedback during execution. Features enterprise GUI, terminal commands, and clean project structure with hidden internal files.

## ✨ New in v2.0

### 🔍 **Step-by-Step Execution Feedback**
- **Real-time Progress**: See exactly what the summarizer is doing at each step
- **Detailed Console Output**: Track file scanning, AI analysis, and changelog generation
- **Professional Progress Indicators**: Clear visual feedback with emojis and status messages
- **Transparent Operations**: Know when files are being analyzed, AI is thinking, and backups are created

### 📁 **Clean Project Structure**
- **Hidden Internal Files**: All system files stored in `.summarizer/` directory
- **User-Friendly Workspace**: Only `CHANGELOG.md` and `changelog.json` visible to users
- **Automatic Setup**: Framework manages all internal structures transparently
- **No Clutter**: `.file_states.json`, backups, and configs hidden from main workspace

### 🎉 **New Project Initialization**
- **Professional Welcome**: Beautiful initial changelog entries for new projects
- **Project Type Detection**: Automatically detects Python, Web, or General project types
- **Setup Guidance**: Helpful instructions and next steps for new users
- **Zero Configuration**: Just run `summarizer` in any new directory to get started

## ✨ Core Features

### 🤖 AI-Powered Analysis
- **Smart Change Detection**: Automatically tracks file modifications and generates meaningful summaries
- **Gemini AI Integration**: Uses Google's Gemini AI for intelligent code analysis and summary generation
- **Multi-format Output**: JSON changelog and Markdown documentation
- **Impact Level Detection**: Automatically categorizes changes as Low/Medium/High/Critical

### 🎨 Enterprise GUI
- **Modern Flat Design**: Professional, Microsoft-inspired interface
- **Easy Configuration**: Visual setup for API keys and settings
- **Real-time Validation**: Instant feedback on configuration changes
- **Profile Management**: Save and load different configuration profiles

### 💻 Terminal Commands
- **Global Commands**: Use `summarizer` from anywhere in your terminal
- **Universal Support**: Works in any directory structure (main project, subdirectories, new projects)
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
# 1. Configure environment variables
cp .env.example .env
# Edit .env with your Gemini API key

# 2. Interactive setup (recommended)
summarizer --setup

# 3. Or use GUI setup
summarizer --gui

# 4. Verify configuration
summarizer --check
```

### Usage

#### Python Import (Simplest)
```python
import summarizer
summarizer()  # Analyzes current project with step-by-step feedback
```

#### Terminal Commands
```bash
# Basic analysis with detailed feedback
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

## 🎯 Example Output

When you run `summarizer`, you'll see detailed step-by-step feedback:

```
🔍 Summarizer Framework v2.0.0 Starting...
==================================================
📝 Step 1/6: Setting up configuration...
✅ Configuration loaded successfully

🔗 Step 2/6: Initializing request manager...
✅ Request manager ready

🤖 Step 3/6: Connecting to Gemini AI...
✅ AI client connected

📁 Step 4/6: Detecting project structure...
📂 Working directory detected: demo_project
   Path: /path/to/demo_project

🔎 Step 5/6: Scanning for file changes...
   🔍 Scanning for changed files...
   📂 Scanning root directory (2 Python files)
   ✅ Found 1 changed files:
      • simple_demo.py
   📊 Analyzing line changes...
   📈 Line changes: +5 added, -0 removed
   🤖 Generating AI analysis...
   ✨ AI analysis completed successfully
   📝 Summary: Added new function for data processing...
   🎯 Impact level: medium
   💾 Saving changelog entry...
   ✅ Changelog entry created (ID: abc12345...)
   🔄 Creating backup files for future comparison...
   ✅ Backup files created

✨ Step 6/6: Analysis complete!
==================================================
📊 Results saved to:
   • CHANGELOG.md - Human readable format
   • changelog.json - Structured data format
   • .summarizer/ - Internal tracking files
✅ Summarizer completed successfully!
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

## 📁 Project Structure

The Summarizer Framework maintains a clean workspace by storing all internal files in a hidden directory:

```
your-project/
├── CHANGELOG.md              # Human-readable changelog
├── changelog.json            # Structured changelog data
├── .summarizer/              # Hidden framework files
│   ├── .file_states.json     # File change tracking
│   ├── user_settings.json    # Configuration settings
│   ├── configuration_schema.json
│   └── file_backups/         # Backup files for comparison
├── your-code-files.py
└── other-project-files
```

### Universal Directory Support

The framework works everywhere:
- ✅ **Main Projects**: Full src/ directory scanning
- ✅ **Sub-projects**: Individual directory tracking  
- ✅ **New Projects**: Automatic initialization with welcome messages
- ✅ **Any Directory**: Universal Python file detection

## 🛠️ Configuration

### API Key Setup

You need a Google Gemini API key for AI features:

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Setup Options**:
   - **GUI**: `summarizer --gui` (recommended)
   - **Interactive**: `summarizer --setup`
   - **Manual**: Copy `.env.example` to `.env` and configure

### Environment Variables

The framework includes a comprehensive `.env.example` file with all available configuration options:

```bash
# Quick setup
cp .env.example .env
# Edit .env with your actual values
```

**Required Configuration:**
```env
# Required: Gemini AI API Key
GEMINI_API_KEY=your-api-key-here

# Environment mode
APP_ENV=development
LOG_LEVEL=INFO
```

**Optional Advanced Configuration:**
```env
# AI Analysis Settings
AI_MODEL_TEMPERATURE=0.3
AI_MAX_TOKENS=1000

# Feature Toggles
ENABLE_AI_ANALYSIS=true
ENABLE_SCREENSHOT_ANALYSIS=true
ENABLE_GUI_INTERFACE=true

# GUI Appearance
GUI_THEME=modern
GUI_WINDOW_SIZE=800x600
```

See `.env.example` for complete configuration options including database, API server, and deployment settings.

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

## 🎉 New Project Initialization

When you run `summarizer` in a new directory, it automatically creates a professional welcome entry:

### For Python Projects:
```markdown
🚀 **YourProject Projesi Başlatıldı**

**Proje Türü**: Python Projesi  
**Başlatılma Tarihi**: 11 Haziran 2025  
**Summarizer Framework**: v2.0.0

**📋 Proje Özeti:**
Bu proje, Summarizer Framework ile otomatik değişiklik takibi ve AI destekli analiz için yapılandırıldı. 

**🔧 Aktif Özellikler:**
- ✅ Otomatik dosya değişiklik takibi
- ✅ AI destekli kod analizi (Gemini AI)
- ✅ JSON ve Markdown changelog oluşturma
- ✅ Etki seviyesi ve değişiklik tipi otomatik tespiti
```

### For Web Projects:
Automatically detects web projects (package.json, index.html) and creates appropriate welcome messages.

### For General Projects:
Creates a universal welcome entry for any other project type.

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
