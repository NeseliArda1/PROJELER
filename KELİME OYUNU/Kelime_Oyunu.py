
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import json # JSON işlemleri için
from datetime import datetime
from collections import Counter # Harf sayısı kontrolü için

# Sabitler
PUZZLE_FILE = "puzzles.json"
HIGH_SCORE_FILE = "high_scores.json"
HINT_PENALTY = 5 # İpucu için puan cezası

class WordGameApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Kelime Oyunu")
        self.root.geometry("600x700") # Boyut biraz ayarlandı
        self.root.configure(bg="#e0f0e0")

        self.all_puzzles_data = []
        self.current_puzzle_idx = -1
        self.current_puzzle = None
        self.target_words = set()
        self.available_letters_counter = Counter()
        self.display_letters_str = ""

        self.found_words = set()
        self.session_score = 0 # Oturum boyunca toplam skor
        self.username = ""
        self.hint_used_this_puzzle = False # Her bulmacada bir ipucu hakkı

        self.setup_ui_style()
        self.create_login_frame()
        self.create_game_frame()

        if not self.load_puzzles_from_file():
            self.root.quit() # Bulmaca yüklenemezse çık

    def setup_ui_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TLabel", font=("Arial", 12), background="#e0f0e0")
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#e0f0e0")
        self.style.configure("Score.TLabel", font=("Arial", 18, "bold"), foreground="#b22222", background="#e0f0e0")
        self.style.configure("Status.TLabel", font=("Arial", 10, "italic"), background="#e0f0e0")
        self.style.configure("Progress.TLabel", font=("Arial", 10), background="#e0f0e0")
        self.style.configure("TEntry", font=("Arial", 14), padding=5)

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.login_frame.pack(pady=100, padx=20, fill="x", expand=True)
        ttk.Label(self.login_frame, text="Kullanıcı Adı:", style="Header.TLabel").pack(pady=10)
        self.entry_name = ttk.Entry(self.login_frame, width=30)
        self.entry_name.pack(pady=5)
        self.entry_name.focus()
        ttk.Button(self.login_frame, text="Oyuna Başla", command=self.start_new_session).pack(pady=10)
        ttk.Button(self.login_frame, text="Yüksek Skorlar", command=self.show_high_scores).pack(pady=5)

    def create_game_frame(self):
        self.game_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.welcome_label = ttk.Label(self.game_frame, text="", style="Header.TLabel")
        self.welcome_label.pack(pady=(0,10))
        self.letters_label = ttk.Label(self.game_frame, text="Harfler: ", style="Header.TLabel")
        self.letters_label.pack(pady=10)
        self.entry_word = ttk.Entry(self.game_frame, width=25)
        self.entry_word.pack(pady=10)
        self.entry_word.bind("<Return>", lambda event: self.check_word())

        button_frame = ttk.Frame(self.game_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Kontrol Et", command=self.check_word).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Temizle", command=self.clear_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Karıştır", command=self.shuffle_display_letters).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İpucu", command=self.get_hint).pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(self.game_frame, text="Kelime girin.", style="Status.TLabel", width=60, anchor="center")
        self.status_label.pack(pady=5)
        self.score_label = ttk.Label(self.game_frame, text="0 ✨", style="Score.TLabel")
        self.score_label.pack(pady=10)
        
        self.progress_label = ttk.Label(self.game_frame, text="Bulunan: 0/0", style="Progress.TLabel")
        self.progress_label.pack(pady=5)

        ttk.Label(self.game_frame, text="Bulunan Kelimeler:", style="TLabel").pack(pady=(10,0))
        self.listbox_words = tk.Listbox(self.game_frame, font=("Arial", 12), width=30, height=6, bg="#f0fff0", selectbackground="#add8e6")
        self.listbox_words.pack(pady=5)
        ttk.Button(self.game_frame, text="Sonraki Bulmaca", command=self.process_next_puzzle).pack(pady=10)

    def load_puzzles_from_file(self):
        try:
            with open(PUZZLE_FILE, 'r', encoding='utf-8') as f:
                loaded_puzzles = json.load(f)
            # Kelime listelerini sete çevir ve display_letters yoksa oluştur
            for puzzle in loaded_puzzles:
                puzzle["words"] = set(w.upper() for w in puzzle["words"])
                if "display_letters" not in puzzle:
                    puzzle["display_letters"] = ", ".join(sorted(list(puzzle["letters"].upper())))
            self.all_puzzles_data = loaded_puzzles
            return True
        except FileNotFoundError:
            messagebox.showerror("Hata", f"Bulmaca dosyası bulunamadı: {PUZZLE_FILE}")
            return False
        except json.JSONDecodeError:
            messagebox.showerror("Hata", f"Bulmaca dosyası formatı bozuk: {PUZZLE_FILE}")
            return False
        except Exception as e:
            messagebox.showerror("Hata", f"Bulmaca yüklenirken bilinmeyen bir hata oluştu: {e}")
            return False


    def start_new_session(self):
        username_attempt = self.entry_name.get().strip()
        if not username_attempt:
            messagebox.showwarning("Uyarı", "Lütfen bir kullanıcı adı girin.")
            return
        self.username = username_attempt
        self.session_score = 0 # Yeni oturumda skoru sıfırla
        self.update_score_display()

        if not self.all_puzzles_data:
            messagebox.showerror("Hata", "Oynanacak bulmaca yok.")
            return

        random.shuffle(self.all_puzzles_data) # Her yeni oturumda bulmacaları karıştır
        self.current_puzzle_idx = -1 # İlk bulmaca için indeksi -1 yap

        self.login_frame.pack_forget()
        self.game_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.welcome_label.config(text=f"Hoş geldin, {self.username}!")
        self.process_next_puzzle() # İlk bulmacayı yükle

    def process_next_puzzle(self):
        self.current_puzzle_idx += 1
        if self.current_puzzle_idx >= len(self.all_puzzles_data):
            self.game_over()
            return
        self.load_puzzle_content()

    def load_puzzle_content(self):
        self.current_puzzle = self.all_puzzles_data[self.current_puzzle_idx]
        self.target_words = self.current_puzzle["words"]
        self.available_letters_counter = Counter(self.current_puzzle["letters"].upper())
        self.display_letters_str = self.current_puzzle["display_letters"]
        self.hint_used_this_puzzle = False # Yeni bulmacada ipucu hakkını yenile

        self.found_words.clear()
        self.listbox_words.delete(0, tk.END)
        self.entry_word.delete(0, tk.END)
        self.letters_label.config(text=f"Harfler: {self.display_letters_str}")
        self.status_label.config(text="Yeni bulmaca yüklendi. Kelime girin.", foreground="black")
        self.update_progress_label()
        self.entry_word.focus()

    def game_over(self):
        messagebox.showinfo("Oyun Bitti", f"Tüm bulmacaları tamamladınız!\n{self.username}, toplam puanınız: {self.session_score}")
        self.save_high_score(self.username, self.session_score)
        self.game_frame.pack_forget()
        self.login_frame.pack(pady=100, padx=20, fill="x", expand=True)

    def shuffle_display_letters(self):
        if self.current_puzzle:
            temp_list = list(self.current_puzzle["letters"].upper())
            random.shuffle(temp_list)
            self.display_letters_str = ", ".join(temp_list) # Karışık sırayı göster
            self.letters_label.config(text=f"Harfler: {self.display_letters_str}")

    def check_word(self):
        if not self.current_puzzle: return
        word = self.entry_word.get().strip().upper()

        if not word:
            self.set_status("Lütfen bir kelime girin.", "orange")
            return

        word_counter = Counter(word)
        valid_letters = True
        for char, count in word_counter.items():
            if self.available_letters_counter[char] < count:
                valid_letters = False
                break
        
        if not valid_letters:
            original_display_letters = self.current_puzzle["display_letters"]
            self.set_status(f"Geçersiz harf! Harfler: '{original_display_letters}'. Harf sayılarına dikkat edin.", "red")
            self.entry_word.delete(0, tk.END)
            return

        if word in self.target_words:
            if word in self.found_words:
                self.set_status(f"'{word}' zaten bulundu!", "blue")
            else:
                self.found_words.add(word)
                points_earned = len(word) * 10
                self.session_score += points_earned
                self.update_score_display()
                self.listbox_words.insert(tk.END, word)
                self.set_status(f"'{word}' bulundu! +{points_earned} puan", "green")
                self.update_progress_label()

                if len(self.found_words) == len(self.target_words):
                    self.set_status("Tebrikler! Bu bulmacadaki tüm kelimeleri buldunuz!", "green")
                    messagebox.showinfo("Bulmaca Tamamlandı!", "Harika iş! Sonraki bulmacaya geçiliyor.")
                    self.process_next_puzzle()
        else:
            self.set_status(f"'{word}' kelimesi listede yok veya yanlış.", "red")
        self.entry_word.delete(0, tk.END)

    def get_hint(self):
        if not self.current_puzzle or self.hint_used_this_puzzle:
            self.set_status("Bu bulmaca için ipucu hakkınızı kullandınız veya ipucu yok." if self.hint_used_this_puzzle else "İpucu için aktif bir bulmaca olmalı.", "orange")
            return

        unfound_words = list(self.target_words - self.found_words)
        if not unfound_words:
            self.set_status("Tüm kelimeler zaten bulundu!", "blue")
            return

        self.session_score -= HINT_PENALTY
        self.update_score_display()
        self.hint_used_this_puzzle = True

        hint_word = random.choice(unfound_words)
        hint_display = list("_" * len(hint_word))
        num_revealed = max(1, len(hint_word) // 3)
        indices_to_reveal = random.sample(range(len(hint_word)), num_revealed)
        for i in indices_to_reveal: hint_display[i] = hint_word[i]
        
        hint_text = f"İpucu (-{HINT_PENALTY}p): {' '.join(hint_display)} ({len(hint_word)} harf)"
        self.set_status(hint_text, "purple")

    def clear_entry(self):
        self.entry_word.delete(0, tk.END)
        self.entry_word.focus()

    def update_score_display(self):
        self.score_label.config(text=f"{self.session_score} ✨")

    def update_progress_label(self):
        if self.current_puzzle:
            total_target_words = len(self.target_words)
            found_count = len(self.found_words)
            self.progress_label.config(text=f"Bulunan: {found_count}/{total_target_words}")
        else:
            self.progress_label.config(text="Bulunan: 0/0")


    def set_status(self, message, color):
        self.status_label.config(text=message, foreground=color)

    def load_high_scores(self):
        try:
            with open(HIGH_SCORE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_high_score(self, username, score):
        scores = self.load_high_scores()
        
        # O anki tarihi ve saati alıp istediğimiz formatta bir metne dönüştürüyoruz
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M") 
        
        # Yeni skoru, oluşturduğumuz gerçek tarih bilgisiyle listeye ekliyoruz
        scores.append({"name": username, "score": score, "date": current_date}) 
        
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:10]
        try:
            with open(HIGH_SCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=4)
        except Exception as e:
            print(f"Yüksek skor kaydedilemedi: {e}")
            
    def show_high_scores(self):
        scores = self.load_high_scores()
        if not scores:
            messagebox.showinfo("Yüksek Skorlar", "Henüz kaydedilmiş bir skor yok.")
            return
        
        score_text = "🏆 Yüksek Skorlar 🏆\n\n"
        for i, entry in enumerate(scores):
            # Skoru ve tarihi birlikte gösteriyoruz
            score_text += f"{i+1}. {entry['name']}: {entry['score']} Puan ({entry.get('date', 'Tarih Yok')})\n"
        
        messagebox.showinfo("Yüksek Skorlar", score_text)

if __name__ == '__main__':
    root = tk.Tk()
    app = WordGameApp(root)
    root.mainloop()