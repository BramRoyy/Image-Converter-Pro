from PIL import Image
from typing import List
from utils.logger import app_logger

class PdfPlugin:
    """Plugin khusus untuk menangani pembuatan dokumen PDF dari gambar."""
    
    @staticmethod
    def images_to_pdf(image_paths: List[str], output_path: str) -> bool:
        """
        Menggabungkan kumpulan gambar menjadi satu file PDF.
        """
        if not image_paths:
            return False
            
        images = []
        try:
            for path in image_paths:
                img = Image.open(path)
                # PDF di Pillow hanya mendukung RGB (tanpa Alpha/Transparansi)
                if img.mode in ('RGBA', 'P', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                images.append(img)

            if images:
                first_image = images[0]
                other_images = images[1:]
                
                # Pillow memiliki fitur bawaan menyimpan multiple frame menjadi PDF
                first_image.save(
                    output_path, 
                    "PDF", 
                    resolution=100.0, 
                    save_all=True, 
                    append_images=other_images
                )
                app_logger.info(f"Berhasil membuat PDF di: {output_path}")
                return True
                
        except Exception as e:
            app_logger.error(f"Gagal membuat PDF: {e}")
            raise e
            
        return False

    @staticmethod
    def register() -> bool:
        """
        Metode wajib yang dipanggil oleh system plugin saat aplikasi pertama kali dibuka.
        Mengembalikan True jika plugin berhasil diinisialisasi.
        """
        try:
            # Memastikan plugin siap dan mencatat statusnya ke log
            app_logger.info("Plugin PDF (Native Pillow) terdeteksi dan aktif.")
            return True
        except Exception as e:
            app_logger.error(f"Gagal menginisialisasi PdfPlugin: {e}")
            return False