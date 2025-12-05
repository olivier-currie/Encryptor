import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from core.enc_dec import encrypt, decrypt, add_history, get_history
from tkinter import PhotoImage
import os


class Dash(ttk.Frame):
    def __init__(self, parent, username, show_welcome, show_history):
        super().__init__(parent)
        self.username = username
        dashframe = ttk.Frame(self)
        dashframe.pack(fill="both", expand=True)
        self.user_icon = PhotoImage(file="assets/user.png")
        self.logout_icon = PhotoImage(file="assets/logout.png")
        self.history_icon = PhotoImage(file="assets/history.png")
        style = ttk.Style()
        style.configure("Navbar.TFrame", background="#2c3e50")
        navbar = ttk.Frame(dashframe, style="Navbar.TFrame", relief="raised", padding=(10, 15))
        navbar.pack(fill="x")
        container = ttk.Frame(dashframe, padding=20)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(5, weight=1)
        container.grid_columnconfigure(1, weight=1)
        user_label = ttk.Label(navbar, text=f"{self.username}", image=self.user_icon, compound="left", foreground="white", background="#2c3e50", font=("Segoe UI", 12))
        user_label.pack(side="left")

        logout_label = ttk.Label(navbar, text="Log out", image=self.logout_icon, compound="top", foreground="white", cursor="hand2", background="#2c3e50", font=("Segoe UI", 8))
        logout_label.pack(side="right")
        logout_label.bind("<Button-1>", show_welcome)
        
        history_label = ttk.Label(navbar, text="History", image=self.history_icon, compound="top", foreground="white", cursor="hand2", background="#2c3e50", font=("Segoe UI", 8))
        history_label.pack(side="right", padx=30)
        history_label.bind("<Button-1>", lambda e: show_history(username, get_history(self.username)))

        

        title = ttk.Label(container, text="Your dashboard",
                          font=("Segoe UI", 22))
        title.grid(row=0, column=0, pady=5)
        ttk.Label(container, text="File to encrypt/decrypt:", font=("Segoe UI", 16)).grid(row=1, column=0, sticky="e")
        self.input_entry = ttk.Entry(container, width=50)
        self.input_entry.grid(row=1, column=1)
        ttk.Button(container, text="Explore", command=self.select_input).grid(row=1, column=2)

        ttk.Label(container, text="Recipient of encryption/decryption", font=("Segoe UI", 16)).grid(row=2, column=0, sticky="e")
        self.output_entry = ttk.Entry(container, width=50)
        self.output_entry.grid(row=2, column=1)
        ttk.Button(container, text="Explore", command=self.select_output).grid(row=2, column=2)

        ttk.Label(container, text="Encryption password", font=("Segoe UI", 16)).grid(row=3, column=0, sticky="e")
        self.password_entry = ttk.Entry(container, width=50, show="*")
        self.password_entry.grid(row=3, column=1)

        encrypt_btn = ttk.Button(container, text="Encrypt", command=self.encrypt_action)
        encrypt_btn.grid(row=4, column=1, pady=10)

        decrypt_btn = ttk.Button(container, text="Decrypt", command=self.decrypt_action)
        decrypt_btn.grid(row=4, column=2, pady=10)

    def encrypt_action(self):
        try:
            password = self.password_entry.get()
            if not password:
                raise ValueError("Password cannot be empty")
            encrypt(self.input_entry.get(), self.output_entry.get(), password)
            add_history(self.username, os.path.basename(self.input_entry.get()), "Encrypted")
            messagebox.showinfo("Success! File encrypted")
            self.password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error: ", str(e))

    def decrypt_action(self):
        try:
            password = self.password_entry.get()
            if not password:
                raise ValueError("Password cannot be empty")
            decrypt(self.input_entry.get(), self.output_entry.get(), password)
            add_history(self.username, os.path.basename(self.input_entry.get()), "Decrypted")
            messagebox.showinfo("Success! File decrypted")
            self.password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error: ", str(e))

    def select_input(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def select_output(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)


