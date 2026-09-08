import os
from PIL import Image
import customtkinter as ctk

# Import didukung dari utilitas filetypes proyek Anda
from utils.filetypes import SUPPORTED_OUTPUT_FORMATS

class Toolbar(ctk.CTkFrame):
    """
    Komponen bilah atas (Toolbar) yang bersih, lega, dan estetis.
    Mendukung opsi format target, AI background removal, pemilih warna latar,
    input manual dimensi (Width x Height dalam px atau cm), dan slider kualitas kompresi.
    """
    def __init__(self, master, on_select_folder, on_convert, on_add_file=None, **kwargs):
        super().__init__(master, **kwargs)

        self.on_select_folder = on_select_folder
        self.on_convert = on_convert

        # --- LOAD IKON DARI FOLDER assets/icons ---
        icons_dir = os.path.join("assets", "icons")

        # 1. Load Ikon Folder Hasil (search_folder.png)
        folder_icon_path = os.path.join(icons_dir, "search_folder.png")
        if os.path.exists(folder_icon_path):
            self.icon_folder = ctk.CTkImage(
                light_image=Image.open(folder_icon_path),
                dark_image=Image.open(folder_icon_path),
                size=(16, 16)
            )
        else:
            self.icon_folder = None

        # 2. Load Ikon Convert (rocket.png)
        rocket_icon_path = os.path.join(icons_dir, "rocket.png")
        if os.path.exists(rocket_icon_path):
            self.icon_rocket = ctk.CTkImage(
                light_image=Image.open(rocket_icon_path),
                dark_image=Image.open(rocket_icon_path),
                size=(18, 18)
            )
        else:
            self.icon_rocket = None

        self.configure(fg_color=("gray90", "#18181B"), corner_radius=0)
        self._setup_widgets()

    def _setup_widgets(self):
        # --- PRIORITAS ULTIMATE: PACK KELOMPOK KANAN TERLEBIH DAHULU ---
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="right", padx=15, pady=10)

        # Folder Hasil Badge (Pill Style)
        folder_badge = ctk.CTkFrame(right_frame, fg_color=("gray80", "#27272A"), corner_radius=8)
        folder_badge.pack(side="left", padx=(0, 10))

        # Config Tombol Folder Hasil
        btn_folder_kwargs = {
            "master": folder_badge,
            "text": "Folder Hasil",
            "font": ctk.CTkFont(size=11),
            "fg_color": "transparent",
            "hover_color": ("gray70", "#3F3F46"),
            "text_color": ("gray10", "gray90"),
            "height": 28,
            "corner_radius": 6,
            "command": self.on_select_folder
        }
        if self.icon_folder:
            btn_folder_kwargs["image"] = self.icon_folder
            btn_folder_kwargs["compound"] = "left"

        self.btn_folder = ctk.CTkButton(**btn_folder_kwargs)
        self.btn_folder.pack(side="left", padx=4, pady=2)

        # Config Tombol Convert Utama
        btn_convert_kwargs = {
            "master": right_frame,
            "text": "Convert",  # Teks bersih tanpa emoji
            "width": 135,
            "height": 34,
            "fg_color": "#10B981",  # Emerald Green
            "hover_color": "#059669",
            "font": ctk.CTkFont(weight="bold", size=12),
            "corner_radius": 8,
            "command": self.on_convert
        }
        if self.icon_rocket:
            btn_convert_kwargs["image"] = self.icon_rocket
            btn_convert_kwargs["compound"] = "left"

        self.btn_convert = ctk.CTkButton(**btn_convert_kwargs)
        self.btn_convert.pack(side="left")

        # --- KELOMPOK KIRI: Format Target, Checkbox AI, & Pemilih Warna ---
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", padx=(15, 5), pady=10)

        self.lbl_format = ctk.CTkLabel(
            left_frame, 
            text="Format:", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_format.pack(side="left", padx=(0, 6))

        # Variabel format
        self.format_var = ctk.StringVar(value="JPEG")
        self.combo_format = ctk.CTkOptionMenu(
            left_frame, 
            values=SUPPORTED_OUTPUT_FORMATS, 
            variable=self.format_var,
            width=85,
            height=32,
            corner_radius=6
        )
        self.combo_format.pack(side="left", padx=(0, 10))

        # Checkbox Hapus Background (AI)
        self.chk_remove_bg_var = ctk.BooleanVar(value=False)
        self.chk_remove_bg = ctk.CTkCheckBox(
            left_frame, 
            text="Remove Background",
            variable=self.chk_remove_bg_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#3B82F6",
            hover_color="#1D4ED8",
            command=self._toggle_bg_color_menu
        )
        self.chk_remove_bg.pack(side="left", padx=(0, 8))

        # Dropdown Opsi Warna Latar Belakang
        self.bg_color_var = ctk.StringVar(value="Transparan")
        self.combo_bg_color = ctk.CTkOptionMenu(
            left_frame,
            values=["Transparan", "Merah (Pasfoto)", "Biru (Pasfoto)", "Hijau (Pasfoto)", "Putih", "Hitam"],
            variable=self.bg_color_var,
            width=135,
            height=32,
            corner_radius=6,
            state="disabled"
        )
        self.combo_bg_color.pack(side="left")

        # --- KELOMPOK TENGAH: Input Dimensi (px / cm) & Slider Kualitas ---
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(side="left", padx=5, pady=10)

        # Input Lebar
        self.entry_width = ctk.CTkEntry(
            center_frame,
            placeholder_text="Lebar",
            width=60,
            height=32,
            corner_radius=6
        )
        self.entry_width.pack(side="left", padx=(0, 2))

        # Teks Pemisah "x"
        self.lbl_x = ctk.CTkLabel(
            center_frame, 
            text="×", 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_x.pack(side="left", padx=2)

        # Input Tinggi
        self.entry_height = ctk.CTkEntry(
            center_frame,
            placeholder_text="Tinggi",
            width=60,
            height=32,
            corner_radius=6
        )
        self.entry_height.pack(side="left", padx=(0, 4))

        # Dropdown Pilihan Satuan (px atau cm)
        self.unit_var = ctk.StringVar(value="px")
        self.combo_unit = ctk.CTkOptionMenu(
            center_frame,
            values=["px", "cm"],
            variable=self.unit_var,
            width=55,
            height=32,
            corner_radius=6
        )
        self.combo_unit.pack(side="left", padx=(0, 8))

        # Slider Kualitas Kompresi
        self.lbl_quality = ctk.CTkLabel(
            center_frame, 
            text="Kualitas: 90%", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_quality.pack(side="left", padx=(0, 4))

        self.quality_slider = ctk.CTkSlider(
            center_frame,
            from_=10,
            to=100,
            number_of_steps=18,
            width=80,
            height=16,
            command=self._update_quality_label
        )
        self.quality_slider.set(90)
        self.quality_slider.pack(side="left")

    def _update_quality_label(self, value):
        self.lbl_quality.configure(text=f"Kualitas: {int(value)}%")

    def _toggle_bg_color_menu(self):
        if self.chk_remove_bg_var.get():
            self.combo_bg_color.configure(state="normal")
        else:
            self.combo_bg_color.configure(state="disabled")

    def get_selected_format(self) -> str:
        return self.format_var.get()

    def get_remove_bg(self) -> bool:
        return bool(self.chk_remove_bg_var.get())

    def get_bg_color_key(self) -> str:
        mapping = {
            "Transparan": "TRANSPARENT",
            "Merah (Pasfoto)": "RED",
            "Biru (Pasfoto)": "BLUE",
            "Hijau (Pasfoto)": "GREEN",
            "Putih": "WHITE",
            "Hitam": "BLACK"
        }
        return mapping.get(self.bg_color_var.get(), "TRANSPARENT")

    def get_quality(self) -> int:
        return int(self.quality_slider.get())

    def get_custom_dimensions(self) -> tuple:
        w_str = self.entry_width.get().strip().replace(',', '.')
        h_str = self.entry_height.get().strip().replace(',', '.')
        unit = self.unit_var.get().lower()

        target_w = None
        target_h = None

        try:
            if w_str:
                val_w = float(w_str)
                if val_w > 0:
                    target_w = int(round(val_w * 300 / 2.54)) if unit == "cm" else int(val_w)

            if h_str:
                val_h = float(h_str)
                if val_h > 0:
                    target_h = int(round(val_h * 300 / 2.54)) if unit == "cm" else int(val_h)

        except ValueError:
            target_w, target_h = None, None

        return target_w, target_h