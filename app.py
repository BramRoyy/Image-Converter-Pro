"""
Image Converter Pro - Main Application Entry Point
"""

from plugins import initialize_plugins
from gui import MainWindow, SplashScreen
from utils.logger import app_logger

class Application:
    """
    Class utama untuk menginisialisasi sistem sebelum GUI dijalankan.
    """
    def __init__(self):
        app_logger.info("Memulai aplikasi Image Converter Pro...")
        
        # 1. Inisialisasi plugin pendukung (Webp, dll)
        initialize_plugins()
        
        # 2. Buat MainWindow tapi sembunyikan terlebih dahulu
        self.window = MainWindow()
        self.window.withdraw()
        
        # 3. Tampilkan SplashScreen sebagai child window
        self.splash = SplashScreen(
            parent=self.window, 
            on_complete_callback=self.show_main_window
        )

    def show_main_window(self):
        """Menampilkan kembali MainWindow setelah Splash Screen selesai."""
        self.window.deiconify()

    def run(self):
        """Menjalankan main loop aplikasi."""
        app_logger.info("Memulai GUI Main Loop...")
        self.window.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()