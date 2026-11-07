"""
MarkItDown Folder Watcher
Automatically watches a folder for new incoming documents and converts them to Markdown in real-time.
"""

import time
import argparse
from pathlib import Path
from markitdown import MarkItDown

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv",
    ".json", ".xml", ".html", ".htm", ".txt", ".mp3",
    ".wav", ".m4a", ".jpg", ".jpeg", ".png"
}


def watch_folder(input_dir: str = "input_watch", output_dir: str = "output_watch", interval: float = 2.0):
    src = Path(input_dir)
    dest = Path(output_dir)
    src.mkdir(parents=True, exist_ok=True)
    dest.mkdir(parents=True, exist_ok=True)

    converter = MarkItDown()
    processed_files = set()

    # Pre-populate with existing files if they already have corresponding markdown
    for item in src.iterdir():
        if item.is_file() and (dest / item.with_suffix(".md").name).exists():
            processed_files.add(item.name)

    print("=" * 60)
    print("👀 MarkItDown Folder Watcher Active")
    print(f"📥 Watching directory: {src.resolve()}")
    print(f"📤 Output directory:   {dest.resolve()}")
    print("Drop any PDF, Word, Excel, PPT, or Media file into the watch folder...")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    try:
        while True:
            for item in src.iterdir():
                if not item.is_file():
                    continue
                if item.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue
                if item.name in processed_files:
                    continue

                # Wait slightly to ensure file copy is finished
                initial_size = -1
                try:
                    initial_size = item.stat().st_size
                    time.sleep(0.5)
                    if item.stat().st_size != initial_size:
                        continue  # File is still being copied
                except Exception:
                    continue

                print(f"\n[+] New file detected: {item.name}")
                out_file = dest / item.with_suffix(".md").name
                
                try:
                    print(f"[*] Converting {item.name} to Markdown...")
                    result = converter.convert(str(item))
                    out_file.write_text(result.text_content, encoding="utf-8")
                    processed_files.add(item.name)
                    print(f"[✓] Successfully saved to: {out_file.name}")
                except Exception as e:
                    print(f"[!] Failed to convert {item.name}: {e}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[!] Watcher stopped.")


def main():
    parser = argparse.ArgumentParser(description="Watch a folder and automatically convert documents to Markdown.")
    parser.add_argument("-i", "--input", default="input_watch", help="Folder to watch (default: input_watch)")
    parser.add_argument("-o", "--output", default="output_watch", help="Destination folder for .md files (default: output_watch)")
    parser.add_argument("-t", "--interval", type=float, default=2.0, help="Check interval in seconds (default: 2.0)")
    args = parser.parse_args()

    watch_folder(input_dir=args.input, output_dir=args.output, interval=args.interval)


if __name__ == "__main__":
    main()

