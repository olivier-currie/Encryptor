import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from core.enc_dec import encrypt, decrypt, add_history, get_history
from tkinter import PhotoImage
import os
from tkinter import BooleanVar
from ui.error_handling import error_message


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
        style.theme_use("clam")
        style.configure("Basic.TLabel", background="#181818", foreground="white")
        style.configure("LabelOnly.TCheckbutton", background="#181818", foreground="white")
        style.configure("Navbar.TFrame", background="#2c3e50")
        style.configure("Hover.TLabel", background="#23313F")
        style.configure("Base.TLabel", background="#2c3e50")
        style.configure("EncryptEntry.TEntry", fieldbackground="#181818", bordercolor="white", foreground="white", borderwidth=4, relief="ridge", padding=5)
        style.configure("Base.TButton", background="#181818", foreground="white", bordercolor="white", borderwidth=2, relief="ridge", font=("Segoe UI", 8))
        style.map("LabelOnly.TCheckbutton",
          background=[("active", "#181818"),
                      ("selected", "#181818"),
                      ("!active", "#181818")],
          foreground=[("active", "white"),
                      ("selected", "white"),
                      ("!active", "white")])
        style.map("Base.TButton",
          background=[("active", "darkgray"),
                      ("selected", "#darkgray"),
                      ("!active", "#181818")],
          foreground=[("active", "white"),
                      ("selected", "white"),
                      ("!active", "white")])
        navbar = ttk.Frame(dashframe, style="Navbar.TFrame", relief="raised", padding=(10, 15))
        navbar.pack(fill="x")
        def on_enter(e, l):
            l.config(style="Hover.TLabel")
        def on_leave(e, l):
            l.config(style="Base.TLabel")
        container = ttk.Frame(dashframe, padding=20)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(6, weight=1)
        container.grid_columnconfigure(1, weight=1)
        user_label = ttk.Label(navbar, text=f"{self.username}", image=self.user_icon, compound="left", foreground="white", style="Base.TLabel", font=("Segoe UI", 12))
        user_label.pack(side="left")

        logout_label = ttk.Label(navbar, text="Log out", image=self.logout_icon, compound="top", foreground="white", cursor="hand2", style="Base.TLabel", font=("Segoe UI", 8))
        logout_label.pack(side="right")
        logout_label.bind("<Button-1>", show_welcome)
        logout_label.bind("<Enter>", lambda e : on_enter(e, logout_label))
        logout_label.bind("<Leave>", lambda e : on_leave(e, logout_label))
        
        history_label = ttk.Label(navbar, text="History", image=self.history_icon, compound="top", foreground="white", cursor="hand2", style="Base.TLabel", font=("Segoe UI", 8))
        history_label.pack(side="right", padx=30)
        history_label.bind("<Button-1>", lambda e: show_history(username, get_history(self.username)))
        history_label.bind("<Enter>", lambda e : on_enter(e, history_label))
        history_label.bind("<Leave>", lambda e : on_leave(e, history_label))

        

        title = ttk.Label(container, text="Your dashboard",
                          font=("Segoe UI", 22), style="Basic.TLabel")
        title.grid(row=0, column=0, pady=5)
        ttk.Label(container, text="File to encrypt/decrypt:", font=("Segoe UI", 16), style="Basic.TLabel").grid(row=1, column=0, sticky="e")
        self.input_entry = ttk.Entry(container, width=50, style="EncryptEntry.TEntry")
        self.input_entry.grid(row=1, column=1)
        ttk.Button(container, text="Explore", command=self.select_input, style="Base.TButton").grid(row=1, column=2)

        ttk.Label(container, text="Recipient of encryption/decryption", font=("Segoe UI", 16), style="Basic.TLabel").grid(row=2, column=0, sticky="e")
        self.output_entry = ttk.Entry(container, width=50, style="EncryptEntry.TEntry")
        self.output_entry.grid(row=2, column=1)
        ttk.Button(container, text="Explore", command=self.select_output, style="Base.TButton").grid(row=2, column=2)

        ttk.Label(container, text="Encryption password", font=("Segoe UI", 16), style="Basic.TLabel").grid(row=3, column=0, sticky="e")
        self.password_entry = ttk.Entry(container, width=50, show="*", style="EncryptEntry.TEntry")
        self.password_entry.grid(row=3, column=1)

        show_var = BooleanVar(value=False)
        def toggle_password():
            if show_var.get():
                self.password_entry.config(show="")
            else:
                self.password_entry.config(show="*")
        show_checkbox = ttk.Checkbutton(container, text="Show password", variable=show_var, command=toggle_password, style="LabelOnly.TCheckbutton")
        show_checkbox.grid(row=4, column=1, pady=10)

        encrypt_btn = ttk.Button(container, text="Encrypt", command=self.encrypt_action, style="Base.TButton")
        encrypt_btn.grid(row=5, column=1, pady=10)

        decrypt_btn = ttk.Button(container, text="Decrypt", command=self.decrypt_action, style="Base.TButton")
        decrypt_btn.grid(row=5, column=2, pady=10)

    def encrypt_action(self):
        try:
            password = self.password_entry.get()
            if not password:
                error_message("Password Error", "Password cannot be empty.")
                return
            encrypt(self.input_entry.get(), self.output_entry.get(), password)
            add_history(self.username, os.path.basename(self.input_entry.get()), "Encrypted")
            error_message("Success!", "File encrypted")
            self.password_entry.delete(0, tk.END)
        except FileNotFoundError:
            error_message("File Error", "File not found.")
        except IsADirectoryError:
            error_message("File Error", "File cannot be a directory.")
        except PermissionError:
            error_message("Permission Error", "Cannot read/write file.")
        except ValueError as e:
            error_message("Encryption Error", str(e))
        except Exception as e:
            error_message("Unknown Error", str(e))

    def decrypt_action(self):
        try:
            password = self.password_entry.get()
            if not password:
                error_message("Password Error", "Password cannot be empty.")
                return
            decrypt(self.input_entry.get(), self.output_entry.get(), password)
            add_history(self.username, os.path.basename(self.input_entry.get()), "Decrypted")
            error_message("Success!", " File decrypted")
            self.password_entry.delete(0, tk.END)
        except FileNotFoundError:
            error_message("File Error", "File not found.")
        except IsADirectoryError:
            error_message("File Error", "File cannot be a directory.")
        except PermissionError:
            error_message("Permission Error", "Cannot read/write file.")
        except ValueError as e:
            error_message("Encryption Error", str(e))
        except Exception as e:
            error_message("Unknown Error", str(e))

    def select_input(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def select_output(self):
        input_file = self.input_entry.get()
        if not input_file:
            error_message("Input Error", "You need to select an input file first.")
            return
        
        _, ext = os.path.splitext(input_file)

        path = filedialog.asksaveasfilename()
        if path:
            if not path.lower().endswith(ext.lower()):
                path += ext

            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)


