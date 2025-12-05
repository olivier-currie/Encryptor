from tkinter import PhotoImage
from tkinter import ttk

class Welcome(ttk.Frame):
    def __init__(self, parent, show_login, show_signup):
        super().__init__(parent)

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)

        self.account_icon = PhotoImage(file="assets/account.png")
        self.login_icon = PhotoImage(file="assets/login.png")

        title = ttk.Label(container, text="Welcome to Encryptor",
                          font=("Segoe UI", 22))
        title.pack(pady=5)

        tagline = ttk.Label(container,
                            text="Securely encrypt and decrypt your files.",
                            font=("Segoe UI", 12))
        tagline.pack(pady=(0, 20))
        options_frame = ttk.Frame(container)
        options_frame.pack()
        acc_label = ttk.Label(options_frame, text="Create an account", image=self.account_icon, compound="top", cursor="hand2")
        acc_label.pack(side="left", pady=20, padx=20)
   
        acc_label.bind("<Button-1>", show_signup)

        log_label = ttk.Label(options_frame, text="Log in", image=self.login_icon, compound="top", cursor="hand2")
        log_label.pack(side="right", pady=20, padx=20)
        log_label.bind("<Button-1>", show_login)
