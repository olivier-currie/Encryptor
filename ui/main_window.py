import tkinter as tk
from ui.welcome import Welcome
from ui.login import Login
from ui.signup import Signup
from ui.email_verif import EmailVerif
from ui.dashboard import Dash
from ui.history import History
from ui.account_info import AccountInfo

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Encryptor")
        self.window_w = 800
        self.window_h = 800
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (self.window_w // 2)
        y = (screen_h // 2) - (self.window_h // 2)
        self.root.geometry(f"{self.window_w}x{self.window_h}+{x}+{y}")
        self.root.resizable(False, False)
        self.current_frame = None
        self.show_welcome()
    
    def switch_frame(self, new_frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self, event=None):
        self.switch_frame(
            Login(
                self.root,
                show_welcome=self.show_welcome,
                show_signup=self.show_signup,
                show_dashboard=self.show_dashboard
            )
        )
    
    def show_signup(self, event=None):
        self.switch_frame(
            Signup(
                self.root,
                show_welcome=self.show_welcome,
                show_login=self.show_login,
                show_emailverif=self.show_emailverif
            )
        )

    def show_dashboard(self, username):
        self.switch_frame(
            Dash(
                self.root,
                username=username,
                show_welcome=self.show_welcome,
                show_history=self.show_history,
                show_account_info=self.show_account_info
            )
        )
    
    def show_emailverif(self, username, email, password, v_code):
        self.switch_frame(
            EmailVerif(
                self.root,
                username=username,
                email=email,
                password=password,
                v_code = v_code,
                show_dashboard=self.show_dashboard,
                show_signup = self.show_signup
            )
        )

    def show_history(self, username, entries):
        self.switch_frame(
            History(
                self.root,
                username=username,
                entries=entries,
                show_welcome=self.show_welcome,
                show_dashboard=self.show_dashboard,
                show_account_info=self.show_account_info
            )
        )
    
    def show_account_info(self, username):
        self.switch_frame(
            AccountInfo(
                self.root,
                username=username,
                show_welcome=self.show_welcome,
                show_dashboard=self.show_dashboard,
                show_history=self.show_history
            )
        )
        

    def show_welcome(self, event=None):
        self.switch_frame(
            Welcome(
                self.root,
                show_login=self.show_login,
                show_signup=self.show_signup
            )
        )
    
    
    def run(self):
        self.root.mainloop()

