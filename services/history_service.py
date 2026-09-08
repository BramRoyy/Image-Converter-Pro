import json
from datetime import datetime
import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import LOG_DIR
from utils.logger import app_logger

class HistoryService:
    """
    Service layer untuk mencatat dan membaca riwayat konversi pengguna.
    Data disimpan dalam format JSON agar ringan dan mudah dibaca.
    """
    HISTORY_FILE = LOG_DIR / "history.json"

    @staticmethod
    def add_record(filename: str, source_format: str, target_format: str, status: str, output_path: str = ""):
        """Menambahkan satu catatan riwayat konversi baru."""
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "source_format": source_format,
            "target_format": target_format,
            "status": status,
            "output_path": output_path
        }
        
        history = HistoryService.get_history()
        history.append(record)
        HistoryService._save_history(history)

    @staticmethod
    def get_history() -> list:
        """Mengambil seluruh riwayat konversi dari file JSON."""
        if not HistoryService.HISTORY_FILE.exists():
            return []
            
        try:
            with open(HistoryService.HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            app_logger.error(f"Gagal membaca riwayat: {e}")
            return []

    @staticmethod
    def clear_history():
        """Menghapus seluruh catatan riwayat."""
        if HistoryService.HISTORY_FILE.exists():
            try:
                HistoryService.HISTORY_FILE.unlink() # Menghapus file
                app_logger.info("Riwayat konversi berhasil dihapus.")
            except Exception as e:
                app_logger.error(f"Gagal menghapus riwayat: {e}")

    @staticmethod
    def _save_history(data: list):
        """Fungsi internal untuk menyimpan list ke file JSON."""
        try:
            with open(HistoryService.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            app_logger.error(f"Gagal menyimpan riwayat: {e}")