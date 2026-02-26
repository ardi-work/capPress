import os
import subprocess
import threading
import tkinter.messagebox as messagebox
import customtkinter as ctk
from tkinter import filedialog

# Constants for FFmpeg CRF values
QUALITY_MAP = {
    "Low Compression (Bigger size, Better quality)": "23",
    "Medium Compression (Balanced) - Default": "28",
    "High Compression (Smaller size, Lower quality)": "32"
}

class CapPressApp(ctk.CTk):
    def __init__(self):
        super().__init__()

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

        self.compress_button = ctk.CTkButton(
            self, text="Mulai Kompres", command=self.start_compression_thread,
            fg_color="#28a745", hover_color="#218838", font=ctk.CTkFont(weight="bold", size=14),
            height=40, width=200
        )
        self.compress_button.pack(pady=10)

    # --- Actions / Logic ---

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Video",
            filetypes=[("Video files", "*.mp4 *.mov")]
        )
        if file_path:
            self.selected_file_path.set(file_path)
            file_name = os.path.basename(file_path)
            self.file_label.configure(text=f"File terpilih: {file_name}", text_color="white")

    def start_compression_thread(self):
        file_path = self.selected_file_path.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning("Peringatan", "Silakan pilih file video terlebih dahulu.")
            return

        # Disable buttons and update UI to show processing state
        self.is_processing = True
        self.compress_button.configure(state="disabled", text="Memproses...")
        self.file_button.configure(state="disabled")
        self.quality_dropdown.configure(state="disabled")
        self.status_label.configure(text="Sedang memproses, mohon tunggu...")

        # Start background thread to run ffmpeg
        thread = threading.Thread(target=self.run_ffmpeg, args=(file_path,))
        thread.daemon = True
        thread.start()

    def run_ffmpeg(self, input_path):
        filename, ext = os.path.splitext(input_path)
        output_path = f"{filename}_compressed{ext}"

        quality_key = self.selected_quality.get()
        crf_value = QUALITY_MAP.get(quality_key, "28")

        command = [
            "ffmpeg",
            "-y", # Overwrite if exists
            "-i", input_path,
            "-vcodec", "libx264",
            "-crf", crf_value,
            output_path
        ]

        try:
            # Run ffmpeg command. Suppress output by capturing it, or let it show in background Console
            process = subprocess.run(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0 # Hide console on windows
            )
            
            if process.returncode == 0:
                self.after(0, self.on_compression_success, output_path)
            else:
                error_msg = process.stderr.decode('utf-8')
                self.after(0, self.on_compression_error, error_msg)
        
        except Exception as e:
            self.after(0, self.on_compression_error, str(e))

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

if __name__ == "__main__":
    app = CapPressApp()
    app.mainloop()
