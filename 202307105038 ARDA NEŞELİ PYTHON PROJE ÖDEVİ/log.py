
import datetime 
from veritabanı import Veritabani

class Log:
    def kaydet(kullanici_id, eylem): # log eklemek için fonksiyon tanımladım
        conn = Veritabani().baglan() # Veritabanına bağlanır
        cursor = conn.cursor() # Veritabanında işlem için imleç oluşturur
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO loglar (kullanici_id, eylem, zaman) VALUES (?, ?, ?)", (kullanici_id, eylem, zaman))
        conn.commit()
        conn.close() # Veritabanı bağlantısını kapatır

    def listele():
        conn = Veritabani().baglan() # Veritabanına bağlanır
        cursor = conn.cursor() # Veritabanında işlem için imleç oluşturur
        cursor.execute("SELECT * FROM loglar") # loglar tablosunu bulur 
        loglar = cursor.fetchall()
        for log in loglar: # Sırayla log kayıtlarını yazdırır
            print(log)
        conn.close() # Veritabanı bağlantısını kapatır
