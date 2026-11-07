"""
MarkItDown Generator
A flexible utility for converting various file types (PDF, Word, Excel, PowerPoint,
images, audio, HTML, etc.) to structured Markdown using Microsoft MarkItDown.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List
from markitdown import MarkItDown


class MarkdownGenerator:
    def __init__(self, enable_plugins: bool = False):
        """Initialize MarkItDown generator instance."""
        self.converter = MarkItDown(enable_plugins=enable_plugins)

    def convert_file(self, input_path: str | Path, output_path: Optional[str | Path] = None) -> str:
        """
        Convert a single file or URL to Markdown.
        
        Args:
            input_path: Path to the input file or URL.
            output_path: Optional destination .md file path.
            
        Returns:
            The converted markdown string.
        """
        input_str = str(input_path)
        print(f"[>] Converting: {input_str}")
        
        result = self.converter.convert(input_str)
        content = result.text_content

        if output_path:
            out_file = Path(output_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(content, encoding="utf-8")
            print(f"[+] Saved markdown to: {out_file.resolve()}")

        return content

    def convert_directory(
        self,
        input_dir: str | Path,
        output_dir: str | Path,
        extensions: Optional[List[str]] = None,
        recursive: bool = True
    ) -> List[Path]:
        """
        Batch convert supported files in a directory to Markdown.
        
        Args:
            input_dir: Directory containing documents.
            output_dir: Destination directory for .md files.
            extensions: Optional list of allowed extensions (e.g. ['.pdf', '.docx']).
            recursive: Whether to search subdirectories.
            
        Returns:
            List of generated markdown file paths.
        """
        src = Path(input_dir)
        dest = Path(output_dir)
        dest.mkdir(parents=True, exist_ok=True)

        if extensions is None:
            extensions = [
                ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv",
                ".json", ".xml", ".html", ".htm", ".txt", ".mp3",
                ".wav", ".m4a", ".jpg", ".jpeg", ".png"
            ]
        extensions = [ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions]

        pattern = "**/*" if recursive else "*"
        generated_files = []

        files = [p for p in src.glob(pattern) if p.is_file() and p.suffix.lower() in extensions]
        if not files:
            print(f"[-] No matching files found in {src.resolve()}")
            return []

        print(f"[*] Found {len(files)} files to convert...")

        for file_path in files:
            try:
                rel_path = file_path.relative_to(src)
                target_md = dest / rel_path.with_suffix(".md")
                self.convert_file(file_path, target_md)
                generated_files.append(target_md)
            except Exception as e:
                print(f"[!] Error converting {file_path.name}: {e}", file=sys.stderr)

        print(f"[✓] Batch conversion complete. {len(generated_files)} files written to {dest.resolve()}")
        return generated_files


def main():
    parser = argparse.ArgumentParser(
        description="MarkItDown Generator - Convert documents, spreadsheets, presentations, and media to Markdown."
    )
    parser.add_argument("input", nargs="?", help="Input file path or URL to convert")
    parser.add_argument("-o", "--output", help="Output .md file path (default: stdout or <input>.md)")
    parser.add_argument("-b", "--batch", help="Batch convert all supported files from the specified input directory")
    parser.add_argument("-d", "--output-dir", default="output", help="Output directory for batch conversion (default: ./output)")
    parser.add_argument("-r", "--no-recursive", action="store_true", help="Do not search subdirectories in batch mode")

    args = parser.parse_args()
    generator = MarkdownGenerator()

    if args.batch:
        generator.convert_directory(
            input_dir=args.batch,
            output_dir=args.output_dir,
            recursive=not args.no_recursive
        )
    elif args.input:
        out = args.output
        if not out and not sys.stdout.isatty():
            content = generator.convert_file(args.input)
            print(content)
        else:
            if not out:
                p = Path(args.input)
                out = p.with_suffix(".md") if p.exists() else "output.md"
            generator.convert_file(args.input, out)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

