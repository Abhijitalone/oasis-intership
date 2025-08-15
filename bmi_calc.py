import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
import datetime

# --- Enhanced Style Constants ---
PRIMARY_BG = "#f4f9fd"
FRAME_BG = "#ffffff"
BUTTON_BG = "#5c8df6"
BUTTON_ACTIVE = "#3c6fe0"
ENTRY_BG = "#ffffff"
LABEL_FONT = ('Segoe UI', 11)
LABEL_BOLD_FONT = ('Segoe UI', 13, 'bold')
BUTTON_FONT = ('Segoe UI', 11, 'bold')

# --- Database Setup ---
conn = sqlite3.connect('bmi_users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS bmi_data (
                user_id INTEGER,
                date TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                FOREIGN KEY(user_id) REFERENCES users(id))''')
conn.commit()

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.configure(bg=PRIMARY_BG)
        self.selected_user_id = None
        self.beautify_ui()
        self.setup_ui()

    def beautify_ui(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TLabelframe', background=FRAME_BG, borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label', background=FRAME_BG, foreground='#274c77', font=LABEL_BOLD_FONT)
        style.configure('TLabel', background=FRAME_BG, foreground='#333', font=LABEL_FONT)
        style.configure('TEntry', fieldbackground=ENTRY_BG, font=LABEL_FONT, padding=5)
        style.configure('TCombobox', fieldbackground=ENTRY_BG, padding=5, font=LABEL_FONT)
        style.map('TCombobox', fieldbackground=[('readonly', ENTRY_BG)])
        style.configure('TButton', background=BUTTON_BG, foreground='white', font=BUTTON_FONT, padding=6)
        style.map('TButton',
                  background=[('active', BUTTON_ACTIVE)],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    def setup_ui(self):
        # User Selection
        self.user_frame = ttk.LabelFrame(self.root, text="User", style='TLabelframe')
        self.user_frame.pack(fill="x", expand=False, padx=20, pady=(20, 10))
        ttk.Label(self.user_frame, text="Select User:", style='TLabel').pack(side="left", padx=10, pady=10)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(self.user_frame, textvariable=self.user_var, state='readonly', font=LABEL_FONT)
        self.user_combo.pack(side="left", padx=5, pady=10)
        self.refresh_user_list()
        ttk.Button(self.user_frame, text="New User", command=self.new_user_window, style='TButton').pack(side="left", padx=12, pady=10, ipadx=4, ipady=2)

        # Input Section
        self.input_frame = ttk.LabelFrame(self.root, text="BMI Input", style='TLabelframe')
        self.input_frame.pack(fill="x", expand=False, padx=20, pady=(5, 15))
        ttk.Label(self.input_frame, text="Weight (kg):", style='TLabel').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.weight_entry = ttk.Entry(self.input_frame, font=LABEL_FONT)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.input_frame, text="Height (cm):", style='TLabel').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.height_entry = ttk.Entry(self.input_frame, font=LABEL_FONT)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.input_frame, text="Calculate BMI", command=self.calculate_bmi, style='TButton').grid(
            row=2, column=0, columnspan=2, pady=12, ipadx=5, ipady=2)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=2)

        # Result display
        self.result_label = ttk.Label(self.root, text="BMI: --", style='TLabel')
        self.result_label.pack(pady=(0, 10))

        # Extra Buttons
        buttons_frame = tk.Frame(self.root, bg=PRIMARY_BG)
        buttons_frame.pack(pady=(0, 15), fill="x")
        ttk.Button(buttons_frame, text="Show History", command=self.show_history, style='TButton').pack(
            side="left", padx=20, pady=4, ipadx=5, ipady=2)
        ttk.Button(buttons_frame, text="Show BMI Trend", command=self.plot_bmi_trend, style='TButton').pack(
            side="left", padx=20, pady=4, ipadx=5, ipady=2)

    def refresh_user_list(self):
        c.execute("SELECT name FROM users")
        users = [row[0] for row in c.fetchall()]
        self.user_combo['values'] = users

    def new_user_window(self):
        popup = tk.Toplevel(self.root)
        popup.title("New User")
        popup.configure(bg=FRAME_BG)
        ttk.Label(popup, text="Username:", style='TLabel').pack(side="left", padx=10, pady=15)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(popup, textvariable=name_var, font=LABEL_FONT)
        name_entry.pack(side="left", padx=10, pady=15)

        def add_user():
            name = name_var.get().strip()
            if name:
                try:
                    c.execute("INSERT INTO users (name) VALUES (?)", (name,))
                    conn.commit()
                except sqlite3.IntegrityError:
                    messagebox.showerror("User Exists", "This user already exists.")
                    return
                popup.destroy()
                self.refresh_user_list()

        ttk.Button(popup, text="Add", command=add_user, style='TButton').pack(side="left", padx=10, pady=15)

    def calculate_bmi(self):
        username = self.user_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Select a user.")
            return
        c.execute("SELECT id FROM users WHERE name=?", (username,))
        user = c.fetchone()
        if not user:
            messagebox.showerror("User Error", "User not found!")
            return
        self.selected_user_id = user[0]
        try:
            weight = float(self.weight_entry.get())
            height_cm = float(self.height_entry.get())
            if weight <= 0 or height_cm <= 0:
                raise ValueError("Enter positive values.")
            height_m = height_cm / 100.0
            bmi = weight / (height_m ** 2)
            self.result_label['text'] = f"BMI: {bmi:.2f}"
            date_str = str(datetime.date.today())
            c.execute("INSERT INTO bmi_data (user_id, date, weight, height, bmi) VALUES (?, ?, ?, ?, ?)",
                      (self.selected_user_id, date_str, weight, height_cm, bmi))
            conn.commit()
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.\n" + str(e))

    def show_history(self):
        if not self.selected_user_id:
            messagebox.showerror("Error", "No user selected!")
            return
        c.execute("SELECT date, weight, height, bmi FROM bmi_data WHERE user_id=? ORDER BY date", (self.selected_user_id,))
        records = c.fetchall()
        win = tk.Toplevel(self.root)
        win.title("BMI History")
        win.configure(bg=FRAME_BG)
        cols = ["Date", "Weight (kg)", "Height (cm)", "BMI"]
        tree = ttk.Treeview(win, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', minwidth=0, width=120)
        for row in records:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, padx=15, pady=15)
        if records:
            av_bmi = sum([r[3] for r in records]) / len(records)
            max_bmi = max([r[3] for r in records])
            min_bmi = min([r[3] for r in records])
            stats = f"Average BMI: {av_bmi:.2f}, Min: {min_bmi:.2f}, Max: {max_bmi:.2f}"
            ttk.Label(win, text=stats, font=('Segoe UI', 11, 'italic'), background=FRAME_BG).pack(pady=5)
        else:
            ttk.Label(win, text="No BMI records yet.", font=('Segoe UI', 11, 'italic'), background=FRAME_BG).pack(pady=10)

    def plot_bmi_trend(self):
        if not self.selected_user_id:
            messagebox.showerror("Error", "No user selected!")
            return
        c.execute("SELECT date, bmi FROM bmi_data WHERE user_id=? ORDER BY date", (self.selected_user_id,))
        data = c.fetchall()
        if not data:
            messagebox.showinfo("No Data", "No BMI data yet.")
            return
        dates, bmis = zip(*data)
        plt.figure(figsize=(7, 4))
        plt.plot(dates, bmis, marker='o', color='#3972b8', linewidth=2.1)
        plt.title("BMI Trend Over Time", fontsize=14, color='#255499')
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("BMI", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(alpha=0.4)
        plt.tight_layout()
        plt.show()

# --- Launch ---
root = tk.Tk()
app = BMICalculator(root)
root.mainloop()
