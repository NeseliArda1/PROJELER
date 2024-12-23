
from veritabanı import Veritabani # veritabanı.py ve kullanici.py ve log.py dosyalarından gerekli sınıfları içe aktarıyor
from kullanici import Kullanici
from log import Log

if __name__ == "__main__": # Eğer bu dosya doğrudan çalıştırılıyorsa (başka bir dosyadan içe aktarılmıyorsa), bu blok çalıştırılır.
    # Veritabanını oluşturur veya zaten mevcutsa var olanı kullanır.
    Veritabani().olustur() # Veritabanını oluşturur veya zaten mevcutsa var olanı kullanır.
    print("Markete hoş geldiniz!") # Kullanıcıya hoş geldiniz mesajı gösterilir.
    while True: # Kullanıcıdan giriş yapmasını, yeni kullanıcı oluşturmasını veya çıkış yapmasını isteyen sonsuz bir döngü başlatılır.
        # Kullanıcıya seçenekler sunulur.
        print("\n1. Giriş Yap")
        print("2. Yeni Kullanıcı Oluştur")
        print("3. Çıkış Yap")
        secim = input("Seçiminiz: ") # Kullanıcının seçimi alınır.
        if secim == '1': # Kullanıcı "1" seçeneğini seçerse giriş yapma işlemi başlatılır.
            kullanici_adi = input("Kullanıcı adı: ") # Kullanıcı adı ve şifre bilgileri istenir.
            sifre = input("Şifre: ")
            kullanici = Kullanici.giris_yap(kullanici_adi, sifre) # Girilen kullanıcı adı ve şifre ile giriş yapılmaya çalışılır.
            if kullanici: # Eğer giriş başarılı olursa kullanıcı menüsüne yönlendirilir.
                Log.kaydet(kullanici_adi, f"Sisteme giriş yaptı")
                kullanici.menu()
            else: # Giriş başarısız olursa hata mesajı gösterilir.
                print("Hatalı kullanıcı adı veya şifre!")
        elif secim == '2': # Kullanıcı "2" seçeneğini seçerse yeni kullanıcı oluşturma işlemi başlatılır.
            kullanici_adi = input("Kullanıcı adı: ") # Yeni kullanıcı adı, şifre ve rol bilgileri istenir.
            sifre = input("Şifre: ")
            rol = input("Rol (admin/misafir): ")
            Kullanici.olustur(kullanici_adi, sifre, rol) # Girilen bilgilerle yeni kullanıcı veritabanına eklenir.
            print(f"Yeni kullanıcı oluşturuldu: {kullanici_adi}") # Yeni kullanıcının oluşturulduğu mesajı gösterilir.
        elif secim == '3': # Kullanıcı "3" seçeneğini seçerse çıkış işlemi başlatılır.
            print("Çıkış yapılıyor...") # Çıkış mesajı gösterilir.
            break # Sonsuz döngü kırılır ve program sonlanır.
        else:
            print("Geçersiz seçim!") # Geçersiz bir seçim yapılırsa uyarı mesajı gösterilir.
