import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class SignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Signature App")
        self.signature = None
        self.signature_image = None
        self.x = 100  # Initial x position for the signature
        self.y = 100  # Initial y position for the signature
        self.width = 100  # Initial width for the signature
        self.height = 50  # Initial height for the signature
        self.is_resizing = False  # Flag to track resizing state
        self.resize_margin = 10  # Margin for resizing the signature

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        # Buttons to open PDF, add signature, and save
        self.open_pdf_button = tk.Button(self.root, text="Open PDF", command=self.open_pdf)
        self.open_pdf_button.pack(side=tk.LEFT)

        self.add_signature_button = tk.Button(self.root, text="Add Signature", command=self.add_signature)
        self.add_signature_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.root, text="Save PDF", command=self.save_pdf)
        self.save_button.pack(side=tk.LEFT)

        self.canvas.bind("<B1-Motion>", self.move_signature)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Enter>", self.on_enter)

    def open_pdf(self):
        # Allow the user to select a PDF file
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.display_pdf(self.pdf_path)

    def display_pdf(self, pdf_path):
        # Use PyMuPDF to open the PDF and convert the first page to an image
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # First page (0-indexed)
        
        # Render the page as a pixmap (image)
        pix = page.get_pixmap()

        # Convert the pixmap to a PIL image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Resize the image to fit the canvas (optional)
        img = img.resize((600, 400))

        # Convert the image to a format that Tkinter can display
        self.pdf_image = ImageTk.PhotoImage(img)

        # Display the image on the tkinter canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pdf_image)

    def add_signature(self):
        # Open a dialog to select the signature image
        self.signature_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        self.signature = Image.open(self.signature_path)

        # Create a PhotoImage object for tkinter
        self.signature_image = ImageTk.PhotoImage(self.signature)
        self.signature_id = self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.signature_image)

        # Create a resize handle
        self.create_resize_handle()

    def create_resize_handle(self):
        # Remove any existing resize handle
        self.canvas.delete("resize_handle")
        
        # Draw the resize handle (a small circle) at the bottom-right corner
        self.resize_handle = self.canvas.create_oval(
            self.x + self.width - self.resize_margin,
            self.y + self.height - self.resize_margin,
            self.x + self.width + self.resize_margin,
            self.y + self.height + self.resize_margin,
            fill="blue", tags="resize_handle"
        )

    def move_signature(self, event):
        if not self.is_resizing:
            # Move the signature image when the mouse is dragged
            self.x = event.x
            self.y = event.y

            # Redraw the canvas with the new position
            self.canvas.coords(self.signature_id, self.x, self.y)

            # Move the resize handle along with the signature
            self.create_resize_handle()

    def on_press(self, event):
        # Check if the click is near the bottom-right corner of the signature
        if (self.x + self.width - self.resize_margin < event.x < self.x + self.width + self.resize_margin and
            self.y + self.height - self.resize_margin < event.y < self.y + self.height + self.resize_margin):
            self.is_resizing = True
            self.initial_x = event.x
            self.initial_y = event.y
            self.initial_width = self.width
            self.initial_height = self.height

    def on_release(self, event):
        # Release the resizing flag when the mouse is released
        self.is_resizing = False

    def on_enter(self, event):
        # Change cursor to indicate resizing when hovering near the resize handle
        if (self.x + self.width - self.resize_margin < event.x < self.x + self.width + self.resize_margin and
            self.y + self.height - self.resize_margin < event.y < self.y + self.height + self.resize_margin):
            self.root.config(cursor="se-resize")  # Change cursor to resize icon
        else:
            self.root.config(cursor="arrow")  # Reset cursor to default

    def resize_signature(self, event):
        if self.is_resizing:
            # Calculate the change in the cursor position
            delta_x = event.x - self.initial_x
            delta_y = event.y - self.initial_y

            # Update the width and height based on the movement
            self.width = self.initial_width + delta_x
            self.height = self.initial_height + delta_y

            # Prevent the signature from becoming too small
            if self.width < 10: self.width = 10
            if self.height < 10: self.height = 10

            # Resize the signature image
            resized_signature = self.signature.resize((self.width, self.height))
            self.signature_image = ImageTk.PhotoImage(resized_signature)

            # Update the signature on the canvas
            self.canvas.itemconfig(self.signature_id, image=self.signature_image)

            # Move the resize handle along with the resized signature
            self.create_resize_handle()

    def save_pdf(self):
        # Combine the PDF and the signature to save a new file
        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        # Read the input PDF
        reader = PdfReader(self.pdf_path)
        writer = PdfWriter()

        # Create a new canvas for the signature to overlay onto the PDF
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(600, 400))
        c.drawImage(self.signature_path, self.x, self.y, width=self.width, height=self.height)
        c.save()

        packet.seek(0)
        signature_pdf = PdfReader(packet)

        # Merge the signature onto the first page
        page = reader.pages[0]
        page.merge_page(signature_pdf.pages[0])

        # Add the remaining pages without modification
        for page_num in range(1, len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Save the output PDF
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"PDF saved as {output_pdf_path}")

# Initialize the tkinter window
root = tk.Tk()
app = SignatureApp(root)
root.mainloop()
