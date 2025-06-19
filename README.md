# 🚀 Summarizer Framework
> Akıllı özetleme ve ekran görüntüsü alma yetenekleri sunan, komut satırı ve GUI desteğine sahip güçlü bir araç.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son güncellemeler, komut satırı arayüzünü genişletmiş, GUI desteği eklemiş, Gemini AI entegrasyonunu iyileştirmiş ve değişiklik günlüğünün yönetimini geliştirmiştir.  Projenin geleceği için AI destekli "Summarizer Eye" özelliği ve sesli komut sistemi gibi ek özellikler planlanmaktadır.  Teknik borç, modüler tasarım ve hata yönetimi iyileştirmeleriyle azaltılmış, ancak yeni özellikler için yeni teknik borçlar da oluşmuştur.

## ✨ Özellikler
* 📄 Metin özetleme (Gemini AI ile güçlendirilmiş)
* 📸 Farklı web tarayıcıları ve uygulamalar için ekran görüntüsü alma (Chrome, Firefox, Code vb.)
* 🖥️ Komut satırı arayüzü (Zengin komut ve seçenek seti)
* 💻 Kullanıcı dostu GUI kurulum ve konfigürasyon
* ⚙️ Interaktif kurulum seçeneği
* 📝 Değişiklik günlüğü yönetimi


## Değişen Dosyalar:
`install_gui.py`, `src/main.py`, `summarizer.py`, `src/core/configuration_manager.py`, `src/utils/git_manager.py`, `src/services/gemini_client.py`, `src/utils/changelog_updater.py`, `scripts/run_ci_checks.py`,  `src/utils/changelog_updater.py`, `src/services/gemini_client.py` (ve muhtemelen `features` klasörü altındaki dosyalar)


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

- **Etkilenen Bileşenler ve Katmanlar:** Değişiklikler, Summarizer Framework'ün çeşitli katmanlarını etkilemiştir.  `summarizer.py` (giriş noktası), `src/main.py` (özetleme mantığı), `features` klasörü (ek özellikler – ekran görüntüsü, kurulum, parametre kontrolü), `src/services/gemini_client.py` (Gemini API entegrasyonu), `src/utils/changelog_updater.py` (değişiklik günlüğü), `src/core/configuration_manager.py` (konfigürasyon yönetimi), `src/utils/git_manager.py` (Git entegrasyonu) ve `scripts/run_ci_checks.py` (sürekli entegrasyon) dosyaları doğrudan etkilenmiştir.  Sistem, giriş katmanı (`summarizer.py`), işlevsellik katmanı (`src/main.py` ve `features` klasörü) ve alt katmanlar (kütüphaneler) olmak üzere katmanlı bir mimariye sahiptir.

- **Mimari Değişikliklerin Etkisi:**  `summarizer.py`'deki `CallableModule` sınıfının eklenmesi, giriş noktasının daha temiz ve çağrılması daha kolay hale getirilmiştir.  `features` klasörünün kullanımı (içerik tam olarak verilmese de), modülerliği ve sürdürülebilirliği artırmayı amaçlamaktadır.  Gemini API ile entegrasyonun her zaman `RequestManager` ile yapılması, daha esnek bir mimari sağlamıştır.  GUI kurulumunun eklenmesi, sistemin kullanıcı etkileşimini önemli ölçüde genişletmiştir.

- **Kod Organizasyonundaki İyileştirmeler:**  `features` klasörü aracılığıyla modüler bir yaklaşım benimsenmiştir.  `summarizer.py`'nin işlevselliği `features` altındaki modüllere taşınarak kod daha okunabilir ve bakımı daha kolay hale getirilmiştir. `argparse` kütüphanesinin kullanımı komut satırı argümanlarının işlenmesini kolaylaştırmıştır.


### 2. İŞLEVSEL ETKİ:

