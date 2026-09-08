from PIL import features
from utils.logger import app_logger

class WebpPlugin:
    """
    Plugin untuk memverifikasi dukungan format WEBP.
    Meskipun Pillow modern sudah mendukung WEBP secara bawaan,
    modul ini bertugas memastikan fitur tersebut benar-benar aktif di sistem pengguna.
    """
    
    @staticmethod
    def register():
        # Mengecek apakah modul Pillow saat ini memiliki fitur WebP
        if features.check('webp'):
            app_logger.info("Plugin WEBP (Native) terdeteksi dan aktif.")
            return True
        else:
            app_logger.warning("Pillow tidak memiliki dukungan WEBP di sistem ini! Beberapa konversi mungkin gagal.")
            return False