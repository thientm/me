# Real Estate & Property Plan

> Lưu trữ lộ trình pháp lý, giấy tờ, và kế hoạch tài chính tổng thể cho các dự án bất động sản.

## Dự án đang thực hiện (Active)

### Dự án 01: Sang tên và lên thổ cư đất ở quê (Linked to G-01)

#### 1. Lộ trình pháp lý & Thủ tục
| Bước | Trạng thái | Ngày cập nhật | Ghi chú |
|---|---|---|---|
| 1. Ký hợp đồng tặng cho tại phòng công chứng | Chưa bắt đầu | | |
| 2. Nộp hồ sơ đăng ký sang tên tại VP Đăng ký đất đai / Bộ phận một cửa | Chưa bắt đầu | | |
| 3. Đóng thuế, phí (TNCN, lệ phí trước bạ - nếu không được miễn) | Chưa bắt đầu | | |
| 4. Nhận sổ đỏ mang tên mình | Chưa bắt đầu | | |
| 5. Nộp đơn xin chuyển mục đích sử dụng đất sang thổ cư + bản vẽ trích lục | Chưa bắt đầu | | |
| 6. Đóng tiền sử dụng đất khi lên thổ cư | Chưa bắt đầu | | |

> Trạng thái dùng: `Chưa bắt đầu` / `Đang làm` / `Chờ (bên ngoài)` / `Xong`. Cập nhật cột Ngày + Ghi chú mỗi khi trạng thái đổi; không xoá lịch sử, chỉ ghi đè trạng thái hiện tại (bảng này là snapshot, không phải log).

#### 2. Kế hoạch tài chính & Trả góp
*Dòng tiền thực tế hàng tháng (trả nợ, tích luỹ...) ghi ở `finance/logs/{YYYY-MM}.md`, mỗi entry liên quan tới dự án này gắn tag `[G-01]` trong `note` để dễ lọc. Mục này chỉ ghi tổng quan/mục tiêu.*
- **Tổng ngân sách dự kiến:** ~3 tỷ (nếu vay đủ để làm sớm)
- **Vốn tự có:** 2.4 tỷ
- **Số tiền cần vay:** 0 - 0.6 tỷ (chưa chốt, tuỳ quyết định — xem Research & Đánh giá bên dưới)
- **Kế hoạch vay:** 
  - Vay ai / Ngân hàng nào:
  - Lãi suất:
  - Thời hạn:
  - Số tiền trả góp dự kiến hàng tháng: (điền số tiền - sau đó update sang `finance/cashflow.md`)
- **Tích luỹ trước khi nộp hồ sơ:**
  - Mục tiêu cần có trước bước nộp hồ sơ/đóng thuế: (điền số tiền)
  - Hiện có: (điền số tiền, cập nhật khi có log tháng mới ở `finance/logs/`)

#### 3. Research & Đánh giá
*Ghi phát hiện/quyết định research vào đây khi có, kèm ngày. Không xoá mục cũ, thêm mục mới bên dưới nếu có cập nhật/đổi ý.*

**Phương án vay**
- 2026-08-03: Đang ở bước lên kế hoạch. Vốn tự có sẵn 2.4 tỷ; cần thêm ~0.6 tỷ nếu vay đủ 3 tỷ. Chiến lược thời điểm/vay phụ thuộc diễn biến khung giá đất khu vực (hiện tại mức 38):
  - Nếu khung giá đất biến động tăng thêm nhiều → vay đủ 3 tỷ, làm sớm để tránh thuế/lệ phí bị tính theo khung giá mới cao hơn.
  - Nếu khung giá đất không biến động nhiều → delay sang đầu năm sau (~sau Tết): vẫn phải vay, nhưng vay ít hơn — nhờ (1) lãi gửi tiết kiệm từ khoản 2.4 tỷ trong lúc chờ, (2) có thêm khoản thưởng Tết bổ sung vào vốn.
  - Chưa chốt phương án; phụ thuộc kết quả research khung giá đất (xem "Việc cần chốt" bên dưới).

**Việc cần chốt (Open)**
- [ ] Research & chốt khung giá đất khu vực — kết quả quyết định: làm sớm (vay đủ 3 tỷ) hay delay qua Tết (vẫn vay, nhưng ít hơn). *(mở từ 2026-08-03)*
  - 2026-08-03: Đã research xong phần cơ chế/luật (xem chi tiết ở mục "Thủ tục pháp lý & chi phí" bên dưới). Còn thiếu: tra đúng Phụ lục (theo vị trí thửa đất) kèm Nghị quyết 52/2025/NQ-HĐND để xác nhận chính xác mức áp cho thửa đất của mình (hiện mới biết mặt bằng chung khu vực Gia Lâm, chưa khớp đúng thửa). Task vẫn mở.