- **Eklenen Özellikler:**  `summarizer ss chrome`, `summarizer ss firefox`, `summarizer ss code` gibi tarayıcıya özgü ekran görüntüsü alma komutları;  `summarizer --gui` ile GUI tabanlı kurulum ve konfigürasyon; `summarizer --setup` ile interaktif kurulum;  `gemini_client.py`'deki `generate_simple_text` fonksiyonu ile basit metin üretme yeteneği eklenmiştir.

- **Değiştirilen Özellikler:**  Mevcut `summarizer` komutunun işlevselliği genişletilmiş ve daha spesifik hale getirilmiştir.  Özetleme işlemi muhtemelen Gemini API entegrasyonundaki iyileştirmeler ile optimize edilmiştir.

- **Kaldırılan Özellikler:**  Bilgi verilmemiştir.

- **Kullanıcı Deneyimi:** Kullanıcı deneyimi önemli ölçüde iyileştirilmiştir.  Daha fazla komut ve seçenek sunulmuş, GUI desteği eklenmiş ve interaktif kurulum seçeneği ile kurulum kolaylaştırılmıştır.

- **Performans, Güvenlik ve Güvenilirlik:**  Performans üzerindeki etki, yapılan optimizasyonlara bağlıdır.  `_truncate_content_for_prompt` fonksiyonu Gemini API'sine gönderilen prompt'un uzunluğunu kontrol ederek performans ve güvenilirliği artırmış olabilir.  Hata yönetimi iyileştirmeleri (try-except blokları) güvenilirliği artırmıştır.  Gemini API anahtarının daha iyi yönetimi güvenliği artırmıştır.  Kesin değerlendirme için kod detaylarına daha fazla ihtiyaç vardır.


### 3. TEKNİK DERINLIK:

- **Tasarım Desenleri:** Modüler tasarım deseni, `features` klasörü ile açıkça kullanılmıştır.  `argparse` kütüphanesinin kullanımı da iyi bir tasarım pratiğidir. `GeminiClient` sınıfı, muhtemelen singleton veya factory desenini kullanmaktadır. `CallableModule` sınıfı yeni bir tasarım yaklaşımı eklemiştir.

- **Kod Kalitesi ve Sürdürülebilirlik:** Kodun okunabilirliği ve sürdürülebilirliği, modüler tasarım, daha açıklayıcı fonksiyon isimleri ve iyileştirilmiş hata yönetimi ile artmıştır.  Ancak, bazı TODO yorumlarının olması, gelecekteki geliştirmelere işaret etmektedir ve teknik borcun varlığını göstermektedir.

- **Yeni Bağımlılıklar:** GUI'nin eklenmesiyle yeni bağımlılıklar eklenmiş olması muhtemeldir.  Kesin liste, `requirements.txt` dosyasının incelenmesini gerektirir.


### 4. SONUÇ YORUMU:

- **Uzun Vadeli Değer ve Etki:** Bu değişiklikler, Summarizer Framework'ün işlevselliğini ve kullanıcı deneyimini önemli ölçüde geliştirmiştir.  Daha fazla özellik eklenmesi ve mevcut özelliklerin iyileştirilmesi, aracın daha kullanışlı ve güçlü olmasını sağlayacaktır.  Gemini AI entegrasyonundaki iyileştirmeler, özetleme kalitesini artıracaktır.

- **Teknik Borç:**  Modüler tasarım ve hata yönetimi iyileştirmeleri teknik borcu azaltmıştır, ancak yeni özellikler için yeni teknik borçlar eklenmiştir (TODO yorumları).

- **Gelecekteki Geliştirmelere Hazırlık:** Modüler tasarım ve iyi dokümantasyon (eğer varsa), gelecekteki geliştirmeleri kolaylaştıracaktır.  "Summarizer Eye" ve sesli komut sistemi gibi planlanan özellikler için mimari hazırlık yapılmış olması muhtemeldir.  Ancak bunun kesinliği kod detaylarının tam olarak incelenmesini gerektirir.

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

**Last updated**: June 20, 2025 by Summarizer Framework v8.3.7
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
