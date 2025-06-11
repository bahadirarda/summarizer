# src/services/gemini_client.py
import logging
import os
from typing import List, Dict, Optional

import google.generativeai as genai  # Gerçek Gemini kütüphanesi

from src.core.configuration_manager import ConfigurationManager # Added import


class GeminiClient:
    def __init__(self, config_manager: ConfigurationManager):  # Added config_manager parameter
        self.logger = logging.getLogger(__name__)
        self.config_manager = config_manager # Store config_manager instance
        self.api_key = self.config_manager.get_api_key() # Get API key from ConfigurationManager
        self.model = None
        self._is_configured = False

        if self.api_key:
            try:
                # Configure Gemini API
                genai.configure(api_key=self.api_key)

                # Initialize the model
                self.model = genai.GenerativeModel("gemini-1.5-flash")

                self._is_configured = True
                self.logger.info(
                    "GeminiClient başarıyla başlatıldı. "
                    "Gerçek AI model entegrasyonu aktif."
                )
            except Exception as e:
                self.logger.error(f"Gemini API konfigürasyonu başarısız: {e}")
                self.model = None
                self._is_configured = False
        else:
            self.logger.warning(
                "GEMINI_API_KEY ortam değişkeni bulunamadı. "
                "GeminiClient AI özetleri oluşturamayacak ancak sistem "
                "entegrasyonu için kaydedilecek. "
                "Lütfen .env dosyasında veya sistem ortam değişkenlerinde ayarlayın.")

        # Always register to RequestManager (even without API key)
        from .request_manager import RequestManager

        request_manager = RequestManager()
        request_manager.register_client("GeminiClient", self)

    def is_ready(self) -> bool:
        """İstemcinin API anahtarı ve model ile düzgün yapılandırılıp
        yapılandırılmadığını döndürür."""
        return self._is_configured and self.model is not None

    def generate_summary(
        self, text_prompt: str, changed_files: Optional[list] = None
    ) -> str:
        """Verilen metin veya dosya değişikliklerine göre
        detaylı anlamsal özet oluşturur."""
        # Re-fetch API key from ConfigurationManager and re-configure before each call
        self.api_key = self.config_manager.get_api_key()
        
        # Log the API key being used (or if it's None)
        if self.api_key:
            self.logger.info(f"Attempting to use API key ending with: ...{self.api_key[-4:]}")
        else:
            self.logger.error("API key from ConfigurationManager is None.")

        if not self.api_key:
            self.logger.error(
                "GEMINI_API_KEY, ConfigurationManager aracılığıyla bulunamadı. Özet oluşturulamıyor."
            )
            return "[GEMINI_API_KEY bulunamadı (ConfigurationManager)]"
        
        try:
            genai.configure(api_key=self.api_key)
            # Re-initialize the model if it wasn't configured or if the key might have changed
            if not self.model or not self._is_configured:
                 self.model = genai.GenerativeModel("gemini-2.0-flash") # Changed to 2.0-flash
                 self._is_configured = True # Assume configuration is successful if no exception
        except Exception as e:
            self.logger.error(f"Gemini API yeniden konfigürasyonu başarısız: {e}")
            self._is_configured = False # Mark as not configured on error
            # self.model will remain None or its previous state
            return f"[Gemini API yeniden konfigürasyonu başarısız: {e}]"


        if not self.is_ready():
            self.logger.error(
                "GeminiClient düzgün yapılandırılmamış. Özet oluşturulamıyor."
            )
            return "[GeminiClient yapılandırılmamış veya API anahtarı eksik]"

        try:
            # Dosya tiplerini analiz et
            file_categories = (self._analyze_file_types(
                changed_files) if changed_files else {})

            # Dosya içeriklerini geçici olarak oku (sadece prompt için)
            file_contents = (
                self._get_file_contents_for_analysis(changed_files)
                if changed_files
                else ""
            )

            # İçeriği truncate et (Gemini token limitine uygun)
            file_contents = self._truncate_content_for_prompt(
                file_contents, max_chars=6000
            )

            # Gelişmiş prompt oluştur
            prompt_intro = (
                "Sen bir senior kod analisti ve teknik yazarsın. "
                "Aşağıdaki yazılım projesindeki değişiklikleri DETAYLI olarak analiz et:"
            )
            
            file_summary = (
                self._format_files_for_analysis(changed_files, file_categories)
                if changed_files else "Genel proje değişiklikleri"
            )
            
            full_prompt = f"""
{prompt_intro}

## Değişiklik Bağlamı:
{text_prompt}

## Değişen Dosyalar:
{file_summary}

## Dosya İçerikleri (Analiz için):
{file_contents}

## ANALİZ GÖREVİ:
Türkçe olarak KAPSAMLI ve ANALİTİK bir özet oluştur. Özet şunları içermeli:

### 1. YAPISAL ANALİZ:
- Hangi sistem bileşenleri ve katmanlar etkilendi?
- Mimari değişikliklerin etkisi nedir?
- Kod organizasyonunda hangi iyileştirmeler yapıldı?

### 2. İŞLEVSEL ETKİ:
- Hangi özellikler eklendi, değiştirildi veya kaldırıldı?
- Kullanıcı deneyimi nasıl etkilendi?
- Performans, güvenlik veya güvenilirlik üzerindeki etkiler?

### 3. TEKNİK DERINLIK:
- Hangi tasarım desenleri uygulandı veya değiştirildi?
- Kod kalitesi ve sürdürülebilirlik nasıl gelişti?
- Yeni bağımlılıklar veya teknolojiler eklendi mi?

### 4. SONUÇ YORUMU:
- Bu değişikliklerin uzun vadeli değeri ve etkisi nedir?
- Projenin teknik borcu nasıl etkilendi?
- Gelecekteki geliştirmelere nasıl hazırlık yapıldı?

ÖNEMLI:
- Yanıtını tam olarak yukarıda belirtilen Markdown başlıklarını (### 1. YAPISAL ANALİZ:, ### 2. İŞLEVSEL ETKİ:, vb.) kullanarak yapılandır.
- Her bölüm için ayrıntılı ve spesifik teknik bilgiler ver.
- Genel ifadelerden kaçın; kod değişikliklerinin gerçek etkisini analiz et.
"""

            # Gemini API çağrısı
            response = self.model.generate_content(full_prompt)

            if response.text:
                self.logger.info("Gemini'den başarıyla AI özeti alındı.")
                return response.text.strip()
            else:
                self.logger.warning("Gemini'den boş yanıt alındı.")
                return "AI özeti alınamadı - boş yanıt döndürüldü."

        except Exception as e:
            self.logger.error(f"Gemini API çağrısında hata: {e}")
            # Fallback to a descriptive summary
            if changed_files:
                return f"Kod tabanında güncellemeler yapıldı. Değişen dosyalar: {', '.join(changed_files)}. (AI özeti alınamadı: {str(e)})"
            else:
                return f"Genel bir güncelleme yapıldı. (AI özeti alınamadı: {str(e)})"

    def _analyze_file_types(self, files: List[str]) -> Dict[str, List[str]]:
        """Dosyaları kategorilere ayırarak anlamsal analiz için hazırlar"""
        categories = {
            "core_logic": [],  # Ana iş mantığı
            "configuration": [],  # Konfigürasyon dosyaları
            "user_interface": [],  # GUI ve kullanıcı arayüzü
            "data_management": [],  # Veri yönetimi ve storage
            "utilities": [],  # Yardımcı araçlar
            "services": [],  # Servis katmanı
            "tests": [],  # Test dosyaları
            "documentation": [],  # Dokümantasyon
        }

        for file in files:
            file_lower = file.lower()

            if any(
                x in file_lower
                for x in ["config", "settings", ".json", ".yaml", ".env"]
            ):
                categories["configuration"].append(file)
            elif any(x in file_lower for x in ["gui", "ui", "interface", "frontend"]):
                categories["user_interface"].append(file)
            elif any(x in file_lower for x in ["manager", "service", "client", "api"]):
                categories["services"].append(file)
            elif any(x in file_lower for x in ["util", "helper", "tool"]):
                categories["utilities"].append(file)
            elif any(x in file_lower for x in ["test", "spec"]):
                categories["tests"].append(file)
            elif any(x in file_lower for x in ["readme", "changelog", ".md", "doc"]):
                categories["documentation"].append(file)
            elif any(x in file_lower for x in ["data", "storage", "db", "json"]):
                categories["data_management"].append(file)
            else:
                categories["core_logic"].append(file)

        # Boş kategorileri temizle
        return {k: v for k, v in categories.items() if v}

    def _format_files_for_analysis(
        self, files: List[str], categories: Dict[str, List[str]]
    ) -> str:
        """Dosyaları anlamsal analiz için formatlar"""
        if not files:
            return "Dosya değişikliği yok"

        formatted_parts = []

        for category, file_list in categories.items():
            if file_list:
                category_names = {
                    "core_logic": "🧠 Ana İş Mantığı",
                    "configuration": "⚙️ Konfigürasyon",
                    "user_interface": "🎨 Kullanıcı Arayüzü",
                    "data_management": "📊 Veri Yönetimi",
                    "utilities": "🔧 Yardımcı Araçlar",
                    "services": "🚀 Servis Katmanı",
                    "tests": "🧪 Test Dosyaları",
                    "documentation": "📚 Dokümantasyon",
                }

                category_display = category_names.get(
                    category, category.title())
                files_display = ", ".join(file_list)
                formatted_parts.append(f"{category_display}: {files_display}")

        return "\n".join(formatted_parts)

    def _get_file_contents_for_analysis(
        self, files: List[str], max_lines_per_file: int = 100
    ) -> str:
        """
        Dosya içeriklerini geçici olarak analiz için okur.
        Çok büyük dosyalar için truncate eder.
        """
        from pathlib import Path

        contents = []
        project_root = Path.cwd()

        for file_path in files:
            try:
                full_path = project_root / file_path
                if not full_path.exists():
                    continue

                # Sadece metin dosyalarını oku
                if not file_path.endswith(
                    (
                        ".py",
                        ".js",
                        ".ts",
                        ".jsx",
                        ".tsx",
                        ".md",
                        ".txt",
                        ".json",
                        ".yaml",
                        ".yml",
                    )
                ):
                    contents.append(
                        f"\n--- {file_path} ---\n[Binary/Non-text file - skipped]")
                    continue

                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                # Çok büyük dosyaları truncate et
                if len(lines) > max_lines_per_file:
                    truncated_msg = (
                        f"\n... [Truncated {len(lines) - max_lines_per_file} "
                        f"lines] ...\n"
                    )
                    truncated_lines = (
                        lines[:max_lines_per_file // 2]
                        + [truncated_msg]
                        + lines[-max_lines_per_file // 2:]
                    )
                    file_content = "".join(truncated_lines)
                else:
                    file_content = "".join(lines)

                contents.append(f"\n--- {file_path} ---\n{file_content}")

            except Exception as e:
                self.logger.warning(
                    f"Could not read file {file_path} for analysis: {e}"
                )
                contents.append(
                    f"\n--- {file_path} ---\n[Error reading file: {e}]")

        return "\n".join(contents)

    def _truncate_content_for_prompt(
            self,
            content: str,
            max_chars: int = 8000) -> str:
        """
        Prompt boyutunu kontrol altında tutmak için içeriği kısaltır.
        """
        if len(content) <= max_chars:
            return content

        # İlk ve son kısımları al, ortayı truncate et
        first_part = content[: max_chars // 2]
        last_part = content[-max_chars // 2:]

        return (
            f"{first_part}\n\n... [Content truncated for analysis] ...\n\n{last_part}")
