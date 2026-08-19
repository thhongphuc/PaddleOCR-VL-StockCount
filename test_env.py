import sys
print("Python:", sys.version)

try:
    import paddle
    print("Paddle version:", paddle.__version__)
except Exception as e:
    print("Paddle error:", e)

try:
    import paddleocr
    print("PaddleOCR version:", getattr(paddleocr, "__version__", "unknown"))
except Exception as e:
    print("PaddleOCR error:", e)

try:
    import cv2
    print("OpenCV version:", cv2.__version__)
except Exception as e:
    print("OpenCV error:", e)

try:
    import pandas as pd
    print("Pandas version:", pd.__version__)
except Exception as e:
    print("Pandas error:", e)

try:
    import openpyxl
    print("Openpyxl version:", openpyxl.__version__)
except Exception as e:
    print("Openpyxl error:", e)

try:
    import fastapi
    print("FastAPI version:", fastapi.__version__)
except Exception as e:
    print("FastAPI error:", e)

print("Environment check completed.")
