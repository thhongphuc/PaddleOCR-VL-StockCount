import torch
import paddle
import paddleocr

print("PaddleOCR attributes:")
print([attr for attr in dir(paddleocr) if not attr.startswith("_")])

from paddleocr import PaddleOCR
print("PaddleOCR class:", PaddleOCR)

try:
    from paddlex import create_pipeline
    print("PaddleX create_pipeline available")
except Exception as e:
    print("paddlex error:", e)
