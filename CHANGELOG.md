# Changelog

Bu dosya otomatik olarak generate edilmiştir.
Düzenlemeler için `changelog.json` dosyasını kullanın.

## 2025-06-11 17:04:12

Bu kod değişiklikleri, AI destekli bir özetleyici framework'ünün çeşitli bileşenlerini etkileyen kapsamlı bir revizyonu yansıtmaktadır.  Yapısal olarak, konfigürasyon yönetimi (`src/config.py`, `src/core/configuration_manager.py`, `src/gui/modern_config_gui.py`) geliştirilmiş, loglama daha esnek hale getirilmiş ve hata yönetimi iyileştirilmiştir. İşlevsel olarak, Gemini API entegrasyonu (`src/services/gemini_client.py`) eklenmiş ve  `src/main_fixed.py` dosyasındaki ana iş mantığında hata düzeltmeleri yapılmıştır.  Teknik olarak,  `urllib3` kütüphanesinden gelen uyarılar bastırılmış,  hata ayıklama ve loglama geliştirilmiş, dosya işlemede  büyük dosyalar için kırpma mekanizması eklenmiştir. Sonuç olarak, kod daha sağlam, sürdürülebilir ve genişletilebilir hale gelmiştir.  Teknik borç kısmen azalmış ve gelecekteki genişletmeler için daha sağlam bir temel oluşturulmuştur.  Özellikle, Gemini API entegrasyonu yeni bir özellik eklerken,  hata yönetimindeki iyileştirmeler güvenilirliği artırmaktadır.

**Değişen Dosyalar:** src/config.py, src/main_fixed.py, src/test_line_tracking.py, src/main.py, src/main_broken.py, src/core/__init__.py, src/core/configuration_manager.py, src/utils/json_changelog_manager.py, src/utils/file_tracker.py, src/utils/changelog_updater.py, src/gui/__init__.py, src/gui/modern_config_gui.py, src/services/request_manager.py, src/services/gemini_client.py
**Etki Seviyesi:** High
**Değişiklik Tipi:** Config
**Satır Değişiklikleri:** +491
**Etiketler:** configuration-manager, client, services, --init--, core, test-line-tracking, file-tracker, modern-config-gui, utils, gui

---

## 2025-06-11 16:09:40

## Değişiklik Analizi Özeti:

Bu yazılım projesindeki değişiklikler, konfigürasyon yönetimi, loglama, kullanıcı arayüzü ve Gemini AI entegrasyonu gibi çeşitli alanları kapsamaktadır.  Değişiklikler, konfigürasyonun `src/config.py` dosyasında  `DevelopmentConfig` ve `ProductionConfig` sınıflarıyla daha esnek hale getirilmesi, loglama mekanizmasının iyileştirilmesi ve farklı ortamlar için özelleştirilmesiyle başlıyor.  `src/main.py` ve `src/services/gemini_client.py` dosyalarında yapılan değişiklikler, Gemini AI entegrasyonunu içerir ve ortam değişkenlerine bağlı olarak çalışabilirliği sağlar.  Yeni bir `RequestManager`  ve  `ConfigurationManager` sınıfı ile konfigürasyon ve istek yönetimi daha modüler hale getirilmiştir. `src/utils` altındaki yardımcı araçlar dosya izleme ve değişiklik günlüğü güncellemelerini iyileştirmektedir.  Sonuç olarak, proje daha yapılandırılmış, sürdürülebilir ve genişletilebilir hale gelmiştir.  Teknik borç kısmen azalırken,  Gemini API entegrasyonu yeni bir bağımlılık eklemiştir. Gelecekteki geliştirmeler için sağlam bir temel oluşturulmuştur.

**Değişen Dosyalar:** src/config.py, src/__init__.py, src/test_line_tracking.py, src/main.py, src/core/__init__.py, src/core/configuration_manager.py, src/utils/__init__.py, src/utils/json_changelog_manager.py, src/utils/file_tracker.py, src/utils/changelog_updater.py, src/gui/__init__.py, src/gui/modern_config_gui.py, src/services/request_manager.py, src/services/__init__.py, src/services/gemini_client.py
**Etki Seviyesi:** High
**Değişiklik Tipi:** Config
**Satır Değişiklikleri:** +2 -2
**Etiketler:** json-changelog-manager, changelog-updater, api, services, modern-config-gui, config, core, file-tracker, client, --init--

---
