# 🚀 project.110620251156 - Akıllı Özetleyici ve Ekran Görüntüsü Aracı
>  project.110620251156, web tabanlı bir özetleme aracıdır.  Komut satırı arayüzü (CLI) ve grafiksel kullanıcı arayüzü (GUI) seçenekleri sunar.  Belgelerin, web sayfalarının ve uygulamaların özetlenmesini ve ekran görüntülerinin alınmasını sağlar.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son değişiklikler, kullanıcı deneyimini iyileştirmeye, işlevselliği genişletmeye ve kod tabanını daha sürdürülebilir hale getirmeye odaklanmıştır.  Ancak, TODO listesindeki bazı geliştirmeler (AI destekli özetleme, sesli komut, otomatik güncelleme) henüz tamamlanmamıştır.

## ✨ Özellikler
* 📄  Belge ve web sayfası özetleme
* 📸 Uygulamaya özgü ekran görüntüsü alma (Chrome, Firefox, Code vb.)
* ⚙️ Komut satırı arayüzü (CLI)
* 🖥️ Grafiksel kullanıcı arayüzü (GUI)
* 🔄 Interaktif kurulum seçeneği (`--setup`)
* 🛠️ Detaylı değişiklik kaydı (changelog)


## Değişen Dosyalar:
`summarizer.py`, `scripts/run_ci_checks.py`, `src/utils/changelog_updater.py`  ve `features` dizini altındaki modüller ( `parameter_checker`, `screenshot`, `terminal_commands`, `gui_installer`).


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

- **Etkilenen Bileşenler ve Katmanlar:** Değişiklikler, projenin üç ana katmanını etkilemiştir:
    * **Giriş Katmanı:** `summarizer.py`, komut satırı argümanlarının işlenmesi ve modül çağrılarının yönetimiyle ilgili değişiklikler içermektedir. `CallableModule` sınıfının eklenmesi, giriş noktasının fonksiyonel bir arayüz olarak sunulmasını sağlamıştır.
    * **İşlevsellik Katmanı:** `src/main` (özetleme işlevi), ve `features` dizini altındaki modüller (ekran görüntüsü alma, parametre kontrolü, GUI, terminal komutları) değişikliklerden etkilenmiştir. Özellikle `screenshot` komutu için `screenshot_command` fonksiyonunun ayrılması, kodun modülerliğini artırmıştır.
    * **CI/CD ve Yardımcı Araçlar:** `scripts/run_ci_checks.py` dosyasındaki değişiklikler CI/CD pipeline'ını, `src/utils/changelog_updater.py` ise changelog yönetimini etkilemiştir.


- **Mimari Değişikliklerin Etkisi:**  Mimari açıdan büyük değişiklikler yapılmamıştır.  Ancak, `CallableModule` sınıfının eklenmesi ve `screenshot_command` fonksiyonunun ayrılması, kodun daha modüler ve bakımı kolay bir yapıya kavuşmasını sağlamıştır.  `run_ci_checks.py`'deki değişiklikler CI/CD pipeline'ının güvenilirliğini artırmıştır (build sonrası eser kontrolü).


- **Kod Organizasyonundaki İyileştirmeler:**  `screenshot` komutu için özel bir fonksiyon ayrılması (`screenshot_command`),  kodun daha okunabilir ve sürdürülebilir olmasını sağlamıştır.  `features` dizini altında modüler bir yaklaşım izlenmesi, farklı işlevlerin ayrı modüllerde yönetilmesine olanak sağlamıştır.  `changelog_updater.py` dosyasında fonksiyon sayısındaki artış, modülerliği artırmış ancak büyük bir dosya oluşturabileceği için gelecekte yeniden yapılandırılmayı gerektirebilir.



### 2. İŞLEVSEL ETKİ:

- **Eklenen Özellikler:**  Uygulamaya özel ekran görüntüsü alma komutları (`summarizer ss chrome`, `summarizer ss firefox`, `summarizer ss code`), GUI tabanlı konfigürasyon (`summarizer --gui`) ve interaktif kurulum (`summarizer --setup`) seçenekleri eklenmiştir.  `changelog_updater.py` dosyasındaki değişiklikler daha detaylı changelog oluşturma yeteneği kazandırmıştır.


- **Değiştirilen Özellikler:**  Mevcut ekran görüntüsü alma komutları (`summarizer screenshot`, `summarizer ss`)  daha modüler bir yapıya kavuşmuştur.


- **Kaldırılan Özellikler:**  Belirtilen değişikliklerde bir özellik kaldırılması gözlenmemiştir.


- **Kullanıcı Deneyimi:**  Kullanıcı deneyimi, uygulamaya özel ekran görüntüsü alma komutları, GUI ve interaktif kurulum sayesinde önemli ölçüde iyileştirilmiştir.  Daha fazla seçenek ve daha açıklayıcı komutlar sunulmuştur.


- **Performans, Güvenlik ve Güvenilirlik:**  Eklenen özelliklerin performans üzerindeki doğrudan etkisi sınırlıdır.  Güvenlik ve güvenilirlik, kullanılan kütüphanelerin güvenilirliğine ve kodun genel kalitesine bağlıdır.  `run_ci_checks.py`'deki değişiklikler, build hatalarının daha erken tespit edilmesini sağlayarak güvenilirliği artırmıştır.



### 3. TEKNİK DERİNLİK:

- **Tasarım Desenleri:**  `CallableModule` sınıfı, bir Facade tasarım deseni olarak işlev görerek `summarizer.py` modülünü daha basit bir arayüz olarak sunmaktadır.  `features` dizini altında modüler tasarım deseni kullanılmıştır.


- **Kod Kalitesi ve Sürdürülebilirlik:**  Kod genel olarak okunaklı ve iyi yapılandırılmıştır.  Modüler yaklaşım, kodun sürdürülebilirliğini artırmıştır.  Ancak, TODO yorumları, gelecekte yapılması gereken geliştirmeleri göstermektedir ve teknik borcun bir göstergesidir.


- **Yeni Bağımlılıklar:**  Kesik kod nedeniyle tam liste bilinmiyor.  GUI'nin eklenmesiyle yeni bağımlılıklar eklenmiş olması muhtemeldir.



### 4. SONUÇ YORUMU:

- **Uzun Vadeli Değer ve Etki:**  Bu değişiklikler, aracın işlevselliğini ve kullanıcı deneyimini önemli ölçüde geliştirmiştir.  Daha sağlam bir CI/CD süreci ve daha detaylı bir changelog yönetimi sağlanmıştır.  Ancak, TODO listesindeki geliştirmelerin tamamlanması, projenin uzun vadeli değerini daha da artıracaktır.


- **Teknik Borç:**  Bazı geliştirmeler (TODO listesi) teknik borç olarak kalmaktadır.  Ancak, modüler tasarım ve CI/CD iyileştirmeleri, teknik borcun azaltılmasına katkı sağlamıştır.  Yeni eklenen özellikler de yeni teknik borç eklemiştir.


- **Gelecekteki Geliştirmelere Hazırlık:**  Modüler tasarım, gelecekteki geliştirmelerin (AI destekli özetleme, sesli komut, otomatik güncelleme) daha kolay entegre edilebilmesi için sağlam bir temel oluşturmuştur.  CI/CD pipeline'ındaki iyileştirmeler de, gelecekteki geliştirmelerin daha güvenli bir şekilde uygulanmasını sağlayacaktır.

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

**Last updated**: June 20, 2025 by Summarizer Framework v8.3.5
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
