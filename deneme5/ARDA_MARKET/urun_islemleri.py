import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox, simpledialog, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import os
import shutil
import veritabani_islemleri as vt
import kullanici_islemleri as ki # Bu import'un varlığını kontrol edin
from metinler import MESAJLAR # Merkezi metinler

# --- Ürün Görüntüleyici Sınıfı ---
class UrunGoruntuleyici(Frame):
    def __init__(self, parent, kullanici_adi, is_admin=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.kullanici_adi = kullanici_adi
        self.is_admin = is_admin

        # Canvas ve Scrollbar oluşturma
        self.canvas = Canvas(self, borderwidth=0)
        self.cerceve = Frame(self.canvas)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.cerceve, anchor="nw")

        self.cerceve.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        self.urunleri_yukle()

    def onFrameConfigure(self, event):
        """Canvas scroll bölgesini ayarlar."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def urunleri_yukle(self):
        """Veritabanından ürünleri çeker ve canvas'a yerleştirir."""
        # Mevcut ürünleri temizle
        for widget in self.cerceve.winfo_children():
            widget.destroy()

        urunler = vt.tum_urunleri_getir()
        row, col = 0, 0
        for urun in urunler:
            urun_karti = self.urun_karti_olustur(urun)
            urun_karti.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            col += 1
            if col > 2: # Her satırda 3 ürün
                col = 0
                row += 1

    def urun_karti_olustur(self, urun):
        """Tek bir ürün için görsel kart oluşturur."""
        kart = Frame(self.cerceve, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10)
        
        # Ürün Resmi
        resim_yolu = urun['resim_yolu']
        if resim_yolu and os.path.exists(resim_yolu):
            img = Image.open(resim_yolu)
            img.thumbnail((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            resim_etiketi = tk.Label(kart, image=img_tk)
            resim_etiketi.image = img_tk # Referansı sakla
            resim_etiketi.pack(pady=5)
        else:
            tk.Label(kart, text="Resim Yok", height=8, width=20, bg="lightgrey").pack(pady=5)

        tk.Label(kart, text=urun['urun_adi'], font=("Arial", 14, "bold")).pack()
        tk.Label(kart, text=f"Fiyat: {urun['fiyat']:.2f} TL", font=("Arial", 12)).pack()
        tk.Label(kart, text=f"Stok: {urun['stok']}", font=("Arial", 10)).pack()
        
        # Satın Al Butonu (Admin değilse göster)
        if not self.is_admin:
            tk.Button(kart, text="Satın Al", command=lambda u=urun: self.satin_al(u), bg="#4CAF50", fg="white").pack(pady=10)

        return kart

    # --- DÜZELTME BAŞLANGICI ---
    def satin_al(self, urun):
        if urun['stok'] <= 0:
            messagebox.showwarning(MESAJLAR["STOK_TUKENDI_UYARI"], MESAJLAR["STOK_TUKENDI_MESAJ"], parent=self) # parent eklendi
            return

        # Ürün miktarı soruldu
        miktar_str = simpledialog.askstring("Satın Al", f"{urun['urun_adi']} ürününden kaç adet satın almak istersiniz?", parent=self)
        if miktar_str is None: # Kullanıcı iptal etti
            return
        
        try:
            miktar = int(miktar_str)
            if miktar <= 0:
                messagebox.showerror("Hata", "Miktar pozitif bir tam sayı olmalıdır.", parent=self)
                return
            if miktar > urun['stok']:
                messagebox.showerror("Hata", f"Yeterli stok yok. Mevcut stok: {urun['stok']}", parent=self)
                return
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz miktar. Lütfen bir sayı girin.", parent=self)
            return

        # 2FA Doğrulaması (Kullanıcı İşlemleri modülünden çağrılıyor)
        if not ki.islem_icin_2fa_iste(self, self.kullanici_adi):
            messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["2FA_DOGRULAMA_BASARISIZ"], parent=self)
            return

        # Toplam tutar hesaplama ve ödeme onayı
        toplam_tutar = miktar * urun['fiyat']
        onay = messagebox.askyesno("Satın Alma Onayı", 
                                   f"{urun['urun_adi']} ürününden {miktar} adet almak istiyor musunuz?\nToplam Tutar: {toplam_tutar:.2f} TL",
                                   parent=self)
        
        if onay:
            vt.urun_stok_guncelle(urun['id'], miktar)
            messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], f"{miktar} adet {urun['urun_adi']} başarıyla satın alındı.", parent=self)
            vt.log_ekle(self.kullanici_adi, "Ürün Satın Aldı", f"{miktar} adet '{urun['urun_adi']}' ({toplam_tutar:.2f} TL) satın alındı.")
            self.urunleri_yukle() # Ürün listesini yenile
        else:
            messagebox.showinfo("İptal Edildi", "Satın alma işlemi iptal edildi.", parent=self)

    # --- DÜZELTME SONU ---
            
