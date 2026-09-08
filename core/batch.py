import threading
from typing import List, Callable, Any

class BatchProcessor:
    """
    Mengelola antrean proses konversi banyak file sekaligus (Batch).
    Berjalan di background thread agar GUI tidak Freeze/Not Responding.
    """

    def __init__(self, 
                 items: List[Any], 
                 process_func: Callable[[Any], None], 
                 on_progress: Callable[[int, int, Any], None] = None,
                 on_finish: Callable[[int, int, bool], None] = None,
                 on_error: Callable[[Any, Exception], None] = None):
        
        self.items = items
        self.process_func = process_func
        self.on_progress = on_progress
        self.on_finish = on_finish
        self.on_error = on_error
        
        # Threading Event digunakan sebagai saklar on/off yang aman antar-thread
        self._cancel_event = threading.Event()
        self._thread = None

    def start(self):
        """Memulai proses batch di background thread."""
        if not self.items:
            if self.on_finish:
                self.on_finish(0, 0, False)
            return

        self._cancel_event.clear()  # Pastikan saklar batal dimatikan
        # daemon=True artinya thread ini otomatis mati jika aplikasi utama ditutup
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def cancel(self):
        """Memerintahkan thread untuk berhenti sesegera mungkin."""
        self._cancel_event.set()

    def _run(self):
        """Looping utama yang berjalan di background."""
        total = len(self.items)
        success_count = 0

        for index, item in enumerate(self.items):
            # Cek apakah user menekan tombol Cancel
            if self._cancel_event.is_set():
                break

            try:
                # Eksekusi fungsi konversi (yang di-inject oleh Service)
                self.process_func(item)
                success_count += 1
            except Exception as e:
                # Jika 1 gambar error (misal file corrupt), lewati dan laporkan,
                # jangan hentikan seluruh batch
                if self.on_error:
                    self.on_error(item, e)

            # Laporkan progres ke GUI
            if self.on_progress:
                self.on_progress(index + 1, total, item)

        # Laporkan bahwa seluruh antrean telah selesai
        if self.on_finish:
            is_cancelled = self._cancel_event.is_set()
            self.on_finish(success_count, total, is_cancelled)