import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    """
    Bilah status di bagian bawah window.
    Menampilkan teks status dan Progress Bar interaktif.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Teks Status
        self.lbl_status = ctk.CTkLabel(
            self, 
            text="Status: Ready", 
            text_color="gray", 
            font=ctk.CTkFont(size=12)
        )
        self.lbl_status.pack(side="left", padx=15, pady=2)

        # Progress Bar (Awalnya tersembunyi/0%)
        self.progress_bar = ctk.CTkProgressBar(self, width=200, height=10)
        self.progress_bar.pack(side="right", padx=15, pady=8)
        self.progress_bar.set(0) # 0.0 sampai 1.0

    def set_status(self, text: str):
        """Memperbarui teks status."""
        self.lbl_status.configure(text=f"Status: {text}")

    def update_progress(self, current: int, total: int):
        """Memperbarui persentase Progress Bar (Nilai 0.0 - 1.0)."""
        if total > 0:
            percentage = current / total
            self.progress_bar.set(percentage)
            self.set_status(f"Converting... ({current}/{total})")

    def reset_progress(self):
        """Mengembalikan Progress Bar ke angka 0."""
        self.progress_bar.set(0)