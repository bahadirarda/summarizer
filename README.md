# 🚀 project.110620251156
> ✨  Sürüm yönetimini ve değişiklik günlüğü güncellemelerini otomatikleştiren, AI destekli bir yardımcı araç.  Daha hızlı ve daha güvenilir bir geliştirme süreci için tasarlanmıştır.

## 📊 Proje Durumu
Proje tamamlanmıştır.  Yeni sürüm yönetimi ve changelog güncelleme sistemi başarıyla entegre edilmiştir.  AI destekli özetleme ve otomatik sürüm artırımı gibi özellikler tam olarak çalışır durumda.  `develop` branch'inden `staging` branch'ine pull request oluşturma özelliği eklenmiştir.  Sürekli entegrasyon (CI) kontrolleri, kod kalitesini ve güvenilirliğini korumak için uygulanmıştır.  Sistem, `gemini_client` adlı bir AI aracı kullanarak değişiklikleri otomatik olarak özetliyor; ancak bu aracın güvenilirliği ve maliyetleri göz önünde bulundurulmalıdır.

## ✨ Özellikler
* 🤖 **AI Destekli Değişiklik Özetleme:** Gemini Client kullanılarak değişiklikler otomatik olarak özetlenir.  AI başarısız olursa, varsayılan bir özet kullanılır.
* 📈 **Otomatik Versiyon Artışı:** Impact Level'a (Critical, High, Medium, Low) göre otomatik versiyon numarası artışı.
* 🗂️ **Gelişmiş Changelog Yönetimi:**  Daha hızlı ve daha tutarlı changelog güncellemeleri.
* 🫗 **Dal Yönetimi:** `main` veya `master` dalında değişiklik yapıldığında yeni bir dal oluşturma isteği. AI önerili dal adı veya kullanıcı girişi kullanılabilir.
* 🚦 **CI Entegrasyonu:** Kod kalitesini ve potansiyel sorunları erken tespit etmek için CI kontrolleri.
* 🔀 **Gelişmiş Git Entegrasyonu:** `develop` branch'inden `staging` branch'ine Pull Request oluşturma desteği.  Push işlemi ve Pull Request oluşturma işlemleri ayrı ve kullanıcı tarafından onaylanabilir adımlar halinde ayrıştırılmıştır.


## Değişen Dosyalar:
`src/utils/changelog_updater.py`, `src/utils/version_manager.py`


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

* **Etkilenen Bileşenler ve Katmanlar:**  Değişiklikler, projenin yardımcı araçlar katmanını (`src/utils`) doğrudan etkilemiştir. Özellikle `changelog_updater.py` ve `version_manager.py` dosyaları büyük ölçüde değiştirilmiştir.  `changelog_updater.py`, `file_tracker`, `json_changelog_manager`, `readme_generator`, `version_manager`, ve `git_manager` gibi diğer modüllerle etkileşim halindedir. Bu modüller arasında veri akışı ve etkileşim değiştirilmiştir.

* **Mimari Değişikliklerin Etkisi:** Mimari açısından büyük bir değişiklik olmamakla birlikte, sürüm yönetimi ve changelog güncelleme süreçleri önemli ölçüde otomatikleştirilmiştir.  `version_manager.py`'de,  `VersionManager` sınıfının daha modüler bir yapıya kavuşması ve tek sorumluluk prensibine daha iyi uyması hedeflenmiştir.  `changelog_updater.py`'deki değişiklikler, Git ile etkileşimin daha ayrıntılı ve kontrollü bir şekilde yönetilmesine yol açmıştır.  Push ve Pull Request işlemleri ayrıştırılmış ve kullanıcı kontrolüne alınmıştır.

* **Kod Organizasyonundaki İyileştirmeler:** Kodun daha modüler hale getirilmesi, özellikle Git işlemlerinin `git_manager` modülüne entegre edilmesiyle sağlanmıştır.  `VersionManager` sınıfı içindeki fonksiyonların daha küçük ve özelleşmiş birimlere ayrılması (örneğin, `_has_breaking_changes`, `_has_new_features`), tek sorumluluk prensibine uyumu artırmıştır.  Bu, kodun okunabilirliğini, sürdürülebilirliğini ve test edilebilirliğini iyileştirmiştir.


