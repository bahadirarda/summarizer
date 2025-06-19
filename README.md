# 🚀 project.110620251156
> Changelog ve sürüm yönetimini otomatikleştiren, AI destekli özetleme ve gelişmiş Git entegrasyonu sunan bir web projesi.

## 📊 Proje Durumu
Geliştirme aşamasında. Son değişiklikler, changelog güncelleme süreçlerini otomatikleştirmeye, sürüm yönetimini iyileştirmeye ve geliştirici deneyimini geliştirmeye odaklanmıştır.  AI entegrasyonu ve gelişmiş Git iş akışı yönetimi sayesinde daha verimli ve hatasız bir sürüm kontrol sistemi sağlanmıştır.

## ✨ Özellikler
* 🔄 **Otomatik Sürüm Artırımı:** Impact seviyesine (Critical, High, Medium, Low) göre otomatik sürüm numarası artışı.
* ✍️ **AI Destekli Changelog Özetleme:** Gemini AI kullanarak değişikliklerin otomatik özetlenmesi.
*  branching **Gelişmiş Branch Yönetimi:**  `main` veya `master` branch'lerinde yapılan değişiklikler için yeni branch oluşturma sorgulaması. AI destekli branch adı önerisi.
* 🤖 **CI Entegrasyonu:** `run_ci_checks.py` script'i ile kod kalitesi ve uyumluluk kontrolleri.
* 💾 **Otomatik Yedekleme:** Değişikliklerden önce dosya yedeklemesi.
* 🔀 **Develop'ten Staging'e Pull Request:**  Yeni bir geliştirme akışı sağlayan `develop` branch'inden `staging` branch'ine pull request oluşturma.
* 🚦**Kontrollü Git İş Akışı:**  Push işlemi onayı ve opsiyonel Pull Request oluşturma.


## Değişen Dosyalar:
`src/utils/changelog_updater.py` dosyasında önemli değişiklikler yapılmıştır.  Diğer yardımcı dosyalar (`file_tracker.py`, `json_changelog_manager.py`, `readme_generator.py`, `version_manager.py`, `git_manager.py`)  `changelog_updater.py` ile etkileşim halindedir ve dolaylı olarak etkilenmiştir.


## ANALİZ GÖREVİ:

### 1. YAPISAL ANALİZ:

- **Etkilenen Sistem Bileşenleri ve Katmanlar:**  Değişiklikler öncelikle yardımcı araçlar katmanındaki `changelog_updater.py` dosyası ve ona bağlı diğer yardımcı modüller (`file_tracker.py`, `json_changelog_manager.py`, `readme_generator.py`, `version_manager.py`, `git_manager.py`) üzerinde yoğunlaşmıştır.  Bu modüller, dosya izleme, changelog yönetimi, README güncellemeleri, sürüm kontrolü ve Git entegrasyonu gibi görevlerden sorumludur.

- **Mimari Değişikliklerin Etkisi:**  Temel mimari değişmemiş olmakla birlikte, `changelog_updater.py` dosyasının işlevselliği önemli ölçüde genişletilmiştir.  Daha önce muhtemelen farklı dosyalarda veya `changelog_updater.py` içinde dağınık olarak bulunan fonksiyonlar, daha iyi organize edilmiş ve modüler bir yapıya kavuşmuş olabilir (tam kod olmadan kesin yorum yapmak zor).  Bu, potansiyel olarak daha iyi sürdürülebilirlik ve bakımı kolay bir kod yapısına yol açar ancak  `changelog_updater.py` dosyasının boyutu, gelecekte daha fazla modülerliğe ihtiyaç duyulabileceğini göstermektedir.

- **Kod Organizasyonunda Yapılan İyileştirmeler:**  Üç farklı log mesajında farklı kod organizasyon iyileştirmelerine dair yorumlar vardır.  Birinci log, ilgili fonksiyonların birlikte gruplandırılmasıyla bir iyileştirmeden bahseder. İkinci log,  `changelog_updater.py`'nin farklı modülleri kullanarak sorumlulukları paylaştırdığını ve bunun iyi bir modülerlik örneği olduğunu belirtir. Üçüncü log ise, Git işlemlerinin `git_manager` modülüne daha iyi entegre edildiğini ve kodun daha temiz ve bakımı kolay olmasını sağladığını vurgular. Bu üç yorum birlikte ele alındığında, kodun daha modüler ve organize hale getirildiği sonucuna varabiliriz.


### 2. İŞLEVSEL ETKİ:

