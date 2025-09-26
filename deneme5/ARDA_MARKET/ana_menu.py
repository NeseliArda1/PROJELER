# --- Gerekli Modüllerin İçeri Aktarılması ---
import tkinter as tk  # Grafiksel kullanıcı arayüzü (GUI) için standart Python kütüphanesi.
from tkinter import messagebox, font  # Mesaj kutuları ve yazı tipi yönetimi için.
import webbrowser  # Web tarayıcısını açmak için.
import os  # İşletim sistemiyle ilgili işlemler için (dosya yolları vb.).

# --- Diğer Proje Modüllerinin İçeri Aktarılması ---
import veritabani_islemleri as vt  # Veritabanı işlemleri için oluşturduğumuz modül.
import kullanici_islemleri as ki # Kullanıcı arayüzleri ve işlemleri için oluşturduğumuz modül.

# --- Ana Menü Sınıfı ---
class AnaMenu:
    """
    Uygulamanın ana başlangıç penceresini oluşturan ve yöneten sınıf.
    Hoş geldiniz ekranı, menüler ve ana giriş seçenekleri burada yer alır.
    """
    def __init__(self, ana_pencere):
        """
        Sınıfın kurucu metodu. Ana pencereyi ayarlar ve arayüzü oluşturur.
        :param ana_pencere: tk.Tk() tarafından oluşturulan ana pencere nesnesi.
        """
        self.ana_pencere = ana_pencere
        
        # --- Pencere Ayarları ---
        self.ana_pencere.title("Arda Market Yönetim Sistemi")  # Pencere başlığı.
        self.ana_pencere.geometry("900x600")  # Pencere boyutu.
        self.ana_pencere.configure(bg="#f0f0f0")  # Arka plan rengi.

        # --- Gerekli Klasörlerin Oluşturulması ---
        # Uygulamanın çalışması için gerekli olan klasörleri kontrol eder ve yoksa oluşturur.
        if not os.path.exists('images'):
            os.makedirs('images') # Ürün resimleri için.
        if not os.path.exists('qr_codes'):
            os.makedirs('qr_codes') # 2FA QR kodları için.
        if not os.path.exists('profile_pics'):
            os.makedirs('profile_pics') # Kullanıcı profil resimleri için.

        # Veritabanı ve tabloları başlat.
        vt.tablolari_olustur()

        # --- Stil ve Yazı Tipleri ---
        self.baslik_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.menu_font = font.Font(family="Arial", size=12, weight="bold")
        self.buton_font = font.Font(family="Arial", size=14)

        # --- Arayüzü Oluştur ---
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        """
        Ana menünün görsel bileşenlerini (widget'lar) oluşturur ve yerleştirir.
        """
        # --- Ana Çerçeve (Yeşil Kenarlıklı) ---
        # Tüm diğer widget'ları içinde barındıran ana çerçeve.
        ana_cerceve = tk.Frame(self.ana_pencere, bg="#E8F5E9",  # Açık yeşil arka plan.
                               highlightbackground="#2E7D32",  # Koyu yeşil çerçeve rengi.
                               highlightthickness=5)  # Çerçeve kalınlığı.
        ana_cerceve.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Üst Menü Çerçevesi ---
        ust_menu_cercevesi = tk.Frame(ana_cerceve, bg="#E8F5E9")
        ust_menu_cercevesi.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # --- Üst Menü Butonları ---
        hakkimizda_buton = tk.Button(ust_menu_cercevesi, text="Hakkımızda", font=self.menu_font, command=self.hakkimizda_goster, bg="#4CAF50", fg="white")
        hakkimizda_buton.pack(side=tk.LEFT, padx=5)

        bilgilendirme_buton = tk.Button(ust_menu_cercevesi, text="Bilgilendirme", font=self.menu_font, command=self.bilgilendirme_goster, bg="#4CAF50", fg="white")
        bilgilendirme_buton.pack(side=tk.LEFT, padx=5)

        yapan_buton = tk.Button(ust_menu_cercevesi, text="Yapan", font=self.menu_font, command=self.yapan_goster, bg="#4CAF50", fg="white")
        yapan_buton.pack(side=tk.LEFT, padx=5)

        # --- Orta Kısım (Başlık ve Butonlar) ---
        orta_cerceve = tk.Frame(ana_cerceve, bg="#E8F5E9")
        orta_cerceve.pack(expand=True)

        # --- Hoş Geldiniz Başlığı ---
        hosgeldiniz_etiketi = tk.Label(orta_cerceve, text="ARDA MARKETE HOŞ GELDİNİZ", font=self.baslik_font, bg="#E8F5E9", fg="#1B5E20")
        hosgeldiniz_etiketi.pack(pady=(50, 20))

        # --- Ana İşlem Butonları ---
        giris_butonu = tk.Button(orta_cerceve, text="Giriş Yap", font=self.buton_font, command=self.giris_yap_penceresi, width=20, height=2, bg="#FFC107")
        giris_butonu.pack(pady=10)

        kayit_butonu = tk.Button(orta_cerceve, text="Kullanıcı Ol (Misafir)", font=self.buton_font, command=self.kayit_ol_penceresi, width=20, height=2, bg="#03A9F4")
        kayit_butonu.pack(pady=10)

        cikis_butonu = tk.Button(orta_cerceve, text="Güvenli Çıkış", font=self.buton_font, command=self.guvenli_cikis, width=20, height=2, bg="#f44336", fg="white")
        cikis_butonu.pack(pady=10)

    # --- Menü Fonksiyonları ---
    def hakkimizda_goster(self):
        """'Hakkımızda' menü seçeneğine tıklandığında bilgi mesajı gösterir."""
        messagebox.showinfo(
            "Hakkımızda",
            "ARDA MARKETE hoş geldiniz!\n\n"
            "2025 yılında market olarak açılan bir kurumuz. "
            "Güçlü vizyonumuzla emin adımlarla büyüyen bir şirket olacağız."
        )

    def bilgilendirme_goster(self):
        """'Bilgilendirme' menü seçeneğine tıklandığında bilgi mesajı gösterir."""
        messagebox.showinfo(
            "Bilgilendirme",
            "Bu proje, dijital çağda market alışverişlerini evimizden "
            "güvenli ve pratik bir şekilde yapılmasını sağlayan "
            "kullanıcı dostu basit bir uygulamadır."
        )

    def yapan_goster(self):
        """'Yapan' menü seçeneğine tıklandığında geliştirici bilgilerini gösterir."""
        # Yeni bir Toplevel pencere oluşturulur.
        yapan_penceresi = tk.Toplevel(self.ana_pencere)
        yapan_penceresi.title("Yapan")
        yapan_penceresi.geometry("400x200")
        yapan_penceresi.configure(bg="#f0f0f0")
        
        tk.Label(yapan_penceresi, text="Numarası: 202307105038", font=("Arial", 12)).pack(pady=5)
        tk.Label(yapan_penceresi, text="Adı Soyadı: Arda NEŞELİ", font=("Arial", 12)).pack(pady=5)
        
        # Tıklanabilir link oluşturma
        github_link = "https://github.com/NeseliArda1/PROJELER"
        link_etiketi = tk.Label(yapan_penceresi, text="GitHub Profili", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
        link_etiketi.pack(pady=10)
        link_etiketi.bind("<Button-1>", lambda e: webbrowser.open_new(github_link))

        yapan_penceresi.transient(self.ana_pencere)  # Ana pencerenin üzerinde kalmasını sağlar.
        yapan_penceresi.grab_set()  # Odağı bu pencereye kilitler.
        self.ana_pencere.wait_window(yapan_penceresi) # Bu pencere kapanana kadar bekler.

    # --- Pencere Yönlendirme Fonksiyonları ---
    def giris_yap_penceresi(self):
        """Giriş yapma penceresini açar."""
        # Ana pencere gizlenmez ve giriş penceresi oluşturulur.
        ki.GirisPenceresi(self.ana_pencere)

    def kayit_ol_penceresi(self):
        """Yeni kullanıcı (misafir) kayıt penceresini açar."""
        # Sadece misafir rolüyle kayıt olunabilir.
        # Ana pencere gizlenmez ve kayıt penceresi oluşturulur.
        ki.KayitPenceresi(self.ana_pencere, 'Misafir')

    def guvenli_cikis(self):
        """Uygulamadan güvenli bir şekilde çıkış yapılmasını sağlar."""
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
            self.ana_pencere.destroy()


# --- Ana Program Bloğu ---
if __name__ == "__main__":
    """
    Bu betik doğrudan çalıştırıldığında çalışacak olan ana blok.
    Eğer başka bir dosya tarafından import edilirse bu blok çalışmaz.
    """
    root = tk.Tk()  # Ana Tkinter penceresini oluştur.
    uygulama = AnaMenu(root)  # AnaMenu sınıfından bir örnek oluştur.
+   root.mainloop()  # Tkinter olay döngüsünü başlatarak pencerenin ekranda kalmasını sağla.
