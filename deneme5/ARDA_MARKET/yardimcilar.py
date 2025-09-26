
# --- Gerekli Modüllerin İçeri Aktarılması ---
import tkinter as tk
from tkinter import Toplevel
import random
import string
import importlib.util  # Modülleri dinamik olarak yüklemek için.
import sys
import os

# --- CAPTCHA Sınıfı ---
class Captcha:
    """
    CAPTCHA oluşturma ve doğrulama işlevlerini bir araya getiren sınıf.
    Kullanıcı girişlerinin bot tarafından yapılmadığını doğrulamak için kullanılır.
    """
    def __init__(self, parent_frame):
        self.canvas = tk.Canvas(parent_frame, width=200, height=80, bg="white", relief=tk.SUNKEN, borderwidth=2)
        self.yenile()

    def captcha_uret(self, uzunluk=5):
        """Belirtilen uzunlukta rastgele CAPTCHA metni oluşturur."""
        karakterler = string.ascii_uppercase + string.digits
        return ''.join(random.choices(karakterler, k=uzunluk))

    def gurultu_ekle(self, genislik, yukseklik, cizgi_sayisi=10, nokta_sayisi=50):
        """CAPTCHA'yı okumayı zorlaştırmak için görsel parazit (çizgi, nokta) ekler."""
        # Rastgele çizgiler
        for _ in range(cizgi_sayisi):
            x1, y1 = random.randint(0, genislik), random.randint(0, yukseklik)
            x2, y2 = random.randint(0, genislik), random.randint(0, yukseklik)
            renk = random.choice(["lightgrey", "lightblue", "lightgreen"])
            self.canvas.create_line(x1, y1, x2, y2, fill=renk, width=1)
        # Rastgele noktalar
        for _ in range(nokta_sayisi):
            x, y = random.randint(0, genislik), random.randint(0, yukseklik)
            renk = random.choice(["grey", "lightgrey"])
            self.canvas.create_oval(x, y, x + 1, y + 1, fill=renk, outline="")

    def captcha_ciz(self, metin):
        """Oluşturulan CAPTCHA metnini canvas üzerine çizer."""
        self.canvas.delete("all")
        genislik, yukseklik = 200, 80
        self.gurultu_ekle(genislik, yukseklik)

        # Her karakteri rastgele konum, renk ve açıyla çizer
        for i, karakter in enumerate(metin):
            x = 25 + i * 35 + random.randint(-5, 5)
            y = random.randint(25, 55)
            aci = random.randint(-40, 40)
            renk = random.choice(["blue", "black", "darkgreen", "red", "purple"])
            yazi_tipi = ("Arial", 28, "bold")
            self.canvas.create_text(x, y, text=karakter, angle=aci, font=yazi_tipi, fill=renk)
    
    def yenile(self):
        """Yeni bir CAPTCHA oluşturur ve ekrana çizer."""
        self.aktif_captcha = self.captcha_uret()
        self.captcha_ciz(self.aktif_captcha)
        
    def dogrula(self, kullanici_girisi):
        """Kullanıcının girdiği metnin CAPTCHA ile eşleşip eşleşmediğini kontrol eder."""
        return kullanici_girisi.upper() == self.aktif_captcha
