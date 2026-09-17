# Mê Tech — điểm vào duy nhất

> **@ đúng file này là đủ.** Nó trỏ tới mọi thứ còn lại.
> Kênh: Facebook Page "Mê Tech" (facebook.com/mecongnghe40) · TikTok · YouTube Shorts
> Định vị: "AI dễ hiểu" — tin AI tiếng Việt, ngắn, luôn có góc ứng dụng thực tế.

## Môi trường — agent không cần lo

`run.sh` **tự kiểm tra và tự vá** trước mỗi lần dựng: ffmpeg, uv, chứng chỉ,
`.venv`, font Be Vietnam Pro, Chromium, và phụ thuộc có khớp `pyproject.toml` không.
Thiếu gì thì tự gọi `bootstrap.sh`. Máy đã sẵn sàng thì mất **~0,3 giây**.

Chỉ hai thứ agent không tự cài được — thiếu thì dừng và báo người dùng:

```bash
brew install uv ffmpeg
```

Muốn kiểm tra mà không dựng: `./run.sh --doctor`

## Chạy một bài (câu lệnh cho agent)

> "chạy daily Mê Tech"

Agent làm theo đúng thứ tự dưới. Dừng lại ở hai chốt duyệt.

### 1 · Chọn tin
- Đọc `logs/{YYYY-MM}.md` → `grep -i "<từ khoá>" logs/*.md` để **chống trùng**
- Research tin AI 24–48h. Ưu tiên: có góc ứng dụng cho người Việt bình thường > có số kiểm chứng được > chưa nằm trong log

### 2 · Viết kịch bản
- Tạo `pipeline/content/<slug>.json`, lấy `pipeline/content/gemini-live.json` làm mẫu
- Luật: **mỗi câu = một nhịp hình** · không kết câu bằng từ viết tắt hay số · số trong `say` viết bằng chữ, trong `show` viết bằng chữ số · từ viết tắt cứ viết thường, `pronounce.json` lo phần đọc
- 🛑 **CHỐT 1 — Thiện duyệt kịch bản.** Sửa chữ ở đây rẻ hơn sửa sau khi render

### 3 · Dựng
```bash
cd pipeline && ./run.sh content/<slug>.json
```
→ `render/<slug>.mp4` (~4 phút). Một file, dùng cho cả ba nền tảng.
- 🛑 **CHỐT 2 — Thiện duyệt video.** Nghe kỹ câu cuối và các mốc số đếm

### 4 · Đăng
| Nền tảng | Khung giờ | Ghi chú |
|---|---|---|
| Facebook Reels | 12:00 / 21:00 | đăng với tư cách Page, Public |
| YouTube Shorts | cùng khung | cùng file, không xuất lại |
| TikTok | lệch 30 phút | cùng file (đã có nhạc nền sẵn) |

### 5 · Ghi log
1 dòng/bài vào `logs/{YYYY-MM}.md`. Sau 24h cập nhật reach/views.

---

## Rule cứng

- **2 bài/ngày mỗi nền tảng, cách nhau ≥ 8 tiếng.** Khung 12:00 và 21:00
- Không đăng 00:00–06:00
- Không đủ tin hay thì đăng 1 bài, hoặc nghỉ. **Không lấp chỗ**
- Không lấy ảnh từ bài báo

Bằng chứng cho rule này, cùng toàn bộ gotcha từng nền tảng: `me-tech-plan.md`

---

## Bản đồ file

| Cần gì | Đọc |
|---|---|
| Rule đầy đủ, bằng chứng số liệu, gotcha Facebook/TikTok/YouTube, quy trình chi tiết | `me-tech-plan.md` |
| Bài đã đăng — tra trước khi chọn tin | `logs/{YYYY-MM}.md` |
| Cách viết `content/*.json`, các `show.type`, các cờ | `pipeline/README.md` |
| Cài đặt, chạy trong Claude Code, bẫy chứng chỉ CITIGO | `pipeline/SETUP.md` |
| Từ viết tắt đọc sai | `pipeline/pronounce.json` |

**Thư mục bị ignore, đừng đọc:** `render/`, `pipeline/.work/`, `pipeline/.venv/`, `pipeline/_legacy/`

---

## Phần nào cần AI, phần nào không

| Bước | Cần agent? |
|---|---|
| 1 · Chọn tin, đánh giá góc ứng dụng | ✅ có |
| 2 · Viết kịch bản tiếng Việt | ✅ có |
| 3 · Dựng video (`build.py`) | ❌ **script thuần**, không gọi AI nào |
| 4 · Đăng qua trình duyệt | ⚠️ tạm thời cần — xem ghi chú dưới |
| 5 · Ghi log | ❌ script được |

Bước 3 đã là script hoàn toàn: TTS chạy local, Whisper chạy local, ffmpeg. Không có lệnh gọi API AI nào.

Bước 4 hiện dùng Chrome vì selector hay đổi. **Có thể script hoá bằng API chính thức** — Facebook Graph API (Reels lên Page), YouTube Data API (`videos.insert`), TikTok Content Posting API. Cả ba đều cần đăng ký app và được duyệt. Khi xong bước đó thì bước 4 cũng thành script, và cả quy trình chỉ còn bước 1–2 cần agent.
