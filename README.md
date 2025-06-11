# project.110620251156: Gelişmiş Versiyon Yönetimi ve Otomatik Changelog Oluşturma

> ⚠️ **GÜVENLİK UYARISI**: Bu projede API anahtarları `.env` dosyasında saklanır. Kurulum için `.env.example` dosyasını `.env` olarak kopyalayın ve kendi API anahtarınızı ekleyin. `.env` dosyasını asla paylaşmayın!

🎉 Bu proje, yazılım geliştirme sürecinizi hızlandırmak ve iyileştirmek için tasarlanmıştır!  Versiyon yönetimini otomatikleştiren ve AI destekli otomatik changelog oluşturma özelliği sunan önemli güncellemeler içeriyor.  🚀

## Özellikler ✨

* **Akıllı Versiyon Yönetimi:** `src/utils/version_manager.py` dosyasındaki güncellemeler sayesinde, versiyon numaraları artık otomatik olarak güncelleniyor.  `auto_increment_based_on_changes` fonksiyonu, dosya değişikliklerini analiz ederek (örneğin, "feature", "add_" gibi ifadeleri arayarak) versiyon artış tipini (major, minor, patch) belirliyor. Bu sayede, yalnızca gerçek işlevsel değişikliklere bağlı olarak versiyon artırımı yapılıyor, daha temiz bir versiyon geçmişi elde ediliyor. 
* **Otomatik Changelog Oluşturma:** `changelog_updater.py` dosyasındaki yeni `demo_framework_analysis` fonksiyonu, yapay zeka özetleme kullanarak demo dosyalarındaki değişikliklere göre otomatik changelog girişi oluşturuyor.  `JsonChangelogManager`, `get_file_line_changes`, `get_aggregate_line_stats` fonksiyonlarını kullanarak demo dosyalarındaki satır değişikliklerini analiz eder ve `ImpactLevel.HIGH` olarak işaretlenmiş bir changelog girişi oluşturur. Bu özellik, geliştirme sürecini hızlandırıyor ve changelog oluşturma işlemini otomatikleştiriyor.

## Kullanım Senaryoları 💡

* Büyük ve sık güncellenen projelerde, versiyon yönetimini kolaylaştırmak ve zaman kazanmak.
* Changelog oluşturma işlemini otomatikleştirerek geliştirme ekibinin verimliliğini artırmak.
* Demo projelerinin sürüm yönetimini kolaylaştırmak ve daha iyi takip edebilmek.


## Faydaları 👍

* **Geliştirilmiş Verimlilik:** Otomatik versiyon yönetimi ve changelog oluşturma, geliştirici zamanını ve çabasını önemli ölçüde azaltır.
* **Azaltılmış Hata Olasılığı:** Manuel versiyonlama ve changelog oluşturma işlemlerinde meydana gelebilecek hatalar ortadan kalkar.
* **Daha Temiz Kod Tabanı:**  Kodun daha iyi organize edilmesi ve versiyonlama işlemlerinin iyileştirilmesi, kod tabanının daha temiz ve sürdürülebilir olmasını sağlar.
* **Gelişmiş Sürdürülebilirlik:** Otomatik versiyonlama ve AI destekli changelog sayesinde, projenin uzun vadeli bakımı ve geliştirmeleri daha kolay hale gelir.
* **Teknik Borç Azaltımı:** Daha iyi organize edilmiş kod ve otomatik versiyonlama ile teknik borç azaltılır.

## ANALİZ ÖZETİ

### 1. YAPISAL ANALİZ:

`src/utils/version_manager.py` ve `changelog_updater.py` dosyaları etkilendi.  `VersionManager` sınıfı, versiyon yönetimi işlevlerini tek bir yerde topladı.  Mimari değişiklik yok, ancak kod organizasyonu iyileştirildi. `changelog_updater.py` dosyasına yeni bir fonksiyon eklendi.

### 2. İŞLEVSEL ETKİ:

Otomatik versiyon artırım mekanizması (`auto_increment_based_on_changes` ve `auto_version_management` fonksiyonları) ve AI destekli otomatik changelog oluşturma (`demo_framework_analysis` fonksiyonu) eklendi. Kullanıcı deneyimi doğrudan etkilenmez, ancak geliştirme süreci hızlanır. Performans üzerindeki etki ihmal edilebilir.

### 3. TEKNİK DERINLIK:

`VersionManager` sınıfı, tek sorumluluk prensibine uygun olarak tasarlandı. Kod kalitesi arttı. Yeni bağımlılıklar eklenmedi.  AI entegrasyonu için bir temel oluşturuldu.

### 4. SONUÇ YORUMU:

Bu değişiklikler, geliştirme verimliliğini ve sürdürülebilirliği artırır.  Teknik borç azalır.  AI destekli otomatik changelog ve akıllı versiyonlama, gelecekteki geliştirmeler için güçlü bir temel oluşturur.  Uzun vadede zaman ve kaynak tasarrufu sağlayarak projenin sürdürülebilirliğini önemli ölçüde iyileştirir.