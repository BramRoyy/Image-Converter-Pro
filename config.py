import json
import os
from pathlib import Path
from models.settings import AppSettings
from utils.constants import BASE_DIR
from utils.logger import app_logger

class ConfigManager:
    """Mengelola proses load/save pengaturan pengguna ke file config.json"""
    CONFIG_FILE = BASE_DIR / "config.json"

    @staticmethod
    def load_config() -> AppSettings:
        if not ConfigManager.CONFIG_FILE.exists():
            return AppSettings() # Kembalikan default jika file belum ada

        try:
            with open(ConfigManager.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return AppSettings(**data)
        except Exception as e:
            app_logger.error(f"Gagal memuat config.json: {e}")
            return AppSettings()

    @staticmethod
    def save_config(settings: AppSettings) -> bool:
        try:
            # dataclass -> dictionary
            data = settings.__dict__
            with open(ConfigManager.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            app_logger.error(f"Gagal menyimpan config.json: {e}")
            return False