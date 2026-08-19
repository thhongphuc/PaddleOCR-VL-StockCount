# 📦 PaddleOCR-VL-1.6 Stock Count Studio

> **Hệ thống Kiểm kê Kho & Trích xuất Dữ liệu Thông minh ứng dụng Mô hình Thị giác - Ngôn ngữ PaddleOCR-VL-1.6**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PaddleOCR-VL-1.6](https://img.shields.io/badge/AI%20Engine-PaddleOCR--VL--1.6-red.svg)](https://github.com/PaddlePaddle/PaddleOCR)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Tính Năng Nổi Bật (Key Features)

1. **AI Vision-Language OCR (PaddleOCR-VL-1.6)**:
   - Tự động nhận diện hướng xoay tài liệu (*Doc Orientation*).
   - Phân tích bố cục tài liệu (*Doc Layout Analysis*): Tiêu đề, Trường thông tin, Bảng biểu, Chữ ký.
   - Nhận diện cấu trúc bảng đa cột & trích xuất Markdown chuẩn xác.
   - Cơ chế Fallback thông minh đảm bảo hệ thống luôn hoạt động ổn định trên cả CPU và GPU.

2. **Phân Tích Dữ Liệu Kiểm Kê Chuyên Sâu (Stock Count Intelligence)**:
   - Tự động bóc tách: Số biên bản, Ngày kiểm kê, Tên kho, Người kiểm, Mã hàng (SKU), Tên sản phẩm, ĐVT, Vị trí (Rack/Bin), Số lượng sổ sách, Số lượng thực tế, Đơn giá, Lô/HSD (Lot/Exp).
   - Tự động tính chênh lệch (*Variance*), giá trị chênh lệch (*Variance Amount*), phân loại trạng thái (*Khớp / Thừa / Thiếu*).

3. **Chỉ Số KPI & Đánh Giá Rủi Ro Tồn Kho (Real-time Analytics)**:
   - Tổng giá trị sổ sách vs Thực tế.
   - Tỷ lệ chính xác tồn kho (*Accuracy Rate %*).
   - Thống kê mặt hàng lệch (Số lượng thiếu / Số lượng thừa).
   - Phân loại rủi ro kiểm kê (*Low / Medium / High Risk*).

4. **Giao Diện Studio Tương Tác Hiện Đại (Modern Web UI)**:
   - Xem song song tài liệu gốc kèm lớp phủ Bounding Box trực quan (*Interactive BBoxes*).
   - Bảng dữ liệu cho phép chỉnh sửa trực tiếp (*In-place Data Editing*).
   - Lọc nhanh theo trạng thái: Tất cả, Khớp, Thừa, Thiếu.
   - Tải mẫu thử có sẵn (*Sample Documents: FMCG, Điện tử, Dược phẩm*).

5. **Xuất Báo Cáo Đa Định Dạng (Multi-Format Export)**:
   - 📊 **Excel (.xlsx)**: File chuẩn kế toán với Header thông tin kho, định dạng số/tiền tệ và highlight màu tự động cho các dòng chênh lệch.
   - 📄 **CSV / JSON**: Dễ dàng tích hợp vào ERP, SAP, Odoo, WMS.
   - 📝 **Markdown**: Báo cáo tóm tắt kiểm kê nhanh gọn.

---

## 🚀 Cài Đặt & Chạy Trên Máy Có GPU (GPU Machine Setup)

### 1. Yêu cầu hệ thống
- **OS**: Linux (Ubuntu 20.04/22.04 khuyến nghị) hoặc Windows 10/11.
- **Python**: 3.10, 3.11 hoặc 3.12.
- **GPU**: NVIDIA GPU (VRAM >= 6GB, khuyến nghị >= 8GB với CUDA 11.8 hoặc 12.x).

---

### 2. Hướng dẫn cài đặt từng bước

#### Bước 1: Clone repository
```bash
git clone https://github.com/thhongphuc/PaddleOCR-VL-StockCount.git
cd PaddleOCR-VL-StockCount
```

#### Bước 2: Tạo môi trường ảo Python
```bash
# Trên Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Trên Windows
python -m venv .venv
.venv\Scripts\activate
```

#### Bước 3: Cài đặt PaddlePaddle GPU
Tùy theo phiên bản CUDA trên máy của bạn:

- **CUDA 11.8**:
  ```bash
  python -m pip install paddlepaddle-gpu==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
  ```

- **CUDA 12.3**:
  ```bash
  python -m pip install paddlepaddle-gpu==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/
  ```

- *(Nếu máy không có GPU, chạy bản CPU)*:
  ```bash
  python -m pip install paddlepaddle==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
  ```

#### Bước 4: Cài đặt các thư viện còn lại
```bash
pip install -r requirements.txt
```

---

### 3. Khởi chạy ứng dụng

#### Cách 1: Chạy trực tiếp bằng Python
```bash
python app.py
```

#### Cách 2: Chạy bằng Uvicorn (Hỗ trợ reload khi dev)
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Sau khi server khởi động, truy cập giao diện web tại:
👉 **`http://localhost:8000`** hoặc **`http://127.0.0.1:8000`**

Tài liệu API Swagger tự động tại:
👉 **`http://localhost:8000/docs`**

---

## 🧪 Kiểm Thử Hệ Thống (Testing Scripts)

| Script | Mô tả |
| :--- | :--- |
| `python test_env.py` | Kiểm tra phiên bản Python, Paddle, OpenCV, FastAPI |
| `python test_pipeline.py` | Chạy toàn bộ pipeline OCR + Parser + Excel Export trên mẫu thử |
| `python test_samples_all.py` | Test gọi API `/api/scan` trên cả 3 tập mẫu dữ liệu |

---

## 📂 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
PaddleOCR-VL-StockCount/
├── engine/
│   ├── paddle_vl_engine.py      # Wrapper cho PaddleOCR-VL-1.6 & Layout Analysis
│   ├── stock_count_parser.py    # Parser bóc tách bảng, metadata & tính KPI
│   └── exporter.py              # Bộ xuất file Excel, CSV, JSON, Markdown
├── sample_data/
│   ├── generate_samples.py      # Script sinh tài liệu kiểm kê mẫu sắc nét
│   ├── sample_1_fmcg_kho_tong.png
│   ├── sample_2_electronics_kho_linh_kien.png
│   └── sample_3_duoc_pham_lot_hsd.png
├── static/
│   ├── index.html               # Giao diện Studio SPA
│   ├── style.css                # CSS Dark/Glassmorphism hiện đại
│   └── app.js                   # Logic tương tác UI, BBox Overlay, Canvas
├── app.py                       # FastAPI Application Server & REST Endpoints
├── requirements.txt             # Danh sách dependencies
├── run_server.bat               # Script khởi động nhanh trên Windows
├── run_server.sh                # Script khởi động nhanh trên Linux
└── README.md                    # Hướng dẫn chi tiết
```

---

## 📡 REST API Reference

### 1. `POST /api/scan`
Quét và bóc tách tài liệu kiểm kê (ảnh hoặc PDF hoặc sample ID).
- **Multipart Form Data**:
  - `file`: File ảnh (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`) hoặc tài liệu (`.pdf`).
  - `sample_id` (Tùy chọn): `"sample_1_fmcg"`, `"sample_2_electronics"`, `"sample_3_pharma"`.

