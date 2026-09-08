from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any

@dataclass
class ImageInfo:
    """
    Model data (Data Transfer Object) untuk menyimpan informasi gambar.
    Memudahkan perpindahan data antara Core, Services, dan GUI.
    """
    # Properti Utama
    filename: str
    filepath: str
    
    # Properti Opsional (diberi nilai default jika gagal dideteksi)
    file_size_bytes: int = 0
    file_size_formatted: str = "0 B"
    is_valid: bool = False
    format: Optional[str] = None
    width: int = 0
    height: int = 0
    color_mode: Optional[str] = None
    has_alpha: bool = False
    dpi: Optional[Tuple[int, int]] = None
    error_message: Optional[str] = None
    
    # Properti tambahan untuk keperluan UI (State Management)
    status: str = "Pending"  # Pilihan: Pending, Converting, Done, Error

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageInfo':
        """
        Factory method: Mengubah dictionary dari ImageDetector menjadi object ImageInfo.
        """
        return cls(
            filename=data.get("filename", ""),
            filepath=data.get("filepath", ""),
            file_size_bytes=data.get("file_size_bytes", 0),
            file_size_formatted=data.get("file_size_formatted", "0 B"),
            is_valid=data.get("is_valid", False),
            format=data.get("format"),
            width=data.get("width", 0),
            height=data.get("height", 0),
            color_mode=data.get("color_mode"),
            has_alpha=data.get("has_alpha", False),
            dpi=data.get("dpi"),
            error_message=data.get("error_message")
        )

    @property
    def resolution(self) -> str:
        """
        Properti tambahan: Memformat resolusi agar mudah dipanggil di GUI (misal: 1920x1080).
        """
        if self.width and self.height:
            return f"{self.width} x {self.height}"
        return "N/A"

# --- TESTING SCRIPT ---
if __name__ == "__main__":
    print("Menguji Model ImageInfo...\n")
    
    # Simulasi dictionary yang didapat dari core/detector.py
    dummy_detector_data = {
        "filename": "foto_liburan.png",
        "filepath": "C:/Images/foto_liburan.png",
        "file_size_bytes": 1048576,
        "file_size_formatted": "1.00 MB",
        "is_valid": True,
        "format": "PNG",
        "width": 1920,
        "height": 1080,
        "color_mode": "RGBA",
        "has_alpha": True,
        "dpi": (72, 72),
        "error_message": None
    }
    
    # Memasukkan dictionary mentah ke dalam Model
    image_model = ImageInfo.from_dict(dummy_detector_data)
    
    # Sekarang kita bisa mengakses data sebagai object (lebih elegan daripada dictionary)
    print(f"Nama File   : {image_model.filename}")
    print(f"Resolusi    : {image_model.resolution}")  # Menggunakan @property yang kita buat
    print(f"Ukuran      : {image_model.file_size_formatted}")
    print(f"Status Awal : {image_model.status}")