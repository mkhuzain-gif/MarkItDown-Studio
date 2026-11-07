@echo off
title MarkItDown Studio
cd /d "%~dp0"

echo ========================================================
echo        Starting MarkItDown Studio Web Interface
echo ========================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv!
    pause
    exit /b 1
)

echo Activating environment and starting server...
start http://127.0.0.1:8000
".venv\Scripts\python.exe" app.py
pause

