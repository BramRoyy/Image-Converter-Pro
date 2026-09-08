from PIL import Image, ExifTags
import os

class MetadataExtractor:
    """
    Bertugas mengekstrak dan memanipulasi informasi metadata (EXIF, ICC Profile)
    dari sebuah file gambar.
    """

    @staticmethod
    def extract_exif(image_path: str) -> dict:
        """
        Membaca data EXIF dari gambar (biasanya foto dari kamera/HP).
        Mengembalikan dictionary berisi informasi yang sudah terbaca manusia.
        """
        exif_data = {}
        try:
            with Image.open(image_path) as img:
                raw_exif = img.getexif()
                
                if not raw_exif:
                    return exif_data
                    
                # Menerjemahkan Tag ID (angka) menjadi nama (string) menggunakan ExifTags
                for tag_id, value in raw_exif.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    exif_data[tag_name] = value
                    
        except Exception as e:
            # Jika gambar tidak punya EXIF atau rusak
            print(f"Peringatan: Gagal membaca metadata EXIF - {e}")
            
        return exif_data

    @staticmethod
    def strip_metadata(img: Image.Image) -> Image.Image:
        """
        Menghapus seluruh metadata (EXIF, Profil Warna) dari object gambar.
        Berguna untuk fitur 'Remove Metadata for Privacy'.
        Mengembalikan gambar baru yang sudah bersih.
        """
        # Membuat gambar baru dengan memori mentah yang sama, tapi tanpa membawa dictionary .info bawaannya
        data = list(img.getdata())
        image_without_metadata = Image.new(img.mode, img.size)
        image_without_metadata.putdata(data)
        
        return image_without_metadata