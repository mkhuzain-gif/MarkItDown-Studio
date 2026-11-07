"""
MarkItDown Studio Web Application
A modern Web UI for converting documents, audio, images, and URLs to Markdown.
"""

import os
import sys
import shutil
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from markitdown import MarkItDown

app = FastAPI(title="MarkItDown Studio", version="1.0.0")

# Initialize MarkItDown engine
converter = MarkItDown()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
# Use system temp directory for compatibility with Vercel / AWS Lambda / Read-only filesystems
TEMP_DIR = Path(tempfile.gettempdir()) / "markitdown_uploads"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class UrlRequest(BaseModel):
    url: str


@app.get("/")
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_file)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "MarkItDown Studio",
        "supported_formats": [
            "pdf", "docx", "pptx", "xlsx", "xls", "csv",
            "json", "xml", "html", "wav", "mp3", "jpg", "png", "youtube"
        ]
    }


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...)):
    """Convert an uploaded file (PDF, Office, audio, image, etc.) to Markdown."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Preserve original extension
    suffix = Path(file.filename).suffix
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=str(TEMP_DIR))
    temp_path = Path(temp_file.name)

    try:
        # Write uploaded contents
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Execute conversion using Microsoft MarkItDown
        result = converter.convert(str(temp_path))
        markdown_text = result.text_content or ""
        title = getattr(result, "title", None) or Path(file.filename).stem

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "title": title,
            "markdown": markdown_text
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": f"Conversion error: {str(e)}"}
        )
    finally:
        # Clean up temporary file
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


@app.post("/api/convert-url")
async def convert_url(request: UrlRequest):
    """Convert a webpage or YouTube video URL to Markdown."""
    url = request.url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Must start with http:// or https://")

    try:
        result = converter.convert(url)
        markdown_text = result.text_content or ""
        title = getattr(result, "title", None) or url

        return JSONResponse({
            "success": True,
            "url": url,
            "title": title,
            "markdown": markdown_text
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": f"URL Conversion error: {str(e)}"}
        )


def start_server(host: Optional[str] = None, port: Optional[int] = None, open_browser: Optional[bool] = None):
    """Start server with auto-detection for local vs cloud deployment."""
    # Cloud platforms (Render, Railway, Hugging Face, Fly.io) pass PORT via environment
    env_port = int(os.environ.get("PORT", 8000))
    env_host = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")
    
    final_host = host if host is not None else env_host
    final_port = port if port is not None else env_port
    
    # Auto-disable browser opening in cloud / container environments
    if open_browser is None:
        open_browser = "PORT" not in os.environ and final_host in ("127.0.0.1", "localhost")

    url = f"http://{final_host}:{final_port}"
    print("\n" + "=" * 60)
    print(f"🚀 MarkItDown Studio running at: {url}")
    print("=" * 60 + "\n")
    
    if open_browser:
        try:
            webbrowser.open(f"http://127.0.0.1:{final_port}")
        except Exception:
            pass

    uvicorn.run("app:app", host=final_host, port=final_port, reload=False, log_level="info")


if __name__ == "__main__":
    start_server()