### 2. İŞLEVSEL ETKİ:

* **Eklenen, Değiştirilen veya Kaldırılan Özellikler:**  En önemli değişiklik, otomatik sürüm artırımı ve AI destekli changelog özetlemesidir.  `develop` branch'inden `staging` branch'ine pull request oluşturma yeteneği eklenmiştir. Push ve Pull Request işlemleri ayrı ve kullanıcı tarafından onaylanabilir adımlar halinde yeniden yapılandırılmıştır.

* **Kullanıcı Deneyimi Üzerindeki Etki:** Kullanıcı deneyimi, otomasyon sayesinde önemli ölçüde iyileştirilmiştir.  Sürüm yönetimi ve changelog güncellemeleri daha kolay ve hızlı hale gelmiştir.  Kullanıcıya daha fazla kontrol sağlayan ve her adımı onaylama olanağı sunan etkileşimli bir akış oluşturulmuştur.

* **Performans, Güvenlik ve Güvenilirlik Üzerindeki Etkiler:** Performans, kullanılan AI aracının performansına ve CI scriptinin süresine bağlıdır.  Güvenlik ve güvenilirlik, CI kontrolleri ve geliştirilmiş dal yönetimi sayesinde artmıştır.  Kodun daha modüler hale getirilmesi ve hata yönetiminin iyileştirilmesi, uzun vadede güvenilirliği artıracaktır.


### 3. TEKNİK DERINLIK:

* **Tasarım Desenleri:** Kodda belirgin bir tasarım deseni değişikliği yoktur, ancak tek sorumluluk prensibi ve açık-kapalı prensibine daha fazla uyum sağlanmıştır.  Modülerlik artırılmıştır.

* **Kod Kalitesi ve Sürdürülebilirlik:** Kod kalitesi ve sürdürülebilirlik, otomasyon, daha iyi hata yönetimi (`try-except` blokları), modüler tasarım ve açıklayıcı isimlendirme ile iyileştirilmiştir.  Tip belirtmeleri (`typing` modülü) kullanılarak kodun okunabilirliği ve bakımı kolaylaştırılmıştır.  Loglama mekanizmasının kullanılması, hata ayıklama ve izlemeyi kolaylaştırır.

* **Yeni Bağımlılıklar:** Yeni bir bağımlılık olan `gemini_client` (AI aracı) eklenmiştir.  `urllib.parse`, `subprocess`, `git`, `json`, `toml`, `pathlib` gibi standart Python kütüphaneleri kullanılmaya devam edilmektedir.


### 4. SONUÇ YORUMU:

* **Uzun Vadeli Değer ve Etki:** Bu değişiklikler, geliştirme sürecinin verimliliğini ve güvenilirliğini artırmaktadır. Uzun vadeli değer, daha hızlı ve daha tutarlı sürüm yönetimi, daha iyi changelog oluşturma ve daha az manuel çalışma anlamına gelir.  Projenin teknik borcu, özellikle manuel changelog ve versiyon yönetimine ilişkin borç azaltılmıştır.

* **Teknik Borç Üzerindeki Etki:** Otomasyon sayesinde, manuel sürüm yönetimi ve changelog güncellemelerine bağlı teknik borç azaltılmıştır.

* **Gelecekteki Geliştirmelere Hazırlık:**  AI entegrasyonu, gelecekte daha gelişmiş otomasyon özelliklerinin eklenmesine olanak tanır.  Daha modüler ve genişletilebilir bir sürüm yönetim sistemi oluşturulmuştur.  Ancak, `gemini_client` aracına bağımlılık, olası bir risk faktörüdür ve bu aracın güvenilirliği ve maliyetleri göz önünde bulundurulmalıdır.  CI scriptinin eksikliği veya başarısızlığı, kod kalitesinin düşmesine neden olabilir.

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

**Last updated**: June 20, 2025 by Summarizer Framework v12.10.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
