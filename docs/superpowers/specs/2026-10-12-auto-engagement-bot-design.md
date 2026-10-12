# Design Spec: Auto Engagement Bot (Reaction & Reply)

- **Date:** 2026-10-12
- **Topic:** Tự động hoá tương tác (Like, Heart, Reply Comment) đa nền tảng cho Mê Tech & Tâm An Lạc
- **Trạng thái:** Đã chốt qua Brainstorming

---

## 1. Mục tiêu & Bối cảnh

### 1.1 Mục tiêu
* Tự động thả tim / like bình luận của khán giả trên YouTube Studio, TikTok Studio và Facebook Business Suite.
* Tự động phản hồi (reply) bình luận hợp lệ theo đúng phong cách (persona) của từng kênh:
  * **Mê Tech:** Thân thiện, ngắn gọn, am hiểu công nghệ/AI, hỗ trợ giải đáp thắc mắc.
  * **Tâm An Lạc:** Điềm đạm, ấm áp, từ bi, lan tỏa an vui và chúc lành.
* Tăng chỉ số tương tác (engagement rate), giữ chân khán giả và kích thích thuật toán phân phối video.
* Vận hành hoàn toàn tự động theo chu kỳ quét thông minh, an toàn, không bị nền tảng gắn cờ spam.

### 1.2 Bối cảnh & Ràng buộc kỹ thuật
* **Hạ tầng sẵn có:** Trình duyệt Chrome chạy nền nối qua giao thức CDP (Chrome DevTools Protocol):
  * Cổng `9333`: Kênh Mê Tech & tài khoản quản trị Facebook Page.
  * Cổng `9555`: Kênh Tâm An Lạc.
* **Quy tắc an toàn hệ thống:**
  * Không cướp chuột / pop-up trước màn hình người dùng (`quiet mode`).
  * Không xung đột với tiến trình dựng & đăng video hiện hữu (`.run/build.lock` và `fb9333.lock`).
  * Rate-limit và Human-like delays nhằm tránh spam detection.

---

## 2. Kiến trúc hệ thống & Luồng xử lý (Data Flow)

```
[Cron / Launchd (08:30, 12:30, 16:30, 20:30)]
                    │
                    ▼
          ┌───────────────────┐
          │   Runner / CLI    │ ── Kiểm tra Lock (.run/build.lock, fb9333.lock)
          └─────────┬─────────┘    (Nếu bận -> tự hoãn chờ ca sau)
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
[Kênh Mê Tech - 9333]       [Kênh Tâm An Lạc - 9555]
      │                           │
      ├─ YouTube Studio           ├─ YouTube Studio
      ├─ TikTok Studio            ├─ TikTok Studio
      └─ Meta Business Suite      └─ Meta Business Suite
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                    ┌───────────────────────────┐
                    │  Comment Extractor        │ Lấy: id, text, author, platform
                    └─────────────┬─────────────┘
                                  ▼
                    ┌───────────────────────────┐
                    │  Ledger Check (Sổ đã lưu) │ Tra logs/engagement_ledger.json
                    └─────────────┬─────────────┘ (Đã xử lý -> Skip trong 1ms)
                                  ▼
                    ┌───────────────────────────┐
                    │  Rule & AI Engine         │
                    │  - Lọc Toxic/Spam         │ -> Bỏ qua
                    │  - Template xoay vòng     │ -> Dành cho chào / chúc / niệm Phật
                    │  - LLM Persona Generator  │ -> Dành cho câu hỏi / thảo luận
                    └─────────────┬─────────────┘
                                  ▼
                    ┌───────────────────────────┐
                    │  Playwright CDP Executor  │
                    │  - Bấm Tim / Like         │ (Delay 4-10s ngẫu nhiên)
                    │  - Gõ text Reply & Gửi    │
                    └─────────────┬─────────────┘
                                  ▼
                    ┌───────────────────────────┐
                    │  Update Ledger & Logs     │ Ghi nhận trạng thái hoàn tất
                    └───────────────────────────┘
```

---

## 3. Thiết kế chi tiết các thành phần

### 3.1 Bộ điều khiển & Chống xung đột (`runner.py`)
* Vị trí: `me-tech/ops/engagement/runner.py`
* Tham số dòng lệnh:
  * `--channel [metech|tamanlac|all]`
  * `--platform [yt|fb|tt|all]`
  * `--dry-run`: Chạy quét, trích xuất và sinh câu trả lời nhưng **không click/gửi thật**.
  * `--limit <N>`: Giới hạn số lượng comment xử lý mỗi lần (mặc định: 5 reply, 15 like).
* Kiểm tra Lock:
  * Đọc kiểm tra file lock `.run/build.lock` và `me-tech/.run/fb9333.lock`.
  * Nếu một trong hai lock đang hoạt động -> Ghi log thông báo và thoát nhẹ nhàng (`exit 0`), không gây gián đoạn pipeline render/publish.

