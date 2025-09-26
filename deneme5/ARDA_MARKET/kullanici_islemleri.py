# --- Gerekli Modüllerin İçeri Aktarılması ---
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, filedialog
from tkinter import font as tkFont
import pyotp
import qrcode
from PIL import Image, ImageTk
import os
import shutil
import bcrypt

# --- Proje Modülleri ---
import veritabani_islemleri as vt
import admin_paneli
import misafir_paneli
import yardimcilar as yr
from metinler import MESAJLAR

# --- Genel Değişken ---
aktif_kullanici = None

# --- MERKEZİ ŞİFRE DEĞİŞTİRME FONKSİYONU ---
def sifre_degistirme_islemi(parent, kullanici_adi):
    """Kullanıcıdan mevcut ve yeni şifreyi alarak değiştirme işlemini yönetir."""
    kullanici = vt.kullanici_getir(kullanici_adi)
    if not kullanici:
        messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["KULLANICI_BULUNAMADI"], parent=parent)
        return

    mevcut_sifre = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["SIFRE_DEGISTIR_MEVCUT"], parent=parent, show="*")
    if not mevcut_sifre:
        return

    # Burada 'sifre' sütununa doğrudan erişim zaten doğruydı
    if not vt.sifre_dogrula(kullanici['sifre'], mevcut_sifre):
        messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["MEVCUT_SIFRE_HATASI"], parent=parent)
        return

    yeni_sifre = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["SIFRE_DEGISTIR_YENI"], parent=parent, show="*")
    if not yeni_sifre:
        return

    if len(yeni_sifre) < 6:
        messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["SIFRE_KARAKTER_HATASI"], parent=parent)
        return

    # Burada 'sifre' sütununa doğrudan erişim zaten doğruydı
    if bcrypt.checkpw(yeni_sifre.encode('utf-8'), kullanici['sifre']):
        messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["AYNI_SIFRE_HATASI"], parent=parent)
        return

    yeni_sifre_tekrar = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["SIFRE_DEGISTIR_TEKRAR"], parent=parent, show="*")
    if not yeni_sifre_tekrar:
        return

    if yeni_sifre != yeni_sifre_tekrar:
        messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["SIFRE_ESLESMIYOR"], parent=parent)
        return

    vt.sifre_guncelle(kullanici_adi, yeni_sifre)
    messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], MESAJLAR["SIFRE_KAYIT_BASARILI"], parent=parent)


# --- Giriş Penceresi Sınıfı ---
class GirisPenceresi(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Giriş Yap")
        self.geometry("350x450")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # self.master.withdraw() # Bu satır yorum satırı yapıldı veya silindi

        self.arayuzu_olustur()

        self.protocol("WM_DELETE_WINDOW", self.guvenli_kapatma)

    def arayuzu_olustur(self):
        cerceve = tk.Frame(self, padx=20, pady=20)
        cerceve.pack(expand=True)

        etiket_font = tkFont.Font(family="Arial", size=10, weight="bold")
        giris_font = tkFont.Font(family="Arial", size=10)

        tk.Label(cerceve, text="Kullanıcı Adı:", font=etiket_font).pack(pady=5)
        self.kullanici_adi_entry = tk.Entry(cerceve, width=30, font=giris_font)
        self.kullanici_adi_entry.pack(pady=5)

        tk.Label(cerceve, text="Şifre:", font=etiket_font).pack(pady=5)
        self.sifre_entry = tk.Entry(cerceve, show="*", width=30, font=giris_font)
        self.sifre_entry.pack(pady=5)

        self.captcha_frame = tk.Frame(cerceve)
        self.captcha_frame.pack(pady=10)
        self.captcha = yr.Captcha(self.captcha_frame)
        self.captcha.canvas.pack(side=tk.LEFT)
        tk.Button(self.captcha_frame, text="Yenile", command=self.captcha.yenile).pack(side=tk.LEFT, padx=5)

        tk.Label(cerceve, text="Doğrulama Kodu:").pack(pady=5)
        self.captcha_entry = tk.Entry(cerceve, width=30, font=giris_font)
        self.captcha_entry.pack(pady=5)

        tk.Button(cerceve, text="Giriş Yap", command=self.giris_yap, bg="#4CAF50", fg="white", font=etiket_font).pack(pady=10)
        tk.Button(cerceve, text="Kaydol", command=self.kayit_ol, bg="#2196F3", fg="white", font=etiket_font).pack(pady=5)

    def guvenli_kapatma(self):
        self.master.deiconify()
        self.destroy()

    def giris_yap(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        girilen_captcha = self.captcha_entry.get().strip()

        if not self.captcha.dogrula(girilen_captcha):
            messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["CAPTCHA_HATASI"], parent=self)
            return

        kullanici_data = vt.kullanici_dogrula(kullanici_adi, sifre)

        if kullanici_data:
            # 'tfa_secret' sütununa doğrudan erişim
            if kullanici_data['tfa_secret']:
                kod_2fa = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["2FA_ISLEM_GEREKLI"], parent=self)
                if not kod_2fa or not dogrula_2fa(kullanici_adi, kod_2fa):
                    messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["2FA_KOD_YANLIS"], parent=self)
                    vt.log_ekle(kullanici_adi, 'Giriş Başarısız', 'Yanlış 2FA Kodu')
                    return

            messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], f"Hoş Geldin, {kullanici_adi}!", parent=self)
            vt.log_ekle(kullanici_adi, 'Giriş Başarılı', MESAJLAR["GIRIS_BASARILI_LOG"])
            self.destroy()
            self.master.withdraw()
            yonlendir(self.master, kullanici_data)
        else:
            messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["GIRIS_HATASI"], parent=self)
            vt.log_ekle(kullanici_adi, 'Giriş Başarısız', MESAJLAR["GIRIS_HATASI_LOG"])

    def kayit_ol(self):
        self.destroy()
        KayitPenceresi(self.master, 'Misafir')

