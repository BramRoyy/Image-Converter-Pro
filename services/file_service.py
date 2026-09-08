import os
import shutil
from pathlib import Path
from tkinter import filedialog
from typing import List, Optional

import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import TEMP_DIR, OUTPUT_DIR
from utils.filetypes import get_file_dialog_filters

class FileService:
    """
    Mengelola interaksi aplikasi dengan File System OS.
    Termasuk membuka dialog pemilihan file dan manajemen direktori.
    """

    @staticmethod
    def select_files() -> List[str]:
        """
        Membuka jendela dialog OS agar user bisa memilih banyak gambar sekaligus.
        Mengembalikan list path file yang dipilih.
        """
        file_paths = filedialog.askopenfilenames(
            title="Pilih Gambar untuk Dikonversi",
            filetypes=get_file_dialog_filters()
        )
        return list(file_paths)

    @staticmethod
    def select_directory(initial_dir: Optional[str] = None) -> Optional[str]:
        """
        Membuka jendela dialog OS untuk memilih folder tujuan (Output Folder).
        """
        if initial_dir is None:
            initial_dir = str(OUTPUT_DIR)
            
        dir_path = filedialog.askdirectory(
            title="Pilih Folder Output",
            initialdir=initial_dir
        )
        return dir_path if dir_path else None

    @staticmethod
    def setup_directories():
        """Memastikan folder temp, output, dan logs tersedia saat aplikasi baru dibuka."""
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def cleanup_temp():
        """
        Menghapus seluruh isi folder temp. 
        Sangat penting dipanggil saat aplikasi ditutup agar cache hilang.
        """
        if TEMP_DIR.exists():
            try:
                # Menghapus seluruh folder temp beserta isinya
                shutil.rmtree(TEMP_DIR)
                # Buat ulang folder temp kosong agar tidak error saat aplikasi dibuka lagi
                TEMP_DIR.mkdir(parents=True, exist_ok=True)
                print("✅ Folder temp berhasil dibersihkan.")
            except Exception as e:
                print(f"⚠️ Gagal membersihkan folder temp: {e}")

# --- TESTING SCRIPT ---
if __name__ == "__main__":
    import tkinter as tk
    
    # Root dummy diperlukan agar jendela filedialog Tkinter bisa muncul
    root = tk.Tk()
    root.withdraw() 
    
    print("Menguji File Service...\n")
    
    # 1. Tes Setup Direktori
    FileService.setup_directories()
    print("1. Setup folder Temp dan Output: Berhasil")
    
    # 2. Tes Pilih File
    print("2. Silakan pilih beberapa gambar pada jendela yang muncul...")
    files = FileService.select_files()
    if files:
        print(f"   -> Anda memilih {len(files)} file.")
    else:
        print("   -> Batal memilih file.")
        
    # 3. Tes Pilih Folder
    print("\n3. Silakan pilih folder untuk Output...")
    folder = FileService.select_directory()
    if folder:
        print(f"   -> Folder Output terpilih: {folder}")
    else:
        print("   -> Batal memilih folder.")
        
    # 4. Tes Cleanup
    print("\n4. Membersihkan folder temporary...")
    FileService.cleanup_temp()
    
    root.destroy()