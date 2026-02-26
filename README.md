# CapPress - Video Compressor

A simple and user-friendly video compression tool built with Python and customtkinter, powered by FFmpeg.

## Features

- **Easy-to-use GUI** - Clean and intuitive interface with dark mode theme
- **Multiple Compression Levels**:
  - Low Compression (Bigger size, Better quality) - CRF: 23
  - Medium Compression (Balanced) - CRF: 28
  - High Compression (Smaller size, Lower quality) - CRF: 32
- **Real-time Processing Status** - Shows progress information
- **Automatic Output Naming** - Saves compressed files with `_compressed` suffix

## Requirements

- Python 3.7+
- FFmpeg installed and available in system PATH
- customtkinter package

## Installation

1. Install Python dependencies:
```bash
pip install customtkinter==5.2.2
```

2. Ensure FFmpeg is installed and accessible. Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

1. Run the application:
```bash
python cap_press.py
```

2. Click "Pilih Video" (Select Video) to choose a video file (MP4 or MOV format supported)

3. Select your preferred compression level from the dropdown

4. Click "Mulai Kompres" (Start Compression) to begin the process

5. The compressed video will be saved in the same directory with `_compressed` suffix

## System Requirements

- Windows 10/11, macOS, or Linux
- FFmpeg must be installed and in your system PATH

## Notes

- The tool automatically handles file overwriting with `-y` flag
- Console window is hidden during processing on Windows
- Processing runs in a background thread to keep the GUI responsive