# --- Kayıt Penceresi Sınıfı ---
class KayitPenceresi(Toplevel):
    def __init__(self, parent, rol):
        super().__init__(parent)
        self.title("Kaydol")
        self.geometry("300x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.rol = rol

        self.arayuzu_olustur()
        self.protocol("WM_DELETE_WINDOW", self.guvenli_kapatma)

    def arayuzu_olustur(self):
        cerceve = tk.Frame(self, padx=20, pady=20)
        cerceve.pack(expand=True)

        tk.Label(cerceve, text="Kullanıcı Adı:").pack(pady=5)
        self.kullanici_adi_entry = tk.Entry(cerceve, width=30)
        self.kullanici_adi_entry.pack(pady=5)

        tk.Label(cerceve, text="Şifre:").pack(pady=5)
        self.sifre_entry = tk.Entry(cerceve, show="*", width=30)
        self.sifre_entry.pack(pady=5)

        tk.Button(cerceve, text="Kaydol", command=self.kayit_ol, bg="#4CAF50", fg="white").pack(pady=10)

    def guvenli_kapatma(self):
        self.master.deiconify()
        self.destroy()

    def kayit_ol(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        if not kullanici_adi or not sifre:
            messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["GEREKLI_ALANLARI_DOLDUR"], parent=self)
            return

        if len(sifre) < 6:
            messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["SIFRE_KARAKTER_HATASI"], parent=self)
            return

        if vt.kullanici_ekle(kullanici_adi, sifre, self.rol):
            messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], "Kayıt başarılı!", parent=self)
            self.guvenli_kapatma()
            self.master.deiconify()
        else:
            messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["KULLANICI_MEVCUT"], parent=self)


