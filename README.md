# 🚀 project.110620251156
> Özetleme yetenekleri sunan modern bir web uygulaması.  Verimli ve güvenilir bir şekilde metin özetleme işlemleri gerçekleştirir.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son güncellemeler, kullanıcı arayüzü iyileştirmeleri, gelişmiş hata yönetimi ve otomatik kod izleme ve yedekleme sistemini içermektedir.  README dosyası da otomatik güncelleme yeteneği kazanmıştır.  Güncellemeler, projenin stabilitesini, güvenilirliğini ve sürdürülebilirliğini artırmaya odaklanmıştır.

## ✨ Özellikler
* Metin özetleme
* Kullanıcı dostu arayüz (GUI)
* Komut satırı arayüzü (CLI) desteği
* Otomatik kod yedekleme ve izleme
* Gelişmiş hata yönetimi
* Otomatik README güncelleme


## Değişen Dosyalar:
`gui_launcher.py`, `install_gui.py`, `api_server.py`, `src/utils/file_tracker.py`, `summarizer.py`, `macos-setup-wizard/setup_installer.py`, `src/utils/readme_generator.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

Birden fazla commit'in analizi sunulduğu için, her bir commit'in yapısını ayrı ayrı inceleyeceğiz:

**Commit 1 (Summarizer Framework Değişiklikleri):**  Bu commit, Summarizer Framework'ün dört ana bileşenini (GUI, API Sunucusu, Yardımcı Araçlar, Ana İş Mantığı) etkilemiştir.  Mimari temelde değişmemiş, ancak `src/main` modülünün `api_server.py` tarafından çağrılması, daha modüler bir yapıya işaret etmektedir.  Kod organizasyonu açısından, katmanlı bir mimari (GUI, API, yardımcı araçlar, ana iş mantığı) kullanımı ve `src` dizini altındaki alt dizinler, kodun daha iyi organize edilmesini sağlamaktadır.  `file_tracker.py` dosyasının eklenmesiyle kod izleme ve yedekleme mekanizması entegre edilmiştir.

**Commit 2 (macOS Kurulum Sihirbazı Değişiklikleri):** Bu commit, `macos-setup-wizard/setup_installer.py` dosyasına odaklanmıştır.  Değişiklikler esas olarak sunum (GUI/CLI) ve uygulama katmanlarını etkilemiştir. Mimari açısından önemli bir değişiklik yoktur.  Ancak, hata yönetimi iyileştirilmiş ve PyQt5 desteği eklenerek GUI kurulumu mümkün hale getirilmiştir.  CLI ve GUI kurulumları arasında daha net bir ayrım yapılmış ve PyQt5 bulunmaması durumunda CLI'a otomatik geçiş sağlanmıştır. Kod organizasyonu, daha sağlam `try...except` blokları ile iyileştirilmiştir.

**Commit 3 (README Generator Değişiklikleri):** Bu commit, sadece `src/utils/readme_generator.py` dosyasını etkilemiştir.  Mimari değişiklik minimaldir; mevcut yardımcı araç geliştirilmiştir. Kod organizasyonu,  `_get_framework_version` fonksiyonunun geliştirilmesi ve `generate_complete_readme_content` fonksiyonunun eklenmesiyle iyileştirilmiştir.  Bu iyileştirmeler, daha sağlam bir versiyon tespiti ve daha okunabilir bir kod yapısı sağlamaktadır.


### 2. İŞLEVSEL ETKİ:

**Commit 1:** `summarizer.py` değişiklikleri nedeniyle ana işlevsellikteki değişiklikler tam olarak belirlenememektedir.  Ancak, `file_tracker.py`'nin eklenmesi, kod değişikliklerinin izlenmesi ve yedeklenmesi işlevselliğini eklemiştir.  GUI değişiklikleri muhtemelen kullanıcı deneyimini etkilemiş ancak ayrıntılar bilinmemektedir. API sunucusunda işlevsel bir değişiklik yoktur, ancak `summarizer()` fonksiyonunun çağrılması, ana iş mantığıyla etkileşimi göstermektedir.

**Commit 2:** Temel işlevsellik değişmemiştir. Ancak, PyQt5 destekli GUI kurulumu eklenmiş, hata yönetimi geliştirilmiş ve CLI seçeneği iyileştirilmiştir.  Kullanıcı deneyimi, GUI ve daha iyi hata mesajları ile iyileşmiştir.  Performans açısından, GUI kurulumu daha yavaş olabilir. Güvenlik ve güvenilirlikte önemli bir değişiklik yoktur.

**Commit 3:** README.md dosyasına otomatik olarak eklenen yeni bölümler (impact_counts ve Tracking Features) eklenmiştir.  Framework versiyon tespiti iyileştirilmiş ve README oluşturma süreci optimize edilmiştir.  Kullanıcı deneyimi doğrudan etkilenmemiş, ancak güncellenmiş README daha iyi bir deneyim sağlar. Performans üzerinde minimal bir iyileşme, güvenilirlikte ise artış vardır.


### 3. TEKNİK DERINLIK:

**Commit 1:** Katmanlı mimari ve modüler tasarım unsurları gözlemlenmektedir. Kod kalitesi ve sürdürülebilirlik, `file_tracker.py` ile iyileştirilmiştir.  `flet` kütüphanesi yeni bir bağımlılık olarak eklenmiştir.

**Commit 2:** "Strategy Pattern" kullanılmıştır (CLI ve GUI kurulum stratejileri). Kod kalitesi, daha iyi hata yönetimi ve daha net kod yapısıyla iyileştirilmiştir. PyQt5 kütüphanesi yeni bir bağımlılık olarak eklenmiştir.

**Commit 3:** Belirgin bir tasarım deseni değişikliği yoktur, ancak ayrıştırma ilkesi uygulanmıştır. Kod kalitesi ve sürdürülebilirlik iyileştirilmiştir. Yeni bağımlılık eklenmemiştir.


### 4. SONUÇ YORUMU:

**Commit 1:** Uzun vadeli değer, `summarizer.py` değişikliklerine bağlıdır.  `file_tracker.py` uzun vadeli değer sağlar. Teknik borç, `file_tracker.py` ile azaltılabilir, ancak `summarizer.py` değişiklikleri bunu artırmış olabilir. Modüler tasarım ve katmanlı mimari, gelecekteki geliştirmelere hazırlık sağlar.

**Commit 2:** Bu değişiklikler, kullanıcı deneyimini ve güvenilirliği önemli ölçüde artırmıştır.  Teknik borç azaltılmıştır.  Modüler yapı, gelecekteki geliştirmelere hazırlık sağlar. PyQt5 bağımlılığı, dağıtımı etkileyebilir.

**Commit 3:** Bu değişiklikler, README'nin güncelliğini ve bilgilendiriciliğini artırarak uzun vadeli değer sağlar. Teknik borç azaltılmıştır.  README güncelleme süreci daha otomatik ve yönetilebilir hale getirilmiştir.  Genel olarak, projenin kalitesi ve sürdürülebilirliği olumlu yönde etkilenmiştir.

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

**Last updated**: June 12, 2025 by Summarizer Framework v7.2.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
