import os
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.detector import ImageDetector
from core.converter import ImageConverter
from models.image_info import ImageInfo

class ImageService:
    """
    Service layer yang menjembatani GUI dengan Core Engine.
    Semua logika orkestrasi (mengatur alur data) terjadi di sini.
    """

    @staticmethod
    def analyze_file(file_path: str) -> ImageInfo:
        """
        1. Meminta Core (Detector) menganalisis file mentah.
        2. Membungkus hasilnya menggunakan Model (ImageInfo) agar siap dipakai GUI.
        """
        raw_data = ImageDetector.analyze(file_path)
        image_info = ImageInfo.from_dict(raw_data)
        
        return image_info

    @staticmethod
    def convert_image(
        image_info: ImageInfo, 
        output_dir: str, 
        target_format: str, 
        quality: int = 90, 
        target_width: int = None,
        target_height: int = None,
        remove_bg: bool = False,
        bg_color: str = "TRANSPARENT"
    ) -> str:
        """
        Menjalankan proses konversi, opsi hapus background (AI) + warna latar, 
        serta mengamankan penamaan file agar tidak tertimpa (overwrite).
        Format keluaran selalu mematuhi pilihan pengguna.
        """
        if not image_info.is_valid:
            raise ValueError(f"File '{image_info.filename}' tidak valid dan tidak bisa dikonversi.")

        # 1. Pastikan folder output eksis
        os.makedirs(output_dir, exist_ok=True)

        # 2. Ekstrak nama tanpa ekstensi
        base_name = Path(image_info.filepath).stem
        
        # 3. Tentukan ekstensi baru sesuai pilihan pengguna
        ext = 'jpg' if target_format.upper() in ['JPG', 'JPEG'] else target_format.lower()
        
        # 4. Susun target path dan cegah Overwrite
        output_filename = f"{base_name}.{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        counter = 1
        while os.path.exists(output_path):
            output_filename = f"{base_name}_{counter}.{ext}"
            output_path = os.path.join(output_dir, output_filename)
            counter += 1

        # Update status model ke Converting
        image_info.status = "Converting"

        try:
            # 5. Perintahkan Core (Converter) untuk memproses
            success = ImageConverter.process_and_save(
                input_path=image_info.filepath,
                output_path=output_path,
                output_format=target_format,
                quality=quality,
                target_width=target_width,
                target_height=target_height,
                remove_bg=remove_bg,
                bg_color=bg_color
            )
            
            if success:
                image_info.status = "Done"
                return output_path
                
        except Exception as e:
            image_info.status = "Error"
            image_info.error_message = str(e)
            raise e