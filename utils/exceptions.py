class ImageConverterError(Exception):
    """Base exception untuk semua error di aplikasi Image Converter."""
    pass

class UnsupportedFormatError(ImageConverterError):
    """Dilempar ketika format gambar tidak dikenali."""
    pass

class FileTooLargeError(ImageConverterError):
    """Dilempar ketika ukuran file melebihi batas (RAM safety)."""
    pass

class ConversionFailedError(ImageConverterError):
    """Dilempar ketika Core Engine gagal memproses gambar."""
    pass