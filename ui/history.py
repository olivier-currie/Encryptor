from tkinter import ttk
from tkinter import PhotoImage

class History(ttk.Frame):
    def __init__(self, parent, username, entries, show_welcome, show_dashboard):
        super().__init__(parent)
        hframe = ttk.Frame(self)
        hframe.pack(fill="both", expand=True)
        self.user_icon = PhotoImage(file="assets/user.png")
        self.logout_icon = PhotoImage(file="assets/logout.png")
        self.history_icon = PhotoImage(file="assets/dash.png")
        style = ttk.Style()
        style.configure("Navbar.TFrame", background="#2c3e50")
        style.configure("Hover.TLabel", background="#23313F")
        style.configure("Base.TLabel", background="#2c3e50")
        style.configure("Basic.TLabel", background="#181818", foreground="white")
        style.configure("Treeview",
            background="#181818",
            fieldbackground="#181818",
            foreground="white"
        )
        style.configure("Treeview.Heading",
            background="#181818",
            foreground="white",
            relief="flat"
        )
        def on_enter(e, l):
            l.config(style="Hover.TLabel")
        def on_leave(e, l):
            l.config(style="Base.TLabel")
        navbar = ttk.Frame(hframe, style="Navbar.TFrame", relief="raised", padding=(10, 15))
        navbar.pack(fill="x")
        user_label = ttk.Label(navbar, text=f"{username}", image=self.user_icon, compound="left", foreground="white", style="Base.TLabel", font=("Segoe UI", 12))
        user_label.pack(side="left")

        logout_label = ttk.Label(navbar, text="Log out", image=self.logout_icon, compound="top", foreground="white", cursor="hand2", style="Base.TLabel", font=("Segoe UI", 8))
        logout_label.pack(side="right")
        logout_label.bind("<Button-1>", show_welcome)
        logout_label.bind("<Enter>", lambda e : on_enter(e, logout_label))
        logout_label.bind("<Leave>", lambda e : on_leave(e, logout_label))

        dash_label = ttk.Label(navbar, text="Dashboard", image=self.history_icon, compound="top", foreground="white", cursor="hand2", style="Base.TLabel", font=("Segoe UI", 8))
        dash_label.pack(side="right", padx=30)
        dash_label.bind("<Button-1>", lambda e: show_dashboard(username))
        dash_label.bind("<Enter>", lambda e : on_enter(e, dash_label))
        dash_label.bind("<Leave>", lambda e : on_leave(e, dash_label))
        title = ttk.Label(hframe, text=f"Encryption history for {username}", font=("Segoe UI", 18), style="Basic.TLabel")
        title.pack(pady=(15,35))
        tree_frame = ttk.Frame(hframe, padding=(10,0,5,0))
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        cols=("filename", "action", "timestamp")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        self.tree.heading("filename", text="File Name")
        self.tree.heading("action", text="Action")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.column("filename", width=250)
        self.tree.column("action", width=100)
        self.tree.column("timestamp", width=180)
        for entry in entries:
            self.tree.insert("", "end", values=entry)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")