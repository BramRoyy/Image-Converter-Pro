import customtkinter as ctk
import os

class Sidebar(ctk.CTkFrame):
    """
    Komponen Sidebar di sebelah kiri aplikasi.
    Bertugas menampilkan daftar antrean file yang akan dikonversi.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Judul Sidebar
        self.lbl_title = ctk.CTkLabel(self, text="Antrean File", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_title.pack(pady=(20, 10), padx=20, anchor="w")

        # Garis pemisah (Separator)
        self.separator = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.separator.pack(fill="x", padx=20, pady=(0, 10))

        # Area Scroll (Bisa di-scroll jika gambar lebih dari 10)
        self.queue_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.queue_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Tombol Hapus Antrean (Warna merah untuk aksi destruktif)
        self.btn_clear = ctk.CTkButton(
            self, 
            text="Hapus Semua", 
            fg_color="#b83535", 
            hover_color="#8f2626", 
            command=self.clear_queue
        )
        self.btn_clear.pack(pady=(10, 20), padx=20, fill="x")

        # List internal untuk menyimpan widget item agar mudah dihapus nanti
        self.queue_items = []

    def add_item(self, filepath: str, status: str = "Pending"):
        """
        Menambahkan satu item ke dalam daftar antrean visual.
        """
        # Ekstrak nama file dari path yang panjang
        filename = os.path.basename(filepath)
        
        # Container untuk satu baris item
        item_frame = ctk.CTkFrame(self.queue_frame, corner_radius=5, fg_color=("gray85", "gray25"))
        item_frame.pack(fill="x", pady=2, ipady=2)

        # Potong nama file jika terlalu panjang agar tidak merusak UI
        display_name = filename if len(filename) < 22 else filename[:19] + "..."
        
        lbl_name = ctk.CTkLabel(item_frame, text=display_name, font=ctk.CTkFont(size=12), anchor="w")
        lbl_name.pack(side="left", padx=10, fill="x", expand=True)

        lbl_status = ctk.CTkLabel(item_frame, text=status, font=ctk.CTkFont(size=10), text_color="gray")
        lbl_status.pack(side="right", padx=10)

        # Simpan referensi ke dalam list
        self.queue_items.append(item_frame)

    def clear_queue(self):
        """Menghapus seluruh item dari area antrean visual."""
        for item in self.queue_items:
            item.destroy()  # Menghapus widget dari memori UI
        self.queue_items.clear()