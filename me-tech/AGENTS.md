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
- Tạo `pipeline/content/<slug>.json`, lấy `pipeline/content/lawzero.json` làm mẫu
- **Độ dài chốt: 32–38 giây** (~12–14 câu). `build.py` tự cảnh báo nếu lệch ra ngoài
- Mỗi câu khai một `mode` và một `group` — xem **Ngữ pháp hình** bên dưới
- Luật chữ: số trong `say` viết bằng chữ, trong `words` viết bằng chữ số, kèm `weights`
  là số âm tiết mà chữ đó đại diện khi đọc lên ("20 GB" ↔ "hai mươi gi-ga" → weight 4)
- Không kết câu bằng từ viết tắt · từ viết tắt cứ viết thường, `pronounce.json` lo phần đọc
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

## Ngữ pháp hình — chốt 17.09.2026

Không phải mỗi tin một phong cách. **Mỗi câu một chế độ, trong cùng một nhận diện.**
Agent chọn `mode` cho từng câu theo đúng luật này:

| `mode` | Dùng khi | Hình ra sao |
|---|---|---|
| `say` | mặc định — câu không rơi vào hai dòng dưới | Chữ ăn theo giọng, cỡ lớn |
| `data` | câu có con số đáng kể, có thứ để đếm hoặc so trước/sau | Lưới ô, mỗi ô là một đơn vị thật; số đọc ra bám đúng số ô |
| `step` | từ hai bước trở lên, có thứ tự | Các thẻ cùng nằm trong một khung, sáng dần theo lời |
| `outro` | **luôn là câu cuối**, không bao giờ đổi | Cảnh kết dùng chung |

`group` gom các câu liên tiếp vào **một trạm**. Máy quay chỉ lia giữa các trạm,
không lia theo từng câu — 13 câu mà chỉ 6 cú lia là nhờ vậy.
Nhắm **5–7 trạm** cho một bài 35 giây.

**Cảnh kết dùng chung** — đừng viết lại cho từng bài:
lời đúng hai chữ "Mê Tếch" · wordmark hổ phách + tên trang · chuông hai nốt A5→E6
tự tổng hợp, vào trước lời 0,30 giây · hai vòng sóng nở theo chuông.

**Bảng màu có nghĩa** — mỗi màu một việc, không dùng để trang trí:

| Màu | Nghĩa |
|---|---|
| Hổ phách `#FFAE2B` | cái đang xảy ra: chữ đang đọc, con số mới, trạng thái sau, số thứ tự bước |
| Xanh rêu `#7E9A87` | cái đang bị thay thế: trạng thái trước, các ô bị bỏ đi |
| Mực ấm `#0E0D0B` | nền — ngả nâu, không ngả xanh |
| Giấy ngà `#F5F1E8` | chữ đã đọc (chữ chưa đọc là chính nó ở 11%) |

**Đừng đụng vào** trong `scene.html` nếu không có lý do đo được:
`SPEED=1150` px/giây · `MV_MIN/MAX` 0,85–1,80 giây mỗi cú lia · easing `eSine`.
Bản trước lia ~3.000 px/giây và bị đánh giá là nhức mắt.

---

## Rule cứng

- **2 bài/ngày mỗi nền tảng, cách nhau ≥ 8 tiếng.** Khung 12:00 và 21:00
- **Video 32–38 giây.** Vùng giao của cả ba nền tảng, một file đăng cả ba
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
| Cách viết `content/*.json`, các `mode`, các cờ | `pipeline/README.md` |
| Cài đặt, chạy trong Claude Code, bẫy chứng chỉ CITIGO | `pipeline/SETUP.md` |
| Từ viết tắt đọc sai | `pipeline/pronounce.json` |

**Thư mục bị ignore, đừng đọc:** `render/`, `pipeline/.work/`, `pipeline/.venv/`

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
