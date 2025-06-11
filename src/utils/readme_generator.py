import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .json_changelog_manager import JsonChangelogManager

logger = logging.getLogger(__name__)


def _get_framework_version(project_root: Path) -> str:
    """Get framework version from package.json"""
    try:
        package_json_path = project_root / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                version = package_data.get('version', '2.0.2')
                return f"v{version}"
        
        # Fallback to checking parent directories for framework package.json
        current_path = project_root
        for _ in range(3):  # Check up to 3 levels up
            parent_path = current_path.parent
            package_json_path = parent_path / "package.json"
            if package_json_path.exists():
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    # Check if this is the summarizer framework
                    if package_data.get('name') == 'summarizer-framework':
                        version = package_data.get('version', '2.0.2')
                        return f"v{version}"
            current_path = parent_path
        
        # Default fallback
        return "v2.0.2"
    except Exception as e:
        logger.warning(f"Could not read framework version: {e}")
        return "v2.0.2"


def generate_readme_content(project_root: Path, project_name: str = None) -> str:
    """Generate comprehensive README.md content based on project state and changelog"""
    
    if project_name is None:
        project_name = project_root.name
        
    # Get project statistics
    json_manager = JsonChangelogManager(project_root)
    stats = json_manager.get_stats()
    recent_entries = json_manager.get_entries(limit=3)
    
    # Detect project type
    project_type = _detect_project_type(project_root)
    
    # Get current date for freshness
    current_date = datetime.now().strftime('%B %d, %Y')
    
    readme_content = f"""# 🚀 {project_name}

> **AI-Powered Project with Intelligent Change Tracking**

{_get_project_description(project_type, project_name)}

## 📊 Project Status

- **Latest Update**: {current_date}
- **Total Changes**: {stats.get('total_entries', 0)} tracked entries
- **Framework Version**: Summarizer {_get_framework_version(project_root)}
- **Project Type**: {project_type.title()} Project
- **AI Analysis**: ✅ Active with Gemini AI

{_get_recent_activity_section(recent_entries)}

## ✨ Key Features

{_get_project_features(project_type, project_root)}

## 🚀 Quick Start

```bash
# Clone and setup
git clone <your-repo-url>
cd {project_name}

# Install dependencies
{_get_install_commands(project_type, project_root)}

# Run the project
{_get_run_commands(project_type, project_root)}
```

## 📁 Project Structure

```
{project_name}/
{_get_project_structure(project_root, project_type)}
```

## 🔧 Configuration

{_get_configuration_section(project_root)}

## 📈 Development Activity

{_get_development_activity(stats, recent_entries)}

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test them
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Use descriptive commit messages

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: [GitHub](<your-repo-url>)
- **Issues**: [Report Issues](<your-repo-url>/issues)
- **Discussions**: [Join Discussions](<your-repo-url>/discussions)

---

**Last updated**: {current_date} by Summarizer Framework v2.0.2  
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
"""
    
    return readme_content


def _detect_project_type(project_root: Path) -> str:
    """Detect project type based on files in directory"""
    
    # Check for web project indicators
    web_files = ["package.json", "index.html", "main.js", "app.js", "webpack.config.js"]
    if any((project_root / f).exists() for f in web_files):
        return "web"
    
    # Check for Python project indicators
    python_files = ["requirements.txt", "setup.py", "pyproject.toml", "main.py"]
    py_files = list(project_root.glob("*.py"))
    if any((project_root / f).exists() for f in python_files) or len(py_files) > 0:
        return "python"
    
    # Check for React/Node project
    if (project_root / "package.json").exists():
        return "react"
        
    # Check for data science project
    data_files = ["jupyter", "notebook", "data", "datasets"]
    if any((project_root / f).exists() for f in data_files):
        return "data-science"
    
    # Default to general project
    return "general"


def _get_project_description(project_type: str, project_name: str) -> str:
    """Get project description based on type"""
    
    descriptions = {
        "python": f"A Python application with intelligent change tracking and AI-powered analysis. This project uses the Summarizer Framework to automatically monitor code changes, generate meaningful summaries, and maintain comprehensive documentation.",
        
        "web": f"A modern web application featuring automated development tracking and intelligent code analysis. Built with the Summarizer Framework for seamless change monitoring and AI-powered documentation generation.",
        
        "react": f"A React application with smart development workflow tracking. Leverages the Summarizer Framework for automatic change detection, intelligent summarization, and comprehensive project documentation.",
        
        "data-science": f"A data science project with automated analysis tracking and intelligent documentation. Uses the Summarizer Framework to monitor notebook changes, track experiments, and generate meaningful project summaries.",
        
        "general": f"A software project enhanced with AI-powered change tracking and intelligent documentation. Built using the Summarizer Framework for automatic development monitoring and comprehensive analysis."
    }
    
    return descriptions.get(project_type, descriptions["general"])


