import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from bs4 import BeautifulSoup
import csv

def extract_table_data(html_content):
    """
    Mengambil dan mem-parsing data dari tabel HTML.
    Mengembalikan semua data dalam bentuk list of dictionaries.
    """
    # Parsing halaman dengan BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Temukan tabel pertama di halaman (sesuaikan dengan kebutuhan)
    table = soup.find("table")  # Ambil tabel pertama yang ditemukan

    if not table:
        print("Tidak ada tabel ditemukan.")
        return []

    # Ambil header tabel
    headers = [header.text for header in table.find_all("th")]

    # Ambil semua baris data
    rows = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) == len(headers):
            rows.append({headers[i]: cells[i].text for i in range(len(headers))})

    return rows

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            data = extract_table_data(html_content)
            if data:
                save_to_csv(data)
            else:
                messagebox.showerror("Error", "Gagal mengonversi tabel dari file HTML.")

def save_to_csv(data):
    if not data:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Success", "Berhasil mengonversi tabel ke file CSV.")
    else:
        messagebox.showerror("Error", "Gagal menyimpan file CSV.")

def convert_from_textbox(textbox):
    html_content = textbox.get("1.0", tk.END)
    data = extract_table_data(html_content)
    if data:
        save_to_csv(data)
    else:
        messagebox.showerror("Error", "Gagal mengonversi tabel dari input HTML.")

def main():
    root = tk.Tk()
    root.title("HTML Table to CSV Converter")

    tk.Label(root, text="Pilih file HTML:").pack(pady=10)
    tk.Button(root, text="Buka File", command=open_file).pack(pady=5)

    tk.Label(root, text="Atau masukkan HTML di bawah ini:").pack(pady=10)
    textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    textbox.pack(pady=5)

    tk.Button(root, text="Konversi dari Textbox", command=lambda: convert_from_textbox(textbox)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()