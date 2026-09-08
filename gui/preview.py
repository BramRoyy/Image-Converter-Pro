import customtkinter as ctk
from PIL import Image
import os

class ImagePreviewPanel(ctk.CTkFrame):
    """
    Panel untuk menampilkan preview gambar, metadata, kontrol manipulasi, 
    zoom, drag to pan, serta judul dinamis berupa nama file.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Judul panel preview (Bersifat dinamis menampilkan nama file)
        self.lbl_title = ctk.CTkLabel(self, text="Preview Gambar", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_title.pack(pady=10)

        # Frame tempat gambar preview dirender
        self.image_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray15"), corner_radius=10)
        self.image_frame.pack(expand=True, fill="both", padx=15, pady=5)

        # 1. Label khusus untuk gambar preview
        self.lbl_image = ctk.CTkLabel(self.image_frame, text="")
        self.lbl_image.place(relx=0.5, rely=0.5, anchor="center")

        # 2. Label terpisah khusus untuk teks placeholder
        self.lbl_placeholder = ctk.CTkLabel(self.image_frame, text="Pilih gambar untuk preview", text_color="gray")
        self.lbl_placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # --- PANEL KONTROL MANIPULASI (ZOOM & ROTATE) ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=5)

        self.btn_zoom_in = ctk.CTkButton(self.control_frame, text="🔍+", width=40, height=28, command=self.zoom_in, state="disabled")
        self.btn_zoom_in.grid(row=0, column=0, padx=3)

        self.btn_zoom_out = ctk.CTkButton(self.control_frame, text="🔍-", width=40, height=28, command=self.zoom_out, state="disabled")
        self.btn_zoom_out.grid(row=0, column=1, padx=3)

        self.btn_rotate = ctk.CTkButton(self.control_frame, text="🔄 Putar", width=70, height=28, command=self.rotate_image, state="disabled")
        self.btn_rotate.grid(row=0, column=2, padx=3)

        # Label Informasi Metadata di bagian bawah
        self.lbl_info = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.lbl_info.pack(pady=5)
        
        # State Data Gambar & Posisi Geser (Panning)
        self.current_image_path = None
        self.current_rotation = 0
        self.zoom_scale = 1.0
        self.image_cache = []
        
        # Variabel untuk melacak geser mouse (Drag to Pan)
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0

        # --- BINDING EVENT (MOUSE SCROLL, KLIK, & DRAG) ---
        for widget in (self.image_frame, self.lbl_image, self.lbl_placeholder):
            widget.bind("<MouseWheel>", self.on_mouse_wheel)
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.on_drag)

    def load_preview(self, image_path: str, width: int = 200, height: int = 200):
        """Membaca dan meresize gambar secara proporsional untuk ditampilkan sebagai thumbnail."""
        if not os.path.exists(image_path):
            return

        self.current_image_path = image_path
        self.current_rotation = 0
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Ambil nama file dari path untuk dijadikan judul panel preview
        filename = os.path.basename(image_path)
        self.lbl_title.configure(text=filename)

        self.render_image()

        # Aktifkan tombol kontrol manipulasi
        self.btn_zoom_in.configure(state="normal")
        self.btn_zoom_out.configure(state="normal")
        self.btn_rotate.configure(state="normal")

    def render_image(self):
        """Merender ulang gambar berdasarkan status zoom dan rotasi saat ini."""
        if not self.current_image_path:
            return

        try:
            with Image.open(self.current_image_path) as img:
                # 1. Terapkan Rotasi
                if self.current_rotation != 0:
                    img = img.rotate(self.current_rotation, expand=True)

                # 2. Terapkan Skala Zoom Tanpa Batas Maksimum
                base_w, base_h = 200, 200
                target_w = int(base_w * self.zoom_scale)
                target_h = int(base_h * self.zoom_scale)
                
                img.thumbnail((target_w, target_h))
                
                # Buat objek CTkImage
                new_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                
                # Masukkan ke cache
                self.image_cache.append(new_image)
                if len(self.image_cache) > 15:
                    self.image_cache.pop(0)
                
                # Tampilkan ke GUI dan terapkan posisi geser offset
                self.lbl_placeholder.place_forget()
                self.lbl_image.configure(image=new_image)
                self.update_image_position()
                
                self.lbl_info.configure(
                    text=f"Rotasi: {self.current_rotation}° | Zoom: {int(self.zoom_scale * 100)}%\nUkuran: {img.width}x{img.height}"
                )
        except Exception as e:
            self.lbl_info.configure(text=f"Gagal memuat: {str(e)}")

    def update_image_position(self):
        """Memperbarui posisi label gambar berdasarkan offset geser mouse."""
        self.lbl_image.place(relx=0.5, rely=0.5, anchor="center", x=self.offset_x, y=self.offset_y)

    def start_drag(self, event):
        """Merekam posisi awal saat mouse diklik dan ditahan."""
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

    def on_drag(self, event):
        """Menggeser gambar secara real-time saat mouse diseret."""
        if not self.current_image_path:
            return
        
        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y
        
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
        self.offset_x += dx
        self.offset_y += dy
        
        self.update_image_position()

    def zoom_in(self):
        """Memperbesar ukuran preview gambar tanpa batasan maksimum."""
        self.zoom_scale += 0.25
        self.render_image()

    def zoom_out(self):
        """Memperkecil ukuran preview gambar dengan batas minimal aman."""
        if self.zoom_scale > 0.2:
            self.zoom_scale -= 0.25
            self.render_image()

    def rotate_image(self):
        """Memutar orientasi gambar sebesar 90 derajat searah jarum jam."""
        self.current_rotation = (self.current_rotation + 90) % 360
        self.offset_x = 0
        self.offset_y = 0
        self.render_image()

    def on_mouse_wheel(self, event):
        """Menangani interaksi scroll mouse untuk zoom in/out."""
        if not self.current_image_path:
            return
        
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def clear(self):
        """Clear total tampilan preview, kembalikan judul default, dan matikan tombol kontrol."""
        try:
            self.lbl_image.configure(image=None)
        except Exception:
            pass
        
        self.image_cache.clear()
        self.current_image_path = None
        self.current_rotation = 0
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Kembalikan judul panel ke teks default
        self.lbl_title.configure(text="Preview Gambar")

        self.btn_zoom_in.configure(state="disabled")
        self.btn_zoom_out.configure(state="disabled")
        self.btn_rotate.configure(state="disabled")

        self.lbl_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_info.configure(text="")