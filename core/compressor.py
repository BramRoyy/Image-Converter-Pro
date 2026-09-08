class ImageCompressor:
    """
    Bertugas mengatur logika kompresi untuk berbagai format gambar.
    Menerjemahkan input dari user (Quality/Lossless) menjadi parameter yang dimengerti oleh Pillow.
    """

    @staticmethod
    def get_save_parameters(target_format: str, quality: int = 90, lossless: bool = False) -> dict:
        """
        Menghasilkan dictionary berisi kwargs (keyword arguments) untuk method img.save() di Pillow.
        """
        fmt = target_format.upper()
        params = {}

        if fmt in ['JPEG', 'JPG']:
            # JPEG tidak mendukung lossless murni, tapi bisa diatur quality dan optimize
            params['quality'] = quality
            params['optimize'] = True
            
        elif fmt == 'WEBP':
            if lossless:
                params['lossless'] = True
            else:
                params['quality'] = quality
                params['method'] = 4  # Kompresi menengah (0=cepat, 6=paling lambat tapi file kecil)
                
        elif fmt == 'PNG':
            # PNG selalu lossless, kompresi di sini berarti mengoptimalkan ukuran file tanpa mengurangi kualitas piksel
            params['optimize'] = True
            params['compress_level'] = 9 if quality < 50 else 6 # 9 adalah kompresi maksimal (lambat)
            
        elif fmt == 'TIFF':
            if not lossless:
                params['compression'] = 'jpeg'
            else:
                params['compression'] = 'tiff_deflate'

        return params