# --- Profil Penceresi Sınıfı ---
class ProfilPenceresi(Toplevel):
    def __init__(self, parent, kullanici_adi):
        super().__init__(parent)
        self.title("Profilim")
        self.geometry("400x550")
        self.transient(parent)
        self.grab_set()

        self.kullanici_adi = kullanici_adi
        self.kullanici_data = vt.kullanici_getir(kullanici_adi)

        self.arayuzu_olustur()
        self.verileri_doldur()

    def arayuzu_olustur(self):
        cerceve = tk.Frame(self, padx=20, pady=20)
        cerceve.pack(fill="both", expand=True)

        tk.Label(cerceve, text="Kullanıcı Adı:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(cerceve, text=self.kullanici_adi, font=("Arial", 12)).pack(pady=2)

        # 'rol' sütununa doğrudan erişim
        tk.Label(cerceve, text="Rol:", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(cerceve, text=self.kullanici_data['rol'], font=("Arial", 12)).pack(pady=2)

        tk.Label(cerceve, text="Profil Resmi:", font=("Arial", 10, "bold")).pack(pady=10)
        self.profil_resmi_canvas = tk.Canvas(cerceve, width=100, height=100, bg="lightgrey", relief="sunken")
        self.profil_resmi_canvas.pack(pady=5)

        tk.Button(cerceve, text="Resim Değiştir", command=self.resim_sec).pack(pady=5)

        tk.Label(cerceve, text="İki Faktörlü Kimlik Doğrulama (2FA):", font=("Arial", 10, "bold")).pack(pady=15)

        self.tfa_durum_label = tk.Label(cerceve, text="", font=("Arial", 10))
        self.tfa_durum_label.pack(pady=2)

        self.tfa_etkinlestir_button = tk.Button(cerceve, text="2FA Etkinleştir", command=self.tfa_etkinlestir)
        self.tfa_etkinlestir_button.pack(pady=5)

        self.tfa_devre_disi_birak_button = tk.Button(cerceve, text="2FA Devre Dışı Bırak", command=self.tfa_devre_disi_birak)
        self.tfa_devre_disi_birak_button.pack(pady=5)

        tk.Button(cerceve, text="Şifre Değiştir", command=self.sifre_degistir, bg="#FFC107", fg="black").pack(pady=20)

        self.guncel_2fa_durumunu_goster()

    def verileri_doldur(self):
        self.profil_resmi_goster()

    def profil_resmi_goster(self):
        self.profil_resmi_canvas.delete("all")
        # 'profil_resmi' sütununa doğrudan erişim
        resim_yolu = self.kullanici_data['profil_resmi']
        if resim_yolu and os.path.exists(resim_yolu):
            try:
                img = Image.open(resim_yolu)
                img = img.resize((100, 100), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.profil_resmi_canvas.create_image(50, 50, image=self.photo, anchor="center")
            except Exception as e:
                print(f"Resim yüklenirken hata: {e}")
                self.profil_resmi_canvas.create_text(50, 50, text="Resim Hatalı", fill="red")
        else:
            self.profil_resmi_canvas.create_text(50, 50, text="Resim Yok", fill="gray")

    def resim_sec(self):
        dosya_yolu = filedialog.askopenfilename(
            title="Profil Resmi Seç",
            filetypes=(("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif"), ("Tüm Dosyalar", "*.*"))
        )
        if not dosya_yolu:
            return

        resim_dizini = "users_profile_pictures"
        os.makedirs(resim_dizini, exist_ok=True)

        orjinal_dosya_adi = os.path.basename(dosya_yolu)
        yeni_resim_adi = f"user_{self.kullanici_adi}_{orjinal_dosya_adi}"
        hedef_yol = os.path.join(resim_dizini, yeni_resim_adi)
        # 'profil_resmi' sütununa doğrudan erişim
        eski_resim_yolu = self.kullanici_data['profil_resmi']

        try:
            shutil.copy2(dosya_yolu, hedef_yol)
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kopyalanırken bir hata oluştu: {e}", parent=self)
            return

        try:
            vt.profil_resmi_guncelle(self.kullanici_adi, hedef_yol)
        except Exception as e:
            messagebox.showerror("Hata", f"Veritabanı güncellenirken bir hata oluştu: {e}", parent=self)
            os.remove(hedef_yol)
            return

        if eski_resim_yolu and eski_resim_yolu != hedef_yol and os.path.exists(eski_resim_yolu):
            try:
                os.remove(eski_resim_yolu)
            except OSError as e:
                print(f"Eski profil resmi silinemedi (kritik olmayan hata): {e}")

        self.kullanici_data = vt.kullanici_getir(self.kullanici_adi)
        self.profil_resmi_goster()
        messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], MESAJLAR["PROFIL_RESMI_GUNCELLENDI"], parent=self)

    def sifre_degistir(self):
        sifre_degistirme_islemi(self, self.kullanici_adi)

    def guncel_2fa_durumunu_goster(self):
        self.kullanici_data = vt.kullanici_getir(self.kullanici_adi)
        # 'tfa_secret' sütununa doğrudan erişim
        if self.kullanici_data['tfa_secret']:
            self.tfa_durum_label.config(text="Durum: Etkin", fg="green")
            self.tfa_etkinlestir_button.config(state=tk.DISABLED)
            self.tfa_devre_disi_birak_button.config(state=tk.NORMAL)
        else:
            self.tfa_durum_label.config(text="Durum: Devre Dışı", fg="red")
            self.tfa_etkinlestir_button.config(state=tk.NORMAL)
            self.tfa_devre_disi_birak_button.config(state=tk.DISABLED)

    def tfa_etkinlestir(self):
        # 'tfa_secret' sütununa doğrudan erişim
        if self.kullanici_data['tfa_secret']:
            messagebox.showinfo(MESAJLAR["BILGI_BASLIK"], MESAJLAR["2FA_ZATEN_ETKIN"], parent=self)
            return

        secret = pyotp.random_base32()
        uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=self.kullanici_adi,
            issuer_name="Arda Market Sistemi"
        )
        
        qr_pencere = Toplevel(self)
        qr_pencere.title("2FA QR Kodu")
        qr_pencere.grab_set()

        img = qrcode.make(uri)
        photo = ImageTk.PhotoImage(img)
        qr_label = tk.Label(qr_pencere, image=photo)
        qr_label.image = photo
        qr_label.pack(pady=10)

        tk.Label(qr_pencere, text="Google Authenticator gibi bir uygulama ile bu kodu tarayın.", font=("Arial", 10)).pack(pady=5)
        tk.Label(qr_pencere, text="Ardından, oluşturulan kodu girin:").pack(pady=5)

        kod_entry = tk.Entry(qr_pencere, width=20)
        kod_entry.pack(pady=5)

        def verify_and_save():
            girilen_kod = kod_entry.get().strip()
            if pyotp.TOTP(secret).verify(girilen_kod, valid_window=1):
                vt.tfa_secret_guncelle(self.kullanici_adi, secret)
                messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], MESAJLAR["2FA_BASARILI"], parent=self)
                self.guncel_2fa_durumunu_goster()
                qr_pencere.destroy()
            else:
                messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["2FA_KOD_YANLIS"], parent=qr_pencere)

        tk.Button(qr_pencere, text="Doğrula ve Etkinleştir", command=verify_and_save, bg="#4CAF50", fg="white").pack(pady=10)

    def tfa_devre_disi_birak(self):
        # 'tfa_secret' sütununa doğrudan erişim
        if not self.kullanici_data['tfa_secret']:
            messagebox.showinfo(MESAJLAR["BILGI_BASLIK"], MESAJLAR["2FA_ZATEN_KAPALI"], parent=self)
            return

        if messagebox.askyesno(MESAJLAR["ONAY_BASLIK"], MESAJLAR["2FA_DEVRE_DISI_BIRAK_ONAY"], parent=self):
            sifre = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["SIFRE_ONAY_GEREKLI"], parent=self, show='*')
            # 'sifre' sütununa doğrudan erişim zaten doğruydı
            if not sifre or not vt.sifre_dogrula(self.kullanici_data['sifre'], sifre):
                messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["MEVCUT_SIFRE_HATASI"], parent=self)
                return

            kod_2fa = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["2FA_ISLEM_GEREKLI"], parent=self)
            if kod_2fa and dogrula_2fa(self.kullanici_adi, kod_2fa):
                vt.tfa_secret_guncelle(self.kullanici_adi, None)
                messagebox.showinfo(MESAJLAR["BASARILI_BASLIK"], MESAJLAR["2FA_DEVRE_DISI_BIRAKILDI"], parent=self)
                self.guncel_2fa_durumunu_goster()
            else:
                messagebox.showerror(MESAJLAR["HATA_BASLIK"], MESAJLAR["2FA_KOD_YANLIS"], parent=self)

