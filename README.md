# 🚀 macOS Özetleyici Yazılımı Kurulum Sihirbazı
> Kullanıcı dostu bir arayüzle macOS için özetleyici yazılımını kolayca kurmanıza olanak sağlayan güçlü bir kurulum sihirbazı.

## 📊 Proje Durumu
Proje aktif geliştirme aşamasındadır.  Son güncellemeler, kullanıcı deneyimini iyileştiren ve kurulum sürecini daha güvenilir hale getiren önemli geliştirmeler içeriyor.  Sürükle ve bırak kurulum desteği eklendi.  GUI ve CLI kurulum seçenekleri arasında sorunsuz geçiş sağlanıyor.

## ✨ Özellikler
* **Kullanıcı Dostu GUI:** PyQt5 tabanlı görsel kurulum arayüzü.
* **Komut Satırı Arabirimi (CLI):**  Esneklik için komut satırı kurulum desteği.
* **Sürükle ve Bırak Kurulumu:** Yeni ve kolay bir kurulum yöntemi.
* **Gelişmiş Hata Yönetimi:**  Daha sağlam ve bilgilendirici hata mesajları.
* **Otomatik Framework Versiyon Tespiti:** README dosyasında proje framework versiyonunun doğru tespiti.
* **Güncellenen README:** Otomatik olarak güncellenen, proje değişikliklerini ve etkilerini gösteren README dosyası.


## Değişen Dosyalar:
`macos-setup-wizard/setup_installer.py`, `macos-setup-wizard/cli_installer.py`, `macos-setup-wizard/gui_installer.py`, `macos-setup-wizard/drag_drop_installer.py`, `macos-setup-wizard/ui/`, `src/utils/readme_generator.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

* **Etkilenen Bileşenler ve Katmanlar:**  Değişiklikler, macOS kurulum sihirbazının tüm katmanlarını etkilemiştir.  `macos-setup-wizard` dizini içindeki `setup_installer.py` (kurulum motorunun giriş noktası), `cli_installer.py`, `gui_installer.py` ve yeni eklenen `drag_drop_installer.py` dosyaları doğrudan etkilenmiştir.  `ui` alt dizini (GUI), `config` alt dizini (ayarlar), `utils` alt dizini (yardımcı fonksiyonlar) ve arka plan görüntü oluşturma ile ilgili dosyalar dolaylı olarak etkilenmiştir.  `src/utils/readme_generator.py` dosyasındaki değişiklikler ise README dosyasının oluşturulmasını ve güncellenmesini etkilemiştir.

* **Mimari Değişikliklerin Etkisi:** Mimari, modüler bir yapıya doğru evrilmiştir.  Başlangıçta muhtemelen tek bir dosyada bulunan kurulum mantığı, farklı kurulum tipleri için ayrı modüllere (CLI, GUI, Drag-and-Drop) ayrılmıştır.  Bu, "Strategy Pattern"e benzer bir yaklaşımı göstermektedir.  MVC veya MVVM mimarisine benzer bir yapıya geçiş yapılmış ve bu da sürdürülebilirliği ve test edilebilirliği artırmıştır.

* **Kod Organizasyonundaki İyileştirmeler:** Kod, alt dizinler ve modüller halinde daha iyi organize edilmiştir.  Hata yönetimi iyileştirilmiş, özellikle `try...except` blokları genişletilmiştir.  `readme_generator.py` dosyasında, `_get_framework_version` fonksiyonu, daha sağlam bir versiyon tespiti için üst dizinleri kontrol edecek şekilde geliştirilmiştir.  README içeriği tek bir noktadan (`generate_complete_readme_content` fonksiyonu) oluşturularak okunabilirlik artırılmıştır.


### 2. İŞLEVSEL ETKİ:

* **Eklenen Özellikler:** Sürükle ve bırak kurulumu eklenmiştir.  GUI kurulumu eklenmiş ve PyQt5 entegrasyonu yapılmıştır. README'ye değişikliklerin etkilerinin dağılımını gösteren bir bölüm eklenmiştir ("impact_counts") ve projedeki değişikliklerin izlenmesiyle ilgili özellikleri özetleyen bir bölüm eklenmiştir ("Tracking Features").  `--cli` argümanı ile komut satırı kurulumu seçeneği eklenmiştir.

* **Değiştirilen Özellikler:**  GUI ve CLI kurulumları arasında daha esnek geçişler sağlanmıştır.  PyQt5 bulunmadığında otomatik olarak CLI'ya geçiş yapılır. README oluşturma süreci optimize edilmiştir.

* **Kaldırılan Özellikler:** Açıkça kaldırılan bir özellik yoktur.

* **Kullanıcı Deneyimi:** Kullanıcı deneyimi, GUI kurulumunun eklenmesi, sürükle ve bırak desteği ve geliştirilmiş hata mesajları ile önemli ölçüde iyileştirilmiştir.

* **Performans, Güvenlik veya Güvenilirlik:** GUI kurulumu CLI'ya göre daha yavaş olabilir, ancak bu beklenen bir durumdur.  Geliştirilmiş hata yönetimi ve modüler yapı güvenilirliği artırır.  Güvenlik açısından belirgin bir değişiklik yok, ancak izinlerin yönetimi konusunda iyileştirmeler yapılmış olabilir.


### 3. TEKNİK DERINLIK:

* **Tasarım Desenleri:** Strategy Pattern (farklı kurulum tipleri için farklı stratejiler), dolaylı olarak Factory Pattern (farklı kurulum tiplerinin oluşturulması) ve Separation of Concerns (sorumlulukların ayrılması) prensipleri kullanılmıştır.

* **Kod Kalitesi ve Sürdürülebilirlik:** Kod kalitesi, modüler tasarım, geliştirilmiş hata yönetimi ve daha iyi kod organizasyonu ile önemli ölçüde iyileştirilmiştir.  Bu, kodun sürdürülebilirliğini ve bakımını kolaylaştırır.

* **Yeni Bağımlılıklar veya Teknolojiler:** PyQt5 (GUI için) ve muhtemelen PIL/Pillow (arka plan görüntü oluşturma için) yeni bağımlılıklar olarak eklenmiştir.


### 4. SONUÇ YORUMU:

* **Uzun Vadeli Değer ve Etki:** Bu değişiklikler, projenin uzun vadeli sürdürülebilirliğini ve kullanıcı deneyimini artırmıştır.  Daha modüler ve daha iyi organize edilmiş kod, gelecekteki geliştirmeleri kolaylaştıracaktır.  Kullanıcılar için daha kullanıcı dostu bir kurulum süreci sunulmuştur.

* **Projenin Teknik Borcu:** Projenin teknik borcu, daha iyi kod organizasyonu ve hata yönetimi sayesinde azaltılmıştır.

* **Gelecekteki Geliştirmelere Hazırlık:** Modüler yapı, gelecekte yeni kurulum yöntemlerinin veya özelliklerin kolayca eklenmesine olanak tanır.  Ancak, PyQt5 bağımlılığı nedeniyle dağıtım stratejisi gözden geçirilmelidir.  Alternatif çözümler (örneğin, PyQt5'in otomatik kurulumu veya alternatif bir GUI kütüphanesi) değerlendirilmelidir.

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

**Last updated**: June 12, 2025 by Summarizer Framework v7.1.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
