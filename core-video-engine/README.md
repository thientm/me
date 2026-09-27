# pipeline — dựng video Mê Tech

```bash
./run.sh content/<slug>.json            # → ../render/<slug>.mp4
./run.sh content/<slug>.json --preview  # thêm bản 540x960 nhẹ để gửi duyệt
./run.sh content/<slug>.json --skip-tts # giữ giọng cũ, chỉ dựng lại hình
./run.sh --doctor                       # kiểm tra môi trường, không dựng
```

Luật nội dung và ngữ pháp hình nằm ở `../AGENTS.md`. File này chỉ nói **cách viết
file nội dung** và **mỗi script làm gì**.

## Chuỗi việc

```
content/<slug>.json
   │
   ├─ tts.py ──► render/vo/<slug>.vo.wav  +  .timing.json     ← nguồn sự thật về thời gian
   ├─ words.py ─► .work/data.js       mốc TỪNG CHỮ (Whisper)
   ├─ deck.py ──► .work/deck.js       gom câu thành trạm, chọn chế độ hình
   ├─ music.py ─► .work/bed.wav       nhạc nền tự tổng hợp
   ├─ chime.py ─► .work/chime.wav     chuông cảnh kết tự tổng hợp
   │
   ├─ scene.html + Playwright ──► .work/frames/
   └─ ffmpeg ──────────────────► render/<slug>.mp4
```

Không có lệnh gọi API AI nào. TTS và Whisper đều chạy local.

## Viết `content/<slug>.json`

```jsonc
{
  "slug": "lawzero",
  "voice": "Xuân Vĩnh",
  "brand": "MÊ TECH",
  "kicker": "LAWZERO · 16.09.2026",   // góc dưới trái
  "date": "17.09.2026",               // góc trên phải
  "gap": 0.24, "lead_in": 0.40, "tail": 2.20,
  "outro": {"mark": "Mê Tech", "handle": "mecongnghe40"},

  "data": { ... },                    // chỉ cần khi có câu mode "data"
  "segments": [ ... ]
}
```

### Mỗi câu

| Khoá | Bắt buộc | Nghĩa |
|---|---|---|
| `id` | ✅ | tên ngắn, hiện trong log dựng |
| `group` | ✅ | các câu liên tiếp cùng `group` chung MỘT trạm — máy quay chỉ lia giữa các trạm |
| `mode` | ✅ | `say` · `data` · `step` · `outro`. Câu cuối **bắt buộc** là `outro` |
| `lab` | | nhãn nhỏ trên trạm; chỉ lấy từ câu ĐẦU của group |
| `say` | ✅ | lời đọc. Số viết bằng chữ, từ viết tắt viết như cách đọc |
| `plain` | ✅ | câu ở dạng người đọc — dùng để chọn cỡ chữ |
| `words` | ✅ | chữ hiện trên hình, tách rời để bật sáng theo giọng |
| `weights` | ✅ | mỗi chữ ứng với mấy âm tiết khi đọc. `"20 GB"` ↔ "hai mươi gi-ga" → `4` |
| `hot` | | chỉ số chữ được tô hổ phách |
| `cards` | với `step` | `[{n, t, d}]` — số thứ tự, tiêu đề, mô tả |
| `splitAt` | với `step` | khi MỘT câu tả cả hai bước: cắt tại chữ thứ mấy |

`weights` là chỗ dễ sai nhất. Sai thì chữ sáng lệch nhịp nói.
Đếm đúng số âm tiết mà chữ đó thay mặt trong `say`.

### Khối `data`

```jsonc
"data": {
  "cells": 36, "unit": 10, "suffix": "việc làm",
  "unitLabel": "1 ô = 10 việc làm",
  "parkLabel": "phần nằm lại trên SSD",     // nhãn cho các ô bị bỏ đi, nếu có
  "stages": [
    {"at": [8, 3], "fill": 36, "color": "now", "label": "toàn thời gian, tại Canada"}
  ]
}
```

- `at` = `[chỉ số câu, chỉ số chữ]` — khối chạy đúng lúc chữ đó được đọc
- `fill` = số ô sau chặng này. Tăng thì ô hiện thêm, **giảm thì ô rơi xuống vạch dưới**
- `color` = `now` (hổ phách) hoặc `was` (xanh rêu)
- Số đọc ra = `ô đang có × unit`, nên luôn khớp với hình. `unit` nguyên thì không hiện số lẻ

## Kiểm tra trước khi giao

- `build.py` tự báo nếu tổng thời lượng lệch khỏi **32–38 giây**
- Cổng Whisper chạy trên từng câu; câu nào không đạt sẽ in `⚠ KHÔNG BẢN NÀO ĐẠT`
  kèm text nghe được — đọc dòng đó rồi sửa `say`, đừng bỏ qua
- Soi vài khung hình trước khi gửi duyệt:
  ```bash
  ffmpeg -i ../render/<slug>.preview.mp4 \
    -vf "select='eq(n\,60)+eq(n\,400)+eq(n\,900)',scale=240:-2,tile=3x1" \
    -frames:v 1 .work/sheet.jpg
  ```

## Thông số đã chốt — đừng đổi nếu không có lý do đo được

| Ở đâu | Là gì |
|---|---|
| `scene.html` `SPEED=1150` | tốc độ lia, px/giây. Bản cũ 3.000 và bị chê nhức mắt |
| `scene.html` `MV_MIN/MAX` | 0,85–1,80 giây mỗi cú lia |
| `scene.html` `eSine` | easing sin, không phải cubic — cubic có đoạn giật tốc |
| `scene.html` `:root` | bảng màu có nghĩa, xem `../AGENTS.md` |
| `build.py` `BED_DB=-9` | mức nhạc nền |
| `build.py` `TARGET` | khoảng thời lượng 32–38s |
| `chime.py` `NOTES` | chuông A5 → E6, lệch 0,17s |
