
import tkinter as tk
from tkinter import Toplevel, messagebox
import veritabani_islemleri as vt
import urun_islemleri
import kullanici_islemleri as ki
import yardimcilar as yr
from metinler import MESAJLAR # Merkezi metinler

class MisafirPaneli:
    def __init__(self, ana_pencere, kullanici_adi):
        self.ana_pencere, self.kullanici_adi = ana_pencere, kullanici_adi
        self.pencere = Toplevel(ana_pencere)
        self.pencere.title(f"Arda Market - Hoş Geldin, {kullanici_adi}")
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

        buton_font = ("Arial", 12)
        butonlar = {
            "Ürünleri Görüntüle": self.urunleri_goster,
            "Profilim": self.profili_goster,
            "Şifre Değiştir": self.sifre_degistir, 
        }
        for text, command in butonlar.items():
            tk.Button(sol_menu, text=text, command=command, font=buton_font).pack(fill=tk.X, pady=8, padx=10)
        
        tk.Button(sol_menu, text="Güvenli Çıkış", command=self.guvenli_cikis, font=buton_font, bg="red", fg="white").pack(side=tk.BOTTOM, fill=tk.X, pady=8, padx=10)

        self.icerik_alani = tk.Frame(ana_cerceve)
        self.icerik_alani.grid(row=0, column=1, sticky="nsew")
        self.urunleri_goster()

    def icerigi_temizle(self):
        for widget in self.icerik_alani.winfo_children(): widget.destroy()

    def urunleri_goster(self):
        self.icerigi_temizle()
        urun_islemleri.UrunGoruntuleyici(self.icerik_alani, self.kullanici_adi, is_admin=False).pack(fill=tk.BOTH, expand=True)

    def profili_goster(self):
        ki.ProfilPenceresi(self.pencere, self.kullanici_adi)

    def sifre_degistir(self):
        # Merkezi fonksiyonu çağır
        ki.sifre_degistirme_islemi(self.pencere, self.kullanici_adi)
   
    def guvenli_cikis(self):
        if messagebox.askokcancel(MESAJLAR["ONAY_BASLIK"], MESAJLAR["CIKIS_ONAY"]):
            self.pencere.destroy()
            self.ana_pencere.deiconify()
            vt.log_ekle(self.kullanici_adi, "Çıkış", "Kullanıcı oturumu kapattı.")
            