import os
import subprocess
import threading
import tkinter.messagebox as messagebox
import customtkinter as ctk
from tkinter import filedialog

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None

# Constants for FFmpeg CRF values
QUALITY_MAP = {
    "Low Compression (Bigger size, Better quality)": "23",
    "Medium Compression (Balanced) - Default": "28",
    "High Compression (Smaller size, Lower quality)": "32"
}

class CapPressApp(ctk.CTk if TkinterDnD is None else type("CTkDND", (ctk.CTk, TkinterDnD.DnDWrapper), {})):
    def __init__(self):
        ctk.CTk.__init__(self)
        if TkinterDnD is not None:
            self.TkdndVersion = TkinterDnD._require(self)

        # --- Window Setup ---
        self.title("CapPress - Video Compressor")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Set Appearance Mode
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # --- State Variables ---
        self.selected_file_path = ctk.StringVar(value="")
        self.selected_quality = ctk.StringVar(value="Medium Compression (Balanced) - Default")
        self.is_processing = False

        # --- UI Layout ---
        self._create_widgets()

    def _create_widgets(self):
        # 1. Title Label
        title_label = ctk.CTkLabel(
            self, text="CapPress", font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(
            self, text="Simple FFmpeg Video Compressor", font=ctk.CTkFont(size=12)
        )
        subtitle_label.pack(pady=(0, 20))

        # 2. File Selection Section
        self.file_button = ctk.CTkButton(
            self, text="Pilih Video", command=self.select_file,
            font=ctk.CTkFont(weight="bold")
        )
        self.file_button.pack(pady=10)

        self.file_label = ctk.CTkLabel(
            self, text="Belum ada file yang dipilih", text_color="gray"
        )
        self.file_label.pack(pady=(0, 20))

        # 3. Quality Selection Section
        quality_label = ctk.CTkLabel(self, text="Pilih Tingkat Kompresi:", font=ctk.CTkFont(weight="bold"))
        quality_label.pack(anchor="w", padx=40, pady=(10, 5))

        self.quality_dropdown = ctk.CTkOptionMenu(
            self, values=list(QUALITY_MAP.keys()),
            variable=self.selected_quality,
            width=350
        )
        self.quality_dropdown.pack(pady=5)

        # 4. Status Label & Execute Button Section
        self.status_label = ctk.CTkLabel(
            self, text="", text_color="yellow", font=ctk.CTkFont(size=12, slant="italic")
        )
        self.status_label.pack(pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(self, width=350)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))

        self.compress_button = ctk.CTkButton(
            self, text="Mulai Kompres", command=self.start_compression_thread,
            fg_color="#28a745", hover_color="#218838", font=ctk.CTkFont(weight="bold", size=14),
            height=40, width=200
        )
        self.compress_button.pack(pady=10)

        if TkinterDnD is not None:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self.handle_drop)
        else:
            self.status_label.configure(text="Drag & drop nonaktif (tkinterdnd2 belum terpasang).")

    # --- Actions / Logic ---

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Video",
            filetypes=[("Video files", "*.mp4 *.mov")]
        )
        if file_path:
            self.update_selected_file(file_path)

    def handle_drop(self, event):
        if self.is_processing:
            return

        dropped_data = self.tk.splitlist(event.data)
        if not dropped_data:
            return

        file_path = dropped_data[0]
        if not os.path.exists(file_path):
            return

        valid_extensions = (".mp4", ".mov")
        if not file_path.lower().endswith(valid_extensions):
            messagebox.showwarning("Format tidak didukung", "Hanya file .mp4 atau .mov yang dapat diproses.")
            return

        self.update_selected_file(file_path)

    def update_selected_file(self, file_path):
        self.selected_file_path.set(file_path)
        file_name = os.path.basename(file_path)
        self.file_label.configure(text=f"File terpilih: {file_name}", text_color="white")

    def start_compression_thread(self):
        file_path = self.selected_file_path.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning("Peringatan", "Silakan pilih file video terlebih dahulu.")
            return

        filename, ext = os.path.splitext(file_path)
        output_path = f"{filename}_compressed{ext}"
        if os.path.exists(output_path):
            should_overwrite = messagebox.askyesno(
                "Konfirmasi Timpa File",
                f"File sudah ada:\n{os.path.basename(output_path)}\n\nTimpa file tersebut?"
            )
            if not should_overwrite:
                return

        # Disable buttons and update UI to show processing state
        self.is_processing = True
        self.compress_button.configure(state="disabled", text="Memproses...")
        self.file_button.configure(state="disabled")
        self.quality_dropdown.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Sedang memproses, mohon tunggu... 0%")

        # Start background thread to run ffmpeg
        thread = threading.Thread(target=self.run_ffmpeg, args=(file_path, output_path))
        thread.daemon = True
        thread.start()

    def run_ffmpeg(self, input_path, output_path):
        quality_key = self.selected_quality.get()
        crf_value = QUALITY_MAP.get(quality_key, "28")

        duration = self.get_video_duration(input_path)

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vcodec", "libx264",
            "-crf", crf_value,
            "-progress", "pipe:1",
            "-nostats",
            output_path
        ]

        try:
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0 # Hide console on windows
            )

            for line in process.stdout:
                if not line.startswith("out_time_ms=") or not duration:
                    continue

                try:
                    out_time_ms = int(line.split("=", 1)[1].strip())
                except ValueError:
                    continue

                progress = min(max((out_time_ms / 1_000_000) / duration, 0), 1)
                self.after(0, self.update_progress, progress)

            process.wait()

            if process.returncode == 0:
                self.after(0, self.update_progress, 1)
                self.after(0, self.on_compression_success, output_path)
            else:
                self.after(0, self.on_compression_error, "FFmpeg mengembalikan status gagal.")
        
        except Exception as e:
            self.after(0, self.on_compression_error, str(e))

    def get_video_duration(self, input_path):
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_path,
        ]
        try:
            output = subprocess.check_output(command, text=True).strip()
            return float(output)
        except Exception:
            return None

    def update_progress(self, progress):
        self.progress_bar.set(progress)
        self.status_label.configure(text=f"Sedang memproses, mohon tunggu... {int(progress * 100)}%")

    def on_compression_success(self, output_path):
        self._reset_ui_state()
        messagebox.showinfo("Sukses!", f"Video berhasil dikompres!\nDisimpan di:\n{output_path}")

    def on_compression_error(self, error_msg):
        self._reset_ui_state()
        print("FFmpeg Error:", error_msg)
        messagebox.showerror("Error", "Gagal mengkompresi video.\nPastikan FFmpeg sudah terinstal.")

    def _reset_ui_state(self):
        self.is_processing = False
        self.compress_button.configure(state="normal", text="Mulai Kompres")
        self.file_button.configure(state="normal")
        self.quality_dropdown.configure(state="normal")
        self.status_label.configure(text="")
        self.progress_bar.set(0)

if __name__ == "__main__":
    app = CapPressApp()
    app.mainloop()
