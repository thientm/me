# Kế Hoạch Tích Hợp Telegram Bot: Notification & Remote Control

> **Tài liệu**: Implementation Plan  
> **Ngày lập**: 12.10.2026  
> **Mục tiêu**: Xây dựng tiện ích điều hành từ xa qua Telegram cho hệ thống Personal OS:  
> - **Level 1**: Bắn thông báo ngắn gọn về kết quả chạy Daily Crypto Review & Video Pipeline 3 kênh.  
> - **Level 2**: Điều khiển từ xa (tra cứu trạng thái, duyệt video qua nút bấm, kích hoạt dry-run / render / publish).

---

## 1. Chuẩn Bị & Cấu Hình Bảo Mật (Người dùng thực hiện một lần)

### Bước 1: Lấy `BOT_TOKEN` từ Telegram
1. Mở app Telegram, tìm kiếm **`@BotFather`** (có tích xanh).
2. Gõ `/newbot`.
3. Đặt tên hiển thị cho bot (ví dụ: `Thien Personal OS`).
4. Đặt username kết thúc bằng `bot` (ví dụ: `thien_personal_os_bot`).
5. Sao chép chuỗi mã Token HTTP API (dạng: `7123456789:AAH...`).

### Bước 2: Lấy `CHAT_ID` của bạn
1. Tìm kiếm **`@userinfobot`** trên Telegram.
2. Bấm `/start` (hoặc gửi bất kỳ tin nhắn nào).
3. Sao chép số `Id` của bạn (ví dụ: `123456789`).

### Bước 3: Lưu vào file bí mật `.env` trên máy cá nhân
Tạo hoặc mở file `.env` ở thư mục gốc repo (file này đã nằm trong `.gitignore` nên an toàn tuyệt đối):
```bash
TELEGRAM_BOT_TOKEN="7123456789:AAH..."
TELEGRAM_CHAT_ID="123456789"
```

---

## 2. Kiến Trúc Thư Mục Module `ops/telegram/`

```
ops/telegram/
├── __init__.py
├── config.py         # Nạp TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID từ .env
├── client.py         # HTTP client nhẹ gửi tin nhắn, ảnh, nút bấm (urllib.request chuẩn)
├── notifier.py       # Định dạng tin nhắn báo cáo Crypto, Pipeline 3 kênh, Cảnh báo lỗi
├── bot.py            # Long-polling daemon nhận lệnh & xử lý callback từ Telegram
├── handlers.py       # Xử lý các lệnh /status, /crypto, /dryrun, /run, /help
├── service.sh        # Script bật/tắt daemon bot ngầm trên máy Mac
└── tests/
    ├── __init__.py
    ├── test_client.py
    ├── test_notifier.py
    └── test_handlers.py
```

---

## 3. Chi Tiết Các Task Triển Khai (TDD)

### Task 1: Telegram Config & HTTP Client Module
- **Files**:
  - `ops/telegram/config.py`
  - `ops/telegram/client.py`
  - `ops/telegram/tests/test_client.py`
- **Chức năng**:
  - Đọc biến môi trường `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`.
  - Hàm `send_message(text, parse_mode="HTML", reply_markup=None)` gửi tin nhắn.
  - Hàm `send_photo(photo_path, caption=None)` gửi ảnh minh hoạ (contact sheet/shot).
  - Không phụ thuộc thư viện ngoài nặng nề, sử dụng `urllib.request` nguyên bản của Python.
- [ ] **Step 1: Viết test mock cho `ops/telegram/client.py`**
- [ ] **Step 2: Triển khai code và kiểm thử PASS 100%**
- [ ] **Step 3: Commit `feat(telegram): add Telegram HTTP client module`**

---

### Task 2: Notifier Module (Level 1 — Báo Cáo Định Dạng Thẻ)
- **Files**:
  - `ops/telegram/notifier.py`
  - `ops/telegram/tests/test_notifier.py`
