
import sqlite3
import random 
from veritabanı import Veritabani
from urun import Urun
from log import Log

class Kullanici:
    def olustur(kullanici_adi, sifre, rol):
        conn = Veritabani().baglan() # Veritabanı bağlantısını oluştur
        cursor = conn.cursor()
        try:
            # Yeni kullanıcıyı veritabanına ekler
            cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre, rol) VALUES (?, ?, ?)", (kullanici_adi, sifre, rol))
            conn.commit()  # Değişiklikleri kaydeder
        except sqlite3.IntegrityError:
            print("Kullanıcı adı zaten mevcut!") # Eğer kullanıcı adı zaten mevcutsa hata mesajı yazdırır
        conn.close()  # Veritabanı bağlantısını kapatır

    def giris_yap(kullanici_adi, sifre):
        conn = Veritabani().baglan() # Veritabanı bağlantısını oluştur
        cursor = conn.cursor() # Girilen kullanıcı adı ve şifre ile eşleşen kullanıcıyı sorgular
        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        kullanici = cursor.fetchone()  # Kullanıcıyı getirir
        conn.close()  # Veritabanı bağlantısını kapatır
        if kullanici:
            print(f"Hoşgeldiniz: {kullanici_adi}") # Eğer kullanıcı bulunduysa hoş geldiniz mesajı yazdırır
            # Kullanıcının rolüne göre Admin veya Misafir sınıfını gönderir
            if kullanici[3] == 'admin':
                return Admin(*kullanici)
            else:
                return Misafir(*kullanici)
        return None  # Kullanıcı bulunamazsa None döndürür

    def sil(kullanici_id):
        conn = Veritabani().baglan() # Veritabanı bağlantısını oluşturur
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kullanicilar WHERE id=?", (kullanici_id,)) # Verilen kullanıcı ID'sine göre kullanıcıyı siler
        conn.commit()  # Değişiklikleri kaydeder
        conn.close()  # Veritabanı bağlantısını kapatır

    def listele():
        conn = Veritabani().baglan() # Veritabanı bağlantısını oluşturur
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar") # Tüm kullanıcıları sorgular ve getirir
        kullanicilar = cursor.fetchall()
        for kullanici in kullanicilar: # Her kullanıcıyı sırayla yazdırır
            print(kullanici)
        conn.close()  # Veritabanı bağlantısını kapatır

class Admin(Kullanici): # Admin sınıfının yapıcı fonksiyon
    def __init__(self, id, kullanici_adi, sifre, rol): 
        self.id = id  # Kullanıcı ID'si
        self.kullanici_adi = kullanici_adi  # Kullanıcı adı
        self.sifre = sifre  # Kullanıcı şifresi
        self.rol = rol  # Kullanıcı rolü (admin)

    def hava_durumu(): # Hava durumu ile ilgili rastgele bir durum ve sıcaklık bilgisi döndüren fonksiyon
        sartlar = ["Güneşli", "Yağmurlu", "Bulutlu", "Rüzgarlı", "Karlı"]  # Olası hava durumu şartları listesi
        sicaklik = random.randint(-10, 35)  # -10 ile 35 derece arasında rastgele bir sıcaklık seçer
        print(f"Hava durumu: {random.choice(sartlar)}, Sıcaklık: {sicaklik}°C")  # Hava durumu ve sıcaklığı ekrana yazdırır

    def menu(self): # Admin menüsü fonksiyonu, kullanıcıya yapılacak işlemleri seçme imkanı sağlar
        while True:  # Kullanıcının çıkış yapana kadar menüde kalmasını sağlar
            print("\nAdmin Menüsü :")  # Admin menüsü başlığı
            print("1. Ürün Satın Al")  # Ürün satın al seçeneği
            print("2. Ürün Ekle")  # Ürün ekle seçeneği
            print("3. Ürün Sil")  # Ürün sil seçeneği
            print("4. Ürünleri Göster")  # Ürünleri göster seçeneği
            print("5. Kullanıcıları Gör")  # Kullanıcıları göster seçeneği
            print("6. Kullanıcı Ekle")  # Yeni kullanıcı ekle seçeneği
            print("7. Kullanıcı Sil")  # Kullanıcı sil seçeneği
            print("8. Log Kayıtlarını Gör")  # Log kayıtlarını göster seçeneği
            print("9. Hava Durumu")  # Hava durumu göster seçeneği
            print("10. Çıkış Yap")  # Çıkış yap seçeneği
            secim = input("Seçiminiz: ")  # Kullanıcıdan bir seçenek girmesini ister
            if secim == '1':  # Kullanıcı 1'i seçerse
                urun_id = int(input("Satın almak istediğiniz ürünün ID'si: "))  # Kullanıcıdan satın almak istediği ürünün ID'sini girmesini ister
                Urun.satin_al(self.id, urun_id)  # Belirtilen ID'ye sahip ürünü satın alır
            elif secim == '2':  # Kullanıcı 2'yi seçerse
                ad = input("Ürün adı: ")  # Kullanıcıdan ürünün adını girmesini ister
                fiyat = float(input("Ürün fiyatı: "))  # Kullanıcıdan ürünün fiyatını girmesini ister
                Urun.ekle(ad, fiyat)  # Belirtilen ad ve fiyata sahip ürünü veritabanına ekler
            elif secim == '3':  # Kullanıcı 3'ü seçerse
                urun_id = int(input("Silmek istediğiniz ürünün ID'si: "))  # Kullanıcıdan silmek istediği ürünün ID'sini girmesini ister
                Urun.sil(urun_id)  # Belirtilen ID'ye sahip ürünü veritabanından siler
                print(f"Silinen ürün: {urun_id}")  # Silinen ürünün ID'sini ekrana yazdırır
            elif secim == '4':  # Kullanıcı 4'ü seçerse
                Urun.listele()  # Tüm ürünleri listeler
            elif secim == '5':  # Kullanıcı 5'i seçerse
                Kullanici.listele()  # Tüm kullanıcıları listeler
            elif secim == '6':  # Kullanıcı 6'yı seçerse
                kullanici_adi = input("Kullanıcı adı: ")  # Kullanıcıdan yeni kullanıcı için kullanıcı adını girmesini ister
                sifre = input("Şifre: ")  # Kullanıcıdan yeni kullanıcı için şifreyi girmesini ister
                rol = input("Rol (admin/misafir): ")  # Kullanıcıdan yeni kullanıcı için rolü (admin veya misafir) girmesini ister
                Kullanici.olustur(kullanici_adi, sifre, rol)  # Yeni kullanıcıyı veritabanına ekler
                print(f"Yeni kullanıcı oluşturuldu: {kullanici_adi}")  # Yeni oluşturulan kullanıcı adını ekrana yazdırır
            elif secim == '7':  # Kullanıcı 7'yi seçerse
                kullanici_id = int(input("Silmek istediğiniz kullanıcının ID'si: "))  # Kullanıcıdan silmek istediği kullanıcının ID'sini girmesini ister
                Kullanici.sil(kullanici_id)  # Belirtilen ID'ye sahip kullanıcıyı veritabanından siler
                print(f"Kullanıcı silindi: {kullanici_id}")  # Silinen kullanıcının ID'sini ekrana yazdırır
            elif secim == '8':  # Kullanıcı 8'i seçerse
                Log.listele()  # Tüm log kayıtlarını listeler
            elif secim == '9':  # Kullanıcı 9'u seçerse
                Admin.hava_durumu()  # Rastgele bir hava durumu ve sıcaklık bilgisi ekrana yazdırır
            elif secim == '10':  # Kullanıcı 10'u seçerse
                print("Çıkış yapılıyor...")  # Çıkış yapıldığını ekrana yazdırır
                break  # Döngüyü kırarak menüden çıkar
            else:
                print("Geçersiz seçim!")  # Geçersiz bir seçim yapıldığında uyarı mesajı ekrana yazdırır

