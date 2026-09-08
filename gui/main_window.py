import os
import ctypes
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

# Import Komponen GUI
from gui.dragdrop import DragDropArea
from gui.sidebar import Sidebar
from gui.toolbar import Toolbar
from gui.statusbar import StatusBar
from gui.widgets import QueueItemWidget
from gui.dialogs import Dialogs
from gui.preview import ImagePreviewPanel

# Import Services & Core
from services import FileService, ImageService, ExportService, HistoryService
from core.batch import BatchProcessor
from config import ConfigManager
from utils.constants import OUTPUT_DIR

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CTkTkinterDnD(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class MainWindow(CTkTkinterDnD):
    def __init__(self):
        super().__init__()

        # --- SET ICON & TASKBAR WINDOWS ---
        try:
            myappid = 'mycompany.imageconverterpro.app.2.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        icon_path = os.path.join("assets", "icons", "logo.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.title("Image Converter Pro")
        # --- PERBAIKAN: Diperluas menjadi 1200x650 agar Toolbar muat sempurna ---
        self.geometry("1200x650")
        self.minsize(1150, 550)

        # --- STATE & CONFIG ---
        self.config = ConfigManager.load_config()
        self.image_queue = []       
        self.queue_widgets = {}     
        self.output_folder = self.config.output_folder or str(OUTPUT_DIR) 
        self.is_converting = False  
        self.current_preview_path = None

        # 3 Kolom: Sidebar (0) | DragDrop (1) | Preview (2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self._setup_ui()

    def _setup_ui(self):
        # 1. TOOLBAR
        self.toolbar = Toolbar(
            self, height=60, corner_radius=0,
            on_select_folder=self.handle_select_folder,
            on_convert=self.handle_convert
        )
        self.toolbar.grid(row=0, column=0, columnspan=3, sticky="new")
        self.toolbar.format_var.set(self.config.default_format)

        # 2. SIDEBAR
        self.sidebar = Sidebar(self, width=280, corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.btn_clear.configure(command=self.clear_all_queue)

        # 3. MAIN CONTENT
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=15)
        
        self.dnd_area = DragDropArea(
            master=self.main_frame, 
            on_drop_callback=self.process_incoming_files,
            on_browse_callback=self.handle_add_file
        )
        self.dnd_area.pack(expand=True, fill="both")

        # 4. PREVIEW PANEL
        self.preview_panel = ImagePreviewPanel(self, width=250, corner_radius=10)
        self.preview_panel.grid(row=1, column=2, sticky="nsew", padx=(0, 15), pady=15)
        self.preview_panel.grid_propagate(False)

        # 5. STATUS BAR
        self.statusbar = StatusBar(self, height=35, corner_radius=0)
        self.statusbar.grid(row=2, column=0, columnspan=3, sticky="sew")
        self.statusbar.set_status(f"Folder Output: {self.output_folder}")

    # --- LOGIKA UI CONTROLLER ---

    def process_incoming_files(self, file_paths):
        if self.is_converting:
            Dialogs.show_warning("Sibuk", "Tunggu konversi selesai.")
            return

        added_count = 0
        for path in file_paths:
            if path in self.queue_widgets: continue

            img_info = ImageService.analyze_file(path)
            self.image_queue.append(img_info)

            card = QueueItemWidget(
                master=self.sidebar.queue_frame,
                filename=img_info.filename,
                filepath=img_info.filepath,
                on_remove_callback=self.remove_item_from_queue,
                on_click_callback=self.show_preview
            )
            card.pack(fill="x", pady=2, ipady=2)
            
            if img_info.is_valid:
                img_info.status = "Ready"
                card.update_status("Ready")
            else:
                card.update_status("Error")

            self.queue_widgets[img_info.filepath] = card
            added_count += 1

            if len(self.image_queue) == 1:
                self.show_preview(img_info.filepath)

        self.statusbar.set_status(f"{added_count} file ditambahkan. Total: {len(self.image_queue)}")

    def show_preview(self, filepath):
        self.preview_panel.load_preview(filepath)
        self.current_preview_path = filepath

    def handle_add_file(self):
        files = FileService.select_files()
        if files: self.process_incoming_files(files)

    def handle_select_folder(self):
        folder = FileService.select_directory(initial_dir=self.output_folder)
        if folder:
            self.output_folder = folder
            self.statusbar.set_status(f"Folder Output: {self.output_folder}")
            self.config.output_folder = folder
            ConfigManager.save_config(self.config)

    def remove_item_from_queue(self, widget: QueueItemWidget):
        if self.is_converting: return
        path = widget.filepath
        self.image_queue = [item for item in self.image_queue if item.filepath != path]
        if path in self.queue_widgets: del self.queue_widgets[path]
        if path == self.current_preview_path:
            self.preview_panel.clear()
            self.current_preview_path = None
        self.statusbar.set_status(f"Sisa antrean: {len(self.image_queue)}")

    def clear_all_queue(self):
        if self.is_converting: return
        for widget in self.queue_widgets.values(): widget.destroy()
        self.image_queue.clear()
        self.queue_widgets.clear()
        self.preview_panel.clear()
        self.current_preview_path = None
        self.statusbar.reset_progress()

    # --- LOGIKA BATCH PROCESSING ---

    def handle_convert(self):
        valid_queue = [img for img in self.image_queue if img.is_valid]
        if not valid_queue:
            Dialogs.show_error("Antrean Kosong", "Tidak ada gambar valid untuk diproses.")
            return

        # 1. Ambil Parameter dari Toolbar
        target_format = self.toolbar.get_selected_format()
        
        remove_bg = False
        if hasattr(self.toolbar, "get_remove_bg"):
            remove_bg = self.toolbar.get_remove_bg()

        bg_color = "TRANSPARENT"
        if hasattr(self.toolbar, "get_bg_color_key"):
            bg_color = self.toolbar.get_bg_color_key()

        # --- LOGIKA DIALOG PERINGATAN (CEK KONFLIK JPG & TRANSPARANSI) ---
        if remove_bg and bg_color == "TRANSPARENT" and target_format.upper() in ["JPG", "JPEG"]:
            user_agree = Dialogs.ask_confirmation(
                "Peringatan Format JPG",
                "Format JPG tidak mendukung latar belakang transparan.\n"
                "Bagian yang transparan akan otomatis diisi dengan warna PUTIH.\n\n"
                "Apakah Anda ingin tetap melanjutkan konversi?"
            )
            if not user_agree:
                return  # Batalkan konversi agar pengguna bisa atur ulang opsi di toolbar

        # 2. Ambil Parameter Tambahan
        quality = 90
        if hasattr(self.toolbar, "get_quality"):
            quality = self.toolbar.get_quality()

        target_w, target_h = (None, None)
        if hasattr(self.toolbar, "get_custom_dimensions"):
            target_w, target_h = self.toolbar.get_custom_dimensions()

        # 3. Mulai Proses Konversi (Jika lolos/disetujui)
        self.is_converting = True
        self.statusbar.reset_progress()
        self.toolbar.btn_convert.configure(state="disabled", text="⏳ Memproses...")

        for img in valid_queue:
            img.status = "Converting"
            if img.filepath in self.queue_widgets:
                self.queue_widgets[img.filepath].update_status("Converting")

        self.update_idletasks()

        self.config.default_format = target_format
        ConfigManager.save_config(self.config)

        def process_single_image(img_info):
            return ImageService.convert_image(
                image_info=img_info, 
                output_dir=self.output_folder, 
                target_format=target_format,
                quality=quality,
                target_width=target_w,
                target_height=target_h,
                remove_bg=remove_bg,
                bg_color=bg_color
            )

        def on_progress(current, total, img_info):
            self.after(0, lambda: self._update_ui_progress(current, total, img_info))

        def on_error(img_info, error, *args):
            self.after(0, lambda: self._update_ui_error(img_info, error))

        def on_finish(success_count, total, is_cancelled):
            self.after(0, lambda: self._update_ui_finish(success_count, total, target_format))

        processor = BatchProcessor(
            items=valid_queue, 
            process_func=process_single_image, 
            on_progress=on_progress,
            on_error=on_error, 
            on_finish=on_finish
        )
        processor.start()

    def _update_ui_progress(self, current, total, img_info):
        self.statusbar.update_progress(current, total)
        if img_info.filepath in self.queue_widgets:
            self.queue_widgets[img_info.filepath].update_status("Done" if img_info.status == "Done" else "Converting")

    def _update_ui_error(self, img_info, error):
        if img_info.filepath in self.queue_widgets:
            self.queue_widgets[img_info.filepath].update_status("Error")

    def _update_ui_finish(self, success_count, total, target_format):
        self.is_converting = False
        self.toolbar.btn_convert.configure(state="normal", text="🚀 Mulai Konversi")
        self.statusbar.set_status(f"Selesai! Berhasil: {success_count}/{total} file.")
        self.statusbar.update_progress(total, total)

        self.after(3000, self.statusbar.reset_progress)

        for img in self.image_queue:
            if img.is_valid and img.status in ["Done", "Error"]:
                HistoryService.add_record(
                    filename=img.filename,
                    source_format=os.path.splitext(img.filepath)[1].upper().lstrip('.'),
                    target_format=target_format,
                    status=img.status
                )
        
        if success_count > 0:
            if Dialogs.ask_confirmation("Selesai", f"Berhasil mengonversi {success_count} gambar.\nBuka folder output?"):
                ExportService.open_output_folder(self.output_folder)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()