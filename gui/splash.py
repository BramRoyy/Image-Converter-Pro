import os
import customtkinter as ctk
from PIL import Image

class SplashScreen(ctk.CTkToplevel):
    """
    Jendela Intro / Splash Screen modern & minimalis berbasis CTkToplevel.
    Didesain dengan skema warna Dark Zinc, tipografi bersih, dan progress bar sleek.
    """
    def __init__(self, parent, on_complete_callback=None):
        super().__init__(parent)

        self.parent = parent
        self.on_complete_callback = on_complete_callback

        # 1. Konfigurasi Jendela Frameless & Always-on-Top
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#18181B")  # Dark Zinc Background

        # 2. Ukuran & Posisikan tepat di tengah layar monitor
        width = 460
        height = 280
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self._setup_ui()

        # 3. Jalankan Animasi Loading
        self.progress_val = 0.0
        self._animate_loading()

    def _setup_ui(self):
        # Card Container Utama dengan Border Tipis Subtle (#27272A)
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="#18181B",
            corner_radius=14, 
            border_width=1, 
            border_color="#27272A"
        )
        self.main_frame.pack(fill="both", expand=True, padx=1, pady=1)

        # 1. Logo / Ikon Aplikasi (Mendukung gambar logo.png jika ada, fallback ke Emoji)
        logo_path = os.path.join("assets", "icons", "logo.png")
        if os.path.exists(logo_path):
            try:
                logo_img = ctk.CTkImage(Image.open(logo_path), size=(64, 64))
                self.lbl_logo = ctk.CTkLabel(self.main_frame, image=logo_img, text="")
                self.lbl_logo.pack(pady=(32, 8))
            except Exception:
                self._create_emoji_logo()
        else:
            self._create_emoji_logo()

        # 2. Judul Utama
        self.lbl_title = ctk.CTkLabel(
            self.main_frame, 
            text="Image Converter Pro", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#FAFAFA"
        )
        self.lbl_title.pack(pady=(0, 2))

        # 3. Subtitle / Versi
        self.lbl_subtitle = ctk.CTkLabel(
            self.main_frame, 
            text="v1.0 • Fast Batch Processing & BiRefNet AI", 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#A1A1AA"
        )
        self.lbl_subtitle.pack(pady=(0, 22))

        # 4. Progress Bar Tipis (Sleek Modern Profile)
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame, 
            width=340, 
            height=3,  # Profil ultra-tipis agar terkesan elegan
            corner_radius=2,
            fg_color="#27272A",
            progress_color="#3B82F6"  # Royal Blue Accent
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 8))

        # 5. Status Text (Loading Indicator)
        self.lbl_status = ctk.CTkLabel(
            self.main_frame, 
            text="Memulai aplikasi...", 
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#71717A"
        )
        self.lbl_status.pack(pady=(0, 16))

    def _create_emoji_logo(self):
        """Fallback jika file gambar logo belum tersedia di folder assets."""
        self.lbl_logo = ctk.CTkLabel(
            self.main_frame, 
            text="🚀", 
            font=ctk.CTkFont(size=42)
        )
        self.lbl_logo.pack(pady=(32, 6))

    def _animate_loading(self):
        if self.progress_val <= 1.0:
            self.progress_bar.set(self.progress_val)
            
            if self.progress_val < 0.3:
                self.lbl_status.configure(text="Memuat dependensi & modul GUI...")
            elif self.progress_val < 0.7:
                self.lbl_status.configure(text="Menyiapkan mesin konversi & BiRefNet AI...")
            else:
                self.lbl_status.configure(text="Membuka antarmuka utama...")

            self.progress_val += 0.015
            self.after(35, self._animate_loading)
        else:
            self.destroy()
            if self.on_complete_callback:
                self.on_complete_callback()