def _get_project_features(project_type: str, project_root: Path) -> str:
    """Get relevant features based on project type"""
    
    base_features = """### 🤖 AI-Powered Development
- **Smart Change Detection**: Automatically tracks and analyzes code modifications
- **Intelligent Summaries**: AI-generated descriptions of changes and improvements
- **Impact Analysis**: Automatic categorization of changes (Low/Medium/High/Critical)
- **Development Insights**: Comprehensive analysis of project evolution"""
    
    type_features = {
        "python": """
### 🐍 Python-Specific Features
- **Module Analysis**: Intelligent tracking of Python modules and packages
- **Import Dependency**: Analysis of import structures and dependencies
- **Code Quality**: Automated analysis of Python code patterns
- **Testing Integration**: Support for pytest and unittest frameworks""",
        
        "web": """
### 🌐 Web Development Features
- **Frontend/Backend Tracking**: Separate analysis for client and server code
- **Asset Management**: Tracking of CSS, JavaScript, and HTML changes
- **Performance Monitoring**: Analysis of web performance impacts
- **Responsive Design**: Support for mobile-first development tracking""",
        
        "react": """
### ⚛️ React Development Features
- **Component Analysis**: Intelligent tracking of React components
- **State Management**: Analysis of state changes and Redux patterns
- **Hook Usage**: Tracking of React hooks and custom hooks
- **Bundle Analysis**: Webpack and build process monitoring""",
        
        "data-science": """
### 📊 Data Science Features
- **Notebook Tracking**: Jupyter notebook change analysis
- **Data Pipeline**: Analysis of data processing workflows
- **Model Versioning**: Tracking of machine learning model changes
- **Experiment Logging**: Comprehensive experiment documentation"""
    }
    
    return base_features + type_features.get(project_type, "")


def _get_install_commands(project_type: str, project_root: Path) -> str:
    """Get installation commands based on project type"""
    
    commands = {
        "python": "pip install -r requirements.txt",
        "web": "npm install",
        "react": "npm install && npm run build",
        "data-science": "pip install -r requirements.txt && jupyter lab",
        "general": "# Follow project-specific installation instructions"
    }
    
    # Check for specific files
    if (project_root / "requirements.txt").exists():
        return "pip install -r requirements.txt"
    elif (project_root / "package.json").exists():
        return "npm install"
    
    return commands.get(project_type, commands["general"])


def _get_run_commands(project_type: str, project_root: Path) -> str:
    """Get run commands based on project type"""
    
    commands = {
        "python": "python main.py  # or python -m src.main",
        "web": "npm start",
        "react": "npm start",
        "data-science": "jupyter lab",
        "general": "# Follow project-specific run instructions"
    }
    
    # Check for specific files
    if (project_root / "main.py").exists():
        return "python main.py"
    elif (project_root / "src" / "main.py").exists():
        return "python -m src.main"
    elif (project_root / "package.json").exists():
        return "npm start"
    
    return commands.get(project_type, commands["general"])


def _get_project_structure(project_root: Path, project_type: str) -> str:
    """Get project structure representation"""
    
    structure_templates = {
        "python": """├── src/                    # Source code
│   ├── main.py            # Main application
│   ├── utils/             # Utility modules
│   └── config.py          # Configuration
├── tests/                 # Test files
├── requirements.txt       # Dependencies
├── README.md             # This file (auto-generated)
├── CHANGELOG.md          # Change history
└── .summarizer/          # AI tracking (hidden)""",
        
        "web": """├── src/                    # Source code
├── public/                # Static assets
├── package.json           # Dependencies
├── README.md             # This file (auto-generated)
├── CHANGELOG.md          # Change history
└── .summarizer/          # AI tracking (hidden)""",
        
        "react": """├── src/                    # React components
│   ├── components/        # Reusable components
│   ├── pages/            # Page components
│   └── hooks/            # Custom hooks
├── public/               # Static assets
├── package.json          # Dependencies
├── README.md            # This file (auto-generated)
└── .summarizer/         # AI tracking (hidden)""",
        
        "general": """├── main files            # Project files
├── README.md             # This file (auto-generated)
├── CHANGELOG.md          # Change history
└── .summarizer/          # AI tracking (hidden)"""
    }
    
    return structure_templates.get(project_type, structure_templates["general"])


def _get_configuration_section(project_root: Path) -> str:
    """Get configuration section based on available files"""
    
    config_section = ""
    
    if (project_root / ".env.example").exists():
        config_section += """### Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit with your actual values
nano .env
```

See `.env.example` for all available configuration options.

"""
    
    if (project_root / "summarizer.py").exists():
        config_section += """### Summarizer Framework

This project uses the Summarizer Framework for automated change tracking:

```bash
# Run analysis
python summarizer.py

# GUI configuration
python summarizer.py --gui

# Check status
python summarizer.py --status
```

"""
    
    return config_section if config_section else "Configuration details will be added as the project evolves."


