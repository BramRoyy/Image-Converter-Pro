import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.exporter import ImageExporter
from utils.helpers import Helpers
from utils.logger import app_logger

class ExportService:
    """
    Service layer yang khusus menangani urusan pasca-konversi (Export).
    Menjembatani GUI dengan Core Exporter dan Helpers.
    """

    @staticmethod
    def prepare_output_path(original_filepath: str, output_dir: str, target_format: str) -> str:
        """
        Menyiapkan dan mengembalikan path aman (anti-overwrite) untuk menyimpan gambar.
        """
        return ImageExporter.generate_safe_output_path(
            original_filepath=original_filepath,
            output_dir=output_dir,
            target_format=target_format
        )

    @staticmethod
    def open_output_folder(output_dir: str) -> bool:
        """
        Membuka folder hasil konversi di sistem operasi pengguna (Explorer/Finder).
        """
        if os.path.exists(output_dir):
            app_logger.info(f"Membuka folder output: {output_dir}")
            return Helpers.open_folder_in_explorer(output_dir)
        else:
            app_logger.error(f"Gagal membuka folder. Path tidak ditemukan: {output_dir}")
            return False