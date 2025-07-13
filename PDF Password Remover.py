import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from ttkthemes import ThemedTk
from PyPDF2 import PdfReader, PdfWriter
import subprocess

def remove_pdf_password():
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not pdf_path:
        return

    # Try to open the PDF
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open PDF: {e}")
        return

    # If encrypted, ask for password
    if reader.is_encrypted:
        pwd = simpledialog.askstring("PDF Password", "Enter PDF password:", show="*")
        if not pwd:
            messagebox.showinfo("Cancelled", "No password entered. Aborting.")
            return
        try:
            result = reader.decrypt(pwd)
            if result == 0:
                messagebox.showerror("Error", "Wrong password. Cannot decrypt PDF.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")
            return

    # Create output folder
    folder = os.path.dirname(pdf_path)
    output_folder = os.path.join(folder, "Without Password")
    os.makedirs(output_folder, exist_ok=True)

    # Write decrypted PDF
    output_path = os.path.join(output_folder, os.path.basename(pdf_path))
    try:
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write PDF: {e}")
        return

    # Show success
    messagebox.showinfo("Success", f"Unlocked PDF saved to:\n{output_path}")

    # Open the folder
    subprocess.Popen(f'explorer "{output_folder}"')

    # Close window
    root.quit()

# GUI setup
root = ThemedTk(theme="arc")
root.title("PDF Password Remover")
root.geometry("400x200")
root.resizable(False, False)

label = ttk.Label(root, text="Click below to select a PDF to unlock:", font=("Helvetica", 12))
label.pack(pady=30)

btn = ttk.Button(root, text="Select PDF & Unlock", command=remove_pdf_password)
btn.pack(pady=10)

root.mainloop()
