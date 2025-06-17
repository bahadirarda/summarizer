# 🚀 Summarizer Framework
> Kullanıcı dostu bir arayüzle özetleme işlemini kolaylaştıran güçlü bir web tabanlı özetleme aracı.


## 📊 Proje Durumu
Proje aktif olarak geliştirilmektedir. Son güncellemeler, kurulum ve GUI başlatma süreçlerini iyileştirmeye odaklanmıştır.  Kullanıcı deneyimini artırmak ve sistemin güvenilirliğini güçlendirmek için hata yönetimi ve kod okunabilirliği üzerinde önemli iyileştirmeler yapılmıştır.


## ✨ Özellikler
* **Güçlü Özetleme Algoritmaları:**  (Algoritma detayları buraya eklenecek)
* **Kullanıcı Dostu Arayüz:**  Kolay ve sezgisel bir GUI ile özetleme işlemini gerçekleştirin.
* **Modüler Tasarım:**  Kolay genişletilebilir ve sürdürülebilir bir mimariye sahiptir.
* **Gelişmiş Hata Yönetimi:**  Beklenmedik hatalara karşı daha dayanıklı ve güvenilir bir sistem.
* **Adım Adım Kurulum:**  Kullanıcı dostu bir kurulum süreci.


## Değişen Dosyalar:
`install_gui.py`, `gui_launcher.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

- **Hangi sistem bileşenleri ve katmanlar etkilendi?**  Değişiklikler, Summarizer Framework'ün kurulum ve GUI başlatma katmanlarını etkilemiştir.  `install_gui.py` dosyası GUI ve terminal komutlarını içeren kurulum sürecini yönetirken, `gui_launcher.py` dosyası GUI'nin başlatılmasını sağlar.  Her iki dosya da GUI bileşenini etkiler.

- **Mimari değişikliklerin etkisi nedir?** Mimariye önemli bir değişiklik eklenmemiştir.  Değişiklikler, mevcut mimariye yeni bir fonksiyonellik eklemek yerine, mevcut fonksiyonların daha kullanıcı dostu ve sağlam hale getirilmesine odaklanmıştır.  `install_gui.py` dosyasındaki değişiklikler, modülerliği artırarak  `features` alt dizinindeki modüllerin (`gui_installer`, `terminal_commands`) kullanımıyla kod organizasyonunu iyileştirmiştir.

- **Kod organizasyonunda hangi iyileştirmeler yapıldı?**  `install_gui.py` dosyasında,  fonksiyonların `features` alt dizinindeki modüllere taşınmasıyla daha modüler bir yapı oluşturulmuştur.  Bu, kodun okunabilirliğini ve sürdürülebilirliğini artırır.  `gui_launcher.py` dosyasında ise `project_root` değişkeninin tanımlanması ve `sys.path.insert` kullanımı, projenin farklı dizinlerden çalıştırılmasını daha sağlam hale getirmiştir.  Her iki dosyada da `try-except` blokları kullanılarak hata yönetimi iyileştirilmiştir.


### 2. İŞLEVSEL ETKİ:

- **Hangi özellikler eklendi, değiştirildi veya kaldırıldı?**  Yeni bir özellik eklenmemiştir.  Kurulum ve GUI başlatma süreçleri iyileştirilmiştir.

- **Kullanıcı deneyimi nasıl etkilendi?**  Kullanıcı deneyimi, daha bilgilendirici hata mesajları ve adım adım ilerleme gösterimi sayesinde önemli ölçüde iyileştirilmiştir.  `install_gui.py` dosyasındaki değişiklikler, kullanıcıya kurulumun başarılı olup olmadığını net bir şekilde bildirir ve sonraki adımlar için yönlendirme yapar.  `gui_launcher.py` dosyasındaki değişiklikler, eksik GUI bileşenleri durumunda kullanıcıya daha açıklayıcı hata mesajları gösterir ve `install_gui.py` betiğini çalıştırmasını önerir.

- **Performans, güvenlik veya güvenilirlik üzerindeki etkiler?** Performans üzerindeki etki ihmal edilebilir düzeydedir.  Güvenlik üzerinde doğrudan bir etkisi yoktur.  Ancak, iyileştirilmiş hata yönetimi sayesinde güvenilirlik artmıştır.


### 3. TEKNİK DERINLIK:

- **Hangi tasarım desenleri uygulandı veya değiştirildi?**  Belirgin bir tasarım deseni değişikliği veya uygulanması gözlemlenmemiştir.  Ancak, kodun modülerliğinin artırılması ve hata yönetiminin iyileştirilmesi iyi bir yazılım geliştirme uygulamasıdır ve dolaylı olarak  (örneğin, açık-kapalı prensibi) tasarım prensiplerini destekler.

- **Kod kalitesi ve sürdürülebilirlik nasıl gelişti?**  Kod kalitesi ve sürdürülebilirlik, modüler tasarım, daha iyi hata yönetimi (`try-except` blokları) ve daha okunabilir kod sayesinde geliştirilmiştir.

- **Yeni bağımlılıklar veya teknolojiler eklendi mi?**  Yeni bir bağımlılık eklenmemiştir.  Mevcut `pathlib` ve `flet` kütüphaneleri kullanılmaya devam edilmiştir.


### 4. SONUÇ YORUMU:

- **Bu değişikliklerin uzun vadeli değeri ve etkisi nedir?**  Bu değişikliklerin uzun vadeli değeri, daha kullanıcı dostu, sağlam ve sürdürülebilir bir kurulum ve GUI başlatma sürecidir.  Bu, daha geniş bir kullanıcı kitlesine ulaşmayı ve daha geniş bir kabul görmeyi kolaylaştırır.

- **Projenin teknik borcu nasıl etkilendi?**  Projenin teknik borcu, daha modüler ve daha iyi dokümante edilmiş bir kod yapısıyla azaltılmıştır.  `gui_launcher.py` dosyasındaki `project_root` değişkeninin sabit kod olarak kullanılması potansiyel bir teknik borç olarak değerlendirilebilir; daha esnek bir çözüm (örneğin, konfigürasyon dosyası) tercih edilebilir.

- **Gelecekteki geliştirmelere nasıl hazırlık yapıldı?**  Modüler tasarım, gelecekte yeni GUI bileşenleri veya terminal komutları eklemeyi kolaylaştırır.  İyileştirilmiş hata yönetimi, beklenmedik hataların daha kolay yönetilmesini sağlar.  `sys.path` manipülasyonu ve daha iyi hata işleme mekanizması, gelecekteki GUI güncellemelerini daha kolay ve güvenilir bir şekilde uygulamayı mümkün kılar.

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

**Last updated**: June 17, 2025 by Summarizer Framework v7.12.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
