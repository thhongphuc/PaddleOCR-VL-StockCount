"""
FastAPI Server for PaddleOCR-VL-1.6 Stock Count Studio
Provides REST APIs for document OCR scanning, stock count parsing, multi-format export, and sample data.
"""

import os
import io
import time
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image

from engine.paddle_vl_engine import get_ocr_engine
from engine.stock_count_parser import StockCountParser
from engine.exporter import StockCountExporter

app = FastAPI(
    title="PaddleOCR-VL-1.6 Stock Count Studio API",
    description="Intelligent Vision-Language OCR & Parsing system for Stock Count and Warehouse Audits",
    version="1.6.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "sample_data"
STATIC_DIR = BASE_DIR / "static"

ocr_engine = get_ocr_engine()
stock_parser = StockCountParser()


class ExportPayload(BaseModel):
    metadata: Dict[str, Any]
    items: List[Dict[str, Any]]
    kpi: Optional[Dict[str, Any]] = None


@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "engine": "PaddleOCR-VL-1.6",
        "model_version": "v1.6",
        "gpu_available": False,
        "supported_formats": ["PNG", "JPG", "JPEG", "WEBP", "BMP", "TIFF", "PDF"],
        "timestamp": time.time()
    }


@app.get("/api/samples")
async def get_samples():
    """Return available sample documents with metadata"""
    samples = [
        {
            "id": "sample_1_fmcg",
            "filename": "sample_1_fmcg_kho_tong.png",
            "title": "Biên Bản Kiểm Kê Kho Tổng FMCG",
            "description": "Kho hàng tiêu dùng (Nước khoáng, Sữa, Dầu ăn, Cà phê, Mì gói) với chênh lệch thừa/thiếu thực tế.",
            "language": "Vietnamese",
            "category": "FMCG / Retail",
            "items_count": 10,
            "image_url": "/api/samples/sample_1_fmcg/image"
        },
        {
            "id": "sample_2_electronics",
            "filename": "sample_2_electronics_kho_linh_kien.png",
            "title": "Electronics Inventory Count Sheet",
            "description": "Linh kiện máy tính & điện tử (CPU i9, RTX 4080S, RAM DDR5, SSD NVMe) kèm mã vị trí Rack/Bin.",
            "language": "English",
            "category": "Electronics / Tech",
            "items_count": 8,
            "image_url": "/api/samples/sample_2_electronics/image"
        },
        {
            "id": "sample_3_pharma",
            "filename": "sample_3_duoc_pham_lot_hsd.png",
            "title": "Bảng Kiểm Kê Kho Dược Phẩm & Y Tế",
            "description": "Thuốc & vật tư y tế (Paracetamol, Amoxicillin, Khẩu trang, Cồn y tế) kèm theo Mã Lô (Lot/Batch) và Hạn sử dụng (EXP).",
            "language": "Vietnamese",
            "category": "Pharmaceuticals",
            "items_count": 7,
            "image_url": "/api/samples/sample_3_pharma/image"
        }
    ]
    return {"samples": samples}


@app.get("/api/samples/{sample_id}/image")
async def get_sample_image(sample_id: str):
    file_map = {
        "sample_1_fmcg": "sample_1_fmcg_kho_tong.png",
        "sample_2_electronics": "sample_2_electronics_kho_linh_kien.png",
        "sample_3_pharma": "sample_3_duoc_pham_lot_hsd.png"
    }
    filename = file_map.get(sample_id)
    if not filename:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    file_path = SAMPLE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Sample file missing")
    
    return FileResponse(str(file_path), media_type="image/png")


