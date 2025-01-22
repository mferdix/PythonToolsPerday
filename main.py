import tkinter as tk
import subprocess

# Membuat jendela utama dengan judul
window = tk.Tk()
window.title("Senjata Rahasia Perday v1.21.3")
window.geometry("500x400")

# Membuat label peringatan
label_peringatan = tk.Label(window, text="Gunakan Senjata ini dengan Bijak", font=("Helvetica", 12, "bold"))
label_peringatan.pack()

# Fungsi untuk menjalankan file Python
def jalankan_file(file_path):
    subprocess.Popen(["python", file_path])

# Membuat tombol-tombol dengan margin atas, bawah, kiri, dan kanan
tombol1 = tk.Button(window, text="PDF Merged", width=25, height=2, padx=50, pady=15, command=lambda: jalankan_file("Tools/PDF-Merge.py"))
tombol2 = tk.Button(window, text="HTML Table 2 CSV", width=25, height=2, padx=50, pady=15, command=lambda: jalankan_file("Tools/HTML-Table2CSV.py"))
tombol3 = tk.Button(window, text="JSON 2 CSV", width=25, height=2, padx=50, pady=15, command=lambda: jalankan_file("Tools/JSON2CSV.py"))
tombol4 = tk.Button(window, text="Hand Tracket Cursor", width=25, height=2, padx=50, pady=15, command=lambda: jalankan_file("Tools/mouse-movement-using-hand.py"))
tombol5 = tk.Button(window, text="PDF Signature", width=25, height=2, padx=50, pady=15, command=lambda: jalankan_file("Tools/PDF-Sign.py"))

tombol_keluar = tk.Button(window, text="Keluar", width=25, height=2, padx=20, pady=15, command=window.destroy)

# Menempatkan tombol-tombol dalam jendela
tombol1.pack()
tombol2.pack()
tombol3.pack()
tombol4.pack()
tombol5.pack()
tombol_keluar.pack(side=tk.BOTTOM)

# Menjalankan jendela
window.mainloop()