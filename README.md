# 🚀 Summarizer Framework
> 📝 Metin özetleme ve analizinde kullanılan, modüler ve genişletilebilir bir Python framework'üdür.  Ekran görüntüsü alma, GUI yönetimi ve AI destekli özetleme gibi gelişmiş özellikler sunar.

## 📊 Proje Durumu
Geliştirme aşamasında.  Son değişiklikler, kodun modülerliğini ve organizasyonunu önemli ölçüde artırmış, yeni özellikler eklemiş ve konfigürasyon yönetimini iyileştirmiştir.  Ancak, API anahtarlarının güvenli bir şekilde yönetilmesi ve büyük `if-else` blokları gibi bazı alanlarda iyileştirmelere ihtiyaç duyulmaktadır.


## ✨ Özellikler
- 💻 Komut satırı arayüzü
- 📸 Ekran görüntüsü alma (Chrome, Firefox, Code)
- ⚙️ GUI kurulum ve kaldırma
- 📊 Sistem durumu gösterimi
- 📄 Değişiklik günlüğü güncellemeleri
- 🤖 Basit metin üretme (Gemini AI entegrasyonu)
- 📝 Gelişmiş özetleme (Gelecek özellik: Summarizer Eye)


## Değişen Dosyalar:
`summarizer.py`, `features/parameter_checker.py`, `features/terminal_commands.py`, `features/__init__.py`, `features/screenshot.py`, `features/gui_installer.py`, `src/core/configuration_manager.py`, `src/utils/changelog_updater.py`, `src/services/gemini_client.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

- **Hangi sistem bileşenleri ve katmanlar etkilendi?**  `summarizer.py` (ana giriş noktası), `features` dizini altındaki modüller (özelliklere özgü işlevler), `src/core/configuration_manager.py` (konfigürasyon yönetimi), `src/utils/changelog_updater.py` (değişiklik günlüğü yönetimi) ve `src/services/gemini_client.py` (Gemini API entegrasyonu) etkilendi.  Değişiklikler, framework'ün ana iş mantığını, konfigürasyonunu ve yardımcı araçlarını kapsayan birden fazla sistem bileşenini ve katmanı etkilemiştir.

- **Mimari değişikliklerin etkisi nedir?**  Esas olarak, özelliklerin daha modüler ve organize bir şekilde sunulmasına odaklanılmıştır.  `features` dizini,  *Yüksek Kohezyon, Düşük Bağlantı* prensibine uygun bir mimari oluşturarak farklı özellikleri bağımsız modüllere ayırmıştır.  Bu, kodun okunabilirliğini, bakımı ve test edilebilirliğini artırır.  Konfigürasyon yönetimi de iyileştirilerek konfigürasyon dosyalarının proje kök dizini altında `.summarizer` adlı bir dizinde tutulması sağlanmıştır. Bu, konfigürasyon verilerinin kaynak kodundan ayrılmasını ve daha düzenli bir proje yapısını sağlar.

- **Kod organizasyonunda hangi iyileştirmeler yapıldı?**  `features` dizini altındaki modülleme ile kod daha organize ve anlaşılır hale getirilmiştir.  `summarizer.py`'deki argüman işleme mantığı iyileştirilmiş,  `changelog_updater.py` ve `gemini_client.py` dosyalarında fonksiyonlar daha iyi ayrıştırılmış ve isimleri daha açıklayıcı hale getirilmiştir.  Konfigürasyon dosyalarının konumunun daha net ve tutarlı hale getirilmesi de önemli bir iyileştirmedir.


### 2. İŞLEVSEL ETKİ:

- **Hangi özellikler eklendi, değiştirildi veya kaldırıldı?**  `screenshot` (ve `ss` kısaltması) komutu ile ekran görüntüsü alma özelliği eklenmiştir.  `--status` komutu ile sistem durumu gösterimi eklenmiştir.  `--setup`, `--gui`, `--install_gui`, `--install_terminal`, `--uninstall_terminal` komutları ile konfigürasyon ve GUI/terminal kurulum/kaldırma işlevleri eklenmiş veya iyileştirilmiştir.  `gemini_client.py` dosyasına basit metin üretme özelliği eklenmiş ve `changelog_updater.py` dosyasındaki değişiklik günlüğü işlevleri geliştirilmiştir.

- **Kullanıcı deneyimi nasıl etkilendi?**  Yeni komutların eklenmesiyle kullanıcılar daha fazla seçeneğe sahip olmuştur.  Ekran görüntüsü alma ve sistem durumu gösterimi özellikleri kullanıcı deneyimini iyileştirmiştir.  Konfigürasyon yönetiminin iyileştirilmesi de kullanıcı deneyimini olumlu etkilemiştir.

- **Performans, güvenlik veya güvenilirlik üzerindeki etkiler?**  Performans üzerindeki doğrudan etki minimaldir.  Ancak, modüler yapı gelecekteki bakımı ve geliştirmeyi kolaylaştırarak dolaylı olarak güvenilirliği artırabilir.  Güvenlik açısından, API anahtarlarının komut satırı üzerinden alınması büyük bir güvenlik açığıdır.  Değişiklik günlüğü ve hata yönetimi iyileştirmeleri güvenilirliği artırmıştır.


### 3. TEKNİK DERINLIK:

- **Hangi tasarım desenleri uygulandı veya değiştirildi?**  Modülleme prensibi açıkça uygulanmıştır.  `GeminiClient` sınıfı singleton deseninin özelliklerini göstermektedir.  MVC tarzı bir yaklaşımın izleri `JsonChangelogManager` sınıfında görülebilir.

- **Kod kalitesi ve sürdürülebilirlik nasıl gelişti?**  Kodun daha organize ve okunabilir hale getirilmesi kod kalitesini artırmıştır.  Modüler tasarım ve daha iyi hata yönetimi sürdürülebilirliği iyileştirmiştir.  Ancak, büyük `if-else` blokları potansiyel kod kokusudur ve iyileştirilmelidir.

- **Yeni bağımlılıklar veya teknolojiler eklendi mi?**  Yeni bağımlılıklar eklenmemiştir.  Ancak,  `changelog_updater.py` muhtemelen changelog yönetimi için bir kütüphane kullanmaktadır ve `gemini_client.py` Gemini API kütüphanesine bağımlıdır.


### 4. SONUÇ YORUMU:

- **Bu değişikliklerin uzun vadeli değeri ve etkisi nedir?**  Kodun daha sürdürülebilir ve genişletilebilir hale getirilmesi.  Modüler tasarım, yeni özelliklerin eklenmesini ve mevcut özelliklerin bakımını kolaylaştırır.

- **Projenin teknik borcu nasıl etkilendi?**  Kodun daha organize hale getirilmesiyle teknik borç azalmıştır, ancak `summarizer.py`'deki büyük `if-else` bloğu ve API anahtarlarının güvensiz yönetimi hala iyileştirilmeyi beklemektedir.

- **Gelecekteki geliştirmelere nasıl hazırlık yapıldı?**  Modüler mimari ve daha iyi organize edilmiş kod yapısı, gelecekteki geliştirmelere hazırlık oluşturmuştur.  Ancak, AI destekli özelliklerin (Summarizer Eye) eklenmesi için daha detaylı planlama ve mimari tasarıma ihtiyaç vardır.  API anahtarlarının güvenli yönetimi de acil bir ihtiyaçtır.

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

**Last updated**: June 20, 2025 by Summarizer Framework v8.3.9
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
