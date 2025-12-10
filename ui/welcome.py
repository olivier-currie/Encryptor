from tkinter import PhotoImage
from tkinter import ttk

class Welcome(ttk.Frame):
    def __init__(self, parent, show_login, show_signup):
        super().__init__(parent)

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)
        style1 = ttk.Style()
        style1.configure("Hover.TLabel", background="#181818", foreground="white", borderwidth=2, relief="ridge")
        style1.configure("Base.TLabel", background="#181818", foreground="white")
        style1.configure("TFrame", background="#181818")

        self.account_icon = PhotoImage(file="assets/account_white.png")
        self.login_icon = PhotoImage(file="assets/login_white.png")

        title = ttk.Label(container, text="Welcome to Encryptor",
                          font=("Segoe UI", 32), style="Base.TLabel")
        title.pack(pady=(0, 20))

        tagline = ttk.Label(container,
                            text="Securely encrypt and decrypt your files.",
                            font=("Segoe UI", 18), style="Base.TLabel")
        tagline.pack(pady=(0, 100))
        options_frame = ttk.Frame(container)
        options_frame.pack()
        acc_label = ttk.Label(options_frame, text="Create an account", image=self.account_icon, compound="top", cursor="hand2", style="Base.TLabel")
        acc_label.pack(side="left", pady=20, padx=40)
        def on_enter(e, l):
            l.config(style="Hover.TLabel")
        def on_leave(e, l):
            l.config(style="Base.TLabel")
   
        acc_label.bind("<Button-1>", show_signup)
        acc_label.bind("<Enter>", lambda e : on_enter(e, acc_label))
        acc_label.bind("<Leave>", lambda e : on_leave(e, acc_label))

        log_label = ttk.Label(options_frame, text="Log in", image=self.login_icon, compound="top", cursor="hand2", style="Base.TLabel")
        log_label.pack(side="right", pady=20, padx=40)
        log_label.bind("<Button-1>", show_login)
        log_label.bind("<Enter>", lambda e : on_enter(e, log_label))
        log_label.bind("<Leave>", lambda e : on_leave(e, log_label))

        credit_label = ttk.Label(container, text="Credit to icons8.com for all icons used.", font=("Segoe UI", 8), style="Base.TLabel")
        credit_label.pack(pady=(150, 0))
