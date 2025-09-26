
# --- Gerekli Modüllerin İçeri Aktarılması ---
import tkinter as tk  # Grafiksel kullanıcı arayüzü (GUI) oluşturmak için temel kütüphane.
from tkinter import messagebox, font  # Mesaj kutuları ve yazı tipi yönetimi için ek modüller.
import sqlite3  # SQLite veritabanı ile çalışmak için kütüphane.
import random  # Rastgele sayılar ve seçimler yapmak için kütüphane.
import webbrowser  # Web tarayıcısını açmak için kütüphane.
import math  # Matematiksel hesaplamalar (örneğin, daire çizimi için) için kütüphane.

# --- Kelime Veri Setleri ---

# Kapsamlı Türkçe kelime listesi. `set` veri tipi, bir kelimenin listede olup olmadığını çok hızlı kontrol etmeyi sağlar.
# Gerçek bir uygulamada bu liste, bir dosyadan (örn. txt) okunarak programa dahil edilmelidir.
TURKCE_SOZLUK = {
    'arda', 'neşeli', 'proje', 'kelime', 'oyun', 'yazılım', 'geliştirici', 'python', 'tkinter', 'veritabanı',
    'puan', 'ipucu', 'doğru', 'yanlış', 'harf', 'karıştır', 'bulmaca', 'ekran', 'menü', 'giriş', 'çıkış',
    'elma', 'armut', 'masa', 'sandalye', 'kitap', 'defter', 'kalem', 'silgi', 'bilgisayar', 'fare', 'klavye',
    'ev', 'araba', 'yol', 'ağaç', 'çiçek', 'güneş', 'ay', 'yıldız', 'deniz', 'kum', 'dalga', 'balık',
    'kedi', 'köpek', 'kuş', 'at', 'eşek', 'inek', 'koyun', 'tavuk', 'horoz', 'ördek', 'kaz', 'aslan',
    'kaplan', 'fil', 'zürafa', 'maymun', 'yılan', 'timsah', 'kartal', 'şahin', 'leylek', 'serçe',
    'su', 'hava', 'toprak', 'ateş', 'taş', 'demir', 'altın', 'gümüş', 'bakır', 'cam', 'plastik',
    'renk', 'kırmızı', 'mavi', 'yeşil', 'sarı', 'siyah', 'beyaz', 'pembe', 'mor', 'turuncu', 'gri',
    'sayı', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz', 'on', 'yüz', 'bin',
    'gel', 'git', 'yap', 'et', 'al', 'ver', 'bak', 'gör', 'oku', 'yaz', 'çiz', 'koş', 'yürü', 'uyu',
    'uyan', 'ye', 'iç', 'sev', 'gül', 'ağla', 'düşün', 'konuş', 'dinle', 'sor', 'cevapla', 'anla',
    'bil', 'öğren', 'öğret', 'çalış', 'dinlen', 'oyna', 'kazan', 'kaybet', 'başla', 'bitir', 'aç',
    'kapat', 'sevgi', 'saygı', 'dostluk', 'aile', 'anne', 'baba', 'kardeş', 'çocuk', 'bebek', 'arkadaş',
    'okul', 'sınıf', 'öğretmen', 'öğrenci', 'ders', 'sınav', 'karne', 'tatil', 'yaz', 'kış', 'bahar',
    'güz', 'mevsim', 'ay', 'yıl', 'hafta', 'gün', 'saat', 'dakika', 'saniye', 'zaman', 'geçmiş',
    'gelecek', 'şimdi', 'bugün', 'yarın', 'dün', 'sabah', 'öğle', 'akşam', 'gece', 'erken', 'geç',
    'kal', 'er', 'el', 'al', 'an', 'at', 'ay', 'az', 'en', 'et', 'ev', 'iş', 'iç', 'il', 'in', 'ip',
    'iz', 'la', 'le', 'ne', 'o', 'on', 'se', 'su', 'şu', 'ta', 'te', 'ti', 'tu', 'ya', 'ye', 'yol',
    'ak', 'al', 'an', 'ar', 'as', 'at', 'ay', 'az', 'ba', 'be', 'bi', 'bu', 'ca', 'ce', 'cı', 'ci',
    'ça', 'çe', 'çı', 'çi', 'da', 'de', 'do', 'du', 'dö', 'dü', 'ed', 'ek', 'el', 'em', 'en', 'er',
    'es', 'eş', 'et', 'ev', 'ey', 'fa', 'fe', 'fi', 'ga', 'ge', 'go', 'gö', 'gü', 'ha', 'he', 'hi',
    'ho', 'hu', 'hı', 'hi', 'ır', 'ıs', 'iş', 'it', 'iz', 'je', 'ji', 'jo', 'ju', 'ka', 'ke', 'kı',
    'ki', 'ko', 'kö', 'ku', 'la', 'le', 'li', 'lo', 'lu', 'lö', 'lü', 'ma', 'me', 'mı', 'mi', 'mo',
    'mu', 'mö', 'mü', 'na', 'ne', 'ni', 'no', 'nu', 'nü', 'of', 'oh', 'ok', 'ol', 'om', 'on', 'oy',
    'öd', 'öl', 'ön', 'ör', 'ös', 'öt', 'öz', 'pa', 'pe', 'pi', 'po', 'ra', 're', 'ri', 'ro', 'ru',
    'sa', 'se', 'sı', 'si', 'so', 'su', 'sö', 'sü', 'şa', 'şe', 'şı', 'şi', 'şu', 'ta', 'te', 'tı',
    'ti', 'to', 'tu', 'tö', 'tü', 'uf', 'uh', 'uk', 'ul', 'um', 'un', 'ur', 'us', 'ut', 'uy', 'uz',
    'üç', 'ün', 'ür', 'üs', 'üt', 'üz', 'va', 've', 'vi', 'ya', 'ye', 'yı', 'yi', 'yo', 'yu', 'za',
    'ze', 'zı', 'zi', 'aşk', 'can', 'ten', 'yün', 'tüy', 'tane', 'kale', 'kare', 'pena', 'rota', 'etap',
    'tava', 'soba', 'kral', 'krem', 'tren', 'spor', 'plan', 'ara', 'aka', 'ala', 'ana', 'asa', 'ata',
    'aya', 'ela', 'yat', 'tay', 'ray', 'çay', 'say', 'köy'
}