### 3.2 Bộ lọc phân loại & Trí tuệ phản hồi (`brain/`)
1. **Lớp Rule Filter (`filter.py`):**
   * Danh sách từ khóa cấm/tiêu cực/quảng cáo rác: Bỏ qua hoàn toàn.
   * Nhận diện lời chào/khen/niệm Phật:
     * Tâm An Lạc: Nhận diện "a di đà phật", "quán thế âm", "cầu an", "chúc", "nam mô", v.v.
     * Mê Tech: Nhận diện "hay quá", "tuyệt", "hóng", "đỉnh", emoji chúc mừng, v.v.
2. **Template Xoay Vòng (`generator.py`):**
   * Lưu danh sách 15–20 câu chúc/cảm ơn đa dạng cho từng kênh.
   * Lựa chọn ngẫu nhiên có trọng số nhằm đảm bảo không gửi liên tiếp 2 câu giống hệt nhau trên cùng một video.
3. **LLM Generation (`personas.py`):**
   * Dành riêng cho câu hỏi và bình luận chia sẻ kiến thức.
   * Sử dụng Gemini API (flash model) gọn nhẹ, latency thấp.
   * **Persona Mê Tech:** Ngắn gọn (≤ 40 từ), xưng "ad" hoặc "mình" - "bạn", thực tế, gợi ý mở để người xem tiếp tục theo dõi.
   * **Persona Tâm An Lạc:** Nhẹ nhàng, trang nghiêm, ấm áp, không phán xét, không hứa hẹn tâm linh sai lệch.

### 3.3 Các bộ điều hợp nền tảng (`adapters/`)
1. **YouTube Studio (`yt_studio.py`):**
   * URL: `https://studio.youtube.com/channel/<CHANNEL_ID>/comments/inbox`
   * Sử dụng filter *"Tôi chưa trả lời"* (I haven't responded).
   * Lấy danh sách thẻ comment.
   * Bấm Creator Heart (`ytcp-icon-button#heart-button`) + Like (`ytcp-icon-button#like-button`).
   * Mở dialog reply, điền text theo nhịp gõ phím, bấm Submit.
2. **Meta Business Suite (`fb_business.py`):**
   * URL: `https://business.facebook.com/latest/inbox/fb_comments?asset_id=<ASSET_ID>`
   * Đọc danh sách comment mới của Page.
   * Bấm Like dưới tư cách Page.
   * Gõ phản hồi và gửi.
3. **TikTok Studio (`tt_studio.py`):**
   * URL: `https://www.tiktok.com/tiktokstudio/comment`
   * Lọc comment chưa tương tác.
   * Thả tim comment và gửi reply.

### 3.4 Sổ theo dõi & Chống lặp (`ledger.py`)
* File lưu trữ: `me-tech/ops/engagement/logs/engagement_ledger.json`
* Cấu trúc lưu:
  ```json
  {
    "yt:metech:comment_12345": {
      "timestamp": "2026-10-12T14:30:15",
      "author": "Nguyễn Văn A",
      "actions": ["heart", "reply"],
      "reply_text": "Cảm ơn bạn nhiều nha!...",
      "status": "success"
    }
  }
  ```

---

## 4. An toàn & Ngăn ngừa rủi ro (Guardrails)

| Rủi ro | Giải pháp kỹ thuật |
|---|---|
| Bị nền tảng phạt vì hành vi spam bot | Giới hạn ≤ 5-8 reply và ≤ 15-20 like mỗi lần chạy; ngẫu nhiên hóa thời gian chờ (4-10 giây giữa các thao tác). |
| AI trả lời ngớ ngẩn / sai kiến thức | Rule filter xử lý 70% trường hợp cơ bản; LLM có prompt ràng buộc nghiêm ngặt; trường hợp không chắc chắn -> chỉ thả tim, không reply. |
| Xung đột trình duyệt với pipeline đăng bài | Kiểm tra `.run/build.lock` và `fb9333.lock` trước khi khởi động; dùng hàm `quiet(browser, ctx)`. |
| Cướp chuột khi người dùng đang thao tác máy | Toàn bộ cửa sổ Chrome giữ trạng thái thu nhỏ / chạy nền như quy định tại `open_chrome.py`. |

---

## 5. Kế hoạch triển khai (Phased Rollout)

1. **Phase 1: Module Nền tảng & Brain:**
   * Dựng cấu trúc thư mục `me-tech/ops/engagement/`.
   * Cài đặt `ledger.py`, `filter.py`, `generator.py`, `personas.py`.
   * Test độc lập logic lọc & sinh reply bằng unit tests và mock data.
2. **Phase 2: YouTube Studio Adapter & Dry-Run:**
   * Cài đặt `yt_studio.py`.
   * Chạy thử với cờ `--dry-run` trên Chrome 9333 và 9555 để kiểm tra selector và chất lượng nội dung.
   * Kích hoạt chạy thực tế cho YouTube.
3. **Phase 3: Meta Business Suite & TikTok Studio:**
   * Cài đặt `fb_business.py` và `tt_studio.py`.
   * Test thực tế trên các cổng Chrome tương ứng.
4. **Phase 4: Tự động hóa qua Lịch trình (Cron / Launchd):**
   * Thiết lập lịch quét định kỳ vào 08:30 · 12:30 · 16:30 · 20:30.
   * Tích hợp cơ chế thông báo trạng thái hoặc ghi log kiểm toán.
