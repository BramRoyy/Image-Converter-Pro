import customtkinter as ctk
from tkinter import messagebox

class Dialogs:
    """
    Class pembantu untuk menampilkan jendela pop-up pemberitahuan / error / konfirmasi.
    """

    @staticmethod
    def show_info(title: str, message: str):
        """Menampilkan dialog informasi biasa."""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning(title: str, message: str):
        """Menampilkan dialog peringatan."""
        messagebox.showwarning(title, message)

    @staticmethod
    def show_error(title: str, message: str):
        """Menampilkan dialog error."""
        messagebox.showerror(title, message)

    @staticmethod
    def ask_confirmation(title: str, message: str) -> bool:
        """Menampilkan dialog konfirmasi Ya / Tidak (Returns True/False)."""
        return messagebox.askyesno(title, message)