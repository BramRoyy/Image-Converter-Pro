import os
from PIL import Image
import customtkinter as ctk
from tkinterdnd2 import DND_FILES

class DragDropArea(ctk.CTkFrame):
    """
    Widget kustom (berbasis CTkFrame) khusus untuk menerima file Drag & Drop
    serta memiliki tombol 'Pilih File Gambar' terintegrasi di dalamnya.
    """
    def __init__(self, master, on_drop_callback, on_browse_callback=None, **kwargs):
        super().__init__(master, **kwargs)

        icons_dir = os.path.join("assets", "icons")

        # 1. Load Ikon Utama Drag & Drop (dragdrop.png)
        dragdrop_path = os.path.join(icons_dir, "dragdrop.png")
        if os.path.exists(dragdrop_path):
            self.icon_dragdrop = ctk.CTkImage(
                light_image=Image.open(dragdrop_path),
                dark_image=Image.open(dragdrop_path),
                size=(64, 64)
            )
        else:
            self.icon_dragdrop = None

        # 2. Load Ikon Tombol Pilih File (search_file.png)
        search_path = os.path.join(icons_dir, "search_file.png")
        if os.path.exists(search_path):
            self.icon_search_file = ctk.CTkImage(
                light_image=Image.open(search_path),
                dark_image=Image.open(search_path),
                size=(18, 18)
            )
        else:
            self.icon_search_file = None

        # Callback
        self.on_drop_callback = on_drop_callback
        self.on_browse_callback = on_browse_callback

        # Desain visual awal kotak Drag & Drop
        self.configure(
            corner_radius=15, 
            border_width=2, 
            border_color="gray", 
            fg_color="transparent"
        )
        
        # Sub-frame agar seluruh elemen berada pas di tengah area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Ikon Utama (Tengah) - Menggunakan dragdrop.png
        if self.icon_dragdrop:
            self.lbl_icon = ctk.CTkLabel(
                self.content_frame, 
                text="", 
                image=self.icon_dragdrop
            )
        else:
            self.lbl_icon = ctk.CTkLabel(self.content_frame, text="📁", font=ctk.CTkFont(size=56))
        self.lbl_icon.pack(pady=(0, 10))
        
        # 2. Teks petunjuk utama
        self.lbl_text = ctk.CTkLabel(
            self.content_frame, 
            text="Drag & Drop Gambar ke Sini", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="gray"
        )
        self.lbl_text.pack(pady=2)

        # 3. Teks pemisah "atau"
        self.lbl_or = ctk.CTkLabel(
            self.content_frame, 
            text="— ATAU —", 
            font=ctk.CTkFont(size=11, weight="bold"), 
            text_color="gray50"
        )
        self.lbl_or.pack(pady=8)

        # 4. Tombol "Pilih File Gambar" Terintegrasi dengan search_file.png
        btn_kwargs = {
            "master": self.content_frame,
            "text": "Pilih File Gambar",
            "font": ctk.CTkFont(size=13, weight="bold"),
            "fg_color": "#3B82F6",
            "hover_color": "#2563EB",
            "height": 38,
            "corner_radius": 8,
            "command": self._on_browse
        }

        if self.icon_search_file:
            btn_kwargs["image"] = self.icon_search_file
            btn_kwargs["compound"] = "left"

        self.btn_browse = ctk.CTkButton(**btn_kwargs)
        self.btn_browse.pack(pady=(2, 0))

        # --- REGISTRASI EVENT DRAG & DROP ---
        self.drop_target_register(DND_FILES)
        
        self.dnd_bind('<<Drop>>', self.on_drop)
        self.dnd_bind('<<DropEnter>>', self.on_drag_enter)
        self.dnd_bind('<<DropLeave>>', self.on_drag_leave)

    def _on_browse(self):
        """Memanggil callback penambahan file dari tombol."""
        if self.on_browse_callback:
            self.on_browse_callback()

    def on_drag_enter(self, event):
        """Efek visual menyala (biru) saat file diseret memasuki area ini."""
        self.configure(border_color="#3B82F6", border_width=3)
        self.lbl_text.configure(text_color="#3B82F6")

    def on_drag_leave(self, event):
        """Kembalikan visual ke semula jika file batal dijatuhkan dan keluar area."""
        self.configure(border_color="gray", border_width=2)
        self.lbl_text.configure(text_color="gray")

    def on_drop(self, event):
        """Menangkap file yang dijatuhkan."""
        self.configure(border_color="gray", border_width=2)
        self.lbl_text.configure(text_color="gray")
        
        # Parsing data dari TkinterDnD2
        raw_files = event.data
        parsed_files = self.tk.splitlist(raw_files)
        
        # Kirim daftar path file ke fungsi callback di main_window
        if self.on_drop_callback:
            self.on_drop_callback(parsed_files)