class Misafir(Kullanici):
    def __init__(self, id, kullanici_adi, sifre, rol): # Misafir sınıfının kurucu metodunu tanımladık
        self.id = id # Misafirin id'sini belirledik
        self.kullanici_adi = kullanici_adi # Misafirin kullanıcı adını belirledik
        self.sifre = sifre # Misafirin şifresini belirledik
        self.rol = rol # Misafirin rolünü belirledik

    def hava_durumu(): # Hava durumunu gösteren metodu tanımladık
        sartlar = ["Güneşli", "Yağmurlu", "Bulutlu", "Rüzgarlı", "Karlı"] # Olası hava şartları listesini oluşturduk
        sicaklik = random.randint(-10, 35) # -10 ile 35 arasında rastgele bir sıcaklık değeri seçtik
        print(f"Hava durumu: {random.choice(sartlar)}, Sıcaklık: {sicaklik}°C") # Rasgele bir hava durumu seçip sıcaklıkla birlikte yazdırdık

    def menu(self): # Misafir menüsünü gösteren ve işlemleri yapan metodu tanımladık
        while True: # Menüde sürekli kalmasını sağlamak için sonsuz döngü oluşturduk
            print("\nMisafir Menüsü :") # Misafir menüsü başlığını yazdırdık
            print("1. Ürün Satın Al") # Ürün satın al
            print("2. Ürün Ekle") # Ürün ekle
            print("3. Ürün Sil") # Ürün sil
            print("4. Ürünleri Göster") # Ürünleri göster
            print("5. Hava Durumu") # Hava durumu
            print("6. Çıkış Yap") # Çıkış yap
            secim = input("Seçiminiz: ") # Kullanıcının seçim yapmasını istedik ve girdiyi aldık
            if secim == '1': # Eğer kullanıcı 1'i seçerse
                urun_id = int(input("Satın almak istediğiniz ürünün ID'si: ")) # Satın alınacak ürünün ID'sini aldık
                Urun.satin_al(self.id, urun_id) # Ürünü satın alma işlemini gerçekleştirdik
            elif secim == '2': # Eğer kullanıcı 2'yi seçerse
                ad = input("Ürün adı: ") # Eklenecek ürünün adını aldık
                fiyat = float(input("Ürün fiyatı: ")) # Eklenecek ürünün fiyatını aldık
                Urun.ekle(ad, fiyat) # Ürünü ekleme işlemini gerçekleştirdik
            elif secim == '3': # Eğer kullanıcı 3'ü seçerse
                urun_id = int(input("Silmek istediğiniz ürünün ID'si: ")) # Silinecek ürünün ID'sini aldık
                Urun.sil(urun_id) # Ürünü silme işlemini gerçekleştirdik
                print(f"Silinen ürün: {urun_id}") # Silinen ürünün ID'sini yazdırdık
            elif secim == '4': # Eğer kullanıcı 4'ü seçerse
                Urun.listele() # Ürünleri listeleme işlemini gerçekleştirdik
            elif secim == '5': # Eğer kullanıcı 5'i seçerse
                Misafir.hava_durumu() # Hava durumu gösterme işlemini gerçekleştirdik
            elif secim == '6': # Eğer kullanıcı 6'yı seçerse
                print("Çıkış yapılıyor...") # Çıkış yapılıyor mesajını yazdırdık
                break # Döngüden çıkarak menüden çıkışı sağladık
            else: # Eğer geçersiz bir seçim yapılırsa
                print("Geçersiz seçim!") # Geçersiz seçim mesajını yazdırdık