- **Chức năng**:
  - `notify_crypto_review(tts_vnd, btc_price, sol_price, floor_violated, notes)`:
    - Báo cáo định dạng thẻ: Tổng tài sản, chênh lệch sàn cứng 540tr, khuyến nghị hành động.
  - `notify_pipeline_status(slot, channel_results)`:
    - Báo cáo trạng thái 3 kênh cho khung giờ 08:00, 12:00, 20:00 (Gate 1, Gate 2, nền tảng đã đăng).
  - `notify_pipeline_alert(channel, error_msg, action_needed)`:
    - Bắn cảnh báo khẩn nếu có Gate bị FAIL hoặc Chrome CDP port offline.
- [ ] **Step 1: Viết test format mẫu tin nhắn và logic bắn thông báo**
- [ ] **Step 2: Triển khai code `notifier.py`**
- [ ] **Step 3: Chạy test PASS và commit `feat(telegram): add multi-channel notifier module`**

---

### Task 3: Remote Control Daemon & Command Handlers (Level 2)
- **Files**:
  - `ops/telegram/handlers.py`
  - `ops/telegram/bot.py`
  - `ops/telegram/tests/test_handlers.py`
- **Chức năng**:
  - Cơ chế **Whitelist User ID**: Bỏ qua 100% tin nhắn không đến từ `TELEGRAM_CHAT_ID`.
  - Xử lý các Slash Commands:
    - `/status`: Gọi `ops.orchestrator.cli` trả về Dashboard 3 kênh ngay lập tức.
    - `/crypto`: Gọi tính toán TTS và trả về số liệu mới nhất.
    - `/dryrun <channel> [slug]`: Chạy dry-run kiểm tra bài đăng.
    - `/doctor`: Chạy kiểm tra môi trường ffmpeg, fonts, chromium.
  - Xử lý Inline Buttons (Callback Queries):
    - Nhận sự kiện bấm nút `[🟢 Duyệt Đăng]` hoặc `[🔴 Hoãn]` để kích hoạt lệnh publish.
- [ ] **Step 1: Viết test cho Command Handlers**
- [ ] **Step 2: Triển khai `handlers.py` và vòng lặp `bot.py` (Long-polling)**
- [ ] **Step 3: Commit `feat(telegram): add interactive remote control daemon`**

---

### Task 4: Tích Hợp Vào Scheduled Background Tasks
- **Files**:
  - Cập nhật scheduler prompt cho `Daily Crypto Review` (`task-74`).
  - Cập nhật scheduler prompt cho `3-Channel Video Pipeline` (`task-76`).
  - Tạo script khởi động nền `ops/telegram/service.sh` (start/stop/status).
- [ ] **Step 1: Tạo script `service.sh` quản lý tiến trình bot nền**
- [ ] **Step 2: Tích hợp hook gọi `notifier.py` khi scheduled cron hoàn tất**
- [ ] **Step 3: Commit `feat(telegram): integrate Telegram notifications into scheduled pipeline`**

---

### Task 5: Dry-Run Verification Toàn Diện
- **Kiểm thử**:
  - Chạy mock dry-run gửi tin nhắn thử nghiệm mà không cần token thật (chế độ `--dry-run` in payload ra terminal).
  - Khi người dùng điền token thật trong `.env`, chạy 1 lệnh test:
    ```bash
    python3 -m ops.telegram.client --test "🚀 Test kết nối Personal OS tới Telegram thành công!"
    ```
- [ ] **Step 1: Thực thi kiểm thử mock dry-run**
- [ ] **Step 2: Xác nhận exit code 0**
- [ ] **Step 3: Commit chốt plan và hướng dẫn sử dụng**

---

## 4. Các Lệnh Điều Khiển Dự Kiến Qua Telegram

| Lệnh | Ý nghĩa | Ví dụ |
| :--- | :--- | :--- |
| `/status` | Xem dashboard 3 kênh và tiến độ khung giờ | `/status` |
| `/crypto` | Xem tổng tài sản Crypto & tỷ giá VND tức thì | `/crypto` |
| `/dryrun` | Kiểm tra kịch bản & assets của bài | `/dryrun me-tech quinnipiac-ai-trust-crisis` |
| `/doctor` | Chẩn đoán sức khoẻ môi trường dựng video | `/doctor` |
| `/help` | Xem danh sách các lệnh hỗ trợ | `/help` |
