import sys
from pathlib import Path
import yt_dlp

try:
    import imageio_ffmpeg  # type: ignore
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = None


def get_default_download_dir() -> Path:
    downloads = Path.home() / "Downloads"
    return downloads if downloads.exists() else Path.cwd()


def format_duration(seconds: int | None) -> str:
    if not seconds:
        return "Unknown"
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}" if hours else f"{mins:02d}:{secs:02d}"


def main():
    print("=" * 40)
    print("        YouTube Downloader")
    print("=" * 40)

    url = input("YouTube URL: ").strip()
    if not url:
        print("Error: URL cannot be empty.")
        return

    default_dir = get_default_download_dir()
    dir_input = input(f"Download Directory (Default: {default_dir}): ").strip()
    target_dir = Path(dir_input) if dir_input else default_dir

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: Could not create directory ({e})")
        return

    print("\nFetching video information...")
    meta_opts = {
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(meta_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"\n[Error] Failed to fetch video information: {e}")
        return
    except Exception as e:
        print(f"\n[Unexpected Error] {e}")
        return

    title = info.get("title", "Unknown Title")
    duration = format_duration(info.get("duration"))
    print(f"\nTitle    : {title}")
    print(f"Duration : {duration}")

    # Filter available resolutions in descending order
    available_heights = sorted(
        {
            f["height"]
            for f in info.get("formats", [])
            if f.get("vcodec") != "none" and f.get("height")
        },
        reverse=True,
    )

    print("\nAvailable Resolutions:")
    for idx, h in enumerate(available_heights, 1):
        tag = " (Highest)" if idx == 1 else ""
        print(f"  {idx}) {h}p{tag}")
    print("  0) Audio Only (Music / Podcast - M4A/MP3)")

    choice = input(f"\nYour Choice [0-{len(available_heights)}] (Default: 1): ").strip()

    if choice == "0":
        format_str = "bestaudio/best"
        merge_mp4 = False
    else:
        try:
            selected_idx = int(choice) if choice else 1
            if 1 <= selected_idx <= len(available_heights):
                h = available_heights[selected_idx - 1]
            else:
                h = available_heights[0]
        except ValueError:
            h = available_heights[0]

        format_str = (
            f"bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/"
            f"bestvideo[height<={h}]+bestaudio/"
            f"best[height<={h}]"
        )
        merge_mp4 = True

    ydl_opts = {
        "format": format_str,
        "outtmpl": str(target_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "no_warnings": True,
    }

    if FFMPEG_EXE:
        ydl_opts["ffmpeg_location"] = FFMPEG_EXE
        if merge_mp4:
            ydl_opts["merge_output_format"] = "mp4"

    try:
        print("\nStarting download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n[Success] File saved to: {target_dir}")
    except yt_dlp.utils.DownloadError as e:
        print(f"\n[Download Error] {e}")
    except KeyboardInterrupt:
        print("\nDownload cancelled by user.")
    except Exception as e:
        print(f"\n[Unexpected Error] {e}")


if __name__ == "__main__":
    main()
