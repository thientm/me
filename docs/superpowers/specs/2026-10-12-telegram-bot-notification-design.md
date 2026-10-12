# Design Spec: Telegram Bot Notification & Remote Control (Personal OS)

- **Date**: 2026-10-12
- **Author**: Thien TM & Antigravity
- **Status**: Approved (Phased Implementation: Level 1 First, Level 2 Next Day)

---

## 1. Mục Tiêu & Phạm Vi (Goals & Scope)

Hệ thống cung cấp kênh giao tiếp và giám sát qua Telegram cá nhân (`@thientm_jarvis_bot`) cho hai luồng vận hành cốt lõi:
1. **Crypto Portfolio Management**: Giám sát Tổng tài sản (TTS), so sánh sàn cứng kỷ luật 540tr, cảnh báo vi phạm và khuyến nghị hành động.
2. **Multi-Channel Video Pipeline**: Giám sát trạng thái 3 kênh nội dung theo từng khung giờ (08:00 Tâm An Lạc, 12:00 Mê Tech, 20:00 Kênh 3) và các cổng chất lượng (Gate 1, Gate 2, Render, Publish).

### Phân kỳ thực hiện (Phasing)
- **Phase 1 (Level 1 - One-way Notifier)**: Triển khai ngay. Gửi thông báo 1 chiều định dạng HTML card, zero external dependencies (`urllib.request`), có dry-run/mock fallback, không cần daemon tiến trình nền.
- **Phase 2 (Level 2 - Remote Control Daemon)**: Triển khai ngày tiếp theo tại công ty. Long-polling daemon xử lý các lệnh tra cứu `/status`, `/crypto`, `/dryrun` và inline buttons duyệt đăng bài.

---

## 2. Kiến Trúc Kỹ Thuật (Architecture)

```
ops/telegram/
├── __init__.py
├── config.py         # Nạp TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID từ .env (fallback OS env)
├── client.py         # HTTP client gửi sendMessage, sendPhoto qua urllib.request
├── notifier.py       # Format message templates (Crypto Review, Pipeline Slot, Alert)
├── cli.py            # CLI entrypoint hỗ trợ test và trigger từ script/cron
├── bot.py            # (Level 2) Long-polling daemon nhận lệnh & callback query
├── handlers.py       # (Level 2) Handlers cho /status, /crypto, /dryrun, /help
└── tests/
    ├── __init__.py
    ├── test_client.py
    └── test_notifier.py
```

### 2.1 Cấu hình bảo mật
- Token và Chat ID được lưu tại `.env` (đã nằm trong `.gitignore`):
  - `TELEGRAM_BOT_TOKEN="8843329194:AAG2y6wUYuyrsxmhBZKwLB7zU20iY6WbkPA"`
  - `TELEGRAM_CHAT_ID="972393810"`
- Cơ chế bảo vệ: Chỉ gửi tới `TELEGRAM_CHAT_ID` đã cấu hình. (Ở Level 2: Bỏ qua 100% request từ bất kỳ User ID nào khác).

### 2.2 Client & Error Handling
- Không sử dụng thư viện bên thứ 3 nặng (như `python-telegram-bot` hay `aiogram`), dùng `urllib.request` nguyên bản của Python để đảm bảo tốc độ khởi động nhanh (<50ms) và không xung đột môi trường.
- Bọc `try...except` an toàn: nếu Telegram API gặp sự cố timeout (10s) hoặc mất kết nối mạng, lỗi được ghi nhận vào stderr/log nhưng **không được phép làm dừng hoặc crash** tiến trình chính (Crypto Engine hay Video Rendering).
- Chế độ `--dry-run`: In trực tiếp nội dung tin nhắn ra console mà không thực hiện HTTP request.

---

## 3. Định Dạng Tin Nhắn (Notification Formats)

### 3.1 Crypto Daily Review Card
```html
📊 <b>CRYPTO DAILY REVIEW — 12/10/2026</b>
━━━━━━━━━━━━━━━━━━━━
💰 <b>Tổng tài sản (TTS):</b> 512.500.000 VND
🛡️ <b>Sàn cứng kỷ luật:</b> 540.000.000 VND (⚠️ Thủng 27.500.000 VND)
📈 <b>Tỷ giá & Vị thế:</b>
  • BTC: $84,140 (0.15931 BTC ≈ 349.6tr)
  • SOL: $113.0 (55.28 SOL ≈ 163.0tr)
  • P2P USDT: 25,895 VND
🚨 <b>Khuyến nghị hành động:</b>
  👉 Kích hoạt lệnh bán SOL ra USDT ngay lập tức để khử rủi ro.
━━━━━━━━━━━━━━━━━━━━
⏳ <i>Hạn chót bảo toàn vốn: 31/10/2026</i>
```

### 3.2 Video Pipeline Status Card
```html
🎬 <b>VIDEO PIPELINE — KHUNG GIỜ 12:00</b>
━━━━━━━━━━━━━━━━━━━━
📺 <b>Kênh:</b> Mê Tech
📌 <b>Chủ đề:</b> <code>quinnipiac-ai-trust-crisis</code>
🚦 <b>Trạng thái các Gate:</b>
  • Gate 1 (Kịch bản & Research): ✅ PASS
  • Gate 2 (Audio & Subtitles): ✅ PASS
  • Render Video: ✅ COMPLETED
  • Upload & Publish: ✅ SUCCESS (TikTok, YouTube, Facebook)
━━━━━━━━━━━━━━━━━━━━
⏰ <i>Slot kế tiếp: 20:00 (Kênh 3)</i>
```

### 3.3 Pipeline Alert Card
```html
🚨 <b>CẢNH BÁO HỆ THỐNG — VIDEO PIPELINE</b>
━━━━━━━━━━━━━━━━━━━━
⚠️ <b>Kênh:</b> Tâm An Lạc (Slot 08:00)
❌ <b>Lỗi phát hiện:</b> Chrome CDP port 9222 không phản hồi khi auto-publish.
🛠️ <b>Hành động cần làm:</b> Kiểm tra profile Chrome và mở lại cổng debug.
```

---

## 4. Kế Hoạch Kiểm Thử (Testing & Verification)
1. **Unit Test `test_client.py`**:
   - Mock response Telegram API HTTP 200: Gửi thành công.
   - Mock response HTTP 400/500/timeout: Xử lý lỗi mượt mà, trả về `False` thay vì crash.
   - Test chế độ Dry-run in output.
2. **Unit Test `test_notifier.py`**:
   - Kiểm tra format chuỗi HTML cho Crypto Review, Video Pipeline slot, và Alert.
   - Đảm bảo các ký tự HTML đặc biệt (`<`, `>`, `&`) được escape đúng chuẩn.
3. **End-to-End Live Verification**:
   - Chạy lệnh test trực tiếp với bot `@thientm_jarvis_bot`:
     ```bash
     python3 -m ops.telegram.cli --test "🚀 Kết nối Personal OS tới Telegram thành công!"
     ```
   - Xác nhận tin nhắn đã đến tài khoản Telegram cá nhân `972393810`.
