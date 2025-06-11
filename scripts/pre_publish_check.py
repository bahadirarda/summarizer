#!/usr/bin/env python3
"""
🔍 Pre-Publish Validation System
================================

Bu script framework'ü publish etmeden önce kritik kontrolleri yapar:
- API key'lerin geçerliliğini test eder
- Temel fonksiyonların çalışıp çalışmadığını kontrol eder
- Version tutarlılığını doğrular
- Git durumunu kontrol eder
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Ana proje klasörünü path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_header(title):
    """Başlık yazdırma"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Adım yazdırma"""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 50)

def print_result(status, message):
    """Sonuç yazdırma"""
    icon = "✅" if status else "❌"
    print(f"   {icon} {message}")
    return status

def test_api_key():
    """API key'in geçerliliğini test et"""
    print_step(1, "Testing API Key Validity")
    
    try:
        # Environment'i yükle
        from src.core.configuration_manager import ConfigurationManager
        config_manager = ConfigurationManager()
        
        # Gemini client'i test et
        from src.services.gemini_client import GeminiClient
        from src.services.request_manager import RequestManager
        
        RequestManager()
        gemini_client = GeminiClient()
        
        # Önce client'in ready olup olmadığını kontrol et
        if not gemini_client.is_ready():
            return print_result(False, "Gemini client is not ready - API key missing or invalid")
        
        # Basit bir test çağrısı yap
        test_response = gemini_client.generate_summary("Test message for API validation")
        
        # Response'da hata mesajı olup olmadığını kontrol et
        if test_response and "AI özeti alınamadı" in test_response:
            return print_result(False, f"API key test failed - {test_response}")
        elif test_response and len(test_response) > 20 and "test" in test_response.lower():
            return print_result(True, "API key is valid and working")
        else:
            return print_result(False, f"API key test failed - unexpected response: {test_response}")
            
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "expired" in error_msg.lower():
            return print_result(False, f"API key is EXPIRED or INVALID: {error_msg}")
        else:
            return print_result(False, f"API test failed: {error_msg}")

def test_core_functionality():
    """Temel fonksiyonların çalışıp çalışmadığını test et"""
    print_step(2, "Testing Core Functionality")
    
    try:
        # Version manager test
        from src.utils.version_manager import VersionManager
        vm = VersionManager(project_root)
        current_version = vm.get_current_version()
        print_result(True, f"Version Manager OK - Current: v{current_version}")
        
        # Changelog manager test
        from src.utils.json_changelog_manager import JsonChangelogManager
        jcm = JsonChangelogManager(project_root)
        entries = jcm.get_entries(limit=1)
        print_result(True, f"Changelog Manager OK - {len(entries)} entries found")
        
        # File tracker test
        from src.utils.file_tracker import get_changed_files_since_last_run
        changed_files = get_changed_files_since_last_run(project_root)
        print_result(True, f"File Tracker OK - {len(changed_files)} files tracked")
        
        return True
        
    except Exception as e:
        return print_result(False, f"Core functionality test failed: {e}")

def validate_version_consistency():
    """Version tutarlılığını kontrol et"""
    print_step(3, "Validating Version Consistency")
    
    try:
        # package.json version
        package_json = project_root / "package.json"
        with open(package_json) as f:
            package_data = json.load(f)
            package_version = package_data.get('version', 'unknown')
        
        # Version manager version
        from src.utils.version_manager import VersionManager
        vm = VersionManager(project_root)
        vm_version = vm.get_current_version()
        
        if package_version == vm_version:
            return print_result(True, f"Version consistency OK - v{package_version}")
        else:
            return print_result(False, f"Version mismatch! package.json: v{package_version}, Version Manager: v{vm_version}")
            
    except Exception as e:
        return print_result(False, f"Version validation failed: {e}")

def check_git_status():
    """Git durumunu kontrol et"""
    print_step(4, "Checking Git Status")
    
    try:
        # Uncommitted changes var mı?
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=project_root)
        
        if result.stdout.strip():
            return print_result(False, "Uncommitted changes found! Please commit all changes before publishing.")
        
        # Remote ile sync mi?
        result = subprocess.run(['git', 'status', '-uno'], 
                              capture_output=True, text=True, cwd=project_root)
        
        if "ahead" in result.stdout:
            return print_result(False, "Local commits not pushed! Please push to remote before publishing.")
        
        return print_result(True, "Git status clean and synced")
        
    except Exception as e:
        return print_result(False, f"Git status check failed: {e}")

def check_required_files():
    """Gerekli dosyaların varlığını kontrol et"""
    print_step(5, "Checking Required Files")
    
    required_files = [
        "README.md",
        "package.json", 
        "requirements.txt",
        ".env.example",
        "summarizer.py",
        "src/main.py"
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print_result(True, f"{file_path} exists")
        else:
            print_result(False, f"{file_path} MISSING!")
            all_good = False
    
    # .env dosyasının gitignore'da olduğunu kontrol et
    gitignore_path = project_root / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            gitignore_content = f.read()
            if ".env" in gitignore_content:
                print_result(True, ".env properly ignored in .gitignore")
            else:
                print_result(False, ".env not found in .gitignore!")
                all_good = False
    
    return all_good

def generate_report():
    """Validation raporu oluştur"""
    print_header("PRE-PUBLISH VALIDATION REPORT")
    
    all_tests = []
    
    # Test 1: API Key
    all_tests.append(test_api_key())
    
    # Test 2: Core Functionality
    all_tests.append(test_core_functionality())
    
    # Test 3: Version Consistency
    all_tests.append(validate_version_consistency())
    
    # Test 4: Git Status
    all_tests.append(check_git_status())
    
    # Test 5: Required Files
    all_tests.append(check_required_files())
    
    # Sonuç
    print_header("FINAL RESULT")
    
    passed_tests = sum(all_tests)
    total_tests = len(all_tests)
    
    if all(all_tests):
        print("🎉 ALL TESTS PASSED! Framework is ready for publishing!")
        print(f"✅ {passed_tests}/{total_tests} tests successful")
        return True
    else:
        print("❌ SOME TESTS FAILED! Do not publish until all issues are resolved!")
        print(f"⚠️  {passed_tests}/{total_tests} tests successful")
        print("\n🔧 Please fix the issues above before publishing.")
        return False

def main():
    """Ana fonksiyon"""
    print_header("SUMMARIZER FRAMEWORK - PRE-PUBLISH VALIDATION")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Project: {project_root}")
    
    success = generate_report()
    
    print(f"\n{'='*60}")
    if success:
        print("🚀 Ready to publish!")
        sys.exit(0)
    else:
        print("🛑 Publishing blocked due to validation failures!")
        sys.exit(1)

if __name__ == "__main__":
    main()
