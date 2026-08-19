import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import torch
import paddle
import paddleocr
from paddleocr import PaddleOCRVL, PaddleOCR
from PIL import Image
import numpy as np

print("Testing PaddleOCRVL predict on sample...")
vl = PaddleOCRVL(pipeline_version="v1.6")
img_path = "c:/Projects/Gemini/OCR-V/sample_data/sample_1_fmcg_kho_tong.png"

res = vl.predict(img_path)
print("Prediction returned:", type(res), len(list(res)) if hasattr(res, '__len__') else res)

for i, item in enumerate(res):
    print(f"--- Item {i} ---")
    print("Type:", type(item))
    print("Attributes:", [a for a in dir(item) if not a.startswith("_")])
    if hasattr(item, "keys"):
        print("Keys:", item.keys())
    if hasattr(item, "json"):
        print("JSON length/type:", type(item.json))
    if hasattr(item, "markdown"):
        print("Markdown preview:\n", str(item.markdown)[:500])
    if hasattr(item, "layout_result"):
        print("layout_result count:", len(item.layout_result))
    if hasattr(item, "dt_polys"):
        print("dt_polys:", len(item.dt_polys))
    if hasattr(item, "rec_text"):
        print("rec_text:", len(item.rec_text))
