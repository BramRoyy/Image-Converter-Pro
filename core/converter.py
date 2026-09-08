import os
import sys
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.compressor import ImageCompressor
from core.metadata import MetadataExtractor

class ImageConverter:
    _sessions = {}

    COLOR_MAP = {
        "RED": (219, 39, 39),
        "BLUE": (37, 99, 235),
        "GREEN": (34, 197, 94),
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0)
    }

    @classmethod
    def _get_session(cls, model_name: str = "birefnet-general"):
        if model_name not in cls._sessions:
            cls._sessions[model_name] = new_session(model_name)
        return cls._sessions[model_name]

    @classmethod
    def remove_background(cls, image: Image.Image, bg_color: str = "TRANSPARENT") -> Image.Image:
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')

        session = cls._get_session("birefnet-general")
        output = remove(image, session=session)

        color_key = bg_color.upper()
        if color_key in cls.COLOR_MAP:
            rgb_val = cls.COLOR_MAP[color_key]
            solid_bg = Image.new("RGBA", output.size, rgb_val + (255,))
            solid_bg.paste(output, mask=output.split()[-1])
            return solid_bg

        return output

    @staticmethod
    def resize_image(img: Image.Image, target_width: int = None, target_height: int = None) -> Image.Image:
        """Mengubah ukuran dimensi gambar berdasarkan piksel kustom (Width x Height)."""
        orig_w, orig_h = img.size

        # Jika kedua kolom kosong atau 0, kembalikan gambar asli
        if not target_width and not target_height:
            return img

        # 1. Jika hanya Lebar yang diisi, hitung Tinggi proporsional
        if target_width and not target_height:
            ratio = target_width / float(orig_w)
            target_height = int(float(orig_h) * ratio)

        # 2. Jika hanya Tinggi yang diisi, hitung Lebar proporsional
        elif target_height and not target_width:
            ratio = target_height / float(orig_h)
            target_width = int(float(orig_w) * ratio)

        # Pastikan nilai minimal 1px
        target_width = max(1, target_width)
        target_height = max(1, target_height)

        return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    @staticmethod
    def process_and_save(input_path: str, output_path: str, output_format: str = None, 
                         quality: int = 90, target_width: int = None, target_height: int = None,
                         remove_metadata: bool = False, remove_bg: bool = False, 
                         bg_color: str = "TRANSPARENT") -> bool:
        try:
            with Image.open(input_path) as img:
                if not output_format:
                    output_format = Path(output_path).suffix.lstrip('.').upper()
                if output_format == 'JPG':
                    output_format = 'JPEG'

                if remove_bg:
                    img = ImageConverter.remove_background(img, bg_color=bg_color)

                # Resize Dimensi Kustom
                if target_width or target_height:
                    img = ImageConverter.resize_image(img, target_width=target_width, target_height=target_height)

                img_processed = ImageConverter._handle_color_mode(img, output_format)

                if remove_metadata:
                    img_processed = MetadataExtractor.strip_metadata(img_processed)

                save_kwargs = ImageCompressor.get_save_parameters(
                    target_format=output_format, 
                    quality=quality, 
                    lossless=(quality == 100)
                )

                img_processed.save(output_path, format=output_format, **save_kwargs)
                return True

        except Exception as e:
            raise RuntimeError(f"Gagal mengonversi file {input_path}. Detail: {str(e)}")

    @staticmethod
    def _handle_color_mode(img: Image.Image, output_format: str) -> Image.Image:
        formats_without_alpha = ['JPEG', 'BMP']
        if output_format in formats_without_alpha:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                return background
            elif img.mode != 'RGB':
                return img.convert('RGB')
        return img