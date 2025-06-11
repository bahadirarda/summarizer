#!/usr/bin/env python3
"""
🔑 API Key Management Helper
============================

Bu script API key yönetimini kolaylaştırır:
- Mevcut key'in durumunu kontrol eder
- Yeni key kurulumu yapar
- Key geçerliliğini test eder
"""

import os
import sys
from pathlib import Path

# Ana proje klasörünü path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.configuration_manager import ConfigurationManager # Added

# Global ConfigurationManager instance
config_manager = ConfigurationManager() # Added

def test_current_key():
    """Mevcut API key'i test et"""
    print("🔍 Testing current API key...")
    
    try:
        from src.services.gemini_client import GeminiClient
        # from src.services.request_manager import RequestManager # No longer directly needed here
        
        # RequestManager() # No longer directly needed here
        
        # Test çağrısı
        # Pass the global config_manager to GeminiClient
        client = GeminiClient(config_manager) # Modified
        
        # Önce client'in hazır olup olmadığını kontrol et
        if not client.is_ready():
            print("❌ API key is not configured or invalid!")
            return False
        
        # Gerçek test çağrısı yap
        response = client.generate_summary("API key validation test")
        
        # Response'da error message olup olmadığını kontrol et
        if response and "AI özeti alınamadı" in response:
            print("❌ API key test failed - AI summary could not be generated")
            print(f"   Response: {response}")
            return False
        elif response and len(response) > 20 and "test" in response.lower():
            print("✅ API key is working!")
            return True
        else:
            print("❌ API key test failed - unexpected or no response")
            print(f"   Response: {response}")
            return False
            
    except Exception as e:
        error_str = str(e)
        if "API_KEY_INVALID" in error_str or "expired" in error_str.lower():
            print("❌ API key is EXPIRED or INVALID!")
            print(f"   Error: {e}")
        else:
            print(f"❌ API test failed: {e}")
        return False

def setup_new_key():
    """Yeni API key kurulumu"""
    print("\n🔑 Setting up new API key...")
    print("📍 Go to: https://makersuite.google.com/app/apikey")
    print("📋 Steps:")
    print("   1. Create a new API key")
    print("   2. Copy the key")
    print("   3. Paste it below")
    
    new_key = input("\n🔐 Enter your new Gemini API key: ").strip()
    
    if not new_key:
        print("❌ No key entered!")
        return False
    
    # Basic validation, can be enhanced in ConfigurationManager if needed
    if not new_key.startswith("AIza"):
        print("❌ Invalid key format! Gemini keys should start with 'AIza'")
        return False
    
    # ConfigurationManager aracılığıyla API key'i güncelle
    try:
        config_manager.set_api_key(new_key)
        config_manager.save_configuration() # Ensure settings are saved to user_settings.json and exported to .env
        print("✅ API key updated via ConfigurationManager.")
        
        # Test et
        print("\n🧪 Testing new API key...")
        if test_current_key(): # test_current_key will now use the updated key from config_manager
            print("🎉 New API key is working perfectly!")
            return True
        else:
            print("❌ New API key test failed!")
            return False
    except Exception as e:
        print(f"❌ Error updating API key via ConfigurationManager: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("🔑 Summarizer Framework - API Key Manager")
    print("=" * 50)
    
    # Mevcut key'i test et
    if test_current_key():
        print("\n✨ Current API key is working fine!")
        choice = input("\n❓ Do you want to update it anyway? (y/N): ").lower()
        if choice != 'y':
            print("👍 Keeping current key.")
            return
    
    # Yeni key kurulumu
    if setup_new_key():
        print("\n✅ API key setup completed successfully!")
    else:
        print("\n❌ API key setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
