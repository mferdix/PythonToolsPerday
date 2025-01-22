import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger

def add_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    for path in file_paths:
        if path not in file_list:
            file_list.append(path)
            file_listbox.insert(tk.END, path)

def remove_file():
    selected_index = file_listbox.curselection()
    if selected_index:
        file_list.pop(selected_index[0])
        file_listbox.delete(selected_index)

def merge_pdfs():
    if not file_list:
        return

    merger = PdfMerger()
    for path in file_list:
        merger.append(path)

    output_path = filedialog.asksaveasfilename(defaultextension=".pdf")
    merger.write(output_path)
    merger.close()

    # Use tkinter.messagebox for pop-up messages
    tk.messagebox.showinfo("Sukses", "File PDF berhasil digabung!")

# List to store file paths
file_list = []

# Create the main window with increased size
root = tk.Tk()
root.title("Penggabung PDF")
root.geometry("600x400")  # Adjust width and height as needed

# Listbox to display selected files with increased size
file_listbox = tk.Listbox(root, width=50, height=15)  # Adjust width and height as needed
file_listbox.pack()

# Buttons with increased size
button_width = 20
button_height = 2

add_button = tk.Button(root, text="Tambah File", command=add_files, width=button_width, height=button_height)
add_button.pack()

remove_button = tk.Button(root, text="Hapus File", command=remove_file, width=button_width, height=button_height)
remove_button.pack()

merge_button = tk.Button(root, text="Gabungkan PDF", command=merge_pdfs, width=button_width, height=button_height)
merge_button.pack()

# Run the main loop
root.mainloop()