from tkinter import ttk
from tkinter import PhotoImage
from core.enc_dec import get_history
from core.auth import get_email, get_account_created, delete_user
from ui.error_handling import error_message

class AccountInfo(ttk.Frame):
    def __init__(self, parent, username, show_welcome, show_dashboard, show_history):
        super().__init__(parent)
        aframe = ttk.Frame(self)
        aframe.pack(fill="both", expand=True)
        self.username = username
        self.email = get_email(username)
        self.account_created = get_account_created(username)
        self.user_icon = PhotoImage(file="assets/user.png")
        self.logout_icon = PhotoImage(file="assets/logout.png")
        self.history_icon = PhotoImage(file="assets/history.png")
        self.dash_icon = PhotoImage(file="assets/dash.png")
        style = ttk.Style()
        style.configure("Navbar.TFrame", background="#2c3e50")
        style.configure("Hover.TLabel", background="#23313F")
        style.configure("Base.TLabel", background="#2c3e50")
        style.configure("Basic.TLabel", background="#181818", foreground="white")
        style.configure("Base.TButton", background="#181818", foreground="white", bordercolor="white", borderwidth=2, relief="ridge", font=("Segoe UI", 8))
        style.map("Base.TButton",
          background=[("active", "darkgray"),
                      ("selected", "#darkgray"),
                      ("!active", "#181818")],
          foreground=[("active", "white"),
                      ("selected", "white"),
                      ("!active", "white")])
        def on_enter(e, l):
            l.config(style="Hover.TLabel")
        def on_leave(e, l):
            l.config(style="Base.TLabel")
        navbar = ttk.Frame(aframe, style="Navbar.TFrame", relief="raised", padding=(10, 15))
        navbar.pack(fill="x")
        user_label = ttk.Label(navbar, text=f"{username}", image=self.user_icon, compound="left", foreground="white", style="Base.TLabel", font=("Segoe UI", 12))
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

        dash_label = ttk.Label(navbar, text="Dashboard", image=self.dash_icon, compound="top", foreground="white", cursor="hand2", style="Base.TLabel", font=("Segoe UI", 8))
        dash_label.pack(side="right", padx=10)
        dash_label.bind("<Button-1>", lambda e: show_dashboard(username))
        dash_label.bind("<Enter>", lambda e : on_enter(e, dash_label))
        dash_label.bind("<Leave>", lambda e : on_leave(e, dash_label))
        title = ttk.Label(aframe, text=f"Account Information for {self.username}", font=("Segoe UI", 18), style="Basic.TLabel")
        title.pack(pady=(15,35))
        email = ttk.Label(aframe, text=f"E-mail: {self.email}", font=("Segoe UI", 12), style="Basic.TLabel")
        email.pack(pady=(20,35))
        acc_created = ttk.Label(aframe, text=f"Account created: {self.account_created}", font=("Segoe UI", 12), style="Basic.TLabel")
        acc_created.pack(pady=(20,35))
        def ondelete():
            delete_user(self.username)
            show_welcome()

        def delete_dialog():
            error_message("Warning", "Are you sure you want to delete your account?", dialog=True, dialogtxt="Delete Account", dialogcmd=ondelete, destroyafter=True)

        go_button = ttk.Button(aframe, text="Delete Account", style="Base.TButton", command=delete_dialog)
        go_button.pack(padx=20, pady=10)



    