from tkinter import ttk
from core.auth import create_user

class EmailVerif(ttk.Frame):
    def __init__(self, parent, username, email, password, v_code, show_dashboard):
        super().__init__(parent)

        self.dashfunc = show_dashboard

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)

        title = ttk.Label(container, text=f"Enter the six digit code sent to {email}:",
                          font=("Segoe UI", 22))
        title.pack(pady=5)
        code_entry = ttk.Entry(container)
        code_entry.pack()
        def onclick():
            if code_entry.get().strip() == v_code:
                if create_user(username, email, password):
                    self.dashfunc(username)

        style = ttk.Style()
        style.configure("button.TButton", font=("Segoe UI", 8))
        go_button = ttk.Button(container, text="Enter", style="button.TButton", command=onclick)
        go_button.pack(padx=20)
