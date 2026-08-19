"""
Realistic Sample Stock Count Documents Generator
Creates high-fidelity synthetic images and documents for demonstration and testing.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_sample_documents():
    sample_dir = Path("c:/Projects/Gemini/OCR-V/sample_data")
    sample_dir.mkdir(parents=True, exist_ok=True)

    # 1. Sample 1: Vietnamese FMCG Warehouse Count Sheet
    create_fmcg_sample(sample_dir / "sample_1_fmcg_kho_tong.png")

    # 2. Sample 2: Electronics Warehouse Count Sheet
    create_electronics_sample(sample_dir / "sample_2_electronics_kho_linh_kien.png")

    # 3. Sample 3: Pharmacy & Medical Supplies Sheet
    create_pharmacy_sample(sample_dir / "sample_3_duoc_pham_lot_hsd.png")

    print("Sample documents generated successfully in", sample_dir)


def get_font(size=14, bold=False):
    # Try system fonts or default
    font_names = [
        "arial.ttf", "calibri.ttf", "segoeui.ttf", "tahoma.ttf", "times.ttf"
    ]
    if bold:
        font_names = ["arialbd.ttf", "calibrib.ttf", "segoeuib.ttf", "tahomabd.ttf"] + font_names
    
    for fname in font_names:
        try:
            return ImageFont.truetype(fname, size)
        except Exception:
            continue
    return ImageFont.load_default()


def create_fmcg_sample(output_path: Path):
    w, h = 1200, 1600
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(26, bold=True)
    f_sub = get_font(15, bold=True)
    f_meta = get_font(13, bold=False)
    f_meta_b = get_font(13, bold=True)
    f_tbl_h = get_font(13, bold=True)
    f_tbl_d = get_font(12, bold=False)
    f_tbl_b = get_font(12, bold=True)

    # Header section
    draw.rectangle([(40, 30), (1160, 180)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((60, 45), "CÔNG TY CỔ PHẦN THƯƠNG MẠI & BÁN LẺ TOÀN CẦU", fill=(30, 58, 138), font=f_sub)
    draw.text((600, 80), "BIÊN BẢN KIỂM KÊ TỒN KHO", fill=(15, 23, 42), font=f_title, anchor="mt")
    draw.text((600, 120), "(Đợt kiểm kê định kỳ Tháng 08/2026)", fill=(71, 85, 105), font=f_meta, anchor="mt")

    # Meta Info block
    draw.text((60, 145), "Kho kiểm kê: Kho Tổng Bình Dương (KHO-01)", fill=(15, 23, 42), font=f_meta_b)
    draw.text((500, 145), "Mã phiếu: KK-20260819-01", fill=(15, 23, 42), font=f_meta_b)
    draw.text((850, 145), "Ngày: 19/08/2026", fill=(15, 23, 42), font=f_meta_b)

    draw.text((60, 195), "Người kiểm kê: Nguyễn Văn An - MSNV: NV-1082", fill=(51, 65, 85), font=f_meta)
    draw.text((500, 195), "Thủ kho: Trần Thị Mai", fill=(51, 65, 85), font=f_meta)
    draw.text((850, 195), "Giám sát: Lê Hoàng Long (Kế toán)", fill=(51, 65, 85), font=f_meta)

    # Table Layout
    y_start = 230
    cols = [
        ("STT", 60, "C"),
        ("Mã SKU", 150, "L"),
        ("Tên Hàng Hóa", 330, "L"),
        ("ĐVT", 70, "C"),
        ("Vị Trí", 100, "C"),
        ("Tồn Sổ", 90, "R"),
        ("Thực Tế", 90, "R"),
        ("Chênh Lệch", 90, "R"),
        ("Ghi Chú", 140, "L")
    ]

    # Draw Header Row
    x_cur = 40
    draw.rectangle([(40, y_start), (1160, y_start + 40)], fill=(30, 58, 138))
    for name, width, align in cols:
        draw.rectangle([(x_cur, y_start), (x_cur + width, y_start + 40)], outline=(255, 255, 255), width=1)
        if align == "C":
            draw.text((x_cur + width // 2, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="mm")
        elif align == "R":
            draw.text((x_cur + width - 10, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="rm")
        else:
            draw.text((x_cur + 10, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="lm")
        x_cur += width

    # Sample Items
    items = [
        ("1", "SKU-8935001", "Nước khoáng Lavie 500ml", "Thùng", "Kệ A1-01", "150", "150", "0", "Khớp tồn kho"),
        ("2", "SKU-8935002", "Sữa tươi TH True Milk 1L", "Thùng", "Kệ A1-02", "80", "78", "-2", "Bao bì rách 2"),
        ("3", "SKU-8935003", "Dầu ăn Simply 1L Canola", "Chai", "Kệ A2-01", "240", "245", "+5", "Hàng tồn đợt trước"),
        ("4", "SKU-8935004", "Bánh Cosy quy bơ 378g", "Hộp", "Kệ A2-05", "120", "120", "0", "Khớp tồn kho"),
        ("5", "SKU-8935005", "Cà phê G7 3in1 Hộp 18 gói", "Hộp", "Kệ B1-03", "300", "295", "-5", "Thất thoát quầy"),
        ("6", "SKU-8935006", "Mì Omachi Xốt bò hầm 80g", "Thùng", "Kệ B2-01", "450", "450", "0", "Khớp tồn kho"),
        ("7", "SKU-8935007", "Nước tương Nam Dương 500ml", "Chai", "Kệ B3-02", "180", "180", "0", "Khớp tồn kho"),
        ("8", "SKU-8935008", "Tương ớt Chinsu Chai 250g", "Chai", "Kệ B3-04", "210", "214", "+4", "Nhập thừa chưa lên phiếu"),
        ("9", "SKU-8935009", "Trà xanh Oolong C2 455ml", "Thùng", "Kệ C1-02", "95", "95", "0", "Khớp tồn kho"),
        ("10", "SKU-8935010", "Gạo ST25 Ông Cua Túi 5kg", "Túi", "Kệ D1-01", "60", "58", "-2", "Bao bục thủng")
    ]

    y_cur = y_start + 40
    for idx, row in enumerate(items):
        bg_col = (255, 255, 255) if idx % 2 == 0 else (248, 250, 252)
        draw.rectangle([(40, y_cur), (1160, y_cur + 36)], fill=bg_col)
        
        x_cur = 40
        for col_idx, val in enumerate(row):
            w_col = cols[col_idx][1]
            align = cols[col_idx][2]
            draw.rectangle([(x_cur, y_cur), (x_cur + w_col, y_cur + 36)], outline=(226, 232, 240), width=1)
            
            # Text styling based on discrepancy
            fill_c = (15, 23, 42)
            f_use = f_tbl_d
            if col_idx == 7: # Variance
                if val == "0":
                    fill_c = (16, 185, 129)
                    f_use = f_tbl_b
                elif "-" in val:
                    fill_c = (239, 68, 68)
                    f_use = f_tbl_b
                else:
                    fill_c = (217, 119, 6)
                    f_use = f_tbl_b

            if align == "C":
                draw.text((x_cur + w_col // 2, y_cur + 18), val, fill=fill_c, font=f_use, anchor="mm")
            elif align == "R":
                draw.text((x_cur + w_col - 10, y_cur + 18), val, fill=fill_c, font=f_use, anchor="rm")
            else:
                draw.text((x_cur + 10, y_cur + 18), val, fill=fill_c, font=f_use, anchor="lm")
            x_cur += w_col

        y_cur += 36

    # Total Row
    draw.rectangle([(40, y_cur), (1160, y_cur + 40)], fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    draw.text((300, y_cur + 20), "TỔNG CỘNG (10 MẶT HÀNG)", fill=(15, 23, 42), font=f_tbl_h, anchor="mm")
    draw.text((790, y_cur + 20), "1,885", fill=(15, 23, 42), font=f_tbl_h, anchor="rm")
    draw.text((880, y_cur + 20), "1,885", fill=(15, 23, 42), font=f_tbl_h, anchor="rm")
    draw.text((970, y_cur + 20), "0", fill=(16, 185, 129), font=f_tbl_h, anchor="rm")

    # Signatures
    y_sig = y_cur + 80
    sigs = [
        ("Người Lập Phiếu\n\n\nNguyễn Văn An", 150),
        ("Thủ Kho\n\n\nTrần Thị Mai", 450),
        ("Kiểm Toán Viên\n\n\nLê Hoàng Long", 750),
        ("Kế Toán Trưởng\n\n\nPhạm Thị Hương", 1020)
    ]
    for text, x_pos in sigs:
        draw.text((x_pos, y_sig), text, fill=(15, 23, 42), font=f_tbl_h, align="center")

    img.save(output_path, "PNG")


def create_electronics_sample(output_path: Path):
    w, h = 1200, 1500
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(14, bold=True)
    f_meta = get_font(13, bold=False)
    f_meta_b = get_font(13, bold=True)
    f_tbl_h = get_font(13, bold=True)
    f_tbl_d = get_font(12, bold=False)

    draw.rectangle([(40, 30), (1160, 160)], fill=(240, 253, 250), outline=(94, 234, 212), width=2)
    draw.text((600, 65), "STOCK COUNT SHEET - ELECTRONICS DIVISION", fill=(15, 118, 110), font=f_title, anchor="mt")
    draw.text((600, 105), "Warehouse: TechHub Global Central Hub - Doc No: SC-ELEC-8830", fill=(51, 65, 85), font=f_sub, anchor="mt")
    draw.text((600, 130), "Audit Date: 2026-08-19 | Auditor: Alex Henderson (Lead Auditor)", fill=(71, 85, 105), font=f_meta, anchor="mt")

    cols = [
        ("No", 60, "C"),
        ("Item Code", 160, "L"),
        ("Description / Specification", 360, "L"),
        ("UOM", 70, "C"),
        ("Rack/Bin", 100, "C"),
        ("Book Qty", 90, "R"),
        ("Counted", 90, "R"),
        ("Variance", 90, "R"),
        ("Audit Note", 100, "L")
    ]

    y_start = 190
    x_cur = 40
    draw.rectangle([(40, y_start), (1160, y_start + 40)], fill=(15, 118, 110))
    for name, width, align in cols:
        draw.rectangle([(x_cur, y_start), (x_cur + width, y_start + 40)], outline=(255, 255, 255), width=1)
        if align == "C":
            draw.text((x_cur + width // 2, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="mm")
        elif align == "R":
            draw.text((x_cur + width - 10, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="rm")
        else:
            draw.text((x_cur + 10, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="lm")
        x_cur += width

    items = [
        ("1", "CPU-INT-14900K", "Intel Core i9-14900K Box Processor", "Pcs", "BIN-01-A", "45", "45", "0", "Verified"),
        ("2", "CPU-AMD-7800X3D", "AMD Ryzen 7 7800X3D Gaming CPU", "Pcs", "BIN-01-B", "60", "59", "-1", "Missing 1 unit"),
        ("3", "GPU-RTX-4080S", "NVIDIA GeForce RTX 4080 Super 16G", "Pcs", "BIN-02-A", "25", "25", "0", "Verified"),
        ("4", "RAM-COR-32G-6000", "Corsair Vengeance DDR5 32GB 6000MHz", "Kit", "BIN-03-C", "120", "122", "+2", "RMA returned"),
        ("5", "SSD-SAM-990P-2TB", "Samsung 990 Pro NVMe PCIe 4.0 2TB", "Pcs", "BIN-04-A", "85", "85", "0", "Verified"),
        ("6", "MB-ASU-Z790-F", "ASUS ROG STRIX Z790-F GAMING WIFI", "Pcs", "BIN-05-A", "30", "30", "0", "Verified"),
        ("7", "PSU-SEA-1000W", "Seasonic Focus GX-1000 Gold 1000W", "Unit", "BIN-06-B", "40", "40", "0", "Verified"),
        ("8", "MOU-LOG-GPROX", "Logitech G Pro X Superlight 2 Mouse", "Pcs", "BIN-07-A", "75", "74", "-1", "Box damaged")
    ]

    y_cur = y_start + 40
    for idx, row in enumerate(items):
        bg_col = (255, 255, 255) if idx % 2 == 0 else (240, 253, 250)
        draw.rectangle([(40, y_cur), (1160, y_cur + 36)], fill=bg_col)
        
        x_cur = 40
        for col_idx, val in enumerate(row):
            w_col = cols[col_idx][1]
            align = cols[col_idx][2]
            draw.rectangle([(x_cur, y_cur), (x_cur + w_col, y_cur + 36)], outline=(204, 251, 241), width=1)
            
            fill_c = (15, 23, 42)
            if col_idx == 7:
                if val == "0":
                    fill_c = (16, 185, 129)
                elif "-" in val:
                    fill_c = (239, 68, 68)
                else:
                    fill_c = (217, 119, 6)

            if align == "C":
                draw.text((x_cur + w_col // 2, y_cur + 18), val, fill=fill_c, font=f_tbl_d, anchor="mm")
            elif align == "R":
                draw.text((x_cur + w_col - 10, y_cur + 18), val, fill=fill_c, font=f_tbl_d, anchor="rm")
            else:
                draw.text((x_cur + 10, y_cur + 18), val, fill=fill_c, font=f_tbl_d, anchor="lm")
            x_cur += w_col
        y_cur += 36

    img.save(output_path, "PNG")


def create_pharmacy_sample(output_path: Path):
    w, h = 1200, 1500
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(14, bold=True)
    f_meta = get_font(13, bold=False)
    f_tbl_h = get_font(13, bold=True)
    f_tbl_d = get_font(12, bold=False)

    draw.rectangle([(40, 30), (1160, 160)], fill=(254, 242, 242), outline=(254, 202, 202), width=2)
    draw.text((600, 65), "BẢNG KIỂM KÊ KHO DƯỢC PHẨM & VẬT TƯ Y TẾ", fill=(185, 28, 28), font=f_title, anchor="mt")
    draw.text((600, 105), "Kho Dược Trung Tâm - Phiếu số: KKDP-2026-088", fill=(51, 65, 85), font=f_sub, anchor="mt")
    draw.text((600, 130), "Ngày kiểm kê: 19/08/2026 | DS. Nguyễn Thị Lan (Phụ trách kho)", fill=(71, 85, 105), font=f_meta, anchor="mt")

    cols = [
        ("STT", 50, "C"),
        ("Mã Thuốc", 130, "L"),
        ("Tên Thuốc / Nồng Độ", 280, "L"),
        ("ĐVT", 60, "C"),
        ("Tồn Sổ", 80, "R"),
        ("Thực Tế", 80, "R"),
        ("Lệch", 70, "R"),
        ("Số Lô", 120, "C"),
        ("Hạn Dùng", 110, "C"),
        ("Ghi Chú", 140, "L")
    ]

    y_start = 190
    x_cur = 40
    draw.rectangle([(40, y_start), (1160, y_start + 40)], fill=(185, 28, 28))
    for name, width, align in cols:
        draw.rectangle([(x_cur, y_start), (x_cur + width, y_start + 40)], outline=(255, 255, 255), width=1)
        if align == "C":
            draw.text((x_cur + width // 2, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="mm")
        elif align == "R":
            draw.text((x_cur + width - 10, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="rm")
        else:
            draw.text((x_cur + 10, y_start + 20), name, fill=(255, 255, 255), font=f_tbl_h, anchor="lm")
        x_cur += width

    items = [
        ("1", "MED-001", "Paracetamol 500mg Hộp 100v", "Hộp", "500", "500", "0", "LOT-240801", "2027-08-01", "Bảo quản tốt"),
        ("2", "MED-002", "Amoxicillin 500mg Kháng sinh", "Hộp", "320", "318", "-2", "LOT-240512", "2026-12-15", "Hộp móp méo"),
        ("3", "MED-003", "Vitamin C 1000mg Effervescent", "Tuýp", "180", "180", "0", "LOT-240901", "2027-09-01", "Đạt chuẩn"),
        ("4", "MED-004", "Natri Clorid 0.9% 500ml", "Chai", "600", "605", "+5", "LOT-240720", "2028-07-20", "Thừa phòng mổ"),
        ("5", "MED-005", "Bông gòn y tế cuộn 1kg", "Cuộn", "90", "90", "0", "LOT-240101", "2029-01-01", "Khớp tồn kho"),
        ("6", "MED-006", "Cồn y tế Ethanol 70 độ 1L", "Chai", "150", "150", "0", "LOT-240610", "2027-06-10", "Khớp tồn kho"),
        ("7", "MED-007", "Khẩu trang y tế 4 lớp kháng khuẩn", "Hộp", "400", "390", "-10", "LOT-240305", "2028-03-05", "Cấp phát chưa nhập")
    ]

    y_cur = y_start + 40
    for idx, row in enumerate(items):
        bg_col = (255, 255, 255) if idx % 2 == 0 else (254, 242, 242)
        draw.rectangle([(40, y_cur), (1160, y_cur + 36)], fill=bg_col)
        
        x_cur = 40
        for col_idx, val in enumerate(row):
            w_col = cols[col_idx][1]
            align = cols[col_idx][2]
            draw.rectangle([(x_cur, y_cur), (x_cur + w_col, y_cur + 36)], outline=(254, 202, 202), width=1)
            
            fill_c = (15, 23, 42)
            if col_idx == 6:
                if val == "0":
                    fill_c = (16, 185, 129)
                elif "-" in val:
                    fill_c = (239, 68, 68)
                else:
                    fill_c = (217, 119, 6)

            if align == "C":
                draw.text((x_cur + w_col // 2, y_cur + 18), val, fill=fill_c, font=f_tbl_d, anchor="mm")
            elif align == "R":
                draw.text((x_cur + w_col - 10, y_cur + 18), val, fill=fill_c, font=f_tbl_d, anchor="rm")
            else:
                draw.text((x_cur + 10, y_cur + 18), val, fill=fill_c, font=f_tbl_d, anchor="lm")
            x_cur += w_col
        y_cur += 36

    img.save(output_path, "PNG")


if __name__ == "__main__":
    create_sample_documents()
