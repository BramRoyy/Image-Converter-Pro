import logging
import os
import sys

# Memastikan module root bisa diakses saat file dites langsung
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import LOG_DIR

def setup_logger():
    """
    Mengonfigurasi sistem logging.
    Akan mencatat pesan error ke file logs/app.log dan juga ke terminal.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "app.log"

    # Membuat instance logger utama
    logger = logging.getLogger("ImageConverterPro")
    logger.setLevel(logging.DEBUG)

    # Menentukan format penulisan (Tanggal - Level Error - Pesan)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler 1: Menyimpan ke file .log (Hanya menyimpan info dan error)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Handler 2: Menampilkan ke terminal (Untuk keperluan kita saat coding)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Mencegah duplikasi log jika fungsi ini terpanggil berkali-kali
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Mengekspos variabel app_logger agar bisa di-import oleh file lain
app_logger = setup_logger()


# --- TESTING SCRIPT ---
if __name__ == "__main__":
    app_logger.info("Aplikasi dijalankan.")
    app_logger.warning("Ini adalah simulasi peringatan memori penuh.")
    app_logger.error("Simulasi error: Gagal menyimpan file karena akses ditolak.")
    print("\n✅ Cek folder 'logs' di dalam proyek Anda, seharusnya ada file app.log yang terbuat!")