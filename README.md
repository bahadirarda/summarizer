# 🚀 Summarizer Framework
> Akıllı özetleme, ekran görüntüsü alma ve terminal komut yönetimi özelliklerini birleştiren güçlü ve modüler bir framework.

## 📊 Proje Durumu
Geliştirme aşamasında.  Son güncellemeler, GUI desteği, gelişmiş ekran görüntüsü alma, terminal komutları yönetimi ve iyileştirilmiş changelog ve versiyonlama sistemini içeriyor.  AI destekli "Summarizer Eye" özelliği için temel atılmış durumda (gelecek sürümlerde).


## ✨ Özellikler
* 📄 Çeşitli kaynaklardan metin özetleme
* 📸 Chrome, Firefox ve Code Editor gibi uygulamaların ekran görüntüsünü alma
* ⚙️ Komut satırı üzerinden konfigürasyon
* 🖥️ Kullanıcı dostu grafiksel arayüz (GUI)
* 终端 Terminal komutlarının kurulumu ve kaldırılması
* 📊 Sistem durumu raporlama
* 📝 Otomatik changelog güncellemesi
* VERSION Gelişmiş versiyon yönetimi


## Değişen Dosyalar:
`src/main.py`, `summarizer.py`, `src/core/configuration_manager.py`, `src/utils/version_manager.py`, `src/utils/changelog_updater.py`, `features/parameter_checker.py`, `features/screenshot.py`, `features/terminal_commands.py`, `features/gui_installer.py`, `tests/test_main.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

* **Etkilenen Bileşenler ve Katmanlar:** Değişiklikler, projenin neredeyse tüm katmanlarını etkilemiştir.  `src/main.py` ve `summarizer.py` (ana iş mantığı), `src/core/configuration_manager.py` (konfigürasyon), `src/utils` dizini (yardımcı araçlar - özellikle `version_manager.py` ve `changelog_updater.py`), `features` dizini (özellik modülleri) ve `tests` dizini (testler) etkilenmiştir.

* **Mimari Değişikliklerin Etkisi:**  Mimari genel olarak korunmuş ancak gelişmiş ve modüler hale getirilmiştir. `features` dizinindeki modüler tasarım, yeni özelliklerin eklenmesini kolaylaştırmıştır.  GUI ve gelişmiş ekran görüntüsü alma gibi yeni özellikler, mevcut mimariye sorunsuz bir şekilde entegre edilmiştir. Versiyon ve changelog yönetimi de `version_manager.py` ve `changelog_updater.py` dosyalarının iyileştirilmesiyle daha sağlam hale getirilmiştir.

* **Kod Organizasyonunda İyileştirmeler:**  `features` dizini, özelliklerin modüler olarak organize edilmesini sağlamıştır. Bu, kodun okunabilirliğini, sürdürülebilirliğini ve bakımı kolaylaştırmıştır. `version_manager.py` ve `changelog_updater.py` dosyalarındaki değişiklikler ise bu dosyaların işlevselliğini daha yapılandırılmış ve modüler hale getirmiştir. Özellikle `changelog_updater.py`'deki `_detect_project_type` fonksiyonunun eklenmesi, changelog oluşturma sürecinin projenin türüne göre özelleştirilmesini sağlamıştır.


### 2. İŞLEVSEL ETKİ:

* **Eklenen Özellikler:** GUI desteği (`--gui` komutu), gelişmiş ekran görüntüsü alma (tarayıcıya özgü komutlar), terminal komut yönetimi (kurulum ve kaldırma komutları), sistem durumu raporlama (`--status` komutu) eklenmiştir.

* **Değiştirilen Özellikler:** Komut satırı argümanlarının işlenmesi `argparse` kütüphanesi kullanılarak iyileştirilmiştir. Özetleme fonksiyonunun çağrılma şekli muhtemelen değiştirilmiştir (detaylar eksik).

* **Kaldırılan Özellikler:** Belirtilmemiştir.

* **Kullanıcı Deneyimi:** Kullanıcı deneyimi, yeni komut satırı seçenekleri, GUI ve daha kapsamlı raporlama ile önemli ölçüde iyileştirilmiştir.

* **Performans, Güvenlik veya Güvenilirlik:** Performans etkisi tam olarak belirlenememektedir.  `version_manager.py` ve `changelog_updater.py` dosyalarındaki değişiklikler, versiyonlama ve changelog yönetimini daha güvenilir hale getirmiştir.  Güvenlik üzerinde doğrudan bir etki gözlenmemiştir.


### 3. TEKNİK DERİNLİK:

* **Tasarım Desenleri:** Modülerlik ve Komut (Command) tasarım deseni belirgindir.  `features` dizini modülerliği desteklerken, komut satırı argümanlarının farklı fonksiyonları tetiklemesi Komut desenine işaret etmektedir. `VersionManager` sınıfı tek sorumluluk prensibine (Single Responsibility Principle) uygundur.

* **Kod Kalitesi ve Sürdürülebilirlik:** Kod kalitesi, modüler tasarım ve testlerin varlığı sayesinde (testler yetersiz olsa da) iyileştirilmiştir.  `changelog_updater.py`'deki değişiklikler, kodun daha okunabilir ve sürdürülebilir olmasını sağlamıştır.

* **Yeni Bağımlılıklar veya Teknolojiler:** `argparse` kütüphanesinin kullanımı belirgindir. Diğer olası bağımlılıklar, `version_manager.py` ve `changelog_updater.py` dosyalarının incelenmesiyle tespit edilebilir.


### 4. SONUÇ YORUMU:

* **Uzun Vadeli Değer ve Etki:**  Bu değişiklikler, Summarizer Framework'ün işlevselliğini önemli ölçüde genişletmiş ve kullanıcı deneyimini iyileştirmiştir. Modüler tasarım, gelecekteki geliştirmeleri kolaylaştırmaktadır.  Gelişmiş versiyon ve changelog yönetimi, sürdürülebilirliği artırmaktadır.  AI destekli "Summarizer Eye" özelliğinin gelecekteki eklenmesine zemin hazırlanmıştır.

* **Projenin Teknik Borcu:**  Testlerin yetersizliği bir teknik borç olarak kalmaktadır. `_has_breaking_changes` fonksiyonunun basit kural tabanlı yaklaşımı da potansiyel bir teknik borçtur; daha gelişmiş bir mekanizma gelecekte ele alınabilir.

* **Gelecekteki Geliştirmelere Hazırlık:**  Modüler tasarım ve gelişmiş versiyon yönetimi sayesinde, gelecekte yeni özellikler eklemek ve mevcut özellikleri geliştirmek daha kolay olacaktır.  Farklı proje türlerine uyum sağlama yeteneği de gelecekteki ölçeklenebilirliği destekleyecektir.

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

**Last updated**: June 20, 2025 by Summarizer Framework v8.6.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
