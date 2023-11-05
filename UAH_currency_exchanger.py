import tkinter as tk
from tkinter import ttk, font, messagebox
import requests

url = ""
resource = ""
USD_currency = 0.0
EUR_currency = 0.0
GBP_currency = 0.0
PLN_currency = 0.0
try:
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    resource = requests.get(url, timeout=10)
    if resource.status_code != 200:
        raise requests.ConnectionError
    else:
        response = resource.json()
        USD_currency = [item for item in response if item['cc'] == 'USD'][0]['rate']
        EUR_currency = [item for item in response if item['cc'] == 'EUR'][0]['rate']
        GBP_currency = [item for item in response if item['cc'] == 'GBP'][0]['rate']
        PLN_currency = [item for item in response if item['cc'] == 'PLN'][0]['rate']
except requests.ConnectionError:
    messagebox.showerror("Помилка з'єднання",
                         "Не вдалося підключитися до ресурсу НБУ. Перевірте підключення до інтернету.")
    quit(9)


def submit():
    try:
        value = float(entry_field.get())
        currency = combobox.get()
        if currency == "$":
            result = value / USD_currency
            result_label.config(text=f"Result: {result:.2f} $")
        elif currency == "€":
            result = value / EUR_currency
            result_label.config(text=f"Result: {result:.2f} €")
        elif currency == "£":
            result = value / GBP_currency
            result_label.config(text=f"Result: {result:.2f} £")
        elif currency == "zł":
            result = value / PLN_currency
            result_label.config(text=f"Result: {result:.2f} zł")
    except ValueError:
        messagebox.showerror("Помилка вводу", "Будь ласка, введіть коректну суму числом.")


root = tk.Tk()
root.title("Currency converter")
root.configure(bg='grey')
root.resizable(False, False)
root.geometry("600x450")

preferred_font = "Times New Roman"
if "Helvetica" in font.families():
    preferred_font = "Helvetica"

style = ttk.Style()
style.theme_use('alt')

style.configure('Submit.TButton', font=(preferred_font, 20), borderwidth=0)
style.map('Submit.TButton',
          foreground=[('active', 'black'), ('pressed', 'red'), ('!disabled', 'black')],
          background=[('active', 'white'), ('pressed', '!disabled', 'grey'), ('!disabled', 'white')])

style.configure('Main.TLabel', font=(preferred_font, 40, "bold"), background='grey', foreground='white')
style.configure('Secondary.TLabel', font=(preferred_font, 15), background='grey', foreground='white')
style.configure('EntryField.TEntry', font=(preferred_font, 20), fieldbackground='white', foreground='black',
                insertbackground='black')
style.configure('Currency.TCombobox', font=(preferred_font, 20))
style.configure('Currency.TFrame', foreground='black', background='grey')

main_label = ttk.Label(root, text="Currency UAH converter", style='Main.TLabel')
input_label = ttk.Label(root, text="Input amount of money in ₴", style='Secondary.TLabel')
entry_field = ttk.Entry(root, style='EntryField.TEntry')
currency_frame = ttk.Frame(root, style='Currency.TFrame')
pick_currency_label = ttk.Label(currency_frame, text="Choose currency:", style='Secondary.TLabel')
combobox = ttk.Combobox(currency_frame, values=["$", "€", "£", "zł"], style='Currency.TCombobox')

combobox.set("$")
submit_button = ttk.Button(root, text="Submit", style='Submit.TButton')
submit_button.config(command=submit)
result_label = ttk.Label(root, text="Result:", style='Main.TLabel')

main_label.pack(pady=(10, 70))
input_label.pack(pady=(10, 0))
entry_field.pack(pady=(0, 10))
currency_frame.pack(pady=(20, 20))
pick_currency_label.pack(side="left")
combobox.pack(side="left", padx=(5, 0))
submit_button.pack(pady=(10, 5))
result_label.pack(pady=(40, 30))

root.mainloop()