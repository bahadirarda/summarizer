# 🚀 Summarizer Framework
> Akıllı özetleme ve doküman analiz aracı.  Gelişmiş CLI ve GUI desteği ile hızlı ve verimli doküman işleme.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son değişiklikler, kullanıcı deneyimini iyileştiren yeni özellikler,  kod tabanının sürdürülebilirliğini artıran mimari iyileştirmeler ve  geliştirme süreçlerini destekleyen yardımcı araçların eklenmesini içermektedir. Google Gemini API entegrasyonu güvenlik ve performans iyileştirmeleri sağlamıştır.  Gelecekteki geliştirmeler için roadmap hazırlanmış olup, otomatik güncelleme mekanizması ve kişisel bilgi havuzunun oluşturulması planlanmaktadır.


## ✨ Özellikler
* **Akıllı Özetleme:**  Uzun dokümanları özetler.
* **Komut Satırı Arayüzü (CLI):**  Kolay ve hızlı doküman işleme.  `screenshot` ve `ss` komutlarıyla ekran görüntüsü alma. `--setup`, `--gui`, `--status` komutlarıyla konfigürasyon ve sistem durumu yönetimi.
* **Grafiksel Kullanıcı Arayüzü (GUI):**  Kullanıcı dostu konfigürasyon seçenekleri.
* **Çoklu Uygulama Desteği:**  Ekran görüntüsü alma işlemi Chrome, Firefox ve VS Code gibi uygulamalar için özelleştirilebilir.
* **Google Gemini API Entegrasyonu:**  Gelişmiş metin oluşturma ve analiz yetenekleri.
* **Değişiklik Günlüğü Yönetimi:**  Otomatik değişiklik günlüğü güncelleme.
* **Demo Framework Analizi:**  Proje analizi ve changelog oluşturma için yardımcı araç.