def _get_recent_activity_section(recent_entries: list) -> str:
    """Generate recent activity section from changelog entries"""
    
    if not recent_entries:
        return """## 🔄 Recent Activity

No changes tracked yet. Run `summarizer` to start tracking project changes!"""
    
    activity_section = "## 🔄 Recent Activity\n\n"
    
    for i, entry in enumerate(recent_entries[:3], 1):
        # Convert entry to dict if it's an object
        if hasattr(entry, '__dict__'):
            entry_dict = entry.__dict__
        else:
            entry_dict = entry
            
        timestamp = entry_dict.get('timestamp', 'Unknown time')
        if isinstance(timestamp, str) and 'T' in timestamp:
            # Parse ISO format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                timestamp = dt.strftime('%B %d, %Y at %H:%M')
            except:
                pass
                
        summary = entry_dict.get('ai_summary', 'Change summary not available')
        impact = entry_dict.get('impact_level', 'medium')
        files = entry_dict.get('changed_files', [])
        
        # Truncate summary if too long
        if len(summary) > 150:
            summary = summary[:150] + "..."
            
        activity_section += f"""### {i}. {timestamp}
**Impact**: {impact.upper()} | **Files Changed**: {len(files)}

{summary}

"""
    
    activity_section += "*More details available in [CHANGELOG.md](CHANGELOG.md)*\n\n"
    
    return activity_section


def _get_development_activity(stats: dict, recent_entries: list) -> str:
    """Generate development activity statistics"""
    
    total_entries = stats.get('total_entries', 0)
    
    if total_entries == 0:
        return """This project is just getting started! Run `summarizer` to begin tracking development activity."""
    
    # Calculate activity metrics
    impact_counts = {}
    for entry in recent_entries:
        if hasattr(entry, '__dict__'):
            entry_dict = entry.__dict__
        else:
            entry_dict = entry
            
        impact = entry_dict.get('impact_level', 'medium')
        impact_counts[impact] = impact_counts.get(impact, 0) + 1
    
    activity_text = f"""This project has **{total_entries} tracked changes** with comprehensive AI analysis.

### Recent Impact Distribution
"""
    
    for impact, count in impact_counts.items():
        if count > 0:
            activity_text += f"- **{impact.upper()}**: {count} changes\n"
    
    activity_text += f"""
### Tracking Features
- ✅ **Automatic Change Detection**: Files monitored continuously
- ✅ **AI-Powered Analysis**: Intelligent change summaries
- ✅ **Impact Assessment**: Automatic risk evaluation
- ✅ **Comprehensive Logging**: Full change history maintained

*All activity is automatically tracked and analyzed by the Summarizer Framework.*"""
    
    return activity_text


def update_readme(project_root: Path, ai_client=None) -> bool:
    """Update README.md with current project state and AI enhancement"""
    
    try:
        print("   📝 Generating updated README.md...")
        
        project_name = project_root.name
        readme_content = generate_readme_content(project_root, project_name)
        
        # Enhance with AI if available
        if ai_client and hasattr(ai_client, 'is_ready') and ai_client.is_ready():
            try:
                print("   🤖 Enhancing README with AI analysis...")
                
                # Get project overview for AI
                json_manager = JsonChangelogManager(project_root)
                recent_entries = json_manager.get_entries(limit=5)
                
                ai_prompt = f"""
Proje adı: {project_name}
Son değişiklikler: {[entry.ai_summary if hasattr(entry, 'ai_summary') else str(entry) for entry in recent_entries[:3]]}

Bu projeye ait README.md dosyasını Türkçe olarak geliştir. Daha çekici, profesyonel ve kullanıcı dostu hale getir. 
Projenin özelliklerini, kullanım senaryolarını ve faydalarını vurgula.
README'yi markdown formatında, emoji kullanarak ve modern bir yaklaşımla yaz.
"""
                
                ai_enhancement = ai_client.generate_summary(
                    text_prompt=ai_prompt,
                    changed_files=[]
                )
                
                if ai_enhancement and len(ai_enhancement) > 100:
                    # AI enhanced version available
                    readme_content = ai_enhancement
                    print("   ✨ README enhanced with AI analysis")
                else:
                    print("   ⚠️  Using generated README (AI enhancement unavailable)")
                    
            except Exception as e:
                print(f"   ⚠️  AI enhancement failed: {e}")
                # Continue with generated content
        
        # Write README file
        readme_path = project_root / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print(f"   ✅ README.md updated ({len(readme_content)} characters)")
        logger.info(f"README.md updated for project: {project_name}")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Could not update README.md: {e}")
        logger.error(f"Error updating README.md: {e}")
        return False
# Test framework version detection
