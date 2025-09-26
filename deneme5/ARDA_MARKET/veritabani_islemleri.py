
# --- Gerekli Modüllerin İçeri Aktarılması ---
import sqlite3
from datetime import datetime
import bcrypt
import os # Resim dosyasını silmek için eklendi

# --- Veritabanı Dosya Adı ---
DB_NAME = "market_veritabani.db"

def veritabani_baglan():
    """Veritabanına bir bağlantı oluşturur ve bağlantı nesnesini döndürür."""
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def tablolari_olustur():
    """Gerekli tabloları oluşturur ve varsayılan admin kullanıcısını ekler."""
    with veritabani_baglan() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                sifre BLOB NOT NULL,
                rol TEXT NOT NULL,
                tfa_secret TEXT,
                profil_resmi TEXT
            )
        """)

        cursor.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, urun_adi TEXT UNIQUE NOT NULL, fiyat REAL NOT NULL, stok INTEGER NOT NULL, resim_yolu TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS loglar (id INTEGER PRIMARY KEY AUTOINCREMENT, zaman_damgasi TEXT NOT NULL, kullanici_adi TEXT NOT NULL, islem TEXT NOT NULL, detay TEXT)")
        
        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = 'admin'")
        if cursor.fetchone() is None:
            sifre_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre, rol) VALUES (?, ?, ?)",
                           ('admin', sifre_hash, 'Admin'))
            zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO loglar (zaman_damgasi, kullanici_adi, islem, detay) VALUES (?, ?, ?, ?)",
                           (zaman_damgasi, 'Sistem', 'Kullanıcı Eklendi', "Varsayılan 'admin' kullanıcısı oluşturuldu."))

def sifre_dogrula(kayitli_hash, girilen_sifre):
    """Girilen şifreyi hash'lenmiş haliyle karşılaştırır."""
    if isinstance(kayitli_hash, str):
        kayitli_hash = kayitli_hash.encode('utf-8')
    return bcrypt.checkpw(girilen_sifre.encode('utf-8'), kayitli_hash)

# --- Log İşlemleri ---
def log_ekle(kullanici_adi, islem, detay=""):
    sql = "INSERT INTO loglar (zaman_damgasi, kullanici_adi, islem, detay) VALUES (?, ?, ?, ?)"
    zaman_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with veritabani_baglan() as conn:
            conn.execute(sql, (zaman_damgasi, kullanici_adi, islem, detay))
    except sqlite3.Error as e:
        print(f"Log eklenirken hata oluştu: {e}")

# --- Kullanıcı İşlemleri ---
def kullanici_ekle(kullanici_adi, sifre, rol, tfa_secret=None, profil_resmi=None):
    sql = "INSERT INTO kullanicilar (kullanici_adi, sifre, rol, tfa_secret, profil_resmi) VALUES (?, ?, ?, ?, ?)"
    if isinstance(sifre, str):
        sifre = sifre.encode('utf-8')
    sifre_hash = bcrypt.hashpw(sifre, bcrypt.gensalt())
    try:
        with veritabani_baglan() as conn:
            conn.execute(sql, (kullanici_adi, sifre_hash, rol, tfa_secret, profil_resmi))
        log_ekle(kullanici_adi, "Kullanıcı Kaydı", f"'{kullanici_adi}' adlı yeni kullanıcı oluşturuldu.")
        return True
    except sqlite3.IntegrityError:
        return False
    
def kullanici_dogrula(kullanici_adi, sifre):
    """Verilen şifreyi veritabanındaki bcrypt hash'i ile karşılaştırır."""
    sql = "SELECT * FROM kullanicilar WHERE kullanici_adi = ?"
    with veritabani_baglan() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (kullanici_adi,))
        kullanici = cursor.fetchone()
        if kullanici:
            kayitli_sifre_hash = kullanici['sifre']
            if bcrypt.checkpw(sifre.encode('utf-8'), kayitli_sifre_hash):
                return kullanici # Şifre doğruysa tüm kullanıcı bilgilerini döndür
    return None

