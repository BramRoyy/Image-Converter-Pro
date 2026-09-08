import os
from pathlib import Path
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.filetypes import SUPPORTED_INPUT_FORMATS

class FileValidator:
    """
    Memastikan file aman untuk diproses oleh sistem (ukuran wajar, format benar).
    """
    # Batas maksimal ukuran file: 50 MB (dalam Bytes)
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024 

    @staticmethod
    def validate(file_path: str) -> bool:
        """
        Memvalidasi file tunggal. 
        Melempar ValueError jika file bermasalah.
        """
        path_obj = Path(file_path)

        # 1. Cek keberadaan file
        if not path_obj.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

        # 2. Cek apakah path tersebut adalah file (bukan folder)
        if not path_obj.is_file():
            raise ValueError(f"Path yang diberikan bukan sebuah file: {file_path}")

        # 3. Cek apakah file kosong (0 bytes)
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise ValueError("File kosong (0 bytes) dan tidak dapat diproses.")

        # 4. Cek format ekstensi
        ext = path_obj.suffix.lower()
        if ext not in SUPPORTED_INPUT_FORMATS:
            raise ValueError(f"Format file '{ext}' tidak didukung oleh aplikasi.")

        # 5. Cek batas ukuran maksimal (mencegah Out of Memory)
        if file_size > FileValidator.MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            raise ValueError(f"Ukuran file ({size_mb:.1f} MB) melebihi batas maksimal 50 MB.")

        return True