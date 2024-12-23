
import sqlite3 # SQLite veritabanı işlemleri için gerekli modülü tanımladım

class Veritabani:  # Veritabanı işlemleri için bir sınıf tanımladım
    def __init__(self, db_name='proje.db'):  # proje.db adında bir veritabanı oluşturacak eğer varsa o dosyadan devam edecek
        self.db_name = db_name  # Veritabanı adı olarak 'proje.db' kullanılıyor, bu isim __init__ fonksiyonu ile belirledim

    def baglan(self):  # Veritabanına bağlanmak için bir fonksiyon tanımladım
        return sqlite3.connect(self.db_name)  # Veritabanına bağlanıp, bağlantı nesnesini geri döndürüyorum

    def olustur(self):  # Veritabanı ve tabloları oluşturmak için bir fonksiyon tanımladım
        conn = self.baglan()  # baglan fonksiyonunu çağırarak veritabanına bağlanıyoruz ve bağlantıyı 'conn' değişkenine atadım
        cursor = conn.cursor()  # Veritabanında işlemler yapmak için bir imleç oluşturdum

        # Eğer 'kullanicilar' tablosu yoksa, oluşturmak için SQL komutunu çalıştırıyor
        cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                            id INTEGER PRIMARY KEY,
                            kullanici_adi TEXT NOT NULL UNIQUE,
                            sifre TEXT NOT NULL,
                            rol TEXT NOT NULL)''') # 'rol' sütunu, metin (TEXT) tipinde ve boş geçilemez (NOT NULL)

        # Eğer 'urunler' tablosu yoksa, oluşturmak için SQL komutunu çalıştırıyoruz
        cursor.execute('''CREATE TABLE IF NOT EXISTS urunler (
                            id INTEGER PRIMARY KEY,
                            ad TEXT NOT NULL,
                            fiyat REAL NOT NULL)''')  # 'fiyat' sütunu, ondalıklı sayı (REAL) tipinde ve boş geçilemez (NOT NULL)

        # Eğer 'loglar' tablosu yoksa, oluşturmak için SQL komutunu çalıştırıyoruz
        cursor.execute('''CREATE TABLE IF NOT EXISTS loglar (
                            id INTEGER PRIMARY KEY,
                            kullanici_id INTEGER,
                            eylem TEXT NOT NULL,
                            zaman TEXT NOT NULL,
                            FOREIGN KEY(kullanici_id) REFERENCES kullanicilar(id))''')  # 'kullanici_id' sütunu, 'kullanicilar' tablosundaki 'id' sütununa yabancı anahtar (Foreign Key) olarak bağlanır

        conn.commit()  # Yapılan değişiklikleri veritabanına kaydediyorum
        conn.close()  # Veritabanı bağlantısını kapatıyorum
