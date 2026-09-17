# Pipeline dựng video Mê Tech

Một lệnh, ra một file, đăng cả ba nền tảng.

```bash
cd me-tech/pipeline
python build.py content/gemini-live.json
```

→ `../render/<slug>.mp4` — **dùng chung cho Facebook Reels, YouTube Shorts và TikTok.**

## Cấu trúc

```
me-tech/
├── me-tech-plan.md              📌 rule nhịp đăng + quy trình đầy đủ (mục 9)
├── logs/2026-09.md              📌 index bài đã đăng — tra trước khi chọn tin
│
├── pipeline/                    ── TOÀN BỘ SOURCE Ở ĐÂY
│   ├── README.md                   file này
│   ├── SETUP.md                    cài đặt, cách chạy trong Claude Code
│   │
│   ├── content/<slug>.json      ✏️  KỊCH BẢN TỪNG BÀI — thứ duy nhất soạn mỗi ngày
│   ├── pronounce.json           ✏️  từ điển phát âm (AI → ây ai). Thêm khi gặp từ đọc sai
│   │
│   ├── build.py                    điều phối cả chuỗi
│   ├── tts.py                      giọng đọc + cổng Whisper + timing.json
│   ├── render.py                   timing.json → HTML → frame
│   ├── music.py                    nhạc nền
│   │
│   ├── .venv/                   🚫 ignore
│   └── .work/                   🚫 ignore — frames, video.html, bed.wav, file tạm
│
└── render/                      🚫 ignore — toàn bộ đầu ra
    ├── <slug>.mp4                  bản chính
    └── vo/                         vo.wav, timing.json, probe/
```

## Mỗi ngày cần @ những file nào

| Việc | @ file |
|---|---|
| Chọn tin, tránh trùng | `me-tech/logs/2026-09.md` |
| Nhớ rule nhịp đăng, khung giờ, gotcha từng nền tảng | `me-tech/me-tech-plan.md` |
| Viết kịch bản bài mới | `pipeline/content/<slug-bài-cũ>.json` (làm mẫu) |

Ba file đó là đủ. Không cần @ code — agent tự đọc khi chạy `build.py`.

## Các cờ

| Cờ | Dùng khi |
|---|---|
| *(không có)* | mặc định — ra 1 file có nhạc nền, đăng cả 3 nơi |
| `--vo-only` | xuất thêm bản **không nhạc**, chỉ khi muốn đè sound native của TikTok |
| `--skip-tts` | đã có giọng, chỉ dựng lại hình (sửa layout, đổi màu…) |
| `--no-verify` | bỏ cổng Whisper cho nhanh — chỉ khi đang thử nghiệm |

## Viết `content/<slug>.json`

```jsonc
{
  "slug": "ten-bai",
  "voice": "Xuân Vĩnh",
  "date_label": "TIN AI · 17.09.2026",
  "gap": 0.30,        // nghỉ giữa hai câu
  "lead_in": 0.60,    // im lặng đầu video
  "tail": 2.20,       // im lặng cuối, cho nhạc fade
  "segments": [
    { "id": "hook", "scene": "hook",
      "say":  "Câu này sẽ được đọc.",
      "show": { "type": "hook", "line1": "…", "line2": "…" } }
  ]
}
```

**Luật viết:**

- **Mỗi câu = một nhịp hình.** Câu nào đọc lên thì thứ tương ứng hiện ra.
- Các câu cùng một khung hình để chung `scene`.
- **Không kết câu bằng từ viết tắt hoặc con số** — luôn có từ tiếng Việt đứng cuối.
- Số trong `say` viết bằng chữ ("tám mươi hai phẩy sáu"); trong `show` viết bằng chữ số.
- Từ viết tắt viết bình thường — `pronounce.json` lo phần đọc.

**Các `show.type` có sẵn:** `hook`, `title`, `body`, `header`, `num`, `bullet`, `cta`.

## Lưu ý

- Độ dài video **do kịch bản quyết định**. Muốn ngắn lại thì cắt câu.
- `.work/` phình lên ~200MB lúc render rồi tự dọn.
- Máy này có proxy MITM của công ty → mọi lệnh Python/uv cần `SSL_CERT_FILE`. Xem `SETUP.md`.
