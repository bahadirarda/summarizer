# 🚀 Summarizer Framework
> Özetleme işlemlerini kolaylaştıran, hem GUI hem de komut satırı arayüzü ile kullanılabilen, modüler ve genişletilebilir bir web projesi.

## 📊 Proje Durumu
Proje aktif olarak geliştiriliyor ve kurulum sürecinin otomasyonu, kullanıcı deneyiminin iyileştirilmesi ve yeni özelliklerin eklenmesi üzerinde duruluyor. Stabilite ve performans iyileştirmeleri de devam ediyor.

## ✨ Özellikler
*   ✨ **GUI ve CLI Desteği:** Hem grafik arayüzü hem de komut satırı üzerinden kullanım imkanı.
*   ⚙️ **Otomatik Kurulum:** GUI ve terminal komutlarının otomatik kurulumu ile kolay kurulum deneyimi.
*   📸 **Ekran Görüntüsü Analizi:** Ekran görüntüsü alma ve analiz etme yeteneği.
*   ✔️ **Durum Kontrolü:** Uygulamanın farklı bileşenlerinin durumunu kontrol etme özelliği.
*   🧩 **Modüler Tasarım:** Yeni özelliklerin kolayca eklenebilmesi için modüler bir yapı.
*   📖 **Geliştirilmiş Kullanıcı Deneyimi:** Kurulum sürecini basitleştiren ve anlaşılır hata mesajları sunan bir deneyim.

## Değişen Dosyalar:
`install_gui.py`, `summarizer.py`

---

### 1. YAPISAL ANALİZ:

*   **Etkilenen Sistem Bileşenleri ve Katmanlar:**
    *   **Kullanıcı Arayüzü Katmanı:** `features.gui_installer` modülü ve `--gui` komutu ile GUI kurulum ve başlatma işlemleri etkilendi.
    *   **Komut Satırı Arayüzü (CLI) Katmanı:** `features.terminal_commands` modülü ve yeni komut satırı argümanları ( `--install_terminal`, `--uninstall_terminal`, `screenshot` vb.) ile CLI etkilendi.
    *   **Çekirdek İş Mantığı:** `src.main.summarizer` modülü, `summarizer.py` üzerinden yapılan çağrılarla dolaylı olarak etkilendi. Yeni özellikler (ekran görüntüsü alma) bu katmanın işleyişini etkileyebilir.
    *   **Giriş Noktası Katmanı:** `summarizer.py` dosyası, uygulamanın ana giriş noktası olarak doğrudan etkilendi. Argüman ayrıştırma, modül çağırma ve özellik aktivasyonu bu katmanın temel sorumlulukları.
*   **Mimari Değişikliklerin Etkisi:**
    *   **Dağıtım Mimarisi:** `install_gui.py`, kurulum sürecini otomatikleştirerek dağıtım mimarisini basitleştiriyor. GUI ve CLI kurulumunu tek bir betik üzerinden yönetmek, "infrastructure as code" yaklaşımına yaklaşıyor.
    *   **Modülerlik ve Genişletilebilirlik:** Yeni komutlar ve özellikler eklemek için modüler bir yaklaşım benimsenmiş. Özellikler ayrı modüllerde tutularak ana kodun daha temiz kalması sağlanıyor.
    *   **Facade Deseni Uygulaması:** `summarizer.py`, kurulum ve özellik yönetimi gibi karmaşık işlemleri alt sistemlere delege ederek kullanıcıya basitleştirilmiş bir arayüz sunuyor. Bu, Facade deseninin bir uygulaması.
*   **Kod Organizasyonunda Hangi İyileştirmeler Yapıldı:**
    *   `install_gui.py` içerisinde GUI ve terminal komutları için kurulum adımları ayrı fonksiyonlara delege edilerek modülerlik arttırıldı. Hata yönetimi (`try...except`) ile kurulumun sağlamlığı iyileştirildi.
    *   `summarizer.py` içerisindeki işlevsellik, `features` dizinindeki farklı modüllere ayrıldı, bu da kodun okunabilirliğini ve bakımını kolaylaştırdı. Komut satırı argümanlarının kullanımı ve açıklamaları daha net bir şekilde tanımlandı.

### 2. İŞLEVSEL ETKİ:

*   **Hangi Özellikler Eklendi, Değiştirildi veya Kaldırıldı:**
    *   **Eklendi:** Otomatik GUI kurulumu (`install_full_gui_package` fonksiyonu aracılığıyla).
    *   **Eklendi:** Otomatik terminal komutu kurulumu (`install_terminal_command` fonksiyonu aracılığıyla).
    *   **Eklendi:** Kurulum adımlarının başarılı/başarısız olduğuna dair geri bildirim.
    *   **Eklendi:** Kurulum tamamlandıktan sonra kullanılabilir komutların listesi ve API anahtarı yapılandırma talimatları (`install_gui.py`).
    *   **Eklendi:** `--setup`, `--gui`, `screenshot`, `ss`, `--install_terminal`, `--uninstall_terminal`, `--status` gibi yeni komut satırı komutları (`summarizer.py`).
    *   **Eklendi:** GUI entegrasyonu ve ekran görüntüsü alma özelliği (`summarizer.py`).
