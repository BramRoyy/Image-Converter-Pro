from rembg import remove
from PIL import Image
import os
from utils.logger import app_logger

class BackgroundRemoverPlugin:
    """Plugin khusus untuk menghapus background gambar menggunakan AI (rembg)."""
    
    @staticmethod
    def process(input_path: str, output_path: str) -> bool:
        """
        Menghapus background dari gambar input dan menyimpannya ke output_path.
        WAJIB disimpan dalam format yang mendukung transparansi (PNG/WEBP).
        """
        if not os.path.exists(input_path):
            return False
            
        try:
            with Image.open(input_path) as img:
                # Proses ajaib penghapusan background
                app_logger.info(f"Memproses hapus background untuk: {input_path}")
                result_img = remove(img)
                ext = output_path.lower().split('.')[-1]
                if ext not in ['png', 'webp', 'tiff']:
                    output_path = os.path.splitext(output_path)[0] + ".png"
                
                result_img.save(output_path)
                app_logger.info(f"Berhasil menghapus background, disimpan di: {output_path}")
                
                return True
                
        except Exception as e:
            app_logger.error(f"Gagal menghapus background: {e}")
            return False

    @staticmethod
    def register() -> bool:
        """Metode inisialisasi plugin."""
        try:
            import rembg
            app_logger.info("Plugin Background Remover (rembg) terdeteksi dan aktif.")
            return True
        except ImportError:
            app_logger.error("Modul 'rembg' belum terinstal. Silakan jalankan: pip install rembg")
            return False