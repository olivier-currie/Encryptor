from tkinter import ttk
from tkinter import BooleanVar
from core.auth import verify_password

class Login(ttk.Frame):
    def __init__(self, parent, show_welcome, show_signup, show_dashboard):
        super().__init__(parent)

        container = ttk.Frame(self, padding=40)
        container.pack(expand=True)
        self.dashfunc = show_dashboard

        title = ttk.Label(container, text="Log In",
                          font=("Segoe UI", 22))
        title.pack(pady=5)

        user_label = ttk.Label(container, text="Username:", font=("Segoe UI", 12))
        user_label.pack(pady=5)
        username_entry = ttk.Entry(container, width=50)
        username_entry.pack()
        pass_label = ttk.Label(container, text="Password:", font=("Segoe UI", 12))
        pass_label.pack(pady=5)
        password_entry = ttk.Entry(container, width=50, show="*")
        password_entry.pack()
        show_var = BooleanVar(value=False)
        def toggle_password():
            if show_var.get():
                password_entry.config(show="")
            else:
                password_entry.config(show="*")
        show_checkbox = ttk.Checkbutton(container, text="Show password", variable=show_var, command=toggle_password)
        show_checkbox.pack()
        link_label = ttk.Label(container, text="Don't have an account? Sign up.", font=("Segoe UI", 8), cursor="hand2")
        link_label.bind("<Button-1>", show_signup)
        link_label.pack()
        def onsubmit():
            u = username_entry.get().strip()
            if verify_password(u, password_entry.get().strip()):
                self.dashfunc(u)
        style = ttk.Style()
        style.configure("button.TButton", font=("Segoe UI", 8))
        login_button = ttk.Button(container, text="Log In", style="button.TButton", command=onsubmit)
        login_button.pack(pady=20)
        goback_button = ttk.Button(container, text="Go Back", style="button.TButton", command=show_welcome)
        goback_button.pack(pady=5)
        