# 🚀 Summarizer Framework
> ✨ Güçlü bir metin özetleme aracı ve kullanıcı dostu bir arayüz sunan, genişletilebilir bir çerçeve.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son değişiklikler, kodun modülerliğini ve sürdürülebilirliğini önemli ölçüde artırmıştır.  GUI ve komut satırı arayüzü iyileştirilmiş, hata yönetimi güçlendirilmiş ve yeni özelliklerin eklenmesine yönelik altyapı oluşturulmuştur.  Ancak, `gui_launcher.py` dosyasında kullanılan mutlak yollar taşınabilirlik sorunlarına yol açabileceğinden, bu bir teknik borç olarak kalmaktadır.

## ✨ Özellikler
* 📄 Metin özetleme yeteneği.
* 🖥️ Kullanıcı dostu bir grafik arayüz (GUI).
* ⌨️ Komut satırı arayüzü (CLI) ile esnek kontrol.
* 📸 Ekran görüntüsü alma ve analiz etme (Chrome, Firefox, Code editörleri için destek).
* 🛠️ Genişletilebilir mimari, kolay özellik ekleme olanağı.
* 📈 Gelişmiş hata yönetimi ve kullanıcı geri bildirimleri.


## Değişen Dosyalar:
`install_gui.py`, `gui_launcher.py`, `summarizer.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

* **Hangi sistem bileşenleri ve katmanlar etkilendi?**  Değişiklikler, projenin sunum (GUI), iş mantığı ve veri erişim katmanlarını etkilemiştir. `install_gui.py`, GUI kurulumunu yönetir. `gui_launcher.py`, GUI'yi başlatır. `summarizer.py`,  özetleme iş mantığını ve CLI'yı içerir.  `features` dizini altında bulunan modüller (`gui_installer.py`, `terminal_commands.py`, `parameter_checker`, `screenshot`) iş mantığının farklı kısımlarını kapsar.

* **Mimari değişikliklerin etkisi nedir?**  `install_gui.py` dosyasının modülerleştirilmesi, GUI ve terminal komutu kurulumunun ayrı modüllere taşınmasıyla,  sistem mimarisinde  "Ayrıştırma (Separation of Concerns)" ilkesinin uygulanması sağlanmıştır. Bu, daha iyi organizasyon, daha yüksek test edilebilirlik ve sürdürülebilirliğe yol açmıştır.  `summarizer.py`'deki değişiklikler ise,  özetleyici modülünün hem kütüphane olarak kullanılabilmesini hem de bağımsız bir komut satırı aracı olarak çalıştırılabilmesini sağlayan daha modüler bir yapıya işaret eder.  Bu,  `CallableModule` sınıfının kullanımıyla sağlanmış olabilir.

* **Kod organizasyonunda hangi iyileştirmeler yapıldı?**  `install_gui.py` dosyası, GUI ve terminal kurulumlarını ayrı modüllere ayırarak daha düzenli hale getirilmiştir. `summarizer.py`,  `features` dizini altındaki modüllerle birlikte,  tek sorumluluk ilkesine (Single Responsibility Principle) daha yakın bir yapıya kavuşmuştur.  Hata yakalama mekanizmalarının iyileştirilmesi (try-except blokları) de kodun okunabilirliğini ve sürdürülebilirliğini artırmıştır.


### 2. İŞLEVSEL ETKİ:

* **Hangi özellikler eklendi, değiştirildi veya kaldırıldı?**  Yeni bir ekran görüntüsü alma özelliği eklenmiştir (`screenshot` ve `ss` komutları). Bu özellik, Chrome, Firefox ve Code editörlerini hedefleyebilir.  Mevcut kurulum süreci iyileştirilmiş ve hata mesajları daha bilgilendirici hale getirilmiştir.  `summarizer.py`'ye yeni komut satırı seçenekleri eklenmiştir.

* **Kullanıcı deneyimi nasıl etkilendi?** Kullanıcı deneyimi, daha ayrıntılı geri bildirim mesajları, daha kullanıcı dostu komut satırı seçenekleri ve GUI başlatma işleminin iyileştirilmesiyle olumlu yönde etkilenmiştir.  `flet` kütüphanesinin eksikliği durumunda bilgilendirici bir hata mesajı gösterilmesi, kullanıcıya daha iyi bir deneyim sunar.

* **Performans, güvenlik veya güvenilirlik üzerindeki etkiler?** Performans üzerinde önemli bir etki beklenmemektedir. Güvenlik veya güvenilirlikte doğrudan bir etki görülmemektedir; ancak hata yakalama mekanizmalarının eklenmesi dolaylı olarak güvenilirliği artırmıştır. Ekran görüntüsü alma özelliği, sistem kaynak kullanımını biraz artırabilir.


### 3. TEKNİK DERINLIK:

* **Hangi tasarım desenleri uygulandı veya değiştirildi?**  `summarizer.py`'de,  `CallableModule` sınıfının kullanımı muhtemelen bir façade pattern'ın varyasyonu veya benzer bir tasarım deseni örneğidir.  Modülerleştirme yaklaşımı, ayrıştırma prensibinin (separation of concerns) bir uygulamasıdır.

* **Kod kalitesi ve sürdürülebilirlik nasıl gelişti?** Kod kalitesi ve sürdürülebilirlik,  modüler yapının benimsenmesi, daha açıklayıcı hata mesajlarının eklenmesi ve hata yönetiminin iyileştirilmesi ile önemli ölçüde geliştirilmiştir. Kod daha okunabilir ve anlaşılır hale gelmiştir.

* **Yeni bağımlılıklar veya teknolojiler eklendi mi?** Yeni bir bağımlılık eklenmemiştir, ancak  `flet` kütüphanesi GUI için gereklidir ve  `gui_launcher.py` bu bağımlılığı kontrol etmektedir. Ekran görüntüsü alma işlemi için sistem kütüphaneleri kullanılmış olabilir.


### 4. SONUÇ YORUMU:

* **Bu değişikliklerin uzun vadeli değeri ve etkisi nedir?**  Bu değişikliklerin uzun vadeli değeri, projenin sürdürülebilirliğini ve ölçeklenebilirliğini artırmasıdır. Kodun daha modüler ve daha iyi organize edilmesi, gelecekteki geliştirmelerin daha hızlı ve daha az hata ile yapılmasını sağlayacaktır. Yeni eklenen özellikler, aracın işlevselliğini genişletmiştir.

* **Projenin teknik borcu nasıl etkilendi?**  Kodun daha iyi organize edilmesiyle teknik borç azalmıştır. Ancak, `gui_launcher.py` dosyasında mutlak yol kullanımı, taşınabilirlik sorunlarına yol açabilecek bir teknik borç olarak kalmaktadır.

* **Gelecekteki geliştirmelere nasıl hazırlık yapıldı?**  Modüler yapı ve iyi dokümantasyon, gelecekteki özellik eklemelerini ve bakım işlemlerini kolaylaştıracaktır.  `TODO` yorumları, gelecekteki geliştirme planlarına (örneğin, AI destekli "Summarizer Eye" özelliği) işaret etmektedir.

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

**Last updated**: June 16, 2025 by Summarizer Framework v7.6.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
