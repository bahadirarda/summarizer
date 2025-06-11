# 🎯 Demo Project Usage

This directory contains simple examples of how to use the Summarizer Framework in your own projects.

## 🚀 Simplest Usage

```python
# Just import and use
import summarizer
summarizer()
```

## 📁 Files

- `simple_demo.py` - Complete standalone demo
- Shows step-by-step usage
- Demonstrates integration

## ▶️ Run the Demo

```bash
cd demo_project
python simple_demo.py
```

## 🔧 Integration Steps

1. **Copy the framework** to your project:
   ```bash
   cp -r ../src your_project/
   cp ../requirements.txt your_project/
   cp ../summarizer.py your_project/
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Use in your code**:
   ```python
   import summarizer
   summarizer()
   ```

## ✨ What it does

- 🤖 **AI Analysis**: Uses Gemini AI to analyze code changes
- 📊 **Change Tracking**: Tracks file modifications automatically  
- 📝 **Changelog**: Generates markdown and JSON changelogs
- 🔍 **Smart Detection**: Categorizes changes by type and impact
- 🌐 **API Ready**: Provides REST API for integration

Perfect for automation, CI/CD pipelines, or development workflows!
