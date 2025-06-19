"""
📸 Screenshot Feature

This module provides screenshot capture and analysis functionality.
Supports full screen captures and application-specific screenshots.
"""

import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def take_screenshot(output_path=None):
    """
    Take a full screen screenshot

    Args:
        output_path (str, optional): Path to save screenshot.
                                   If None, creates temp file.

    Returns:
        str: Path to the saved screenshot
    """
    if output_path is None:
        # Create temporary file
        temp_dir = Path(tempfile.gettempdir())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = temp_dir / f"summarizer_screenshot_{timestamp}.png"

    output_path = Path(output_path)

    try:
        if sys.platform == "darwin":  # macOS
            cmd = ["screencapture", "-x", str(output_path)]
        elif sys.platform == "win32":  # Windows
            # Use PowerShell for Windows screenshot
            cmd = [
                "powershell",
                "-Command",
                f"Add-Type -AssemblyName System.Windows.Forms; "
                f"$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
                f"$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height; "
                f"$graphics = [System.Drawing.Graphics]::FromImage($bitmap); "
                f"$graphics.CopyFromScreen(0, 0, 0, 0, $bitmap.Size); "
                f"$bitmap.Save('{output_path}', [System.Drawing.Imaging.ImageFormat]::Png); "
                f"$graphics.Dispose(); $bitmap.Dispose()",
            ]
        else:  # Linux
            # Try different Linux screenshot tools
            for tool in ["gnome-screenshot", "scrot", "import"]:
                if subprocess.run(["which", tool], capture_output=True).returncode == 0:
                    if tool == "gnome-screenshot":
                        cmd = ["gnome-screenshot", "-f", str(output_path)]
                    elif tool == "scrot":
                        cmd = ["scrot", str(output_path)]
                    elif tool == "import":
                        cmd = ["import", "-window", "root", str(output_path)]
                    break
            else:
                raise RuntimeError("No screenshot tool available on Linux")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Screenshot failed: {result.stderr}")

        if not output_path.exists():
            raise RuntimeError("Screenshot file was not created")

        print(f"📸 Screenshot saved: {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
        return None


def take_app_screenshot(app_name, output_path=None):
    """
    Take screenshot of specific application window

    Args:
        app_name (str): Name of the application (e.g., 'chrome', 'firefox', 'code')
        output_path (str, optional): Path to save screenshot

    Returns:
        str: Path to the saved screenshot
    """
    if output_path is None:
        temp_dir = Path(tempfile.gettempdir())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = temp_dir / f"summarizer_{app_name}_screenshot_{timestamp}.png"

    output_path = Path(output_path)

    # Application name mappings
    app_mappings = {
        "chrome": ["Google Chrome", "chrome", "chromium"],
        "firefox": ["Firefox", "firefox"],
        "safari": ["Safari", "safari"],
        "code": ["Visual Studio Code", "code", "vscode"],
        "vscode": ["Visual Studio Code", "code", "vscode"],
        "terminal": ["Terminal", "terminal", "iterm", "iTerm"],
        "finder": ["Finder", "finder"],
        "slack": ["Slack", "slack"],
        "discord": ["Discord", "discord"],
        "zoom": ["zoom.us", "Zoom", "zoom"],
    }

    # Get possible app names
    possible_names = app_mappings.get(app_name.lower(), [app_name])

    try:
        if sys.platform == "darwin":  # macOS
            # Try to find and focus the application window
            for name in possible_names:
                # Try to bring app to front
                subprocess.run(
                    ["osascript", "-e", f'tell application "{name}" to activate'],
                    capture_output=True,
                )

                # Small delay to let window come to front
                import time

                time.sleep(1)

                # Take screenshot of frontmost window
                result = subprocess.run(
                    ["screencapture", "-o", "-w", str(output_path)], capture_output=True
                )

                if result.returncode == 0 and output_path.exists():
                    print(f"📸 {name} screenshot saved: {output_path}")
                    return str(output_path)

        elif sys.platform == "win32":  # Windows
            # Windows implementation using PowerShell
            for name in possible_names:
                cmd = [
                    "powershell",
                    "-Command",
                    f"""
                    Add-Type -AssemblyName System.Windows.Forms
                    Add-Type -AssemblyName System.Drawing
                    
                    $process = Get-Process | Where-Object {{$_.ProcessName -like '*{name}*' -or $_.MainWindowTitle -like '*{name}*'}} | Select-Object -First 1
                    if ($process -and $process.MainWindowHandle -ne 0) {{
                        [Microsoft.VisualBasic.Interaction]::AppActivate($process.Id)
                        Start-Sleep -Milliseconds 500
                        
                        $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
                        $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
                        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
                        $graphics.CopyFromScreen(0, 0, 0, 0, $bitmap.Size)
                        $bitmap.Save('{output_path}', [System.Drawing.Imaging.ImageFormat]::Png)
                        $graphics.Dispose()
                        $bitmap.Dispose()
                    }}
                    """,
                ]

                result = subprocess.run(cmd, capture_output=True)
                if result.returncode == 0 and output_path.exists():
                    print(f"📸 {name} screenshot saved: {output_path}")
                    return str(output_path)

        else:  # Linux
            # Linux implementation - try to focus window and screenshot
            for name in possible_names:
                # Try to find and focus window
                subprocess.run(["wmctrl", "-a", name], capture_output=True)

                # Take screenshot
                result = subprocess.run(
                    ["gnome-screenshot", "-w", "-f", str(output_path)],
                    capture_output=True,
                )

                if result.returncode == 0 and output_path.exists():
                    print(f"📸 {name} screenshot saved: {output_path}")
                    return str(output_path)

        # If app-specific screenshot failed, fall back to full screen
        print(f"⚠️  Could not capture {app_name} window, taking full screenshot instead")
        return take_screenshot(output_path)

    except Exception as e:
        print(f"❌ App screenshot failed: {e}")
        print(f"⚠️  Falling back to full screenshot")
        return take_screenshot(output_path)


def analyze_screenshot(screenshot_path, custom_prompt=""):
    """
    Analyze screenshot using Gemini Vision API

    Args:
        screenshot_path (str): Path to screenshot file
        custom_prompt (str): Custom prompt for analysis

    Returns:
        str: Analysis result
    """
    try:
        # Import Gemini client
        sys.path.append(str(Path(__file__).parent.parent))
        from src.core.configuration_manager import ConfigurationManager
        from src.services.gemini_client import GeminiClient

        # ConfigurationManager will determine its paths based on its own location
        # in src/core, ensuring it uses the central .summarizer directory.
        config_manager = ConfigurationManager()

        client = GeminiClient(config_manager=config_manager)

        if not client.is_ready():
            print("❌ Gemini API not configured. Run 'summarizer --setup' first.")
            return None

        # Read screenshot file
        screenshot_path = Path(screenshot_path)
        if not screenshot_path.exists():
            print(f"❌ Screenshot file not found: {screenshot_path}")
            return None

        # Prepare prompt
        base_prompt = """
Bu ekran görüntüsünü detaylı olarak analiz et:

1. **Ne görüyorsun?**
   - Açık uygulamalar ve pencereler
   - Ana içerik ve aktiviteler
   - Kullanıcı arayüzü elementleri

2. **Teknik Analiz:**
   - Kullanılan uygulamalar ve araçlar
   - Görünen kod veya teknik içerik
   - Sistem durumu ve bilgileri

3. **Çalışma Bağlamı:**
   - Kullanıcı ne üzerinde çalışıyor olabilir?
   - Hangi görevler yapılıyor?
   - Çalışma akışı nasıl görünüyor?

4. **Öneriler:**
   - Verimliliği artırma önerileri
   - Dikkat çeken noktalar
   - İyileştirme fırsatları

Türkçe ve detaylı bir analiz yap.
        """

        if custom_prompt:
            prompt = f"{base_prompt}\n\nÖzel İstek: {custom_prompt}"
        else:
            prompt = base_prompt

        # Read image as base64
        import base64

        with open(screenshot_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        # Call Gemini with image
        try:
            import google.generativeai as genai

            # Create image part
            image_part = {"mime_type": "image/png", "data": image_data}

            response = client.model.generate_content([prompt, image_part])

            if response and response.text:
                return response.text
            else:
                return "❌ Gemini API'den yanıt alınamadı"

        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return None

    except ImportError:
        print("❌ Gemini client not available")
        return None
    except Exception as e:
        print(f"❌ Screenshot analysis failed: {e}")
        return None


def screenshot_command(args):
    """
    Handle screenshot command with arguments

    Args:
        args (list): Command line arguments
    """
    print("📸 Screenshot Analysis Mode")
    print("=" * 40)

    app_name = None
    custom_prompt = ""

    # Parse arguments
    if len(args) > 0:
        app_name = args[0]
        if len(args) > 1:
            custom_prompt = " ".join(args[1:])

    # Take screenshot
    if app_name and app_name not in ["screenshot", "ss"]:
        print(f"📱 Taking screenshot of {app_name}...")
        screenshot_path = take_app_screenshot(app_name)
    else:
        print("🖥️  Taking full screen screenshot...")
        screenshot_path = take_screenshot()

    if not screenshot_path:
        print("❌ Failed to take screenshot")
        return False

    # Analyze screenshot
    print("🤖 Analyzing screenshot with AI...")
    analysis = analyze_screenshot(screenshot_path, custom_prompt)

    if analysis:
        print("\n" + "=" * 50)
        print("🔍 SCREENSHOT ANALYSIS")
        print("=" * 50)
        print(analysis)
        print("=" * 50)

        # Optionally save analysis
        analysis_path = Path(screenshot_path).with_suffix(".txt")
        try:
            with open(analysis_path, "w", encoding="utf-8") as f:
                f.write(f"Screenshot Analysis - {datetime.now()}\n")
                f.write(f"Screenshot: {screenshot_path}\n")
                f.write("=" * 50 + "\n")
                f.write(analysis)
            print(f"💾 Analysis saved: {analysis_path}")
        except Exception as e:
            print(f"⚠️  Could not save analysis: {e}")

        return True
    else:
        print("❌ Failed to analyze screenshot")
        return False
