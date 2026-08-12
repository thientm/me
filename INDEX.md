# INDEX

Router cho agent/bản thân: đọc file nào tuỳ câu hỏi/tác vụ.

| Cần gì | Đọc file |
|---|---|
| **🧭 Main process đang chạy (Việc 1 làm sổ / Việc 2 chỗ ở & hôn nhân)** | `real-estate/real-estate-plan.md` → mục "Cấu trúc chủ đạo" (đầu file) |
| Tầm nhìn dài hạn, mục tiêu to/nhỏ | `plan/master-plan.md` |
| Chiến lược, mục tiêu phân bổ đầu tư | `portfolio/portfolio-plan.md` |
| Log giao dịch/thay đổi portfolio | `portfolio/logs/{YYYY-MM}.md` |
| Review định kỳ portfolio | `portfolio/reviews/{kỳ}-review.md` |
| Snapshot dòng tiền hiện tại | `finance/cashflow.md` |
| Log thu/chi theo ngày hoặc tuần | `finance/logs/{YYYY-MM}.md` |
| Kế hoạch BĐS (sổ đỏ, pháp lý, tài chính) | `real-estate/real-estate-plan.md` |
| Kế hoạch Crypto (exit strategy, playbook) | `crypto/crypto-plan.md` |
| Log giao dịch/review crypto theo tuần/tháng | `crypto/logs/{YYYY-MM}.md` |

## Quy tắc chung
- File `*-plan.md`: bán tĩnh, chỉ sửa khi chiến lược/mục tiêu thật sự đổi.
- File `logs/*.md`: append-only, 1 file/tháng, mỗi entry có ngày, không sửa/xoá entry cũ.
- File `reviews/*.md`: derived, tổng hợp từ plan + log, tạo định kỳ (tự chọn nhịp).
- Domain mới sau này: copy pattern `xxx-plan.md` + `logs/` + `reviews/` (nếu cần).