# Oyunda kullanılacak ana kelimeler listesi.
BULMACA_KELIMELERI = [
    "KARDEŞLİK", "KÜTÜPHANE", "BİLGİSAYAR", "ÖĞRETMENLİK",
    "TELEVİZYON", "TÜRKİYE", "İSTANBUL", "ANKARA", "CUMHURİYET",
    "DEMOKRASİ", "GELİŞTİRİCİ", "PROGRAMCI"
]

# --- Ana Oyun Sınıfı ---
class KelimeOyunu:
    # Kurucu metot (constructor): Program başladığında ilk çalışan fonksiyondur.
    def __init__(self, pencere):
        self.pencere = pencere  # Ana pencere nesnesini saklar.
        self.pencere.title("Kelime Bulmaca Oyunu")  # Pencerenin başlığını ayarlar.
        self.pencere.geometry("800x600")  # Pencerenin boyutlarını ayarlar (genişlik x yükseklik).
        self.pencere.configure(bg="#2E7D32")  # Pencerenin arka plan rengini (yeşil çerçeve) ayarlar.
        self.pencere.resizable(False, False)  # Pencerenin yeniden boyutlandırılmasını engeller.

        # Veritabanı bağlantısını başlatır. Eğer dosya yoksa, oluşturur.
        self.vt_baglantisi = sqlite3.connect("kelime_oyunu.db")
        self.tablo_olustur()  # Veritabanında kullanıcılar tablosunu oluşturur veya kontrol eder.

        # Arayüzde kullanılacak yazı tiplerini tanımlar.
        self.varsayilan_yazi_tipi = font.Font(family="Arial", size=12)
        self.kalin_yazi_tipi = font.Font(family="Arial", size=12, weight="bold")
        self.baslik_yazi_tipi = font.Font(family="Arial", size=16, weight="bold")
        self.tuval_yazi_tipi = font.Font(family="Arial", size=16, weight="bold")

        # Oyun durumuyla ilgili değişkenleri sıfırlar.
        self.aktif_kullanici = None  # O anki oyuncunun adını tutar.
        self.puan = 0  # Oyuncunun puanını tutar.
        self.ana_kelime = ""  # Bulmacanın ana kelimesini tutar.
        self.karisik_harfler = []  # Ana kelimenin karıştırılmış harflerini tutar.
        self.olasi_kelimeler = set()  # Ana kelimeden türetilebilecek tüm kelimeleri tutar.
        self.bulunan_kelimeler = set()  # Kullanıcının bulduğu kelimeleri tutar.

        # Arayüz elemanlarını tutacak olan ana çerçeveyi oluşturur.
        self.ana_cerceve = tk.Frame(pencere, bg="#2E7D32")
        self.ana_cerceve.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Çerçeveyi pencereye yerleştirir.

        self.giris_ekranini_goster()  # Program başladığında giriş ekranını gösterir.

    # Veritabanında 'users' tablosunu oluşturan fonksiyon.
    def tablo_olustur(self):
        """Kullanıcılar tablosunu (eğer yoksa) oluşturur."""
        imlec = self.vt_baglantisi.cursor()  # Veritabanında işlem yapmak için bir imleç oluşturur.
        imlec.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                score INTEGER NOT NULL DEFAULT 0
            )
        """)  # SQL komutu ile tabloyu oluşturur.
        self.vt_baglantisi.commit()  # Yapılan değişiklikleri veritabanına kaydeder.

    # Kullanıcıyı veritabanından getiren veya yeni kullanıcı oluşturan fonksiyon.
    def kullaniciyi_al(self, kullanici_adi):
        """Kullanıcıyı veritabanından alır veya yeni bir kullanıcı oluşturur."""
        imlec = self.vt_baglantisi.cursor()
        imlec.execute("SELECT score FROM users WHERE username = ?", (kullanici_adi,)) # Kullanıcı adına göre arama yapar.
        kullanici = imlec.fetchone()  # Arama sonucunu alır.
        if kullanici:  # Eğer kullanıcı varsa
            self.puan = kullanici[0]  # Kayıtlı puanını değişkene atar.
        else:  # Eğer kullanıcı yoksa
            imlec.execute("INSERT INTO users (username, score) VALUES (?, 0)", (kullanici_adi,)) # Yeni kullanıcıyı 0 puanla ekler.
            self.vt_baglantisi.commit()  # Değişikliği kaydeder.
            self.puan = 0  # Puanı sıfırlar.
        self.aktif_kullanici = kullanici_adi  # Aktif kullanıcıyı ayarlar.

    # Kullanıcının puanını veritabanında güncelleyen fonksiyon.
    def puani_veritabaninda_guncelle(self):
        """Kullanıcının skorunu veritabanında günceller."""
        if self.aktif_kullanici:  # Eğer bir kullanıcı giriş yapmışsa
            imlec = self.vt_baglantisi.cursor()
            imlec.execute("UPDATE users SET score = ? WHERE username = ?", (self.puan, self.aktif_kullanici)) # Puanı günceller.
            self.vt_baglantisi.commit()  # Değişikliği kaydeder.

    # Ana çerçeve içindeki tüm arayüz elemanlarını (widget) temizleyen fonksiyon.
    def cerceveyi_temizle(self):
        """Ana çerçeveyi temizler, böylece yeni ekran yüklenebilir."""
        for widget in self.ana_cerceve.winfo_children():
            widget.destroy()  # Çerçevedeki her bir widget'ı siler.

    # Kullanıcı giriş ekranını gösteren fonksiyon.
    def giris_ekranini_goster(self):
        """Giriş ekranını oluşturur ve gösterir."""
        self.cerceveyi_temizle()  # Önceki ekranı temizler.
        self.puani_veritabaninda_guncelle()  # Oyundan çıkan önceki kullanıcının puanını kaydeder.
        self.aktif_kullanici = None  # Aktif kullanıcıyı sıfırlar.

        # Giriş elemanlarını gruplayan bir çerçeve oluşturur.
        giris_cercevesi = tk.Frame(self.ana_cerceve, bg="#E8F5E9", padx=20, pady=20)
        giris_cercevesi.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Çerçeveyi ekranın ortasına yerleştirir.

        # "Kullanıcı Adı" etiketini oluşturur.
        tk.Label(giris_cercevesi, text="Kullanıcı Adı", font=self.baslik_yazi_tipi, bg="#E8F5E9").pack(pady=10)
        
        # Kullanıcı adının girileceği metin kutusunu oluşturur.
        self.kullanici_adi_girisi = tk.Entry(giris_cercevesi, font=self.varsayilan_yazi_tipi, width=30)
        self.kullanici_adi_girisi.pack(pady=5)
        self.kullanici_adi_girisi.focus_set() # İmleci otomatik olarak bu kutuya odaklar.

        # "Oyuna Başla" butonunu oluşturur.
        tk.Button(giris_cercevesi, text="Oyuna Başla", font=self.kalin_yazi_tipi, bg="#4CAF50", fg="white", command=self.oyunu_baslat).pack(pady=20, ipadx=10, ipady=5)

    # Oyunu başlatan fonksiyon.
    def oyunu_baslat(self):
        """Kullanıcı adını alarak oyunu başlatır."""
        kullanici_adi = self.kullanici_adi_girisi.get().strip()  # Giriş kutusundaki metni alır ve boşlukları temizler.
        if not kullanici_adi:  # Eğer kullanıcı adı boşsa
            messagebox.showerror("Hata", "Kullanıcı adı boş olamaz!")  # Hata mesajı gösterir.
            return  # Fonksiyonu sonlandırır.
        
        self.kullaniciyi_al(kullanici_adi)  # Kullanıcıyı veritabanından alır veya oluşturur.
        self.oyun_ekranini_goster()  # Oyun ekranına geçer.
        self.yeni_bulmaca()  # Yeni bir bulmaca yükler.

    # Ana oyun ekranını oluşturan fonksiyon.
    def oyun_ekranini_goster(self):
        """Ana oyun arayüzünü oluşturur."""
        self.cerceveyi_temizle()  # Giriş ekranını temizler.
        
        # Üst bilgi çubuğunu (Bilgi menüsü, Hoş geldiniz yazısı, Puan) tutan çerçeve.
        ust_cerceve = tk.Frame(self.ana_cerceve, bg="#2E7D32")
        ust_cerceve.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # "Bilgi" menü butonu.
        self.bilgi_butonu = tk.Menubutton(ust_cerceve, text="Bilgi", font=self.kalin_yazi_tipi, relief=tk.RAISED, bg="#AED581", fg="#1B5E20")
        self.bilgi_butonu.pack(side=tk.LEFT, padx=5)
        bilgi_menusu = tk.Menu(self.bilgi_butonu, tearoff=0) # Menüyü oluşturur.
        self.bilgi_butonu["menu"] = bilgi_menusu # Menüyü butona bağlar.
        bilgi_menusu.add_command(label="Hakkında", command=self.hakkindayi_goster) # Menüye "Hakkında" seçeneğini ekler.

        # "Hoş geldiniz" mesajı etiketi.
        self.hosgeldin_etiketi = tk.Label(ust_cerceve, text=f"Hoş geldiniz, {self.aktif_kullanici}", font=self.baslik_yazi_tipi, bg="#2E7D32", fg="white")
        self.hosgeldin_etiketi.pack(side=tk.LEFT, expand=True)
        
        # Puan göstergesi etiketi.
        self.puan_etiketi = tk.Label(ust_cerceve, text=f"Puan: {self.puan}", font=self.baslik_yazi_tipi, bg="#2E7D32", fg="white")
        self.puan_etiketi.pack(side=tk.RIGHT, padx=10)

        # Orta bölümü (harf tuvali ve kelime kutuları) tutan çerçeve.
        orta_cerceve = tk.Frame(self.ana_cerceve, bg="#E8F5E9")
        orta_cerceve.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Karışık harflerin gösterileceği dairesel alan (Canvas).
        self.harf_tuvali = tk.Canvas(orta_cerceve, width=300, height=300, bg="#E8F5E9", highlightthickness=0)
        self.harf_tuvali.pack(pady=10)

        # Bulunacak kelimelerin kutularını içeren çerçeve.
        self.kelimeler_cercevesi = tk.Frame(orta_cerceve, bg="#E8F5E9")
        self.kelimeler_cercevesi.pack(pady=10, fill=tk.X, padx=20)
        self.kelime_etiketleri = {} # Kelime etiketlerini saklamak için bir sözlük (dictionary).

        # Alt bölümü (giriş kutusu ve kontrol butonları) tutan çerçeve.
        alt_cerceve = tk.Frame(self.ana_cerceve, bg="#C8E6C9", pady=10)
        alt_cerceve.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Durum ve uyarı mesajlarının gösterileceği etiket.
        self.durum_etiketi = tk.Label(alt_cerceve, text="Oyuna hoş geldiniz!", font=self.varsayilan_yazi_tipi, bg="#C8E6C9")
        self.durum_etiketi.pack(fill=tk.X)
        
        # Kelime giriş alanını gruplayan çerçeve.
        kelime_giris_cercevesi = tk.Frame(alt_cerceve, bg="#C8E6C9")
        kelime_giris_cercevesi.pack(pady=10)
        tk.Label(kelime_giris_cercevesi, text="Kelime:", font=self.kalin_yazi_tipi, bg="#C8E6C9").pack(side=tk.LEFT)
        self.kelime_girisi = tk.Entry(kelime_giris_cercevesi, font=self.varsayilan_yazi_tipi, width=30)
        self.kelime_girisi.pack(side=tk.LEFT, padx=5)
        self.kelime_girisi.bind("<Return>", self.kelimeyi_kontrol_et) # Enter tuşuna basıldığında kelimeyi kontrol eder.
        self.kelime_girisi.focus_set() # İmleci odaklar.

        # Kontrol butonlarını gruplayan çerçeve.
        buton_cercevesi = tk.Frame(alt_cerceve, bg="#C8E6C9")
        buton_cercevesi.pack(pady=5)
        
        tk.Button(buton_cercevesi, text="Yazılanları Temizle", command=self.girisi_temizle, bg="#FFC107").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cercevesi, text="Harfleri Karıştır", command=self.karistir_ve_ciz, bg="#03A9F4").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cercevesi, text="İpucu Al (-5 Puan)", command=self.ipucu_al, bg="#FF9800").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cercevesi, text="Ana Menüye Dön", command=self.giris_ekranini_goster, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cercevesi, text="Güvenli Çıkış Yap", command=self.guvenli_cikis, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
    
    # "Hakkında" penceresini gösteren fonksiyon.
    def hakkindayi_goster(self):
        """Oyun ve geliştirici hakkında bilgi veren bir pencere gösterir."""
        hakkinda_metni = """
        Bu oyun bir kelime oyunudur.
        Yukarıda rastgele çıkan kelimelerden içindeki kelimeleri bulup yazıyoruz.
        Eğer doğruysa puan kazanıyoruz.
        Eğer yanlışsa başka kelime deniyoruz.
        İpucu alabilirsiniz ama ipucu -5 puan demektir.

        Yapan: Arda NEŞELİ
        """
        hakkinda_penceresi = tk.Toplevel(self.pencere) # Ana pencerenin üzerinde yeni bir pencere oluşturur.
        hakkinda_penceresi.title("Hakkında")
        hakkinda_penceresi.geometry("540x210")
        hakkinda_penceresi.configure(bg="#E8F5E9")
        hakkinda_penceresi.resizable(False, False)

        tk.Label(hakkinda_penceresi, text=hakkinda_metni, justify=tk.LEFT, font=self.varsayilan_yazi_tipi, bg="#E8F5E9").pack(pady=10, padx=10)
        
        # Tıklanabilir GitHub linki etiketi.
        baglanti_etiketi = tk.Label(hakkinda_penceresi, text="GitHub Linki", fg="blue", cursor="hand2", font=self.kalin_yazi_tipi, bg="#E8F5E9")
        baglanti_etiketi.pack()
        baglanti_etiketi.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/NeseliArda1/PROJELER"))
        
        hakkinda_penceresi.transient(self.pencere)  # Pencereyi ana pencereye bağlı kılar.
        hakkinda_penceresi.grab_set()  # Odağı bu pencereye kilitler.
        self.pencere.wait_window(hakkinda_penceresi) # Bu pencere kapanana kadar ana programı bekletir.

    # Verilen bir kelimenin harflerinden türetilebilecek tüm alt kelimeleri bulan fonksiyon.
    def alt_kelimeleri_bul(self, kelime):
        """Ana kelimeden türetilebilecek geçerli Türkçe alt kelimeleri bulur."""
        alt_kelimeler = set()
        kelime = kelime.lower() # Karşılaştırma için kelimeyi küçük harfe çevirir.
        n = len(kelime)
        from itertools import permutations # Permütasyon (farklı sıralama) için fonksiyonu ithal eder.
        for i in range(3, n + 1): # En az 3 harfli kelimelerden başlayarak kelime uzunluğuna kadar döner.
            for p in permutations(kelime, i): # Ana kelimenin harflerinin i'li permütasyonlarını alır.
                alt_kelime = "".join(p) # Harf demetini birleştirerek kelimeye dönüştürür.
                if alt_kelime in TURKCE_SOZLUK: # Eğer oluşturulan kelime sözlükte varsa
                    alt_kelimeler.add(alt_kelime) # Kümeye ekler.
        return sorted(list(alt_kelimeler), key=len) # Bulunan kelimeleri uzunluklarına göre sıralar.

    # Yeni bir bulmaca (yeni kelime) başlatan fonksiyon.
    def yeni_bulmaca(self):
        """Yeni bir bulmaca başlatır."""
        self.ana_kelime = random.choice(BULMACA_KELIMELERI)  # Listeden rastgele bir ana kelime seçer.
        self.karisik_harfler = list(self.ana_kelime)  # Kelimeyi harf listesine çevirir.
        self.olasi_kelimeler = set(self.alt_kelimeleri_bul(self.ana_kelime)) # Ana kelimeden türeyen kelimeleri bulur.
        self.bulunan_kelimeler = set() # Bulunan kelimeler listesini sıfırlar.
        
        self.karistir_ve_ciz()  # Harfleri karıştırıp tuvale çizer.
        self.kelime_kutularini_guncelle()  # Kelime kutularını oluşturur.
        self.durumu_guncelle("Yeni bulmaca! İyi şanslar.", "green") # Durum mesajını günceller.
        self.kelime_girisi.focus_set() # İmleci kelime giriş kutusuna odaklar.

    # Harfleri karıştırıp tuvale çizen ana fonksiyon.
    def karistir_ve_ciz(self):
        """Harfleri karıştırır ve tuval üzerine yeniden çizer."""
        random.shuffle(self.karisik_harfler)  # Harf listesini yerinde karıştırır.
        self.harfleri_daire_icine_ciz()  # Karışık harfleri tuvale çizer.

    # Harfleri dairesel bir yörüngede tuval üzerine çizen fonksiyon.
    def harfleri_daire_icine_ciz(self):
        """Harfleri dairesel bir şekilde canvas (tuval) üzerine çizer."""
        self.harf_tuvali.delete("all")  # Tuvaldeki eski çizimleri temizler.
        merkez_x, merkez_y = 150, 150  # Dairenin merkez koordinatları.
        yaricap = 100  # Dairenin yarıçapı.
        aci_adimi = 360 / len(self.karisik_harfler)  # Harfler arasındaki açı farkı.
        
        for i, harf in enumerate(self.karisik_harfler): # Her bir harf için döner.
            aci = math.radians(i * aci_adimi)  # Harfin açısını radyana çevirir.
            x = merkez_x + yaricap * math.cos(aci)  # Harfin x koordinatını hesaplar.
            y = merkez_y + yaricap * math.sin(aci)  # Harfin y koordinatını hesaplar.
            self.harf_tuvali.create_text(x, y, text=harf, font=self.tuval_yazi_tipi, fill="black") # Harfi tuvale çizer.

    # Bulunacak kelimeler için alt kısımdaki kutucukları (etiketleri) oluşturan/güncelleyen fonksiyon.
    def kelime_kutularini_guncelle(self):
        """Bulunacak kelimeler için kutucukları oluşturur veya günceller."""
        for widget in self.kelimeler_cercevesi.winfo_children(): # Kelime çerçevesindeki eski etiketleri temizler.
            widget.destroy()
        
        self.kelime_etiketleri.clear() # Kelime etiketleri sözlüğünü boşaltır.
        
        max_sutun = 6  # Bir satırda gösterilecek maksimum kelime kutusu sayısı.
        satir = 0
        sutun = 0

        for kelime in sorted(list(self.olasi_kelimeler), key=len): # Kelimeleri uzunluklarına göre sıralayarak döner.
            if sutun >= max_sutun: # Eğer satır dolduysa
                sutun = 0 # Sütunu sıfırla
                satir += 1 # Yeni satıra geç
            
            kutu_metni = " ".join(["_" for _ in kelime]) # Kelimenin uzunluğu kadar alt çizgi oluşturur.
            etiket = tk.Label(self.kelimeler_cercevesi, text=kutu_metni, font=self.kalin_yazi_tipi, bg="#BDBDBD", fg="black", padx=5, pady=2, relief=tk.RIDGE)
            etiket.grid(row=satir, column=sutun, padx=5, pady=5, sticky="ew") # Etiketi grid layout ile yerleştirir.
            self.kelime_etiketleri[kelime] = etiket # Etiketi, kelime anahtarıyla sözlüğe kaydeder.
            sutun += 1
        
        for i in range(max_sutun): # Sütunların eşit genişlikte olmasını sağlar.
             self.kelimeler_cercevesi.grid_columnconfigure(i, weight=1)

    # Kullanıcının girdiği kelimeyi kontrol eden fonksiyon.
    def kelimeyi_kontrol_et(self, event=None):
        """Kullanıcının girdiği kelimeyi kontrol eder, puan verir ve durumu günceller."""
        kullanici_kelimesi = self.kelime_girisi.get().lower().strip() # Girilen kelimeyi alır, küçük harfe çevirir.
        self.girisi_temizle() # Giriş kutusunu temizler.

        if not kullanici_kelimesi: # Eğer giriş boşsa
            return # Hiçbir şey yapma.

        if kullanici_kelimesi in self.bulunan_kelimeler: # Eğer kelime daha önce bulunduysa
            self.durumu_guncelle(f"'{kullanici_kelimesi.upper()}' kelimesini zaten buldunuz.", "orange")
        elif kullanici_kelimesi in self.olasi_kelimeler: # Eğer kelime doğru ve bulunmamışsa
            self.puan += len(kullanici_kelimesi) # Kelimenin harf sayısı kadar puan ekler.
            self.bulunan_kelimeler.add(kullanici_kelimesi) # Kelimeyi bulunanlar listesine ekler.
            self.puan_etiketini_guncelle() # Puan etiketini günceller.
            self.durumu_guncelle(f"Doğru! +{len(kullanici_kelimesi)} puan kazandınız.", "green") # Başarı mesajı gösterir.
            
            # İlgili kelime kutusunun rengini ve metnini günceller.
            etiket = self.kelime_etiketleri.get(kullanici_kelimesi)
            if etiket:
                etiket.config(text=kullanici_kelimesi.upper(), bg="#66BB6A", fg="white")

            # Tüm kelimeler bulunmuş mu diye kontrol eder.
            if len(self.bulunan_kelimeler) == len(self.olasi_kelimeler):
                messagebox.showinfo("Tebrikler!", "Tüm kelimeleri buldunuz! Yeni bulmacaya geçiliyor.")
                self.yeni_bulmaca() # Yeni bulmaca başlatır.
        else: # Eğer kelime yanlışsa
            self.durumu_guncelle("Geçersiz veya yanlış kelime. Tekrar deneyin.", "red") # Hata mesajı gösterir.

    # Kullanıcıya ipucu veren fonksiyon.
    def ipucu_al(self):
        """Kullanıcıya henüz bulunmamış bir kelimeyi ipucu olarak verir ve puan düşürür."""
        if self.puan < 5: # Yeterli puan yoksa
            self.durumu_guncelle("İpucu için yeterli puanınız yok (En az 5 puan).", "red")
            return

        bulunmayan_kelimeler = self.olasi_kelimeler - self.bulunan_kelimeler # Henüz bulunmamış kelimeleri bulur.
        if not bulunmayan_kelimeler: # Eğer bulunacak kelime kalmadıysa
            self.durumu_guncelle("Tüm kelimeler zaten bulundu!", "blue")
            return

        ipucu_kelimesi = random.choice(list(bulunmayan_kelimeler)) # Rastgele bir ipucu kelimesi seçer.
        
        self.puan -= 5 # İpucu bedeli olarak 5 puan düşer.
        self.bulunan_kelimeler.add(ipucu_kelimesi) # İpucu kelimesini bulunanlara ekler.
        self.puan_etiketini_guncelle() # Puan etiketini günceller.
        self.durumu_guncelle(f"İpucu: '{ipucu_kelimesi.upper()}'. -5 puan.", "blue") # İpucu mesajı gösterir.
        
        # İpucu kelimesinin kutusunu günceller.
        etiket = self.kelime_etiketleri.get(ipucu_kelimesi)
        if etiket:
            etiket.config(text=ipucu_kelimesi.upper(), bg="#29B6F6", fg="white")
        
        # İpucundan sonra tüm kelimeler bulunduysa yeni bulmacaya geçer.
        if len(self.bulunan_kelimeler) == len(self.olasi_kelimeler):
                messagebox.showinfo("Tebrikler!", "Tüm kelimeleri buldunuz! Yeni bulmacaya geçiliyor.")
                self.yeni_bulmaca()

    # Puan etiketini güncelleyen fonksiyon.
    def puan_etiketini_guncelle(self):
        """Arayüzdeki puan etiketinin metnini günceller."""
        self.puan_etiketi.config(text=f"Puan: {self.puan}")
    
    # Durum/uyarı etiketini güncelleyen fonksiyon.
    def durumu_guncelle(self, mesaj, renk):
        """Arayüzdeki durum etiketinin metnini ve rengini günceller."""
        self.durum_etiketi.config(text=mesaj, fg=renk)

    # Kelime giriş kutusunu temizleyen fonksiyon.
    def girisi_temizle(self):
        """Kelime giriş kutusunun içeriğini siler."""
        self.kelime_girisi.delete(0, tk.END)

    # Oyundan güvenli bir şekilde çıkan fonksiyon.
    def guvenli_cikis(self):
        """Mevcut puanı veritabanına kaydederek uygulamayı kapatır."""
        self.puani_veritabaninda_guncelle() # Son puanı kaydeder.
        self.vt_baglantisi.close() # Veritabanı bağlantısını kapatır.
        self.pencere.destroy() # Tkinter penceresini kapatır.

# --- Programın Başlatılması ---
# Bu kontrol, betiğin doğrudan mı çalıştırıldığını yoksa başka bir betik tarafından mı
# içeri aktarıldığını anlamak için kullanılır. Doğrudan çalıştırıldığında oyun başlar.
if __name__ == "__main__":
    pencere = tk.Tk()  # Ana Tkinter penceresini oluşturur.
    uygulama = KelimeOyunu(pencere)  # KelimeOyunu sınıfından bir nesne oluşturarak uygulamayı başlatır.
    # Pencerenin kapatma (X) butonuna basıldığında 'guvenli_cikis' fonksiyonunun çağrılmasını sağlar.
    pencere.protocol("WM_DELETE_WINDOW", uygulama.guvenli_cikis) 
    pencere.mainloop()  # Tkinter olay döngüsünü başlatır, bu da pencerenin ekranda kalmasını sağlar.
