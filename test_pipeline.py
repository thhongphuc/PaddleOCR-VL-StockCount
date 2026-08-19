import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from engine.paddle_vl_engine import get_ocr_engine
from engine.stock_count_parser import StockCountParser
from engine.exporter import StockCountExporter

def test_pipeline():
    sample_path = Path("c:/Projects/Gemini/OCR-V/sample_data/sample_1_fmcg_kho_tong.png")
    print("Testing OCR on:", sample_path)

    engine = get_ocr_engine()
    ocr_res = engine.process_image(sample_path)

    print("OCR Done! Execution time:", ocr_res["execution_time_ms"], "ms")
    print("Model used:", ocr_res["model_used"])
    print("Found blocks count:", len(ocr_res["blocks"]))

    parser = StockCountParser()
    stock_data = parser.parse(ocr_res)

    print("\n--- Stock Count Parsed Metadata ---")
    print(json.dumps(stock_data["metadata"], ensure_ascii=False, indent=2))

    print("\n--- Stock Count KPIs ---")
    print(json.dumps(stock_data["kpi"], ensure_ascii=False, indent=2))

    print(f"\n--- Extracted Items ({len(stock_data['items'])}) ---")
    for item in stock_data["items"][:5]:
        print(f"[{item['sku']}] {item['description']} - Sổ: {item['book_qty']} | Thực: {item['actual_qty']} | Lệch: {item['variance']} ({item['status']})")

    # Test Excel export
    excel_bytes = StockCountExporter.export_excel(stock_data)
    print("\nExcel export size:", len(excel_bytes), "bytes")
    
    # Test Markdown export
    md = StockCountExporter.export_markdown(stock_data)
    print("\nMarkdown snippet:\n", md[:300])

    print("\nAll pipeline tests passed!")

if __name__ == "__main__":
    test_pipeline()