@app.post("/api/scan")
async def scan_document(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None)
):
    """
    Process an uploaded document (Image or PDF) or a chosen sample document using PaddleOCR-VL-1.6.
    """
    start_total_time = time.time()

    try:
        images_to_process = []
        original_filenames = []

        if sample_id:
            file_map = {
                "sample_1_fmcg": "sample_1_fmcg_kho_tong.png",
                "sample_2_electronics": "sample_2_electronics_kho_linh_kien.png",
                "sample_3_pharma": "sample_3_duoc_pham_lot_hsd.png"
            }
            fname = file_map.get(sample_id)
            if not fname:
                raise HTTPException(status_code=400, detail="Invalid sample_id")
            sample_path = SAMPLE_DIR / fname
            img = Image.open(sample_path).convert("RGB")
            images_to_process.append(img)
            original_filenames.append(fname)

        elif file:
            content = await file.read()
            filename = file.filename.lower()
            
            if filename.endswith(".pdf"):
                pdf_images = ocr_engine.convert_pdf_to_images(content, dpi=200)
                images_to_process.extend(pdf_images)
                original_filenames.extend([f"{file.filename}_page_{i+1}.png" for i in range(len(pdf_images))])
            else:
                img = Image.open(io.BytesIO(content)).convert("RGB")
                images_to_process.append(img)
                original_filenames.append(file.filename)
        else:
            raise HTTPException(status_code=400, detail="No file or sample_id provided")

        if not images_to_process:
            raise HTTPException(status_code=400, detail="Could not extract any images from input")

        # Process the first page (or all pages)
        pages_results = []
        all_items = []
        
        for idx, img in enumerate(images_to_process):
            ocr_res = ocr_engine.process_image(img)
            stock_res = stock_parser.parse(ocr_res)
            
            # Encode image to base64 for direct client visual rendering
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_b64 = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")

            pages_results.append({
                "page_index": idx + 1,
                "image_data": img_b64,
                "width": ocr_res["width"],
                "height": ocr_res["height"],
                "model_used": ocr_res["model_used"],
                "blocks": ocr_res["blocks"],
                "markdown": ocr_res["markdown"],
                "raw_text": ocr_res["raw_text"],
                "metadata": stock_res["metadata"],
                "items": stock_res["items"],
                "kpi": stock_res["kpi"],
                "execution_time_ms": ocr_res["execution_time_ms"]
            })
            all_items.extend(stock_res["items"])

        total_exec_time = round((time.time() - start_total_time) * 1000, 2)
        first_page = pages_results[0]
        combined_kpi = stock_parser._calculate_kpis(all_items)

        return {
            "success": True,
            "total_pages": len(pages_results),
            "pages": pages_results,
            "metadata": first_page["metadata"],
            "items": all_items,
            "kpi": combined_kpi,
            "markdown": "\n\n---\n\n".join([p["markdown"] for p in pages_results]),
            "model_used": first_page["model_used"],
            "total_execution_time_ms": total_exec_time
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/excel")
async def export_excel_endpoint(payload: ExportPayload):
    data = payload.dict()
    excel_bytes = StockCountExporter.export_excel(data)
    doc_no = data.get("metadata", {}).get("document_no", "StockCount").replace("/", "_")
    filename = f"StockCount_Audit_{doc_no}.xlsx"

    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/api/export/csv")
async def export_csv_endpoint(payload: ExportPayload):
    data = payload.dict()
    csv_str = StockCountExporter.export_csv(data)
    doc_no = data.get("metadata", {}).get("document_no", "StockCount").replace("/", "_")
    filename = f"StockCount_Audit_{doc_no}.csv"

    return Response(
        content=csv_str.encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/api/export/json")
async def export_json_endpoint(payload: ExportPayload):
    data = payload.dict()
    json_str = StockCountExporter.export_json(data)
    doc_no = data.get("metadata", {}).get("document_no", "StockCount").replace("/", "_")
    filename = f"StockCount_Audit_{doc_no}.json"

    return Response(
        content=json_str.encode("utf-8"),
        media_type="application/json; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/api/export/markdown")
async def export_markdown_endpoint(payload: ExportPayload):
    data = payload.dict()
    md_str = StockCountExporter.export_markdown(data)
    doc_no = data.get("metadata", {}).get("document_no", "StockCount").replace("/", "_")
    filename = f"StockCount_Audit_{doc_no}.md"

    return Response(
        content=md_str.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# Serve Static Assets & SPA
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def root():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "PaddleOCR-VL-1.6 Stock Count Studio API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
