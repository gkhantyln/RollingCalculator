import tkinter as tk
from tkinter import ttk
import configparser
import os

class RollingCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rolling Hesaplama")
        self.root.geometry("600x600")
        self.root.configure(bg="#F0F0F0")

        self.betting_data = []  # Bahis verilerini saklar
        self.initial_balance = 0

        # Üst kısım - Giriş alanları
        top_frame = tk.Frame(self.root, bg="#F0F0F0", pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Oran:", bg="#F0F0F0").grid(row=0, column=0, padx=5, pady=5)
        self.odds_entry = tk.Entry(top_frame)
        self.odds_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Başlangıç Bahis Tutarı:", bg="#F0F0F0").grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(top_frame)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(top_frame, text="Başlangıç Kasa:", bg="#F0F0F0").grid(row=1, column=0, padx=5, pady=5)
        self.balance_entry = tk.Entry(top_frame)
        self.balance_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Rolling Sayısı:", bg="#F0F0F0").grid(row=1, column=2, padx=5, pady=5)
        self.roll_count_entry = tk.Entry(top_frame)
        self.roll_count_entry.grid(row=1, column=3, padx=5, pady=5)

        # Seçenekler: Sabit veya %
        tk.Label(top_frame, text="Sabit/%:", bg="#F0F0F0").grid(row=2, column=0, padx=5, pady=5)
        self.option_var = tk.StringVar(value="Sabit")
        self.option_menu = ttk.Combobox(top_frame, textvariable=self.option_var, values=["Sabit", "%"])
        self.option_menu.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Değer:", bg="#F0F0F0").grid(row=2, column=2, padx=5, pady=5)
        self.option_value_entry = tk.Entry(top_frame)
        self.option_value_entry.grid(row=2, column=3, padx=5, pady=5)

        tk.Button(top_frame, text="Ekle", command=self.add_bets).grid(row=3, column=0, columnspan=4, padx=5, pady=10)

        # Alt kısım - Bahis tablosu
        self.table_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Sıra", "Bahis Oranı", "Bahis Tutarı", "Olası Kazanç", "Güncel Kasa")
        self.treeview = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.treeview.heading("Sıra", text="Sıra")
        self.treeview.heading("Bahis Oranı", text="Bahis Oranı")
        self.treeview.heading("Bahis Tutarı", text="Bahis Tutarı")
        self.treeview.heading("Olası Kazanç", text="Olası Kazanç")
        self.treeview.heading("Güncel Kasa", text="Güncel Kasa")

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

                self.betting_data.append({
                    "sequence": i + 1,
                    "odds": odds,
                    "amount": amount,
                    "possible_win": possible_win,
                    "current_balance": new_balance
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
                f"{bet['current_balance']:.2f}"
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
            config['Bets'][f'Bet{i+1}_Odds'] = str(bet['odds'])
            config['Bets'][f'Bet{i+1}_Amount'] = str(bet['amount'])
            config['Bets'][f'Bet{i+1}_PossibleWin'] = str(bet['possible_win'])
            config['Bets'][f'Bet{i+1}_CurrentBalance'] = str(bet['current_balance'])

        with open('conf_log.ini', 'w') as configfile:
            config.write(configfile)


    def load_report(self):
        """INI dosyasından değerleri yükler ve uygulamaya uygular."""
        config = configparser.ConfigParser(interpolation=None)  # Interpolation'ı kapat

        if not os.path.exists('conf_log.ini'):
            return

        config.read('conf_log.ini')

        settings = config['Settings']
        self.odds_entry.insert(0, settings.get('Odds', ''))
        self.amount_entry.insert(0, settings.get('InitialAmount', ''))
        self.balance_entry.insert(0, settings.get('InitialBalance', ''))
        self.roll_count_entry.insert(0, settings.get('RollCount', ''))
        self.option_var.set(settings.get('OptionType', 'Sabit'))
        self.option_value_entry.insert(0, settings.get('OptionValue', ''))

        bets = config['Bets']
        self.betting_data = []
        for i in range(len(bets) // 5):  # Assuming there are 5 keys per bet
            bet = {
                'sequence': int(bets.get(f'Bet{i+1}_Sequence', 0)),
                'odds': float(bets.get(f'Bet{i+1}_Odds', 0)),
                'amount': float(bets.get(f'Bet{i+1}_Amount', 0)),
                'possible_win': float(bets.get(f'Bet{i+1}_PossibleWin', 0)),
                'current_balance': float(bets.get(f'Bet{i+1}_CurrentBalance', 0))
            }
            self.betting_data.append(bet)
        self.update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = RollingCalculatorApp(root)
    root.mainloop()
