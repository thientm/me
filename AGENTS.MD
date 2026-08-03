# AGENTS.md — Personal OS

Đây là hệ thống memory/plan cá nhân dạng file-based. Nếu bạn là agent đang làm việc trong thư mục này, hãy tuân theo các quy tắc dưới đây trước khi đọc/sửa bất kỳ file nào.

## Bắt đầu từ đâu
Luôn đọc `INDEX.md` trước để biết câu hỏi/tác vụ hiện tại nên đọc file nào. Không đoán cấu trúc, không tự tạo file mới ngoài pattern đã có.

## Quy tắc theo loại file

- **`*-plan.md`** (vd `plan/master-plan.md`, `portfolio/portfolio-plan.md`): bán tĩnh. Chỉ sửa khi chiến lược/mục tiêu thật sự thay đổi, không dùng để ghi log hàng ngày.
- **`logs/*.md`**: append-only, 1 file/tháng. KHÔNG sửa hoặc xoá entry cũ — chỉ thêm entry mới có ngày tháng rõ ràng. Nếu thông tin cũ sai, thêm entry mới ghi chú correction, không edit ngược lại quá khứ.
- **`reviews/*.md`**: derived — tổng hợp từ plan + logs. Chỉ tạo/cập nhật khi được yêu cầu review định kỳ, không tự phát sinh.
- **`cashflow.md`**: snapshot hiện tại, không phải log. Biến động theo tháng nằm ở `finance/logs/`.

## Khi thêm domain mới
Copy pattern đã có: `xxx-plan.md` + `logs/` + `reviews/` (nếu cần định kỳ). Không đổi cấu trúc domain cũ.

## Khi không chắc
Nếu một tác vụ có thể ghi đè/xoá dữ liệu cũ trong `logs/`, dừng lại và hỏi trước khi thực hiện.