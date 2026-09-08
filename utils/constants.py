import os
from pathlib import Path

# Mendapatkan absolute path dari direktori root aplikasi (2 level ke atas dari folder utils)
BASE_DIR = Path(__file__).resolve().parent.parent

# Informasi Aplikasi
APP_NAME = "Image Converter Pro"
APP_VERSION = "1.0.0"

# Mendefinisikan Path Folder Utama
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# Standar Ukuran Jendela
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600