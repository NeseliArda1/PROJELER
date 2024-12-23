
from veritabanı import Veritabani  # Veritabanı işlemleri için gerekli sınıfı içe aktarır
from log import Log

class Urun:
    def ekle(kullanici_id, ad, fiyat, urun):  # Ürün eklemek için fonksiyon tanımı
        conn = Veritabani().baglan()  # Veritabanına bağlanır
        cursor = conn.cursor()  # Veritabanı üzerinde işlem yapabilmek için imleç oluşturur
        cursor.execute("INSERT INTO urunler (ad, fiyat) VALUES (?, ?)", (ad, fiyat))  # Veritabanına yeni ürün eklemek için SQL sorgusu çalıştırır
        Log.kaydet(kullanici_id, f"Ürün eklendi: {urun[1]}, Fiyat: {urun[2]} TL")
        conn.commit()  # Yapılan değişiklikleri veritabanına kaydeder
        conn.close()  # Veritabanı bağlantısını kapatır

    def sil(kullanici_id, urun_id):  # Ürün silmek için fonksiyon tanımı
        conn = Veritabani().baglan()  # Veritabanına bağlanır
        cursor = conn.cursor()  # Veritabanı üzerinde işlem yapabilmek için imleç oluşturur
        cursor.execute("DELETE FROM urunler WHERE id=?", (urun_id,))  # Belirtilen id'ye sahip ürünü silmek için SQL sorgusu çalıştırır
        Log.kaydet(kullanici_id, f"Ürün silindi: {urun_id[1]}")
        conn.commit()  # Yapılan değişiklikleri veritabanına kaydeder
        conn.close()  # Veritabanı bağlantısını kapatır

    def satin_al(kullanici_id, urun_id):  # Ürün satın almak için fonksiyon tanımı
        conn = Veritabani().baglan()  # Veritabanına bağlanır
        cursor = conn.cursor()  # Veritabanı üzerinde işlem yapabilmek için imleç oluşturur
        cursor.execute("SELECT * FROM urunler WHERE id=?", (urun_id,))  # Belirtilen id'ye sahip ürünü veritabanından seçmek için SQL sorgusu çalıştırır
        urun = cursor.fetchone()  # SQL sorgusunun döndürdüğü ilk satırı alır (tek bir ürün)
        if urun:  # Eğer ürün bulunduysa
            Log.kaydet(kullanici_id, f"Ürün satın alındı: {urun[1]}, Fiyat: {urun[2]} TL")  # Satın alma işlemini log kaydeder
            print(f"Satın alındı: {urun[1]}, Fiyat: {urun[2]} TL")  # Ürün satın alındığını ekrana yazdırır
        else:  # Eğer ürün bulunamadıysa
            print("Ürün bulunamadı!")  # Ürün bulunamadığını ekrana yazdırır
        conn.close()  # Veritabanı bağlantısını kapatır

    def listele():  # Ürünleri listelemek için fonksiyon tanımı
        conn = Veritabani().baglan()  # Veritabanına bağlanır
        cursor = conn.cursor()  # Veritabanı üzerinde işlem yapabilmek için imleç oluşturur
        cursor.execute("SELECT * FROM urunler")  # Veritabanındaki tüm ürünleri seçmek için SQL sorgusu çalıştırır
        urunler = cursor.fetchall()  # SQL sorgusunun döndürdüğü tüm satırları alır
        for urun in urunler:  # Her bir ürünü döngüyle teker teker işler
            print(urun)  # Ürünü ekrana yazdırır
        conn.close()  # Veritabanı bağlantısını kapatır