## Değişen Dosyalar:
`summarizer.py`, `features` dizini altındaki dosyalar (`parameter_checker.py`, `terminal_commands.py`, `__init__.py`), `src/main.py`, `src/core/configuration_manager.py`, `src/utils` dizini altındaki dosyalar (`version_manager.py`, `git_manager.py`, `changelog_updater.py`), `tests/test_main.py`, `src/services/gemini_client.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

* **Etkilenen Bileşenler ve Katmanlar:** Değişiklikler, Summarizer Framework'ün neredeyse tüm katmanlarını etkilemiştir.  `summarizer.py` (ana giriş noktası ve CLI), `features` dizini (özellikler: parametre kontrolü, terminal komutları, GUI), `src/main.py` (özetleme mantığı), `src/core/configuration_manager.py` (konfigürasyon yönetimi), `src/utils` dizini (yardımcı araçlar: sürüm yönetimi, Git entegrasyonu, değişiklik günlüğü güncelleme), `tests/test_main.py` (testler) ve `src/services/gemini_client.py` (Gemini API ile etkileşim) dosyaları doğrudan etkilenmiştir.

* **Mimari Değişikliklerin Etkisi:**  Mimari, daha modüler ve genişletilebilir bir yapıya doğru evrilmiştir.  `features` dizini, özelliklerin bağımsız olarak geliştirilmesini ve sürdürülmesini kolaylaştırır. `CallableModule` sınıfının `summarizer.py` içinde kullanımı, sistemin hem komut satırı aracı hem de Python kütüphanesi olarak kullanılmasını mümkün kılar.  Google Gemini API entegrasyonu, Dependency Injection tasarım deseni ile daha modüler ve test edilebilir bir yapı oluşturmuştur.

* **Kod Organizasyonundaki İyileştirmeler:** Kod, `features` dizini altında modüler olarak düzenlenmiştir. Bu, okunabilirliği, sürdürülebilirliği ve bakımı kolaylaştırır. API anahtarının `ConfigurationManager` üzerinden yönetilmesi, güvenliği ve sürdürülebilirliği artırmıştır.


### 2. İŞLEVSEL ETKİ:

* **Eklenen, Değiştirilen veya Kaldırılan Özellikler:**  Ekran görüntüsü alma (`screenshot`, `ss` komutları) özelliği eklenmiştir ve farklı uygulamalar için özelleştirilebilir hale getirilmiştir. GUI tabanlı konfigürasyon desteği (`--gui`) eklenmiştir.  `--setup` ve `--status` komutları eklenerek konfigürasyon ve sistem durumu yönetimi kolaylaştırılmıştır.  Değişiklik günlüğü güncelleme işlemi iyileştirilmiş ve otomatikleştirilmiştir.  `demo_framework_analysis` fonksiyonu eklenerek otomatik changelog girişi oluşturma özelliği eklenmiştir.  `GeminiClient` sınıfına `generate_simple_text` fonksiyonu eklenerek basit metin oluşturma yeteneği sağlanmıştır.

* **Kullanıcı Deneyiminin Etkilenmesi:** Kullanıcı deneyimi, yeni komutlar ve GUI desteğiyle önemli ölçüde iyileştirilmiştir.  Kullanıcılar daha fazla seçeneğe sahiptir ve konfigürasyonu daha kolay yönetebilirler.

* **Performans, Güvenlik veya Güvenilirlik Üzerindeki Etkiler:** Ekran görüntüsü alma işleminin performansı, alınacak ekran görüntüsünün boyutuna ve uygulamaya bağlı olarak değişebilir.  API anahtarının `.env` dosyasından veya ortam değişkenlerinden alınması güvenliği artırmıştır.  Yeni özelliklerin güvenlik açıkları açısından test edilmesi ve güvenilirliğinin sağlanması önemlidir.  `demo_framework_analysis` fonksiyonunun performans, güvenlik ve güvenilirlik üzerindeki etkisi ihmal edilebilir düzeydedir.


### 3. TEKNİK DERINLIK:

* **Tasarım Desenleri:** "Command Pattern" genişletilmiş olarak kullanılmıştır. Her terminal komutu bir komut nesnesi olarak temsil edilir.  Dependency Injection tasarım deseni, `GeminiClient` sınıfı ve `ConfigurationManager` sınıfı arasında uygulanmıştır.

* **Kod Kalitesi ve Sürdürülebilirlik:** Kod kalitesi, modülerlik ve okunabilirliğin iyileştirilmesiyle artmıştır.  Yorumların daha detaylı olması ve kodun daha iyi yapılandırılması, sürdürülebilirliği artırır.  API anahtarının merkezi yönetimi ve hata işleme mekanizmalarının eklenmesi kod kalitesini iyileştirmiştir.

* **Yeni Bağımlılıklar veya Teknolojiler:** `google.generativeai` kütüphanesi Google Gemini API entegrasyonu için eklenmiştir.  `changelog_updater.py` muhtemelen JSON dosyası yönetimi için bir kütüphane kullanmaktadır.  Mevcut bağımlılıkların güncellenmiş versiyonlarının kullanımı da olasıdır.


### 4. SONUÇ YORUMU:

* **Uzun Vadeli Değer ve Etki:** Bu değişiklikler, daha kullanıcı dostu bir arayüz, gelişmiş işlevsellik ve daha iyi sürdürülebilir bir kod tabanı sunmaktadır.  Ekran görüntüsü alma özelliği ve Google Gemini API entegrasyonu önemli katkılardır.  Modüler tasarım, gelecekte yeni özelliklerin eklenmesini kolaylaştıracaktır.

* **Teknik Borcun Etkilenmesi:** Kodun daha iyi yapılandırılması ve dokümantasyonun iyileştirilmesiyle teknik borç azalmıştır.  Ancak, `TODO` yorumlarında belirtilen otomatik güncelleme mekanizması ve kişisel know-how havuzunun oluşturulması gibi konular gelecekteki geliştirmeler için önemlidir.

* **Gelecekteki Geliştirmelere Hazırlık:** Modüler tasarım ve genişletilebilir mimari, gelecekteki geliştirmelere hazırlık olarak önemli bir adımdır. Yeni özelliklerin eklenmesi daha kolay ve daha az riskli hale gelmiştir.  `RequestManager` entegrasyonu, farklı servislerle kolay entegrasyon olanağı sağlayacaktır.

## 🛠️ Kurulum (Installation)

1.  **Depo Klonlama ve Sanal Ortam Kurulumu:**
    ```bash
    git clone https://github.com/bahadirarda/summarizer # Veya kendi fork adresiniz
    cd summarizer
    python -m venv venv
    source venv/bin/activate  # macOS/Linux için
    # venv\Scripts\activate    # Windows için
    ```

2.  **Gerekli Paketlerin Yüklenmesi:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Summarizer CLI Kurulumu:**
    `summarizer` komutunu terminalinizden doğrudan çalıştırabilmek için:
    ```bash
    python summarizer.py --install-terminal
    ```
    Bu komut, `summarizer`'ı sistem genelinde kullanılabilir hale getirecektir.

4.  **(Opsiyonel) GUI Bileşenlerinin Kurulumu:**
    Eğer GUI arayüzünü kullanmak isterseniz:
    ```bash
    python summarizer.py --install-gui
    ```

## 🚀 Kullanım (Usage)

`summarizer` CLI kurulduktan sonra, terminalinizde aşağıdaki gibi kullanabilirsiniz:

**Temel Komutlar:**
```bash
# Proje analizi başlatma (temel)
summarizer