### 2. `POST /api/export/excel`
Xuất dữ liệu kiểm kê thành file Excel `.xlsx` chuyên nghiệp kèm định dạng màu sắc.

### 3. `POST /api/export/csv`
Xuất dữ liệu dạng bảng định dạng UTF-8 CSV.

### 4. `POST /api/export/json`
Xuất toàn bộ metadata, line items và KPIs dạng JSON cấu trúc.

### 5. `POST /api/export/markdown`
Xuất báo cáo kiểm kê dạng bảng Markdown.

### 6. `GET /api/samples`
Lấy danh sách các tài liệu kiểm kê mẫu có sẵn trong hệ thống.

### 7. `GET /api/health`
Kiểm tra trạng thái hoạt động của OCR Engine và API server.

---

## 💡 Mẹo Khi Chạy Trên GPU (GPU Optimization Tips)

1. **VRAM Optimization**:
   Mô hình `PaddleOCR-VL-1.6` (0.9B parameters) tiêu tốn khoảng ~3-4GB VRAM khi inference ở chế độ FP16. Đảm bảo GPU của bạn có ít nhất 6GB VRAM.
2. **Batch Processing**:
   Đối với tài liệu nhiều trang PDF, hệ thống sẽ tự động phân giải từng trang ở mức 200 DPI để đạt độ chi tiết cao nhất cho bảng số liệu.

---

## 📄 License
Dự án được phân phối dưới giấy phép MIT License.