# --- Yardımcı Fonksiyonlar ---
def yonlendir(ana_pencere, kullanici):
    """Kullanıcıyı rolüne göre doğru panele yönlendirir."""
    panel_class = admin_paneli.AdminPaneli if kullanici['rol'] == 'Admin' else misafir_paneli.MisafirPaneli
    panel_class(ana_pencere, kullanici['kullanici_adi'])

def dogrula_2fa(kullanici_adi, girilen_kod):
    """Verilen 2FA kodunun doğruluğunu kontrol eder."""
    kullanici = vt.kullanici_getir(kullanici_adi)
    # 'tfa_secret' sütununa doğrudan erişim
    if kullanici and kullanici['tfa_secret']:
        if not girilen_kod.strip().isdigit():
            return False
        return pyotp.TOTP(kullanici['tfa_secret']).verify(girilen_kod, valid_window=1)
    return False

def islem_icin_2fa_iste(parent, kullanici_adi):
    """Kritik işlemler öncesi 2FA doğrulaması ister."""
    kullanici = vt.kullanici_getir(kullanici_adi)
    # 'tfa_secret' sütununa doğrudan erişim
    if not kullanici or not kullanici['tfa_secret']:
        return True # 2FA etkin değilse, işlemi yapmaya izin ver

    kod = simpledialog.askstring(MESAJLAR["ONAY_BASLIK"], MESAJLAR["2FA_ISLEM_GEREKLI"], parent=parent)
    if kod and dogrula_2fa(kullanici_adi, kod):
        return True
    
    messagebox.showwarning(MESAJLAR["UYARI_BASLIK"], MESAJLAR["2FA_ISLEM_IPTAL"], parent=parent)
    return False

if __name__ == "__main__":
    root = tk.Tk()
    # root.withdraw() # Bu satır yorum satırı yapıldı veya silindi
    GirisPenceresi(root)
    root.mainloop()