*   **Kullanıcı Deneyimi Nasıl Etkilendi:**
    *   Kurulum süreci basitleştirilerek kullanıcı deneyimi iyileştirildi. Manuel kurulum adımları ortadan kaldırıldı ve kullanıcıya daha akıcı bir deneyim sunuldu (`install_gui.py`).
    *   Yeni komut satırı komutları ve GUI entegrasyonu sayesinde uygulama daha çok yönlü hale geldi. Kullanıcılar, farklı görevleri daha hızlı ve kolay bir şekilde tamamlayabiliyor (`summarizer.py`).
    *   Başarısız kurulum durumunda sağlanan hata mesajları ve çözüm önerileri de kullanıcı deneyimini destekliyor (`install_gui.py`).
*   **Performans, Güvenlik veya Güvenilirlik Üzerindeki Etkiler:**
    *   **Performans:** Ekran görüntüsü alma ve işleme gibi yeni özellikler uygulamanın performansını etkileyebilir. Bu özellikler için optimizasyonlar yapılması gerekebilir (`summarizer.py`).
    *   **Güvenlik:** Ekran görüntüsü alma özelliği, hassas bilgilerin yanlışlıkla paylaşılması riskini taşıyor. Bu nedenle güvenlik önlemleri alınmalı (örn. izin kontrolü) (`summarizer.py`). `install_gui.py` içerisindeki kurulum fonksiyonlarının sistemde ayrıcalıklı işlemler yapması durumunda güvenlik açıkları oluşma potansiyeli var.
    *   **Güvenilirlik:** Modüler tasarım, bir modüldeki hatanın tüm uygulamayı etkileme olasılığını azaltıyor.

### 3. TEKNİK DERINLIK:

*   **Hangi Tasarım Desenleri Uygulandı veya Değiştirildi:**
    *   **Facade Pattern:** `install_gui.py` ve `summarizer.py`, kurulum işlemlerini ve alt modüllerin işlevselliğini basitleştirilmiş bir arayüz aracılığıyla sunarak Facade Pattern'i uyguluyor.
    *   **Command Pattern:** `summarizer.py` içerisindeki komut satırı argümanlarının işlenmesi ve ilgili fonksiyonların çağrılması, Command Pattern'in bir uygulaması olarak görülebilir.
*   **Kod Kalitesi ve Sürdürülebilirlik Nasıl Gelişti:**
    *   Modüler tasarım, kodun okunabilirliğini, test edilebilirliğini ve sürdürülebilirliğini artırıyor.
    *   Docstring'ler ve yorumlar, kodun anlaşılmasını kolaylaştırıyor.
    *   `install_gui.py` ve `summarizer.py` içerisinde hata yönetimi uygulanmış, bu da kodun daha sağlam olmasını sağlıyor.
*   **Yeni Bağımlılıklar veya Teknolojiler Eklendi mi:**
    *   `install_gui.py` doğrudan yeni bir bağımlılık eklememiş. Ancak `features.gui_installer` ve `features.terminal_commands` modüllerinin bağımlılıkları kontrol edilmeli.
    *   `summarizer.py` içerisinde `argparse` ve `pathlib` modülleri kullanılıyor. Ekran görüntüsü alma özelliği için ek kütüphaneler (örn. `PIL`, `mss`) gerekebilir. GUI entegrasyonu için GUI kütüphaneleri (örn. `Tkinter`, `PyQt`, `wxPython`) kullanılıyor olabilir.

### 4. SONUÇ YORUMU:

*   **Bu Değişikliklerin Uzun Vadeli Değeri ve Etkisi Nedir:**
    *   Uygulamanın daha kullanıcı dostu, erişilebilir ve genişletilebilir hale gelmesini sağlıyor.
    *   Yeni özelliklerin kolayca entegre edilmesine olanak tanıyor.
    *   Modüler tasarım, kodun bakımını ve güncellenmesini kolaylaştırıyor.
    *   Otomatik kurulum, dağıtım ve bakım maliyetlerini düşürebilir.
*   **Projenin Teknik Borcu Nasıl Etkilendi:**
    *   Modüler tasarım ve daha iyi dokümantasyon, teknik borcu azaltıyor.
    *   Ekran görüntüsü alma ve GUI entegrasyonu gibi karmaşık özellikler, eğer iyi tasarlanmaz ve test edilmezse teknik borcu artırabilir.
    *   `install_gui.py`'deki yetersiz hata yönetimi, belirsiz hata mesajları ve eksik testler ileride kurulum sorunlarına yol açabilir.
    *   `TODO` yorumları, çözülmesi gereken sorunları veya iyileştirilmesi gereken alanları gösteriyor.
*   **Gelecekteki Geliştirmelere Nasıl Hazırlık Yapıldı:**
    *   Modüler tasarım, gelecekteki özelliklerin eklenmesini kolaylaştırıyor.
    *   Açık arayüzler, farklı bileşenler arasındaki etkileşimleri netleştirerek, gelecekteki değişikliklerin etkisini anlamayı kolaylaştırıyor.
    *   `TODO` yorumları, gelecekteki geliştirme yönlerini gösteriyor. Konfigürasyon yönetimi için harici bir konfigürasyon dosyası kullanılabilir hale getirilmelidir. Otomatik testler yazılmalı ve kurulumun farklı senaryolarda doğru bir şekilde çalıştığı doğrulanmalıdır. `features.gui_installer` ve `features.terminal_commands` modülleri daha da modüler hale getirilebilir.

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

**Last updated**: June 20, 2025 by Summarizer Framework v15.16.8
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
