import tkinter as tk
from tkinter import ttk

def error_message(title, msg):
    window = tk.Toplevel()
    window.title(title)
    window.configure(bg="#181818")
    window_w = 350
    window_h = 250
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w // 2) - (window_w // 2)
    y = (screen_h // 2) - (window_h // 2)
    window.geometry(f"{window_w}x{window_h}+{x}+{y}")
    window.overrideredirect(True)
    style = ttk.Style()
    style.configure("Basik.TLabel", background="#181818", foreground="white")
    style.configure("Base.TButton", background="#181818", foreground="white", bordercolor="white", borderwidth=2, relief="ridge")
    style.configure("Border.TFrame", background="#181818", borderwidth=5, relief="solid")
    container = ttk.Frame(window, style="Border.TFrame")
    container.pack(expand=True, fill="both")
    title_l = ttk.Label(container, text=title, font=("Segoe UI", 22), style="Basik.TLabel")
    title_l.pack(padx=20, pady=(30, 5))
    label = ttk.Label(container, text=msg, font=("Segoe UI", 12), style="Basik.TLabel")
    label.pack(padx=20, pady=(30, 5))
    
    button = ttk.Button(container, text="OK", command=window.destroy, style="Base.TButton")

    button.pack(pady=10)
    
    window.grab_set()