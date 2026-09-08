import os
import sys
import subprocess
import re
from pathlib import Path

class Helpers:
    """
    Kumpulan fungsi bantuan (utility functions) yang bisa dipanggil dari mana saja.
    Tidak bergantung pada class atau module lain.
    """

    @staticmethod
    def open_folder_in_explorer(folder_path: str) -> bool:
        """
        Membuka folder secara langsung di File Explorer (Windows), 
        Finder (Mac), atau File Manager (Linux).
        Sangat berguna untuk tombol "Buka Folder Output" di GUI.
        """
        path_obj = Path(folder_path)
        if not path_obj.exists():
            return False

        try:
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
            return True
        except Exception as e:
            print(f"Gagal membuka folder: {e}")
            return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Membersihkan nama file dari karakter ilegal yang ditolak oleh OS (Windows/Mac).
        Contoh: "gambar:ku?.png" -> "gambarku.png"
        """
        # Menghapus karakter ilegal: < > : " / \ | ? *
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    @staticmethod
    def format_time_elapsed(seconds: float) -> str:
        """
        Mengubah waktu (detik) menjadi format string yang rapi untuk UI.
        Contoh: 65 -> "01:05" (MM:SS)
        """
        mins, secs = divmod(int(seconds), 60)
        return f"{mins:02d}:{secs:02d}"

# --- TESTING SCRIPT ---
if __name__ == "__main__":
    print("Menguji Helpers...")
    
    # 1. Tes Format Waktu
    print(f"Waktu 125 detik = {Helpers.format_time_elapsed(125)}")
    
    # 2. Tes Sanitize (Pembersihan nama file)
    nama_kotor = 'foto?liburan:bali*.jpg'
    print(f"Nama dibersihkan: {Helpers.sanitize_filename(nama_kotor)}")
    
    # 3. Tes Buka Folder (Akan membuka folder Utils ini di Explorer Anda)
    print("Membuka folder saat ini di File Explorer...")
    Helpers.open_folder_in_explorer(os.path.dirname(os.path.abspath(__file__)))