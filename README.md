# CapPress - Video Compressor

A simple and user-friendly video compression tool built with Python and CustomTkinter, powered by FFmpeg.

## Features

- **Easy-to-use GUI** - Clean and intuitive interface with dark mode theme.
- **Drag & Drop Video** - Drop `.mp4` / `.mov` files directly into the app window.
- **Multiple Compression Levels**:
  - Low Compression (Bigger size, Better quality) - CRF: 23
  - Medium Compression (Balanced) - CRF: 28
  - High Compression (Smaller size, Lower quality) - CRF: 32
- **Progress Bar While Compressing** - Shows compression progress in percent.
- **Automatic Output Naming** - Saves compressed files with `_compressed` suffix.
- **Overwrite Confirmation** - If `<filename>_compressed.<ext>` already exists, app will ask to overwrite or cancel.

## Requirements

- Python 3.7+
- FFmpeg installed and available in system PATH
- FFprobe installed and available in system PATH (usually included with FFmpeg)

## Installation (Recommended: `venv`)

1. Clone this repository and open the project directory.
2. Create virtual environment:

```bash
python -m venv .venv
```

3. Activate virtual environment:

- **Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

- **Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

- **macOS / Linux:**

```bash
source .venv/bin/activate
```

4. Install Python dependencies:

```bash
pip install -r requirements.txt
```

5. Ensure FFmpeg is installed and accessible.
   Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

1. Run the application:

```bash
python cap_press.py
```

2. Select video by either:
   - Clicking **"Pilih Video"**, or
   - Drag & drop file into the app window.

3. Choose your preferred compression level.
4. Click **"Mulai Kompres"** to start compression.
5. If output file already exists, choose:
   - **Yes** to overwrite, or
   - **No** to cancel compression.
6. The compressed video will be saved in the same directory with `_compressed` suffix.

## Build Executable

This project includes `cap_press.spec` for PyInstaller.

1. Install build dependency:

```bash
pip install pyinstaller
```

2. Build using spec file:

```bash
pyinstaller cap_press.spec
```

3. Build output:
   - Executable files: `dist/`
   - Build artifacts: `build/`

## System Requirements

- Windows 10/11, macOS, or Linux
- FFmpeg/FFprobe must be installed and in your system PATH

## Notes

- Compression runs in a background thread to keep the GUI responsive.
- On Windows, FFmpeg console window is hidden during processing.
- Drag & drop requires `tkinterdnd2` (already included in `requirements.txt`).
