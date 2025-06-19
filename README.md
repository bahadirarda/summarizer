# 🚀 Summarizer Framework
> Akıllı özetleme ve ekran görüntüsü alma yetenekleri sunan, komut satırı ve GUI arayüzüne sahip güçlü bir framework.


## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son değişiklikler komut satırı arayüzünün zenginleştirilmesini,  GUI kurulumunun iyileştirilmesini ve kodun modülerliğinin artırılmasını hedeflemiştir.  AI destekli özetleme özelliği (Gemini API entegrasyonu) mevcuttur ve sürekli iyileştirilmektedir.  Gelecek geliştirme planları arasında sesli komut desteği ve otomatik güncelleme bulunmaktadır.


## ✨ Özellikler
* 📄  Metin özetleme (AI destekli Gemini API entegrasyonu)
* 📸 Uygulamaya özel ekran görüntüsü alma (`summarizer ss chrome`, `summarizer ss firefox`, `summarizer ss code`)
* 💻 Komut satırı arayüzü (CLI)
* 🖥️ Grafik kullanıcı arayüzü (GUI) kurulumu ve konfigürasyonu
* ⚙️ Interaktif kurulum (`summarizer --setup`)
* ✨  (Gelecek) Sesli komut sistemi
* 🔄 (Gelecek) Otomatik güncelleme


## Değişen Dosyalar:
`install_gui.py`, `src/main.py`, `summarizer.py`, `src/core/configuration_manager.py`, `src/utils/git_manager.py`, `src/services/gemini_client.py`, `src/utils/changelog_updater.py`, `scripts/run_ci_checks.py`, `features` klasörü altındaki modüller (kesin içerik bilinmiyor ancak `parameter_checker`, `screenshot`, `terminal_commands`, `gui_installer` gibi modüller olduğu tahmin ediliyor).



## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

* **Etkilenen Bileşenler ve Katmanlar:** Değişiklikler, Summarizer Framework'ün neredeyse tüm katmanlarını etkilemiştir.  Giriş katmanı (`summarizer.py`), işlevsellik katmanı (`src/main.py`, `features` klasörü), konfigürasyon yönetimi (`src/core/configuration_manager.py`),  API entegrasyonu (`src/services/gemini_client.py`),  Git entegrasyonu (`src/utils/git_manager.py`),  değişiklik günlüğü güncelleme (`src/utils/changelog_updater.py`) ve CI süreçleri (`scripts/run_ci_checks.py`)  hepsi değişikliklerden etkilenmiştir. GUI kurulumu da (`install_gui.py`) güncellenmiştir.

* **Mimari Değişikliklerin Etkisi:**  Mimari açısından bakıldığında, değişiklikler katmanlar arası etkileşimleri değiştirmiştir.  Özellikle, `summarizer.py` ve `src/services/gemini_client.py` dosyalarındaki değişiklikler,  Gemini API ile etkileşimin nasıl yapıldığını ve sonuçların nasıl işlendiğini doğrudan etkiler.  `features` klasörünün kullanımıyla kodun modülerliğinin artması, mimariye bir iyileştirme getirir. `CallableModule` sınıfının kullanımı ile giriş noktası daha fonksiyonel ve temiz bir hale getirilmiştir.

* **Kod Organizasyonundaki İyileştirmeler:**  `features` klasörünün kullanımı ile kodun modülerliği artmıştır.  `screenshot` komutu için ayrı bir fonksiyon (`screenshot_command`) oluşturulması da kod okunabilirliğini ve sürdürülebilirliğini iyileştirmiştir.


### 2. İŞLEVSEL ETKİ:

* **Eklenen Özellikler:**  `summarizer ss chrome`, `summarizer ss firefox`, `summarizer ss code` gibi uygulamaya özgü ekran görüntüsü alma komutları eklenmiştir.  `summarizer --gui` ile GUI tabanlı konfigürasyon ve  `summarizer --setup` ile interaktif kurulum seçenekleri eklenmiştir.

* **Değiştirilen Özellikler:** Mevcut `summarizer screenshot` ve `summarizer ss` komutları geliştirilmiş ve daha spesifik hale getirilmiş olabilir (kodun tam içeriğinin olmaması nedeniyle kesin olarak söylenemez). `generate_simple_text` fonksiyonu iyileştirilmiş veya yeni basit metin üretme özelliği eklenmiş olabilir.

* **Kaldırılan Özellikler:**  Bilgi yok.

* **Kullanıcı Deneyimi:** Kullanıcı deneyimi, özellikle komut satırı arayüzü kullanımında önemli ölçüde iyileştirilmiştir. Yeni komutlar ve seçenekler eklenmesiyle daha esnek bir kullanım sağlanmıştır. GUI seçeneği, kullanıcı dostu bir deneyim sunar.

* **Performans, Güvenlik ve Güvenilirlik:** Performans, güvenlik ve güvenilirlik üzerindeki etkiler, yapılan spesifik kod değişikliklerine bağlıdır ve kesin olarak belirlenemez. Hata yönetimi ve loglama iyileştirmeleri güvenilirliği artırabilir.  Ancak,  performans iyileştirmeleri veya güvenlik güçlendirmeleri olup olmadığı koddan açıkça görülmemektedir.


### 3. TEKNİK DERİNLİK:

* **Tasarım Desenleri:**  `CallableModule` sınıfı, bir Facade veya Singleton deseni olarak düşünülebilir (kesin olarak söylenemez).  `features` klasörü, modüler tasarım desenini gösterir. `argparse` kütüphanesinin kullanımı da iyi bir tasarım pratiğidir.

* **Kod Kalitesi ve Sürdürülebilirlik:**  Kodun modülerliği ve `CallableModule` sınıfının kullanımı, kod kalitesini ve sürdürülebilirliğini artırır.  Ancak, eksik kod parçaları nedeniyle kesin bir değerlendirme yapılamaz.  TODO yorumlarının varlığı, gelecekte yapılması gereken geliştirmeleri ve potansiyel teknik borcu göstermektedir.

* **Yeni Bağımlılıklar:**  Yeni bağımlılıkların eklenip eklenmediği belirsizdir.  `requirements.txt` veya benzeri bir dosyanın içeriği olmadan bu sorunun cevabı verilemez. GUI'nin eklenmesi yeni bağımlılıklar gerektiriyor olabilir.


### 4. SONUÇ YORUMU:

* **Uzun Vadeli Değer ve Etki:** Bu değişiklikler, uygulamanın kullanıcı dostu bir şekilde gelişmesine ve AI özetleme özelliğinin daha sağlam bir şekilde entegre edilmesine katkıda bulunur. Komut satırı arayüzünün genişletilmesi ve GUI desteği olumlu etkilerdir.

* **Teknik Borcun Etkilenmesi:**  Projenin teknik borcu, kodun modülerliğinin iyileştirilmesiyle kısmen azalmış olabilir, ancak TODO yorumlarının varlığı yeni teknik borçlar olduğunu gösterir.  

* **Gelecekteki Geliştirmelere Hazırlık:** Modüler kod yapısı ve iyi dokümantasyon (eğer varsa), gelecekteki geliştirmeleri kolaylaştırır.  Ancak, spesifik olarak gelecek geliştirmeler için yapılmış hazırlıkların detayları koddan anlaşılmamaktadır.  AI destekli özelliklerin eklenmesine yönelik bir altyapı oluşturulmuş olması muhtemeldir.

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

**Last updated**: June 20, 2025 by Summarizer Framework v8.3.6
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