# Versiyon bilgisini ve özellikleri gösterme
summarizer --version

# API anahtarları ve yapılandırma için interaktif kurulum
summarizer --setup

# GUI yapılandırma arayüzünü başlatma
summarizer --gui

# Mevcut yapılandırma durumunu kontrol etme
summarizer --check

# Sistem durumunu gösterme
summarizer --status
```

**Ekran Görüntüsü Analizi:**
```bash
# Tam ekran analizi
summarizer screenshot

# Belirli bir pencere analizi (örneğin Chrome)
summarizer ss chrome
```

**Yardım:**
Daha fazla komut ve seçenek için yardım mesajını görüntüleyebilirsiniz:
```bash
summarizer --help
```

**Python İçinde Kullanım:**
`summarizer`'ı bir Python betiği içinde de kullanabilirsiniz (projenizin ana dizininde olduğunuzdan emin olun):
```python
import summarizer

# Mevcut projeyi analiz et. 
# Bu kullanım `summarizer --help` çıktısındaki örneğe dayanmaktadır.
# `summarizer.py` dosyasının kendisinin veya paketinin `summarizer()` çağrısını uygun şekilde ele aldığı varsayılır.
summarizer() 
```

## 📁 Project Structure

```
project.110620251156/
├── src/                    # Source code
├── public/                # Static assets
├── package.json           # Dependencies
├── README.md             # This file (auto-generated)
├── CHANGELOG.md          # Change history
└── .summarizer/          # AI tracking (hidden)
```

## 🔧 Configuration

### Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit with your actual values
nano .env
```

See `.env.example` for all available configuration options.

### Summarizer Framework

This project uses the Summarizer Framework for automated change tracking:

```bash
# Run analysis
python summarizer.py

# GUI configuration
python summarizer.py --gui

# Check status
python summarizer.py --status
```



## 📈 Development Activity

This project is just getting started! Run `summarizer` to begin tracking development activity.

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

## 📜 Lisans (License)

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: [GitHub](https://github.com/bahadirarda/summarizer)
- **Issues**: [Report Issues](https://github.com/bahadirarda/summarizer/issues)
- **Discussions**: [Join Discussions](https://github.com/bahadirarda/summarizer/discussions)

---

**Last updated**: June 20, 2025 by Summarizer Framework v12.5.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
