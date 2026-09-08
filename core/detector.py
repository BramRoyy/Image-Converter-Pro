import os
from pathlib import Path
from PIL import Image, UnidentifiedImageError

class ImageDetector:
    """
    Bertugas mendeteksi dan mengekstrak informasi detail dari sebuah file gambar.
    Membantu validasi dan UI untuk menampilkan data (resolusi, ukuran, format).
    """

    @staticmethod
    def analyze(file_path: str) -> dict:
        """
        Membaca header file dan mengembalikan dictionary berisi informasi gambar.
        Tidak memuat (load) seluruh piksel gambar sehingga prosesnya sangat cepat.
        """
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

        # Template data awal
        info = {
            "filename": path_obj.name,
            "filepath": str(path_obj.resolve()),
            "file_size_bytes": os.path.getsize(file_path),
            "file_size_formatted": ImageDetector._format_size(os.path.getsize(file_path)),
            "is_valid": False,
            "format": None,
            "width": 0,
            "height": 0,
            "color_mode": None,
            "has_alpha": False,
            "dpi": None,
            "error_message": None
        }

        try:
            # Buka gambar (Pillow otomatis hanya membaca header pada tahap ini)
            with Image.open(file_path) as img:
                info["is_valid"] = True
                info["format"] = img.format  # Contoh: 'JPEG', 'PNG', 'WEBP'
                info["width"], info["height"] = img.size
                info["color_mode"] = img.mode
                
                # Deteksi keberadaan Alpha Channel (Transparansi)
                # getbands() akan mengembalikan tuple seperti ('R', 'G', 'B', 'A')
                bands = img.getbands()
                info["has_alpha"] = 'A' in bands or 'a' in bands
                
                # Mengambil data DPI jika metadata tersebut tersedia di gambar
                info["dpi"] = img.info.get('dpi')

        except UnidentifiedImageError:
            # Jika file yang dimasukkan ternyata PDF, TXT, atau gambar yang rusak
            info["is_valid"] = False
            info["error_message"] = "File bukan gambar yang didukung atau rusak (corrupt)."
        except OSError as e:
            # Jika ada masalah akses file (Permission denied, dll)
            info["is_valid"] = False
            info["error_message"] = f"Error membaca file: {str(e)}"

        return info

    @staticmethod
    def _format_size(size_in_bytes: int) -> str:
        """Helper internal untuk mengubah Byte menjadi KB, MB secara rapi."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} TB"