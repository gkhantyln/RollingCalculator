import tkinter as tk
from tkinter import ttk
import configparser
import os

class RollingCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rolling Hesaplama")
        
        # Topmost özelliği
        self.root.wm_attributes("-topmost", 1)
        
        # Yeniden boyutlandırmayı iptal etme
        self.root.resizable(False, False)

        self.root.geometry("600x500")  # Pencere boyutunu biraz genişlettim
        self.root.configure(bg="#F0F0F0")

        self.betting_data = []  # Bahis verilerini saklar
        self.initial_balance = 0

        # Üst kısım - Giriş alanları
        top_frame = tk.Frame(self.root, bg="#F0F0F0", pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Max Tekil Oran:", bg="#F0F0F0").grid(row=0, column=0, padx=5, pady=5)
        self.odds_entry = tk.Entry(top_frame, width=8)  # Giriş kutularını küçülttüm
        self.odds_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Başlangıç Bahis Tutarı:", bg="#F0F0F0").grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(top_frame, width=8)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(top_frame, text="Başlangıç Kasa Tutarı:", bg="#F0F0F0").grid(row=1, column=0, padx=5, pady=5)
        self.balance_entry = tk.Entry(top_frame, width=8)
        self.balance_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Rolling Sayısı:", bg="#F0F0F0").grid(row=1, column=2, padx=5, pady=5)
        self.roll_count_entry = tk.Entry(top_frame, width=8)
        self.roll_count_entry.grid(row=1, column=3, padx=5, pady=5)

        # Seçenekler: Sabit veya %
        tk.Label(top_frame, text="Sabit/%:", bg="#F0F0F0").grid(row=2, column=0, padx=5, pady=5)
        self.option_var = tk.StringVar(value="Sabit")
        self.option_menu = ttk.Combobox(top_frame, textvariable=self.option_var, values=["Sabit", "%"], width=7)
        self.option_menu.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Değer:", bg="#F0F0F0").grid(row=2, column=2, padx=5, pady=5)
        self.option_value_entry = tk.Entry(top_frame, width=8)
        self.option_value_entry.grid(row=2, column=3, padx=5, pady=5)

        tk.Button(top_frame, text="Ekle", command=self.add_bets).grid(row=3, column=0, columnspan=4, padx=5, pady=10)

        # Stil ayarları yaparak tablo içeriklerini ortalıyoruz
        style = ttk.Style()
        style.configure("Treeview.Heading", anchor="center")  # Başlıkları ortala
        style.configure("Treeview", rowheight=25)  # Satır yüksekliği ayarla
        style.configure("Treeview", font=('Arial', 10))  # Yazı tipi ayarla

        # Alt kısım - Bahis tablosu
        self.table_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Sıra", "Bahis Oranı", "Bahis Tutarı", "Olası Kazanç", "Güncel Kasa", "Net Kar")
        self.treeview = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Sütun genişliklerini ayarlıyoruz
        self.treeview.column("Sıra", width=50, anchor="center")
        self.treeview.column("Bahis Oranı", width=80, anchor="center")
        self.treeview.column("Bahis Tutarı", width=100, anchor="center")
        self.treeview.column("Olası Kazanç", width=100, anchor="center")
        self.treeview.column("Güncel Kasa", width=100, anchor="center")
        self.treeview.column("Net Kar", width=100, anchor="center")

        self.treeview.heading("Sıra", text="Sıra")
        self.treeview.heading("Bahis Oranı", text="Bahis Oranı")
        self.treeview.heading("Bahis Tutarı", text="Bahis Tutarı")
        self.treeview.heading("Olası Kazanç", text="Olası Kazanç")
        self.treeview.heading("Güncel Kasa", text="Güncel Kasa")
        self.treeview.heading("Net Kar", text="Net Kar")

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Butonlar
        button_frame = tk.Frame(self.root, bg="#F0F0F0", pady=10)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Temizle", command=self.clear_bets).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="Rapor Kaydet", command=self.save_report).grid(row=0, column=4, padx=5, pady=5)

        # Dosyadan okuma işlemi
        self.load_report()

    def add_bets(self):
        """Rolling aşamalarını otomatik olarak ekler."""
        try:
            odds = float(self.odds_entry.get())
            initial_amount = float(self.amount_entry.get())
            self.initial_balance = float(self.balance_entry.get())
            roll_count = int(self.roll_count_entry.get())
            option_type = self.option_var.get()
            option_value = float(self.option_value_entry.get())

            self.betting_data = []  # Önceki bahis verilerini temizle

            current_balance = self.initial_balance
            amount = initial_amount

            for i in range(roll_count):
                possible_win = amount * odds
                new_balance = current_balance - amount + possible_win  # Kaybetme ve kazanma hesaplama
                net_profit = new_balance - self.initial_balance  # Net kar hesaplama

                self.betting_data.append({
                    "sequence": i + 1,
                    "odds": odds,
                    "amount": amount,
                    "possible_win": possible_win,
                    "current_balance": new_balance,
                    "net_profit": net_profit
                })

                # Bahis tutarını belirle - sabit veya %'lik değer ile
                if option_type == "Sabit":
                    amount = new_balance / option_value
                elif option_type == "%":
                    amount = (new_balance * option_value) / 100

                current_balance = new_balance  # Güncel kasa güncellenir

            self.update_table()

        except ValueError:
            pass  # Geçersiz girişleri göz ardı ederiz

    def update_table(self):
        """Bahis tablosunu günceller."""
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        for bet in self.betting_data:
            self.treeview.insert("", tk.END, values=(
                f"{bet['sequence']}", 
                f"{bet['odds']:.2f}", 
                f"{bet['amount']:.2f}", 
                f"{bet['possible_win']:.2f}", 
                f"{bet['current_balance']:.2f}",
                f"{bet['net_profit']:.2f}"
            ))

    def clear_bets(self):
        """Bahis listesini temizler."""
        self.betting_data.clear()
        self.update_table()

    def save_report(self):
        """Girilen değerleri ve tabloyu INI dosyasına kaydeder."""
        config = configparser.ConfigParser(interpolation=None)  # Interpolation'ı kapat

        # Girilen değerleri kaydet
        config['Settings'] = {
            'Odds': self.odds_entry.get(),
            'InitialAmount': self.amount_entry.get(),
            'InitialBalance': self.balance_entry.get(),
            'RollCount': self.roll_count_entry.get(),
            'OptionType': self.option_var.get(),
            'OptionValue': self.option_value_entry.get()
        }

        # Tablo verilerini kaydet
        if not self.betting_data:
            return

        config['Bets'] = {}
        for i, bet in enumerate(self.betting_data):
            config['Bets'][f'Bet{i+1}_Sequence'] = str(bet['sequence'])
            config['Bets'][f'Bet{i+1}_Odds'] = f"{bet['odds']:.2f}"
            config['Bets'][f'Bet{i+1}_Amount'] = f"{bet['amount']:.2f}"
            config['Bets'][f'Bet{i+1}_PossibleWin'] = f"{bet['possible_win']:.2f}"
            config['Bets'][f'Bet{i+1}_CurrentBalance'] = f"{bet['current_balance']:.2f}"
            config['Bets'][f'Bet{i+1}_NetProfit'] = f"{bet['net_profit']:.2f}"

        with open("conf_log.ini", "w") as configfile:
            config.write(configfile)

    def load_report(self):
        """Daha önce kaydedilmiş verileri yükler."""
        if not os.path.exists("conf_log.ini"):
            return

        config = configparser.ConfigParser(interpolation=None)
        config.read("conf_log.ini")

        # Girilen değerleri yükle
        if 'Settings' in config:
            self.odds_entry.insert(0, config['Settings'].get('Odds', ''))
            self.amount_entry.insert(0, config['Settings'].get('InitialAmount', ''))
            self.balance_entry.insert(0, config['Settings'].get('InitialBalance', ''))
            self.roll_count_entry.insert(0, config['Settings'].get('RollCount', ''))
            self.option_var.set(config['Settings'].get('OptionType', 'Sabit'))
            self.option_value_entry.insert(0, config['Settings'].get('OptionValue', ''))

        # Tablo verilerini yükle
        if 'Bets' in config:
            self.betting_data = []
            i = 1
            while f'Bet{i}_Sequence' in config['Bets']:
                bet = {
                    "sequence": int(config['Bets'][f'Bet{i}_Sequence']),
                    "odds": float(config['Bets'][f'Bet{i}_Odds']),
                    "amount": float(config['Bets'][f'Bet{i}_Amount']),
                    "possible_win": float(config['Bets'][f'Bet{i}_PossibleWin']),
                    "current_balance": float(config['Bets'][f'Bet{i}_CurrentBalance']),
                    "net_profit": float(config['Bets'][f'Bet{i}_NetProfit'])
                }
                self.betting_data.append(bet)
                i += 1
            self.update_table()

# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = RollingCalculatorApp(root)
    root.mainloop()
