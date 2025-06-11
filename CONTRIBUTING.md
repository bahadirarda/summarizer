# 🤝 Contributing to Summarizer Framework

Thank you for your interest in contributing to the Summarizer Framework! This document provides guidelines for contributing to this project.

## 🎯 Ways to Contribute

### 1. 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide system information (OS, Python version, etc.)
- Include error messages and logs

### 2. ✨ Feature Requests
- Describe the feature you'd like to see
- Explain the use case and benefits
- Consider backward compatibility

### 3. 📝 Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and grammar

### 4. 💻 Code Contributions
- Follow the coding standards below
- Write tests for new features
- Update documentation as needed

## 🛠️ Development Setup

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Git
git --version
```

### Setup Development Environment
```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/summarizer-framework
cd summarizer-framework

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Install GUI components
python install_gui.py

# 6. Run tests
python -m pytest tests/
```

## 📋 Coding Standards

### Python Code Style
- Follow PEP 8 standards
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 88 characters (Black formatter)

### Code Formatting
```bash
# Format code with Black
black src/ features/

# Lint with flake8
flake8 src/ features/

# Type checking with mypy
mypy src/
```

### Commit Messages
Follow conventional commits:
```
feat: add screenshot analysis feature
fix: resolve GUI import issue
docs: update installation guide
refactor: improve modular architecture
test: add unit tests for core functions
```

## 🏗️ Project Structure

```
📁 Summarizer Framework
├── 📄 summarizer.py           # Main entry point
├── 📁 src/                   # Core framework
│   ├── 📄 main.py           # Main logic
│   ├── 📁 gui/              # GUI components
│   ├── 📁 services/         # AI services
│   └── 📁 utils/            # Utilities
├── 📁 features/             # Modular features
├── 📁 tests/               # Test suite
└── 📁 docs/                # Documentation
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_main.py

# Run with coverage
python -m pytest --cov=src
```

### Writing Tests
- Use pytest framework
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test both success and error cases

Example:
```python
def test_summarizer_function():
    # Arrange
    test_data = {...}
    
    # Act
    result = summarizer_function(test_data)
    
    # Assert
    assert result is not None
    assert result.status == "success"
```

## 🔄 Pull Request Process

### Before Submitting
1. **Fork the repository** and create a feature branch
2. **Write or update tests** for your changes
3. **Ensure all tests pass** locally
4. **Format your code** with Black and flake8
5. **Update documentation** if needed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process
1. Automated checks must pass
2. At least one maintainer review required
3. Address feedback and update if needed
4. Maintainer will merge when approved

## 🐛 Issue Templates

### Bug Report
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. macOS, Windows, Linux]
- Python Version: [e.g. 3.9]
- Framework Version: [e.g. 2.0.0]
```

### Feature Request
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Additional context**
Add any other context about the feature request.
```

## 🚀 Release Process

### Version Numbering
- Follow Semantic Versioning (SemVer)
- Major.Minor.Patch (e.g., 2.1.0)
- Breaking changes = Major
- New features = Minor
- Bug fixes = Patch

### Release Checklist
- [ ] Update version in `package.json`
- [ ] Update version in `src/config.py`
- [ ] Create release notes
- [ ] Tag release in git
- [ ] Update documentation

## 🤔 Questions?

- Check existing [Issues](https://github.com/bahadirarda/summarizer-framework/issues)
- Start a [Discussion](https://github.com/bahadirarda/summarizer-framework/discussions)
- Contact maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Summarizer Framework! 🎉**
