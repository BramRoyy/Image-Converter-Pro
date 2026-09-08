import customtkinter as ctk

class QueueItemWidget(ctk.CTkFrame):
    """
    Widget kustom berbentuk Card untuk setiap file di dalam daftar antrean Sidebar.
    Memiliki indikator status warna, tombol hapus, dan BISA DIKLIK untuk preview.
    """
    def __init__(self, master, filename: str, filepath: str, on_remove_callback=None, on_click_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.filepath = filepath
        self.on_remove_callback = on_remove_callback
        self.on_click_callback = on_click_callback

        self.configure(corner_radius=6, fg_color=("gray85", "gray25"))
        self.configure(cursor="hand2")

        # --- KONFIGURASI GRID (Agar Layout Kaku & Rapi) ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # --- BINDING KLIK EVENT ---
        self.bind("<Button-1>", self._on_click)

        # Format nama file cerdas (Mempertahankan ekstensi di belakang)
        display_name = self._truncate_filename(filename, max_length=16)

        # Nama File
        self.lbl_name = ctk.CTkLabel(self, text=display_name, font=ctk.CTkFont(size=12), anchor="w")
        self.lbl_name.grid(row=0, column=0, sticky="ew", padx=(10, 4), pady=6)
        self.lbl_name.bind("<Button-1>", self._on_click)

        # Status Badge (Default diatur ke Ready dengan warna Biru)
        self.lbl_status = ctk.CTkLabel(self, text="Ready", font=ctk.CTkFont(size=10, weight="bold"), text_color="#3B82F6")
        self.lbl_status.grid(row=0, column=1, padx=4, sticky="e")
        self.lbl_status.bind("<Button-1>", self._on_click)

        # Tombol Hapus (❌) dengan ukuran mutlak (width=24, height=24)
        self.btn_remove = ctk.CTkButton(
            self, text="✕", width=24, height=24, fg_color="transparent", 
            hover_color="#b83535", text_color="gray",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_remove
        )
        self.btn_remove.grid(row=0, column=2, padx=(2, 8), sticky="e")

    def _truncate_filename(self, filename: str, max_length: int = 16) -> str:
        """Memotong nama file panjang dan memastikan ekstensi file tetap terlihat di ujung."""
        if len(filename) <= max_length:
            return filename
        
        ext = ""
        if "." in filename:
            ext = filename.split(".")[-1]
            name_part = filename[:-(len(ext) + 1)]
        else:
            name_part = filename

        chars_to_keep = max_length - len(ext) - 4
        if chars_to_keep < 3:
            chars_to_keep = 3
            
        front = name_part[:chars_to_keep]
        return f"{front}....{ext}"

    def update_status(self, status: str):
        """Memperbarui teks dan warna indikator status pada kartu antrean."""
        if status == "Ready":
            self.lbl_status.configure(text="Ready", text_color="#3B82F6")
        elif status == "Converting":
            self.lbl_status.configure(text="Converting...", text_color="#F59E0B")
        elif status == "Done":
            self.lbl_status.configure(text="Done ✓", text_color="#10B981")
        elif status == "Error":
            self.lbl_status.configure(text="Error ❌", text_color="#EF4444")
        else:
            self.lbl_status.configure(text="Pending", text_color="gray")

    def _on_remove(self):
        if self.on_remove_callback:
            self.on_remove_callback(self)
        self.destroy()

    def _on_click(self, event):
        """Memicu fungsi show_preview di main_window"""
        if self.on_click_callback:
            self.on_click_callback(self.filepath)