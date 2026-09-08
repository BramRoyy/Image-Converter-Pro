from utils.logger import app_logger

class HeicPlugin:
    """Plugin untuk menambahkan dukungan format HEIC/HEIF ke dalam ekosistem Pillow."""
    
    @staticmethod
    def register():
        try:
            import pillow_heif
            # Mendaftarkan opener HEIF ke Pillow
            pillow_heif.register_heif_opener()
            app_logger.info("Plugin HEIC berhasil diaktifkan.")
            return True
        except ImportError:
            app_logger.warning("Modul 'pillow-heif' tidak ditemukan. Format HEIC dinonaktifkan.")
            return False