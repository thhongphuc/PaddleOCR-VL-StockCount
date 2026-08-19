#!/usr/bin/env bash
set -e

echo "==================================================="
echo "Starting PaddleOCR-VL-1.6 Stock Count Studio..."
echo "==================================================="

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed or not in PATH!"
    exit 1
fi

python3 app.py
