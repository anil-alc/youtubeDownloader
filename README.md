# YouTube Downloader

A fast, compact, and modern YouTube video and audio downloader built with `yt-dlp`.

## Features

- **Modern & Reliable:** Powered by `yt-dlp`, actively maintained against YouTube's anti-bot protections, cipher changes, and throttling.
- **Compact & Focused:** Single-purpose, readable, and clean codebase (~90 lines).
- **Resolution Selection:** Automatically inspects the video and lets you choose from available resolutions (1080p, 720p, 480p, 360p, etc.).
- **Automatic FFmpeg Integration:** Bundles `imageio-ffmpeg` so that separate high-definition video and audio streams are automatically merged into a clean `.mp4` on Windows without requiring manual system FFmpeg installation.
- **Audio Only Option:** Download pure audio (music/podcast) with option `0`.
- **Smart Directory Handling:** Defaults to your Windows `Downloads` folder (`~/Downloads`) if no path is entered, and creates missing folders automatically.
- **Playlist Protection:** Safe against radio/mix URLs (`&list=...`) by downloading only the requested single video.
- **Real-Time Progress:** Built-in terminal progress bar showing percentage, download speed, and ETA.

## Installation

Ensure you have Python 3.10+ installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python yt_downloader.py
```

Follow the prompts:
1. Paste the YouTube URL.
2. Enter the target directory (or press `Enter` to use the default `Downloads` folder).
3. Select your desired resolution (`1` for highest quality, `2` for next, `0` for audio only).