def sifre_guncelle(kullanici_adi, yeni_sifre):
    """Kullanıcının şifresini bcrypt ile günceller."""
    sql = "UPDATE kullanicilar SET sifre = ? WHERE kullanici_adi = ?"
    yeni_sifre_hash = bcrypt.hashpw(yeni_sifre.encode('utf-8'), bcrypt.gensalt())
    with veritabani_baglan() as conn:
        conn.execute(sql, (yeni_sifre_hash, kullanici_adi))
    log_ekle(kullanici_adi, "Şifre Değiştirildi", "Kullanıcı şifresini başarıyla güncelledi.")

# --- Diğer Fonksiyonlar 
def kullanici_getir(kullanici_adi):
    sql = "SELECT * FROM kullanicilar WHERE kullanici_adi = ?"
    with veritabani_baglan() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (kullanici_adi,))
        return cursor.fetchone()

def tum_kullanicilari_getir():
    sql = "SELECT id, kullanici_adi, rol FROM kullanicilar"
    with veritabani_baglan() as conn:
        return conn.cursor().execute(sql).fetchall()

def kullanici_sil(kullanici_adi):
    sql = "DELETE FROM kullanicilar WHERE kullanici_adi = ?"
    with veritabani_baglan() as conn:
        conn.execute(sql, (kullanici_adi,))
    log_ekle('Sistem', 'Kullanıcı Silindi', f"'{kullanici_adi}' adlı kullanıcı silindi.")

def tfa_secret_guncelle(kullanici_adi, secret):
    sql = "UPDATE kullanicilar SET tfa_secret = ? WHERE kullanici_adi = ?"
    with veritabani_baglan() as conn:
        conn.execute(sql, (secret, kullanici_adi))
    log_ekle(kullanici_adi, "2FA Ayarlandı", "Kullanıcı iki faktörlü kimlik doğrulamayı etkinleştirdi.")

def profil_resmi_guncelle(kullanici_adi, resim_yolu):
    sql = "UPDATE kullanicilar SET profil_resmi = ? WHERE kullanici_adi = ?"
    with veritabani_baglan() as conn:
        conn.execute(sql, (resim_yolu, kullanici_adi))

def urun_ekle(urun_adi, fiyat, stok, resim_yolu):
    sql = "INSERT INTO urunler (urun_adi, fiyat, stok, resim_yolu) VALUES (?, ?, ?, ?)"
    try:
        with veritabani_baglan() as conn:
            conn.execute(sql, (urun_adi, fiyat, stok, resim_yolu))
        log_ekle('Admin', 'Ürün Eklendi', f"'{urun_adi}' adlı ürün eklendi.")
        return True
    except sqlite3.IntegrityError:
        return False

def tum_urunleri_getir():
    sql = "SELECT * FROM urunler ORDER BY urun_adi"
    with veritabani_baglan() as conn:
        return conn.cursor().execute(sql).fetchall()
def urun_sil(urun_id):
    """Ürünü ve ilişkili resim dosyasını siler."""
    urun = None
    resim_yolu = None
    with veritabani_baglan() as conn:
        cursor = conn.cursor()
        # Önce silinecek ürünün bilgilerini al
        cursor.execute("SELECT urun_adi, resim_yolu FROM urunler WHERE id = ?", (urun_id,))
        urun = cursor.fetchone()
        
        if urun:
            resim_yolu = urun['resim_yolu']
            # Veritabanından ürünü sil
            cursor.execute("DELETE FROM urunler WHERE id = ?", (urun_id,))
            conn.commit() # Değişikliği onayla
            log_ekle('Admin', 'Ürün Silindi', f"'{urun['urun_adi']}' adlı ürün silindi.")

    # Veritabanı işlemi başarılı olduktan sonra dosyayı sil
    if resim_yolu:
        try:
            if os.path.exists(resim_yolu):
                os.remove(resim_yolu)
        except OSError as e:
            print(f"Resim dosyası silinirken hata oluştu: {e}")

def urun_stok_guncelle(urun_id, satin_alinan_miktar):
    sql = "UPDATE urunler SET stok = stok - ? WHERE id = ?"
    with veritabani_baglan() as conn:
        conn.execute(sql, (satin_alinan_miktar, urun_id))

def tum_loglari_getir():
    sql = "SELECT zaman_damgasi, kullanici_adi, islem, detay FROM loglar ORDER BY id DESC"
    with veritabani_baglan() as conn:
        return conn.cursor().execute(sql).fetchall()
    