
# Arda Market Yönetim Sistemi

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://www.sqlite.org/index.html)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

## İçindekiler

* [Proje Hakkında](#proje-hakkında)
* [Problemler ve Çözümler](#problemler-ve-çözümler)
* [Özellikler](#özellikler)
* [Kurulum](#kurulum)
* [Kullanım](#kullanım)
* [Dosya Yapısı](#dosya-yapısı)
* [Geliştirme Ortamı](#geliştirme-ortamı)
* [Yapan](yapan)

## Proje Hakkında

`Arda Market Yönetim Sistemi`, geleneksel küçük ve orta ölçekli market işletmelerinin karşılaştığı operasyonel zorlukları gidermek amacıyla geliştirilmiş, modern ve güvenli bir masaüstü uygulamasıdır. Python programlama dili ve Tkinter kütüphanesi kullanılarak geliştirilen bu sistem, marketlerin stok, ürün, kullanıcı ve güvenlik yönetimini dijitalleştirerek verimliliği, güvenliği ve rekabetçiliği artırmayı hedefler.

## Problemler ve Çözümler

Geleneksel market işletmelerinin karşılaştığı başlıca problemler ve `Arda Market Yönetim Sistemi`'nin sunduğu çözümler:

1.  **Verimsiz Stok ve Ürün Yönetimi:**
    * **Problem:** Manuel ürün takibi, stok sayımı ve fiyat güncellemeleri zaman alıcıdır ve insan kaynaklı hatalara açıktır, bu da finansal kayıplara yol açar.
    * **Çözüm:** **`urun_islemleri.py`** modülü aracılığıyla kolay ürün ekleme, silme, fiyat ve stok güncelleme imkanı sunar. Ürünler, merkezi bir SQLite veritabanında (**`veritabani_islemleri.py`**) düzenli bir şekilde saklanır.

2.  **Güvensiz Kullanıcı Yönetimi ve Veri Depolama:**
    * **Problem:** Müşteri ve personel bilgilerinin kağıt üzerinde veya güvensiz dijital dosyalarda tutulması veri güvenliği riskleri taşır.
    * **Çözüm:** Kullanıcı bilgileri ve şifreleri, **`veritabani_islemleri.py`**'deki `bcrypt` kullanımıyla güvenli bir şekilde hashlenerek merkezi bir SQLite veritabanında depolanır. Profil resimleri için güvenli dizin yönetimi de sağlanır.

3.  **Eksik Erişim Kontrolü ve Yetkilendirme:**
    * **Problem:** Tüm çalışanların sistemdeki kritik verilere ve işlevlere erişimi, kötüye kullanıma ve yanlış değişikliklere yol açabilir.
    * **Çözüm:** **`kullanici_islemleri.py`**, **`admin_paneli.py`** ve **`misafir_paneli.py`** modülleri ile 'Admin' ve 'Misafir' gibi farklı kullanıcı rolleri tanımlanmıştır. Her rol için özel menüler ve işlevler ayrıştırılarak yetki bazlı erişim kontrolü sağlanır.

4.  **Zayıf Kimlik Doğrulama Mekanizmaları:**
    * **Problem:** Basit kullanıcı adı/şifre tabanlı girişler, kaba kuvvet saldırılarına ve yetkisiz girişlere karşı savunmasızdır.
    * **Çözüm:** **`yardimcilar.py`** modülündeki `Captcha` sınıfı ile bot saldırılarına karşı koruma sağlanır. Ayrıca, **`kullanici_islemleri.py`** modülünde `pyotp` kütüphanesi kullanılarak İki Faktörlü Kimlik Doğrulama (2FA) desteği entegre edilmiştir.

5.  **İşlem Takibi ve Raporlama Eksikliği:**
    * **Problem:** Yapılan satışların, kullanıcı işlemlerinin veya sistemdeki önemli değişikliklerin kaydının tutulmaması, geriye dönük analiz ve güvenlik ihlali tespiti imkanını ortadan kaldırır.
    * **Çözüm:** **`veritabani_islemleri.py`** modülündeki `log_ekle` fonksiyonu ve `loglar` tablosu sayesinde, sisteme yapılan her kritik işlem zaman damgası, kullanıcı adı, işlem ve detay bilgisi ile kaydedilir. Bu log kayıtları **`admin_paneli.py`** üzerinden görüntülenebilir.

## Özellikler

* **Kullanıcı Yönetimi:**
    * Güvenli kullanıcı kaydı ve giriş sistemi (bcrypt şifreleme).
    * İki Faktörlü Kimlik Doğrulama (2FA) desteği (TOTP tabanlı).
    * CAPTCHA doğrulaması ile bot saldırılarına karşı koruma.
    * Admin ve Misafir rolleriyle yetkilendirme.
    * Kullanıcı profil yönetimi (profil resmi güncelleme, şifre değiştirme).
* **Ürün ve Stok Yönetimi (Admin Yetkisi ile):**
    * Ürün ekleme, silme, güncelleme.
    * Ürün fiyat ve stok bilgisi yönetimi.
    * Ürün resim desteği.
    * Kapsamlı ürün listeleme ve görüntüleme.
* **Güvenlik ve İzlenebilirlik:**
    * Detaylı sistem loglama (girişler, ürün işlemleri, şifre değişiklikleri vb.).
    * Admin panelinden log kayıtlarını görüntüleme.
* **Kullanıcı Dostu Arayüz:**
    * Tkinter ile geliştirilmiş sezgisel ve kolay kullanımlı grafik arayüz.
    * Merkezi mesaj yönetimi (**`metinler.py`**) ile tutarlı kullanıcı geri bildirimleri.
* **Ek Özellikler:**
    * Küçük bir kelime oyunu ile kullanıcı deneyimini zenginleştirme (modüler olarak yüklenir).

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edin:

1.  **Python Kurulumu:**
    Sisteminizde Python 3.x yüklü olduğundan emin olun. Python'u [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz.

2.  **Gerekli Kütüphaneleri Yükleme:**
    Proje dizininde (yukarıdaki `cd ArdaMarketYonetimSistemi` komutundan sonra) aşağıdaki komutu çalıştırarak gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
    *(**`requirements.txt`** dosyasının içeriği aşağıdaki gibi olmalıdır. Eğer yoksa, bu dosyayı oluşturup içine bu satırları ekleyin.)*
    ```
    tkinter # Genellikle Python ile gelir, ancak emin olmak için eklenebilir.
    Pillow
    bcrypt
    pyotp
    qrcode
    ```
3.  **Veritabanı Oluşturma:**
    Uygulamayı ilk çalıştırdığınızda otomatik olarak `market_veritabani.db` adında bir SQLite veritabanı oluşturulacak ve varsayılan bir yönetici (`admin`) hesabı eklenecektir.

## Kullanım

Projeyi başlattıktan sonra, ana menü ekranı karşınıza gelecektir.

1.  **Uygulamayı Başlatma:**
    Proje dizininde (klonladığınız veya indirdiğiniz konum) aşağıdaki komutu çalıştırın:
    ```bash
    python ana_menu.py
    ```

2.  **Giriş Yapma:**
    * Varsayılan yönetici hesabı:
        * **Kullanıcı Adı:** `admin`
        * **Şifre:** `admin`
    * Giriş yaparken CAPTCHA doğrulamasını geçmeniz gerekecektir.
    * İlk girişte Admin hesabı için 2FA kurulumu istenecektir. Google Authenticator gibi bir uygulama ile QR kodu okutarak veya gizli anahtarı manuel girerek kurulumu tamamlayın.
    * Admin hesabından `Kullanıcı İşlemleri` menüsünden yeni 'Misafir' kullanıcılar oluşturabilirsiniz.

3.  **Admin Paneli (`admin_paneli.py`):**
    * Ürün Ekle/Sil/Güncelle: Market envanterini yönetmek için.
    * Kullanıcıları Yönet: Yeni kullanıcı ekleme, mevcut kullanıcıları görüntüleme/silme.
    * Sistem Logları: Yapılan tüm kritik işlemlerin loglarını görüntüleme.
    * Profil Yönetimi: Admin profil resmini ve şifresini değiştirme.

4.  **Misafir Paneli (`misafir_paneli.py`):**
    * Ürünleri Görüntüle: Mevcut ürünleri listeleme.
    * Profil Yönetimi: Kendi profil resmini ve şifresini değiştirme.
   

5.  **Güvenli Çıkış:**
    Her panelde bulunan "Güvenli Çıkış" butonu ile uygulamadan güvenle çıkış yapabilirsiniz.

## Dosya Yapısı

Projenin temel dosya yapısı ve her bir dosyanın amacı:

ArdaMarketYonetimSistemi/
├── admin_paneli.py           # Admin kullanıcı arayüzü ve işlevleri.
├── ana_menu.py               # Uygulamanın başlangıç noktası ve ana menü.
├── kullanici_islemleri.py     # Kullanıcı kayıt, giriş, profil yönetimi ve 2FA işlemleri.
├── metinler.py               # Uygulama genelinde kullanılan metin mesajları ve uyarılar.
├── misafir_paneli.py         # Misafir kullanıcı arayüzü ve işlevleri.
├── urun_islemleri.py         # Ürünlerin eklenmesi, silinmesi, güncellenmesi ve görüntülenmesi.
├── veritabani_islemleri.py   # SQLite veritabanı bağlantısı, tablo oluşturma, CRUD işlemleri ve loglama.
├── yardimcilar.py            # CAPTCHA oluşturma gibi yardımcı sınıflar ve fonksiyonlar.
├── requirements.txt          # Proje bağımlılıklarını listeleyen dosya.
├── market_veritabani.db      # Uygulama tarafından oluşturulan SQLite veritabanı dosyası (ilk çalıştırmada oluşur).
├── images/                   # Ürün resimlerinin depolandığı dizin (otomatik oluşturulur).
└── users_profile_pictures/   # Kullanıcı profil resimlerinin depolandığı dizin (otomatik oluşturulur).

## Geliştirme Ortamı

* **Dil:** Python 3.x
* **GUI Kütüphanesi:** Tkinter
* **Veritabanı:** SQLite3
* **Bağımlılıklar:** Pillow, bcrypt, pyotp, qrcode

## Yapan

Numarası: 202307105038
Proje Sahibi: Arda NEŞELİ
