from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from models.image_info import ImageInfo

@dataclass
class ConvertTask:
    """Model data untuk satu tugas di dalam antrean (queue)."""
    image: ImageInfo
    target_format: str
    target_quality: int = 90
    remove_metadata: bool = False
    
    # Status Task
    output_path: Optional[str] = None
    status: str = "Pending"
    start_time: Optional[datetime] = None
    finish_time: Optional[datetime] = None