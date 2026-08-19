@echo off
echo ===================================================
echo Starting PaddleOCR-VL-1.6 Stock Count Studio...
echo ===================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not found in PATH! Please install Python 3.10+
    pause
    exit /b 1
)

python app.py
pause
