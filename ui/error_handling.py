import tkinter as tk
from tkinter import ttk

def error_message(title, msg, dialog=False, dialogtxt=None, dialogcmd=None, destroyafter=False):
    window = tk.Toplevel()
    window.title(title)
    window.configure(bg="#181818")
    if dialogcmd is not None and destroyafter:
        def dialog_command():
            dialogcmd()
            window.destroy()
    if dialogcmd is not None and not destroyafter:
        def dialog_command():
            dialogcmd()

    if dialog:
        window_w = 450
        window_h = 400
    else:
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

    if dialog:
        dialogbtn = ttk.Button(container, text=dialogtxt, command=dialog_command, style="Base.TButton")
        dialogbtn.pack(pady=10)

    if dialog:
        button = ttk.Button(container, text="Cancel", command=window.destroy, style="Base.TButton")
    else:
        button = ttk.Button(container, text="OK", command=window.destroy, style="Base.TButton")
    

    button.pack(pady=10)
    
    window.grab_set()