# project.110620251156 Projesi: Otomatik Versiyonlama ve Değişiklik Takibi ile Geliştirilmiş Yazılım Geliştirme

👋 Merhaba! Bu proje, yazılım geliştirme süreçlerini iyileştirmek için otomatik versiyonlama ve gelişmiş değişiklik takibi sistemlerini entegre eder.  🚀

## Proje Özellikleri ✨

* **Otomatik Versiyonlama:**  `version_manager.py` dosyasındaki geliştirmeler sayesinde, versiyon numaraları artık otomatik olarak güncellenir.  `auto_increment_based_on_changes` fonksiyonu, dosya değişikliklerini analiz ederek (örneğin, "feature", "add_" gibi ifadeleri arayarak) semantik versiyonlama (major, minor, patch) kurallarına uygun olarak versiyon artışını belirler. Bu, yalnızca gerçek işlevsel değişikliklere bağlı olarak versiyon artırımının yapılmasını sağlar. 
* **Gelişmiş Değişiklik Takibi:**  `changelog_updater.py` dosyası, detaylı changelog oluşturma ve güncelleme işlevselliği ekler.  `ImpactLevel` (CRITICAL, HIGH, MEDIUM, LOW) sınıfı sayesinde değişikliklerin etkisi sınıflandırılır.  Yeni fonksiyonlar, daha anlamlı changelog kayıtları oluşturulmasını sağlar.
* **Otomatik Dokümantasyon Güncelleme:**  `main.py` dosyasındaki değişiklikler, changelog ve README dosyalarının otomatik güncellenmesini sağlar. Bu, dokümantasyonun her zaman güncel olmasını garanti eder.


## Kullanım Senaryoları 🧑‍💻

* Proje geliştiricileri, versiyon numaralarını elle güncellemek zorunda kalmadan,  sürüm kontrol sistemine yapılan her değişiklikten sonra otomatik olarak güncellenen bir versiyon numarası elde ederler.
*  Geliştiriciler, projedeki her değişikliğin etkisini (CRITICAL, HIGH, MEDIUM, LOW) belirterek detaylı bir changelog oluşturabilirler.
*  Kullanıcılar, güncel README ve CHANGELOG dosyalarına erişim sağlayarak projenin son durumuna ve yapılan değişikliklere kolayca ulaşabilirler.


## Faydaları 👍

* **Geliştirici Verimliliği:** Otomatik versiyonlama ve changelog oluşturma, geliştiricilerin zamanını ve çabasını önemli ölçüde azaltır.
* **Hata Azaltımı:** Manuel versiyonlama işlemlerinden kaynaklanan hataların önüne geçilir.
* **Daha İyi İşbirliği:**  Detaylı changelog sayesinde ekip üyeleri arasındaki iletişim ve işbirliği iyileşir.
* **Sürdürülebilirlik:** Daha düzenli ve okunabilir kod yapısı, projenin uzun vadeli bakımını kolaylaştırır.
* **Teknik Borç Azaltımı:**  Otomasyon ve iyileştirilmiş kod organizasyonu, teknik borcu azaltır.


## Analiz Özeti 📝

### 1. YAPISAL ANALİZ:

`src/main.py`, `src/utils/changelog_updater.py` ve `src/utils/version_manager.py` dosyaları etkilendi.  `changelog_updater.py` dosyası modüler hale getirilerek yeni sınıflar (`ImpactLevel`, `ChangeType`, `JsonChangelogManager`) ve fonksiyonlar eklendi. Versiyonlama mantığı `VersionManager` sınıfında gruplandırılarak kod organizasyonu iyileştirildi. Mimari değişiklik, changelog ve versiyon yönetimini daha modüler ve genişletilebilir hale getirdi.

### 2. İŞLEVSEL ETKİ:

Otomatik changelog oluşturma, otomatik versiyon artırımı, dosya değişikliklerine göre versiyonlama türü belirleme (major, minor, patch) ve değişikliklerin etki seviyesi belirleme özellikleri eklendi. Kullanıcı deneyimi, otomatik olarak güncellenen README ve CHANGELOG dosyaları ile iyileştirildi. Performans etkisi ihmal edilebilir düzeyde.

### 3. TEKNİK DERINLIK:

`JsonChangelogManager` sınıfı, Factory veya Strategy Pattern'in bir varyasyonunu temsil edebilir (çoklu changelog formatı desteği için esneklik sağlar).  `VersionManager` sınıfı tek sorumluluk prensibine uygun tasarlandı.  Kod kalitesi ve sürdürülebilirlik iyileştirildi. Yeni bağımlılık eklenmedi.

### 4. SONUÇ YORUMU:

Bu değişiklikler, projenin sürdürülebilirliğini ve geliştirici verimliliğini önemli ölçüde artırdı.  Otomatik dokümantasyon ve versiyonlama, hata olasılığını azaltırken,  daha modüler kod yapısı gelecekteki geliştirmeleri kolaylaştırdı.  Teknik borç azalırken, proje daha sağlam ve genişletilebilir bir temel üzerine kuruldu.


Bu proje, daha temiz, daha sürdürülebilir ve daha verimli bir yazılım geliştirme süreci hedefliyor.  🎉