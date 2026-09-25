# Crypto Portfolio Plan (Mock Fixture)

> Kế hoạch cơ cấu, theo dõi và tối ưu danh mục Crypto.
> Nhật ký giao dịch và thay đổi cấu trúc nằm ở `logs/{YYYY-MM}.md`. Review định kỳ nằm ở `reviews/`.

## 1. Thông tin dòng vốn
- **Tổng vốn gốc (initial):** 650,000,000 VND
- **Giá trị hiện tại (2026-09-24 12:00, đo từ giá spot + P2P realtime):** **$21.235 ≈ 550.643.256 VND** (P2P 25.930; tạm lỗ ~99,3tr / −15,3%). **BTC 0,159310 ($84.262) = 348,1tr · SOL 55,28 ($115,72) = 165,8tr · stables $1.415 = 36,6tr.** Cơ cấu: BTC 63,2% · SOL 30,1% · stables 6,7%. Tiến độ rút VND **0%**. Còn **37 ngày** tới 31/10/2026, **17 ngày** tới override #1 (11/10/2026).
- **Hard Floor (Sàn cứng):** **540.000.000 VND (540tr)**. Thủng sàn thì Market Sell ALL ngay lập tức ra VND.
- **Take-profit Band:** **≥ 540.000.000 VND (≥540tr)**. Bán 50% coin ngay lập tức (xả sạch SOL trước, rút toàn bộ Stables).
- **Deadline an toàn rút tiền:** **Late October 2026 (31/10/2026)**.

## 2. Target Allocation & Tình trạng hiện tại (đo 2026-09-24 12:00)

| Tài sản | SL | Giá | Giá trị | Định hướng xử lý |
|---|---|---|---|---|
| **BTC** | **0.159310** | $84.262 | **348,1tr** (63,2%) | Giữ lại một phần sau lệnh band. Stop-market $75.900. |
| **SOL** | **55.28** | $115,72 | **165,8tr** (30,1%) | XẢ TOÀN BỘ trong lệnh band ≥540tr (tài sản biến động cao). |
| **Stables** (USDT+USDC) | **1415.0** | $1,00 | **36,6tr** (6,7%) | Rút ra VND ngay qua Binance P2P. |

## 3. Nguyên tắc & Chiến lược tối ưu
- Hard Floor 540tr: Nếu TTS < 540tr -> Bán sạch toàn bộ danh mục ngay lập tức.
- Binary Rule: TTS >= 540tr -> Bán 50% ngay lập tức.
- Thứ tự ưu tiên xả vốn: Stables -> SOL -> BTC.
- Phạt chậm nộp thuế đất: 38.750 VND/giờ (930.000 VND/ngày) trên gốc 3,1 tỷ VND.
- Ngân sách BĐS: 3.100.000.000 VND. Tự có: 1.300.000.000 (bố mẹ) + 705.000.000 (cá nhân) + TTS crypto. Trần vay: 615.000.000 VND.

## 4. Nhật ký giao dịch gần nhất
- 2026-08-04: Khởi tạo danh mục vốn 650tr.
- 2026-09-04: Cập nhật quy tắc quản trị.
- 2026-09-21: Nâng hard floor lên 500tr.
- 2026-09-24: Nâng hard floor lên 540tr và take-profit band >= 540tr theo quyết định mới nhất.

## 5. Lộ trình Exit — Glidepath
- 2026-09-24: Tranche 1 (15% gốc)
- 2026-09-29: Tranche 2 (20% gốc)
- 2026-10-07: Tranche 3 (15% gốc)
- 2026-10-31: Hạn chót dòng tiền hoàn tất cash-out (Late October 2026)

## 7.5 Review Format Template
Mỗi review ghi vào `logs/{YYYY-MM}.md` theo chuẩn Section 7.5.
