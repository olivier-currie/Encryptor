from tkinter import ttk
from core.auth import send_email_verif
import random
from tkinter import messagebox, BooleanVar
import threading
import re
from ui.error_handling import error_message

class Signup(ttk.Frame):
    def __init__(self, parent, show_welcome, show_login, show_emailverif):
        super().__init__(parent)

        self.emailveriffunc = show_emailverif

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)

        def on_enter(e, l):
            l.config(style="Hover.TLabel")
        def on_leave(e, l):
            l.config(style="Base.TLabel")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#181818")
        style.configure("Hover.TLabel", background="#181818", foreground="white", borderwidth=2, relief="ridge")
        style.configure("Base.TLabel", background="#181818", foreground="white")
        style.configure("LabelOnly.TCheckbutton", background="#181818", foreground="white")
        style.configure("SignUp.TEntry", fieldbackground="#181818", bordercolor="white", foreground="white", borderwidth=4, relief="ridge", padding=5)
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
        title = ttk.Label(container, text="Sign Up",
                          font=("Segoe UI", 30), style="Base.TLabel")
        title.pack(pady=(0, 30))
        user_label = ttk.Label(container, text="Username:", font=("Segoe UI", 12), style="Base.TLabel")
        user_label.pack(pady=10)
        username_entry = ttk.Entry(container, width=50, style="SignUp.TEntry")
        username_entry.pack()
        email_label = ttk.Label(container, text="E-Mail:", font=("Segoe UI", 12), style="Base.TLabel")
        email_label.pack(pady=10)
        email_entry = ttk.Entry(container, width=50, style="SignUp.TEntry")
        email_entry.pack()
        pass_label = ttk.Label(container, text="Password:", font=("Segoe UI", 12), style="Base.TLabel")
        pass_label.pack(pady=10)
        password_entry = ttk.Entry(container, width=50, show="*", style="SignUp.TEntry")
        password_entry.pack()
        conf_label = ttk.Label(container, text="Confirm password:", font=("Segoe UI", 12), style="Base.TLabel")
        conf_label.pack(pady=10)
        conf_entry = ttk.Entry(container, width=50, show="*", style="SignUp.TEntry")
        conf_entry.pack()
        show_var = BooleanVar(value=False)
        def toggle_password():
            if show_var.get():
                password_entry.config(show="")
                conf_entry.config(show="")
            else:
                password_entry.config(show="*")
                conf_entry.config(show="*")
        show_checkbox = ttk.Checkbutton(container, text="Show password", variable=show_var, command=toggle_password, style="LabelOnly.TCheckbutton")
        show_checkbox.pack(pady=10)
        link_label = ttk.Label(container, text="Already have an account? Log in here.", font=("Segoe UI", 8), cursor="hand2", style="Base.TLabel")
        link_label.bind("<Button-1>", show_login)
        link_label.bind("<Enter>", lambda e : on_enter(e, link_label))
        link_label.bind("<Leave>", lambda e : on_leave(e, link_label))
        link_label.pack(pady=10)

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
                error_message("Username Error", "Username must be at least 2 characters long")
                return
            if (len(p) < 6) or (len(c) < 6):
                error_message("Password Error", "Password must be at least 6 characters long")
                return
            if p == c:
                verification_code = str(random.randint(100000, 999999))
                try:
                    e = email_entry.get().strip()
                    if not is_valid_email(e):
                        error_message("Email Error", "Invalid Email Address")
                        return
                    send_email_thread(e, verification_code)
                    self.emailveriffunc(u, e, p, verification_code)
                except Exception as e:
                    error_message("Email Verification Error", str(e))
            else:
                error_message("Passwords must match", "Your passwords are different")
            
        signup_button = ttk.Button(container, text="Sign up", style="Base.TButton", command=onsubmit)
        signup_button.pack(pady=20)
        goback_button = ttk.Button(container, text="Go Back", style="Base.TButton", command=show_welcome)
        goback_button.pack(pady=5)