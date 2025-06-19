# 🚀 project.110620251156 - Akıllı Özetleyici
> Çeşitli kaynaklardan metin özetleme, ekran görüntüsü alma ve changelog güncelleme gibi özelliklere sahip, modüler ve genişletilebilir bir web projesi.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son değişiklikler,  kodun modülerliğini, sürdürülebilirliğini ve kullanıcı deneyimini önemli ölçüde iyileştirmiştir.  Yeni özellikler eklenmiş,  hata yönetimi geliştirilmiş ve versiyonlama süreci otomatikleştirilmiştir.  Gemini API entegrasyonu,  projenin yeteneklerini genişletmektedir.


## ✨ Özellikler
* 📄 Çeşitli kaynaklardan metin özetleme (AI destekli)
* 📸 Uygulama ekran görüntüleri alma ve analiz etme
* ⚙️ Komut satırı arayüzü (CLI) ile esnek kontrol
* 🖥️ Görsel konfigürasyon için GUI
* 🔄 Otomatik changelog güncelleme
* 🔢 Gelişmiş versiyon yönetimi ve kod adı ataması
* 📦 Modüler ve genişletilebilir mimari
* 📈 Durum izleme


## Değişen Dosyalar:
`summarizer.py`, `src/services/gemini_client.py`, `src/utils/version_manager.py`, `src/utils/changelog_updater.py`, `src/main.py` ve `features` dizini altındaki modüller.  Tam değişiklik listesi ve kod değişikliklerinin ayrıntıları eksik olduğundan, bu liste tamamlanamamıştır.


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

- **Etkilenen Bileşenler ve Katmanlar:** Değişiklikler, ana iş mantığını (`summarizer.py`, `src/main.py`), servis katmanını (`src/services/gemini_client.py`), yardımcı fonksiyonları (`src/utils/version_manager.py`, `src/utils/changelog_updater.py`) ve yeni özellik modüllerini (`features` dizini) etkilemiştir.  Sistem, modüler bir mimariye sahip olup,  her bir modül belirli bir görevi yerine getirir.

- **Mimari Değişikliklerin Etkisi:**  En önemli mimari değişiklik,  kodun modülerliğinin artırılmasıdır.  Özellikle `summarizer.py`,  farklı işlevleri `features` dizini altındaki modüllerden import ederek tek bir giriş noktasından yönetir. Bu,  sistemin genişletilebilirliğini ve sürdürülebilirliğini artırır.  `VersionManager` ve `changelog_updater.py` gibi yardımcı araçların geliştirilmesi de sistemin versiyonlama ve güncelleme süreçlerini iyileştirmiştir.

- **Kod Organizasyonundaki İyileştirmeler:** Kod, fonksiyonların ve modüllerin daha iyi ayrıştırılmasıyla daha düzenli ve okunabilir hale getirilmiştir.  `argparse` kütüphanesinin kullanımı, komut satırı argümanlarının işlenmesini kolaylaştırırken,  her bir özelliğin kendi modülünde kapsüllenmesi,  kodun yeniden kullanılabilirliğini ve bakımını kolaylaştırır.  `CallableModule` sınıfının kullanımı,  `summarizer.py`'nin hem komut satırı aracı hem de Python modülü olarak çalıştırılmasına olanak tanır.


### 2. İŞLEVSEL ETKİ:

- **Eklenen Özellikler:** Ekran görüntüsü alma (`screenshot`, `ss` seçenekleri ve uygulamaya özel seçenekler), GUI tabanlı konfigürasyon (`--gui`), interaktif kurulum (`--setup`), sistem durumu kontrolü (`--status`), otomatik changelog güncelleme ve kod adı belirleme.

- **Değiştirilen Özellikler:** Ana özetleme işlevi daha modüler hale getirilmiştir (`_summarizer` fonksiyonuna taşınmıştır). Komut satırı argümanlarının işlenmesi `argparse` ile iyileştirilmiştir.

- **Kaldırılan Özellikler:** Açıkça kaldırılan bir özellik gözlenmemiştir.

- **Kullanıcı Deneyimi:**  Kullanıcılar daha fazla komut satırı seçeneği ve GUI ile daha esnek ve kullanıcı dostu bir deneyime sahiptir.  Otomatik changelog güncellemeleri ve kod adları da kullanıcılar için faydalıdır.

- **Performans, Güvenlik veya Güvenilirlik:**  `gemini_client.py`'deki hata yakalama ve loglama mekanizmaları güvenilirliği artırır.  Dosya değişikliklerinin taranması performansı hafifçe etkileyebilir, ancak bu etki projenin boyutuna bağlıdır.  Güvenlikle ilgili belirgin bir değişiklik gözlenmemiştir.


### 3. TEKNİK DERINLIK:

- **Tasarım Desenleri:** Command Pattern (`argparse` ile komut satırı işleme), Modülerlik prensibi (fonksiyon ve modül ayrıştırılması), Singleton Pattern'e benzer bir yaklaşım (`gemini_client.py`'deki RequestManager).

- **Kod Kalitesi ve Sürdürülebilirlik:** Modüler tasarım,  iyi dokümantasyon ve loglama mekanizmaları kod kalitesini ve sürdürülebilirliğini artırmıştır.  Fonksiyonlar ve modüller iyi tanımlanmış sorumluluklara sahiptir, bu da bakımını kolaylaştırır.

- **Yeni Bağımlılıklar veya Teknolojiler:** `argparse` kütüphanesi kullanılmış (varsa yeni bağımlılık eklenmemiştir), Gemini API entegrasyonu yeni bir bağımlılıktır.  AI özetleme için başka kütüphaneler de kullanılmış olabilir, ancak bu belgelere yansımamıştır.


### 4. SONUÇ YORUMU:

- **Uzun Vadeli Değer ve Etki:** Bu değişiklikler projenin sürdürülebilirliğini, genişletilebilirliğini ve kullanıcı deneyimini önemli ölçüde iyileştirmiştir.  Otomatik changelog güncelleme ve gelişmiş versiyonlama,  geliştirme sürecini hızlandırırken,  modüler tasarım gelecekteki geliştirmeleri kolaylaştırır.

- **Teknik Borcun Etkilenmesi:** Kodun daha düzenli ve modüler hale getirilmesi, teknik borcu azaltmıştır.  Ancak, Gemini API'sine bağımlılık bir risk oluşturur ve bu riski azaltmak için API etkileşimini soyutlayan bir katman eklenmelidir.

- **Gelecekteki Geliştirmelere Hazırlık:** Modüler tasarım,  yeni özelliklerin eklenmesi için iyi bir temel oluşturur.  Loglama ve hata yakalama mekanizmaları,  gelecekteki sorunların tespitini ve çözümünü kolaylaştırır.  Gemini API'sine bağımlılık riski göz önünde bulundurularak, gelecekte farklı API'lerle uyumluluk sağlanmalıdır.

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

**Last updated**: June 19, 2025 by Summarizer Framework v7.15.5
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
