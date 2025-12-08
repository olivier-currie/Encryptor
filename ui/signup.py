from tkinter import ttk
from core.auth import send_email_verif
import random
from tkinter import messagebox, BooleanVar
import threading
import re

class Signup(ttk.Frame):
    def __init__(self, parent, show_welcome, show_login, show_emailverif):
        super().__init__(parent)

        self.emailveriffunc = show_emailverif

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)

        title = ttk.Label(container, text="Sign Up",
                          font=("Segoe UI", 22))
        title.pack(pady=5)

        user_label = ttk.Label(container, text="Username:", font=("Segoe UI", 12))
        user_label.pack(pady=5)
        username_entry = ttk.Entry(container, width=50)
        username_entry.pack()
        email_label = ttk.Label(container, text="E-Mail:", font=("Segoe UI", 12))
        email_label.pack(pady=5)
        email_entry = ttk.Entry(container, width=50)
        email_entry.pack()
        pass_label = ttk.Label(container, text="Password:", font=("Segoe UI", 12))
        pass_label.pack(pady=5)
        password_entry = ttk.Entry(container, width=50, show="*")
        password_entry.pack()
        conf_label = ttk.Label(container, text="Confirm password:", font=("Segoe UI", 12))
        conf_label.pack(pady=5)
        conf_entry = ttk.Entry(container, width=50, show="*")
        conf_entry.pack()
        show_var = BooleanVar(value=False)
        def toggle_password():
            if show_var.get():
                password_entry.config(show="")
                conf_entry.config(show="")
            else:
                password_entry.config(show="*")
                conf_entry.config(show="*")
        show_checkbox = ttk.Checkbutton(container, text="Show password", variable=show_var, command=toggle_password)
        show_checkbox.pack()
        link_label = ttk.Label(container, text="Already have an account? Log in here.", font=("Segoe UI", 8), cursor="hand2")
        link_label.bind("<Button-1>", show_login)
        link_label.pack()
        style = ttk.Style()
        style.configure("button.TButton", font=("Segoe UI", 8))
        def is_valid_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        def send_email_thread(to_email, code):
            thread = threading.Thread(target=send_email_verif, args=(to_email, code))
            thread.daemon = True
            thread.start()
        def onsubmit():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            c = conf_entry.get().strip()
            if len(u) < 2:
                messagebox.showerror("Username Error", "Username must be at least 2 characters long")
                return
            if (len(p) < 6) or (len(c) < 6):
                messagebox.showerror("Password Error", "Password must be at least 6 characters long")
                return
            if p == c:
                verification_code = str(random.randint(100000, 999999))
                try:
                    e = email_entry.get().strip()
                    if not is_valid_email(e):
                        messagebox.showerror("Email Error", "Invalid Email Address")
                        return
                    send_email_thread(e, verification_code)
                    self.emailveriffunc(u, e, p, verification_code)
                except Exception as e:
                    messagebox.showerror("Email Verification Error", str(e))
            else:
                messagebox.showinfo("Passwords must match", "Your passwords are different")
            
        signup_button = ttk.Button(container, text="Sign up", style="button.TButton", command=onsubmit)
        signup_button.pack(pady=20)
        goback_button = ttk.Button(container, text="Go Back", style="button.TButton", command=show_welcome)
        goback_button.pack(pady=5)