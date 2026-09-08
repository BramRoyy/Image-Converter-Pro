from plugins.heic import HeicPlugin
from plugins.avif import AvifPlugin
from plugins.webp import WebpPlugin
from plugins.pdf import PdfPlugin
from utils.logger import app_logger

def initialize_plugins():
    """
    Fungsi ini dipanggil satu kali saat aplikasi start.
    Tugasnya mendaftarkan dan memverifikasi semua ekstensi format ke dalam Pillow.
    """
    app_logger.info("Memuat sistem plugin...")
    
    webp_status = WebpPlugin.register()
    pdf_status = PdfPlugin.register()
    heic_status = HeicPlugin.register()
    avif_status = AvifPlugin.register()
    
    if webp_status and pdf_status and heic_status and avif_status:
        app_logger.info("Semua plugin berhasil dimuat dan diverifikasi.")
    else:
        app_logger.warning("Beberapa plugin tidak dapat dimuat. Cek log di atas.")