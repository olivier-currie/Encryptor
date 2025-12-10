from tkinter import ttk
from core.auth import create_user
from ui.error_handling import error_message

class EmailVerif(ttk.Frame):
    def __init__(self, parent, username, email, password, v_code, show_dashboard):
        super().__init__(parent)

        self.dashfunc = show_dashboard

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#181818")
        style.configure("Base.TLabel", background="#181818", foreground="white")
        style.configure("EmailEntry.TEntry", fieldbackground="#181818", bordercolor="white", width=40, foreground="white", borderwidth=4, relief="ridge", padding=5)
        style.configure("Base.TButton", background="#181818", foreground="white", bordercolor="white", borderwidth=2, relief="ridge", font=("Segoe UI", 8))
        style.map("Base.TButton",
          background=[("active", "darkgray"),
                      ("selected", "#darkgray"),
                      ("!active", "#181818")],
          foreground=[("active", "white"),
                      ("selected", "white"),
                      ("!active", "white")])

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)

        title = ttk.Label(container, text=f"Enter the six digit code sent to {email}:",
                          font=("Segoe UI", 20), style="Base.TLabel")
        title.pack(pady=(0, 30))
        code_entry = ttk.Entry(container, style="EmailEntry.TEntry")
        code_entry.pack(pady=30)
        def onclick():
            c = code_entry.get().strip()
            if not c:
                error_message("Verification Code Error", "Verification code cannot be empty.")
                return
            if c == v_code:
                if create_user(username, email, password):
                    self.dashfunc(username)
                else:
                    error_message("Account Error", "Account cannot be created")
                    return

        go_button = ttk.Button(container, text="Enter", style="Base.TButton", command=onclick)
        go_button.pack(padx=20, pady=10)
