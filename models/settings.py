from dataclasses import dataclass
from typing import Optional

@dataclass
class AppSettings:
    """Model data untuk menyimpan preferensi pengguna."""
    output_folder: Optional[str] = None
    default_format: str = "JPEG"
    quality: int = 90
    remove_metadata: bool = False
    theme: str = "System"
    language: str = "ID"