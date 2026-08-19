import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import torch
import paddle
from paddleocr import PaddleOCRVL
import json

vl = PaddleOCRVL(pipeline_version="v1.6")
res = vl.predict("c:/Projects/Gemini/OCR-V/sample_data/sample_1_fmcg_kho_tong.png")

item = res[0]
print("--- parsing_res_list ---")
if hasattr(item, "parsing_res_list") and item.parsing_res_list:
    for idx, p in enumerate(item.parsing_res_list):
        print(f"Block {idx}:", p)

print("\n--- layout_res ---")
if hasattr(item, "layout_res") and item.layout_res:
    print("layout_res type:", type(item.layout_res))
    if hasattr(item.layout_res, "boxes") or isinstance(item.layout_res, list):
        print("layout_res sample:", item.layout_res[:3] if isinstance(item.layout_res, list) else item.layout_res)
    elif hasattr(item.layout_res, "keys"):
        print("layout_res keys:", item.layout_res.keys())
        print("layout_res sample:", {k: str(item.layout_res[k])[:100] for k in item.layout_res.keys()})