**Thủ tục pháp lý & chi phí (thuế TNCN, lệ phí trước bạ, điều kiện lên thổ cư ở địa phương...)**
- 2026-08-03: Research khung giá đất / bảng giá đất (để đánh giá rủi ro tăng giá cho quyết định vay ở trên):
  - Luật Đất đai 2024 (hiệu lực 1/8/2024) **bỏ hẳn "khung giá đất"** cũ (cơ chế Chính phủ ban hành trần/sàn 5 năm/lần theo Luật Đất đai 2013). Mức 4.5tr/m² trước đây ở khu vực mình là theo khung cũ này, áp dụng đến hết 31/12/2025.
  - Từ 1/1/2026, Hà Nội áp dụng **"Bảng giá đất lần đầu"** theo Nghị quyết 52/2025/NQ-HĐND (HĐND TP thông qua 26/11/2025), xây dựng theo **nguyên tắc thị trường** (không còn bị khung giá đất cũ khống chế trần), chia theo vị trí VT1-VT4 (theo tên đường/mặt đường) + hệ số điều chỉnh cho nhà nhiều mặt tiền, giảm giá theo khoảng cách tới đường chính. → Đây là nguồn gốc mức 38tr đang thấy.
  - **Kết luận sơ bộ**: mức tăng 4.5tr → 38tr chủ yếu do **đổi hẳn phương pháp luận một lần** (chuyển từ khung giá đất bị khống chế thấp hơn thị trường nhiều năm, sang bảng giá theo thị trường), không phải biến động thị trường thông thường của 1 năm — bản chất giống "one-time reset" hơn là bước đầu của một chuỗi tăng dồn dập.
  - **Cơ chế điều chỉnh sau 2026**: Luật quy định bảng giá đất áp dụng/điều chỉnh **hàng năm** (khác chu kỳ 5 năm cũ), nhưng Nghị quyết 52/2025 không quy định mức tăng tự động — mỗi lần điều chỉnh vẫn cần UBND TP trình HĐND TP xem xét, quyết nghị lại. Không có cơ chế leo thang tự động.
  - **2 yếu tố khiến rủi ro tăng tiếp vẫn thật, không chỉ lý thuyết**:
    1. Giá rao bán thị trường thực tế quanh Yên Viên hiện ~50-70tr/m² (mặt đường thương mại 70-120tr/m²) — cao hơn nhiều so với 38tr bảng giá NN → dù đã "nhảy" ~8 lần, bảng giá vẫn thấp hơn thị trường, còn dư địa điều chỉnh tăng tiếp theo đúng nguyên tắc thị trường của luật mới.
    2. Gia Lâm đang tái cơ cấu hành chính (vận hành mô hình mới từ 1/7/2025, gộp còn 17 đơn vị cấp xã) và có định hướng lên quận — chất xúc tác riêng có thể khiến giá khu vực này tăng nhanh hơn mặt bằng chung trong các đợt điều chỉnh tới.
  - **Nguồn**: [cafef.vn - Từ 1/8 Luật Đất đai bỏ khung giá đất](https://cafef.vn/tu-1-8-luat-dat-dai-bo-khung-gia-dat-bang-gia-dat-lan-dau-duoc-ap-dung-tu-1-1-2026-188240716105310487.chn), [luatvietnam.vn - Bỏ khung giá đất ảnh hưởng thế nào đến người dân](https://luatvietnam.vn/dat-dai-nha-o/bo-khung-gia-dat-anh-huong-nhu-the-nao-den-nguoi-dan-567-96754-article.html), [luatvietnam.vn - Nghị quyết 52/2025/NQ-HĐND](https://luatvietnam.vn/dat-dai/nghi-quyet-52-2025-nq-hdnd-ha-noi-bang-gia-dat-lan-dau-ap-dung-tu-01-01-2026-420193-d2.html), [thanhuyhanoi.vn - Gia Lâm hoàn tất sắp xếp đơn vị hành chính](https://thanhuyhanoi.vn/tin-tuc/huyen-gia-lam/huyen-gia-lam-hoan-tat-sap-xep-don-vi-hanh-chinh-san-sang-van-hanh-mo-hinh-moi-tu-2025-50018267.html).
  - **Chưa xác minh**: số 38tr cụ thể có đúng khớp Phụ lục/vị trí (VT1-VT4) áp dụng cho đúng thửa đất của mình hay không — cần tra file Phụ lục đính kèm NQ 52/2025/NQ-HĐND (chia 17 khu vực) để chốt chính xác.

**Khác**
- (Chưa có)

## Lưu trữ dự án cũ (Completed)
- (Chưa có)
