import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, Listbox, END, Scrollbar
import veritabani_islemleri as vt
import urun_islemleri
import kullanici_islemleri as ki
import yardimcilar as yr
from metinler import MESAJLAR  # Merkezi metinler

class AdminPaneli:
    def __init__(self, ana_pencere, kullanici_adi):
        self.ana_pencere, self.kullanici_adi = ana_pencere, kullanici_adi
        self.pencere = Toplevel(ana_pencere)
        self.pencere.title(f"Yönetici Paneli - Hoş Geldin, {kullanici_adi}")
        self.pencere.geometry("800x600")
        self.pencere.protocol("WM_DELETE_WINDOW", self.guvenli_cikis)
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        ana_cerceve = tk.Frame(self.pencere, padx=20, pady=20)
        ana_cerceve.pack(fill=tk.BOTH, expand=True)
        ana_cerceve.grid_rowconfigure(0, weight=1)
        ana_cerceve.grid_columnconfigure(0, weight=1)
        ana_cerceve.grid_columnconfigure(1, weight=3)

        sol_menu = tk.Frame(ana_cerceve, width=200, relief=tk.RAISED, borderwidth=2)
        sol_menu.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        butonlar = {
            "Ürünleri Görüntüle": self.urunleri_goster,
            "Ürün Ekle": self.urun_ekle,
            "Ürün Sil": self.urun_sil,
            "Kullanıcıları Görüntüle": self.kullanicilari_goster,
            "Kullanıcı Ekle": self.kullanici_ekle,
            "Kullanıcı Sil": self.kullanici_sil,
            "Log Kayıtları": self.loglari_goster,
            "Profilim": self.profili_goster,
            "Şifre Değiştir": self.sifre_degistir,
        }

        buton_font = ("Arial", 12)
        for text, command in butonlar.items():
            tk.Button(sol_menu, text=text, command=command, font=buton_font).pack(fill=tk.X, pady=8, padx=10)

        tk.Button(sol_menu, text="Güvenli Çıkış", command=self.guvenli_cikis, font=buton_font, bg="red", fg="white").pack(side=tk.BOTTOM, fill=tk.X, pady=8, padx=10)

        self.icerik_alani = tk.Frame(ana_cerceve)
        self.icerik_alani.grid(row=0, column=1, sticky="nsew")
        tk.Label(self.icerik_alani, text="Yapmak istediğiniz işlemi soldaki menüden seçin.", font=("Arial", 14)).pack(pady=50)

    def icerigi_temizle(self):
        for widget in self.icerik_alani.winfo_children():
            widget.destroy()

    def urunleri_goster(self):
        self.icerigi_temizle()
        urun_islemleri.UrunGoruntuleyici(self.icerik_alani, self.kullanici_adi, is_admin=True).pack(fill=tk.BOTH, expand=True)

    def urun_ekle(self):
        urun_islemleri.UrunEklemePenceresi(self.pencere, self.kullanici_adi)
        self.urunleri_goster()

    def urun_sil(self):
        urun_islemleri.UrunSilmePenceresi(self.pencere, self.kullanici_adi)
        self.urunleri_goster()

    def kullanicilari_goster(self):
        self.icerigi_temizle()
        tk.Label(self.icerik_alani, text="Kayıtlı Kullanıcılar", font=("Arial", 16, "bold")).pack(pady=10)

        liste_cerceve = tk.Frame(self.icerik_alani)
        liste_cerceve.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        listbox = Listbox(liste_cerceve, font=("Courier", 12), width=50)
        scrollbar = Scrollbar(liste_cerceve, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.insert(END, f"{'ID':<5}{'KULLANICI ADI':<25}{'ROL':<15}")
        listbox.insert(END, "-" * 50)
        for kullanici in vt.tum_kullanicilari_getir():
            listbox.insert(END, f"{kullanici['id']:<5}{kullanici['kullanici_adi']:<25}{kullanici['rol']:<15}")

    def kullanici_ekle(self):
        if not ki.islem_icin_2fa_iste(self.pencere, self.kullanici_adi):
            return

        pencere = Toplevel(self.pencere)
        pencere.title("Yeni Kullanıcı Ekle")
        cerceve = tk.Frame(pencere, padx=20, pady=20)
        cerceve.pack()

        tk.Label(cerceve, text="Kullanıcı Adı:").grid(row=0, column=0, sticky="w")
        k_adi_giris = tk.Entry(cerceve)
        k_adi_giris.grid(row=0, column=1, pady=5)

        tk.Label(cerceve, text="Şifre:").grid(row=1, column=0, sticky="w")
        sifre_giris = tk.Entry(cerceve, show="*")
        sifre_giris.grid(row=1, column=1, pady=5)

        tk.Label(cerceve, text="Rol:").grid(row=2, column=0, sticky="w")
        rol_secim = tk.StringVar(value="Misafir")
        tk.Radiobutton(cerceve, text="Admin", variable=rol_secim, value="Admin").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(cerceve, text="Misafir", variable=rol_secim, value="Misafir").grid(row=3, column=1, sticky="w")

        def ekle():
            k_adi, sifre, rol = k_adi_giris.get(), sifre_giris.get(), rol_secim.get()
            if k_adi and sifre:
                if vt.kullanici_ekle(k_adi, sifre, rol):
                    messagebox.showinfo("Başarılı", f"{k_adi} kullanıcısı eklendi.", parent=pencere)
                    vt.log_ekle(self.kullanici_adi, 'Kullanıcı Eklendi', f"'{k_adi}' adlı kullanıcıyı ({rol}) ekledi.")
                    pencere.destroy()
                    self.kullanicilari_goster()
                else:
                    messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut.", parent=pencere)
            else:
                messagebox.showerror("Hata", "Tüm alanlar doldurulmalıdır.", parent=pencere)

        tk.Button(cerceve, text="Ekle", command=ekle).grid(row=4, columnspan=2, pady=10)

    def kullanici_sil(self):
        k_adi = simpledialog.askstring("Kullanıcı Sil", "Silmek istediğiniz kullanıcının adını girin:", parent=self.pencere)
        if k_adi:
            if k_adi == self.kullanici_adi:
                messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["KENDINI_SILEMEZSIN"], parent=self.pencere)
                return
            if vt.kullanici_getir(k_adi):
                onay_mesaji = MESAJLAR["KULLANICI_SIL_ONAY"].format(k_adi)
                if messagebox.askyesno(MESAJLAR["ONAY_BASLIK"], onay_mesaji, parent=self.pencere):
                    if ki.islem_icin_2fa_iste(self.pencere, self.kullanici_adi):
                        vt.kullanici_sil(k_adi)
                        messagebox.showinfo(MESAJLAR["BASARILI_BASARILI_BASLIK"], MESAJLAR["KULLANICI_SILINDI"], parent=self.pencere)
                        self.kullanicilari_goster()
            else:
                messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["KULLANICI_BULUNAMADI"], parent=self.pencere)

    def loglari_goster(self):
        self.icerigi_temizle()
        tk.Label(self.icerik_alani, text="Sistem Log Kayıtları", font=("Arial", 16, "bold")).pack(pady=10)

        liste_cerceve = tk.Frame(self.icerik_alani)
        liste_cerceve.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        listbox = Listbox(liste_cerceve, font=("Courier", 10))
        scrollbar = Scrollbar(liste_cerceve, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for log in vt.tum_loglari_getir():
            listbox.insert(END, f"[{log['zaman_damgasi']}] {log['kullanici_adi']} -> {log['islem']}: {log['detay']}")

    def profili_goster(self):
        ki.ProfilPenceresi(self.pencere, self.kullanici_adi)

    def sifre_degistir(self):
        ki.sifre_degistirme_islemi(self.pencere, self.kullanici_adi)

    def guvenli_cikis(self):
        if messagebox.askokcancel("Çıkış", "Oturumu kapatıp ana menüye dönmek istediğinize emin misiniz?"):
            self.pencere.destroy()
            self.ana_pencere.deiconify()
            vt.log_ekle(self.kullanici_adi, "Çıkış", "Yönetici oturumu kapattı.")
