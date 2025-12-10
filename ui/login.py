from tkinter import ttk
import tkinter as tk
from tkinter import BooleanVar
from core.auth import verify_password
from tkinter import messagebox
from ui.error_handling import error_message

class Login(ttk.Frame):
    def __init__(self, parent, show_welcome, show_signup, show_dashboard):
        super().__init__(parent)

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)
        self.dashfunc = show_dashboard

        title = ttk.Label(container, text="Log In",
                          font=("Segoe UI", 30), style="Base.TLabel")
        title.pack(pady=(0, 30))

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
        style.configure("LoginEntry.TEntry", fieldbackground="#181818", bordercolor="white", foreground="white", borderwidth=4, relief="ridge", padding=5)
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
        user_label = ttk.Label(container, text="Username:", font=("Segoe UI", 12), style="Base.TLabel")
        user_label.pack(pady=10)
        username_entry = ttk.Entry(container, width=50, style="LoginEntry.TEntry")
        username_entry.pack()
        pass_label = ttk.Label(container, text="Password:", font=("Segoe UI", 12), style="Base.TLabel")
        pass_label.pack(pady=10)
        password_entry = ttk.Entry(container, width=50, show="*", style="LoginEntry.TEntry")
        password_entry.pack()
        show_var = BooleanVar(value=False)
        def toggle_password():
            if show_var.get():
                password_entry.config(show="")
            else:
                password_entry.config(show="*")
        show_checkbox = ttk.Checkbutton(container, text="Show password", variable=show_var, command=toggle_password, style="LabelOnly.TCheckbutton")
        show_checkbox.pack(pady=10)
        link_label = ttk.Label(container, text="Don't have an account? Sign up.", font=("Segoe UI", 8), cursor="hand2", style="Base.TLabel")
        link_label.bind("<Button-1>", show_signup)
        link_label.bind("<Enter>", lambda e : on_enter(e, link_label))
        link_label.bind("<Leave>", lambda e : on_leave(e, link_label))
        link_label.pack(pady=10)
        def onsubmit():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            if not u:
                error_message("Username Error", "Username cannot be empty.")
                return
            if not p:
                error_message("Password Error", "Password cannot be empty.")
                return
            try:
                if verify_password(u, p):
                    self.dashfunc(u)
                else:
                    error_message("Login Error", "Incorrect Password.")
            except TypeError as e:
                error_message("Login Error", "Incorrect Username.")
            except Exception as e:
                error_message("Login Error", str(e))
        
        login_button = ttk.Button(container, text="Log In", style="Base.TButton", command=onsubmit)
        login_button.pack(pady=20)
        goback_button = ttk.Button(container, text="Go Back", style="Base.TButton", command=show_welcome)
        goback_button.pack(pady=10)
        