- **Eklenen, Değiştirilen veya Kaldırılan Özellikler:**
    * **Eklenen Özellikler:** Otomatik sürüm artırımı (impact seviyesine göre), AI destekli changelog özetleme, gelişmiş branch yönetimi (AI destekli branch adı önerisi ve kullanıcı onayı), CI entegrasyonu, otomatik dosya yedekleme, `develop` branch'inden `staging` branch'ine pull request oluşturma, kontrollü Git iş akışı (push onayı ve opsiyonel pull request oluşturma).
    * **Değiştirilen Özellikler:**  Mevcut changelog ve sürüm yönetimi işlemleri otomatikleştirilmiştir. Git ile etkileşim daha kontrollü ve kullanıcı dostu hale getirilmiştir.
    * **Kaldırılan Özellikler:** Açıkça belirtilmemiştir, ancak manuel sürüm yönetimi ve manuel changelog oluşturma işlemleri kısmen veya tamamen otomasyonla yer değiştirmiştir.

- **Kullanıcı Deneyiminin Etkilenmesi:** Kullanıcı deneyimi önemli ölçüde iyileştirilmiştir.  Manuel işlemler otomatikleştirildiğinden, geliştiriciler daha az zaman harcayarak daha verimli çalışabilirler.  Ancak, AI özeti ve branch adı önerisi gibi bazı noktalarda hala kullanıcı etkileşimi mevcuttur.  Kontrollü Git iş akışı, hataların önlenmesine ve daha güvenli bir geliştirme sürecine katkıda bulunur.

- **Performans, Güvenlik veya Güvenilirlik Üzerindeki Etkiler:** Performans, AI aracının (Gemini) performansına ve CI kontrol sürelerine bağlıdır.  Güvenlik ve güvenilirlik, CI kontrolleri, otomatik yedekleme ve kontrollü Git iş akışı sayesinde iyileştirilmiştir.  Ancak, AI aracına olan bağımlılık potansiyel bir risktir.


### 3. TEKNİK DERİNLİK:

- **Tasarım Desenleri:**  `ImpactLevel` enum'u ve `_detect_impact_level` fonksiyonunun, Strateji Deseni'ni izlediği belirtilmiştir.  Bu, farklı impact seviyelerine göre farklı sürüm artırım kurallarının uygulanabilmesini sağlar.  Kodda başka tasarım desenleri olup olmadığı, tam kod olmadan kesin olarak belirlenemez.

- **Kod Kalitesi ve Sürdürülebilirliğin Gelişimi:** Kod kalitesi ve sürdürülebilirliği, daha iyi modülerlik (potansiyel olarak), tip ipuçlarının kullanımı (`typing` modülü), logging mekanizması (`logger_changelog`) ve hata yönetiminin iyileştirilmesi (`try-except` blokları) ile geliştirilmiştir.  Ancak, `changelog_updater.py` dosyasının uzunluğu hala bir iyileştirme gerektiğini göstermektedir.

- **Yeni Bağımlılıklar veya Teknolojiler:** Gemini AI aracı entegre edilmiştir. Bu, yeni bir dış bağımlılık anlamına gelir.  `urllib.parse` ve `subprocess` gibi kütüphanelerin kullanımı da belirtilmiştir.


### 4. SONUÇ YORUMU:

- **Uzun Vadeli Değer ve Etki:**  Bu değişiklikler, changelog ve sürüm yönetimini otomatikleştirerek uzun vadede geliştirici verimliliğini artıracaktır.  Hata olasılığı azaltılmış ve daha tutarlı bir geliştirme süreci sağlanmıştır. AI entegrasyonu, geliştiricilerin zamanını daha iyi kullanmalarını sağlar.  Kontrollü Git iş akışı, daha güvenli ve şeffaf bir geliştirme süreci sunar.

- **Projenin Teknik Borcunun Etkilenmesi:**  `changelog_updater.py` dosyasının uzunluğu, potansiyel bir teknik borçtur.  Ancak, kodun daha modüler hale getirilmesi bu borcu azaltmaya yardımcı olabilir.

- **Gelecekteki Geliştirmelere Hazırlık:**  Daha fazla otomasyon ve entegre araçlar eklemek daha kolay olacaktır.  Ancak, AI entegrasyonunun sürdürülebilirliği ve bakımının dikkate alınması gerekir.  `changelog_updater.py` dosyasının yeniden yapılandırılması, gelecekteki geliştirmeleri daha kolay ve daha yönetilebilir hale getirecektir.  `develop`'ten `staging`'e pull request özelliği, geliştirme akışına daha fazla esneklik katmıştır.

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

**Last updated**: June 20, 2025 by Summarizer Framework v13.0.0
*This README is automatically generated and updated based on project activity.*

> *"Automatically maintained with AI-powered analysis"*
