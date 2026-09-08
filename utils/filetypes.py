# Daftar format input yang didukung (Format baca)
SUPPORTED_INPUT_FORMATS = [
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", 
    ".gif", ".tiff", ".ico", ".heic", ".avif"
]

# Daftar format output yang tersedia di versi 1 (Format simpan)
SUPPORTED_OUTPUT_FORMATS = [
    "JPG", "PNG", "WEBP", "BMP", "TIFF", "ICO", "PDF"
]

def get_file_dialog_filters():
    """
    Membentuk filter format yang digunakan untuk jendela dialog OS 'Open File'.
    Agar user hanya bisa memilih file yang didukung oleh aplikasi.
    """
    extensions = ";*".join(SUPPORTED_INPUT_FORMATS)
    return [
        ("Image Files", f"*{extensions}"),
        ("All Files", "*.*")
    ]