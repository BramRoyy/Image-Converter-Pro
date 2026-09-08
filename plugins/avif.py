from utils.logger import app_logger

class AvifPlugin:
    """Plugin untuk menambahkan dukungan format AVIF menggunakan library yang sama (pillow-heif)."""
    
    @staticmethod
    def register():
        try:
            import pillow_heif
            # Mendaftarkan opener AVIF ke Pillow
            pillow_heif.register_avif_opener()
            app_logger.info("Plugin AVIF berhasil diaktifkan.")
            return True
        except ImportError:
            app_logger.warning("Modul 'pillow-heif' tidak ditemukan. Format AVIF dinonaktifkan.")
            return False