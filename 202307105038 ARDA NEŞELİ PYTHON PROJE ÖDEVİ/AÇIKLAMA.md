
# Market Uygulaması

Bu proje, SQLite veritabanını kullanarak bir market yönetim sistemi geliştirmektedir. Proje, kullanıcıların ürün satın almasına, ürün eklemesine, ürün silmesine, kullanıcı eklemesine ve kullanıcı silmesine olanak tanır. Ayrıca admin ve misafir kullanıcılar için ayrı menüler bulunmaktadır.

# Dosya Yapısı

1. veritabanı.py: Veritabanı bağlantısı ve tablo oluşturma işlemlerini içerir.
2. urun.py: Ürünlerle ilgili işlemleri içerir.
3. kullanici.py: Kullanıcılarla ilgili işlemleri içerir.
4. log.py : Log kayıt işlemleri buradan gerçekleşir.
5. main.py: Programın giriş noktasıdır.
6. AÇIKLAMA.md: Proje hakkında açıklamalar ve kullanım kılavuzunu içerir.

# Kullanım Kılavuzu

Programı çalıştırmak için yukarıda gördüğünüz sırada dosyaları sırayla çalıştırmanız gerekmektedir.

# Veritabanı Oluşturma

Program çalıştığında, `veritabanı.py` dosyasındaki `Veritabani` sınıfı kullanılarak veritabanı ve tablolar oluşturulur.
proje.db adına sahip olarak bir sqlite3 tablosu oluşur 3 tane tablo oluşur kullanıcılar loglar ve ürünler isminde.

# Kullanıcı İşlemleri

- Yeni Kullanıcı Oluşturma: `main.py` dosyasındaki menüden "Yeni Kullanıcı Oluştur" seçeneği ile kullanıcı oluşturabilirsiniz.
- Giriş Yapma: Kullanıcı adı ve şifre ile giriş yapabilir ve kullanıcı rolüne göre admin veya misafir menüsüne erişebilirsiniz.
- Aşağıdaki menülerde yazan her işlemide yapabilirsiniz.
 
# Admin Menüsü

Admin kullanıcıları için aşağıdaki işlemler yapılabilir:
1. Ürün Satın Al
2. Ürün Ekle
3. Ürün Sil
4. Ürünleri Göster
5. Kullanıcıları Gör
6. Kullanıcı Ekle
7. Kullanıcı Sil
8. Log Kayıtlarını Gör
9. Hava Durumu
10. Çıkış Yap

# Misafir Menüsü

Misafir kullanıcıları için aşağıdaki işlemler yapılabilir:
1. Ürün Satın Al
2. Ürün Ekle
3. Ürün Sil
4. Ürünleri Göster
5. Hava Durumu
6. Çıkış Yap

# Kod Açıklamaları

Her dosyada bulunan sınıf ve fonksiyonlar detaylı yorum satırları ile açıklanmıştır. Bu açıklamalar, kodun ne yaptığını ve nasıl kullanıldığını anlamanıza yardımcı olacaktır.

# OKUL NUMARASI = 202307105038
# AD SOYAD = ARDA NEŞELİ
