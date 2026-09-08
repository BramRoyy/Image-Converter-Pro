import tkinter as tk

def create_app_menu(root, on_open_files, on_exit):
    """Membentuk Baris Menu Atas (MenuBar)."""
    menubar = tk.Menu(root)
    
    # Menu File
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open Files...", command=on_open_files)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_exit)
    menubar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menubar)