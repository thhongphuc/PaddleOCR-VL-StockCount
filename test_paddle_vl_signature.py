import torch
import paddle
from paddleocr import PaddleOCRVL, PaddleOCRVLOptions, PaddleOCR
import inspect

print("PaddleOCRVL doc / init signature:")
print(inspect.signature(PaddleOCRVL.__init__))

try:
    print("PaddleOCRVLOptions fields:")
    print(dir(PaddleOCRVLOptions))
except Exception as e:
    print("PaddleOCRVLOptions error:", e)