# --- Ürün Ekleme Penceresi ---
class UrunEklemePenceresi(Toplevel):
    def __init__(self, parent, kullanici_adi):
        super().__init__(parent)
        self.title("Yeni Ürün Ekle")
        self.kullanici_adi = kullanici_adi
        self.resim_yolu = None
        
        cerceve = Frame(self, padx=20, pady=20)
        cerceve.pack()
        
        tk.Label(cerceve, text="Ürün Adı:").grid(row=0, column=0, sticky="w", pady=5)
        self.urun_adi_giris = tk.Entry(cerceve, width=30)
        self.urun_adi_giris.grid(row=0, column=1)
        
        tk.Label(cerceve, text="Fiyat (TL):").grid(row=1, column=0, sticky="w", pady=5)
        self.fiyat_giris = tk.Entry(cerceve, width=30)
        self.fiyat_giris.grid(row=1, column=1)
        
        tk.Label(cerceve, text="Stok (Adet):").grid(row=2, column=0, sticky="w", pady=5)
        self.stok_giris = tk.Entry(cerceve, width=30)
        self.stok_giris.grid(row=2, column=1)
        
        tk.Button(cerceve, text="Resim Seç...", command=self.resim_sec).grid(row=3, column=0, pady=10)
        self.resim_etiketi = tk.Label(cerceve, text="Resim seçilmedi.")
        self.resim_etiketi.grid(row=3, column=1)

        tk.Button(cerceve, text="Ürünü Ekle", command=self.urun_ekle, font=("Arial", 12, "bold")).grid(row=4, columnspan=2, pady=20)

    def resim_sec(self):
        dosya_yolu = filedialog.askopenfilename(title="Ürün Resmi Seç", filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg")])
        if dosya_yolu:
            self.resim_yolu = dosya_yolu
            self.resim_etiketi.config(text=os.path.basename(dosya_yolu))

    def urun_ekle(self):
        urun_adi = self.urun_adi_giris.get()
        try:
            fiyat = float(self.fiyat_giris.get())
            stok = int(self.stok_giris.get())
        except ValueError:
            messagebox.showerror("Hata", "Fiyat ve stok sayısal değerler olmalıdır.", parent=self)
            return

        if not (urun_adi and fiyat > 0 and stok >= 0):
            messagebox.showerror("Hata", "Tüm alanlar doğru bir şekilde doldurulmalıdır.", parent=self)
            return
            
        if not ki.islem_icin_2fa_iste(self, self.kullanici_adi):
            return

        # Resmi kaydet
        kaydedilen_resim_yolu = None
        if self.resim_yolu:
            hedef_klasor = 'images'
            # Dosya adını ürün adından türetmek çakışmaları önleyebilir
            dosya_uzantisi = os.path.splitext(self.resim_yolu)[1]
            yeni_dosya_adi = f"{urun_adi.replace(' ', '_')}{dosya_uzantisi}"
            kaydedilen_resim_yolu = os.path.join(hedef_klasor, yeni_dosya_adi)
            os.makedirs(hedef_klasor, exist_ok=True) # Klasörün varlığını kontrol et ve yoksa oluştur
            shutil.copy(self.resim_yolu, kaydedilen_resim_yolu)
        
        if vt.urun_ekle(urun_adi, fiyat, stok, kaydedilen_resim_yolu):
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Hata", "Bu ürün adı zaten mevcut.", parent=self)

# --- Ürün Silme Penceresi ---
class UrunSilmePenceresi(Toplevel):
    def __init__(self, parent, kullanici_adi):
        super().__init__(parent)
        self.title("Ürün Sil")
        self.kullanici_adi = kullanici_adi
        
        cerceve = Frame(self, padx=20, pady=20)
        cerceve.pack(fill="both", expand=True)
        
        tk.Label(cerceve, text="Silmek istediğiniz ürünü seçin:").pack(pady=10)
        
        self.listbox = tk.Listbox(cerceve, width=50, height=15)
        self.listbox.pack()
        
        self.urunleri_listele()
        
        tk.Button(cerceve, text="Seçili Ürünü Sil", command=self.urun_sil, bg="red", fg="white").pack(pady=10)

    def urunleri_listele(self):
        self.urunler = vt.tum_urunleri_getir()
        self.listbox.delete(0, tk.END)
        for urun in self.urunler:
            self.listbox.insert(tk.END, f"ID: {urun['id']} - {urun['urun_adi']}")

    def urun_sil(self):
        secili_index = self.listbox.curselection()
        if not secili_index:
            messagebox.showerror("Hata", "Lütfen silmek için bir ürün seçin.", parent=self)
            return
        
        secili_urun = self.urunler[secili_index[0]]
        
        if messagebox.askyesno("Onay", f"'{secili_urun['urun_adi']}' adlı ürünü silmek istediğinize emin misiniz?", parent=self):
            if ki.islem_icin_2fa_iste(self, self.kullanici_adi):
                vt.urun_sil(secili_urun['id'])
                messagebox.showinfo("Başarılı", "Ürün silindi.", parent=self)
                self.urunleri_listele() # Listeyi yenile
                