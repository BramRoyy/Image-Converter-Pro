import os
from pathlib import Path

class ImageExporter:
    """
    Mengelola logika ekspor file (menyiapkan folder & nama file output yang aman).
    """

    @staticmethod
    def generate_safe_output_path(original_filepath: str, output_dir: str, target_format: str) -> str:
        """
        Membentuk path tujuan dengan mengecek apakah file dengan nama yang sama sudah ada.
        Jika ada, tambahkan angka _1, _2, dst untuk mencegah Overwrite (tertimpa).
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Ekstrak nama asli ('foto_kucing.png' -> 'foto_kucing')
        base_name = Path(original_filepath).stem
        
        # Normalisasi ekstensi target
        if target_format.upper() == 'JPEG':
            ext = 'jpg'
        else:
            ext = target_format.lower()
        
        output_filename = f"{base_name}.{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        # Logika iterasi Auto-Rename
        counter = 1
        while os.path.exists(output_path):
            output_filename = f"{base_name}_{counter}.{ext}"
            output_path = os.path.join(output_dir, output_filename)
            counter += 1
            
        return output_path
