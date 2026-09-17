# Chạy Mê Tech trong Claude Code (macOS)

Pipeline này dựng xong trong Cowork, nhưng **chạy được nguyên xi trong Claude Code** — và nên chuyển sang đó, vì Cowork bị chặn egress nên không gọi được API TTS (FPT.AI, Google) từ script.

## 1. Cài một lần

```bash
brew install ffmpeg
npm i playwright && npx playwright install chromium
pip3 install numpy scipy pillow
uv add --native-tls vieneu faster-whisper playwright   # trong venv của pipeline
```

Font: tải **Be Vietnam Pro** từ Google Fonts, kéo vào Font Book. Không có font thì Chromium rơi về font mặc định và bố cục chữ trong video sẽ vỡ.

Kiểm tra:
```bash
ffmpeg -version | head -1
node -e "require.resolve('playwright')" && echo playwright ok
python3 -c "import numpy,scipy,PIL; print('py ok')"
fc-list 2>/dev/null | grep -ci "be vietnam" || ls ~/Library/Fonts | grep -i bevietnam
```

## 2. Dựng video

```bash
cd me-tech/pipeline
# sửa nội dung bài mới trong scene.js (xem README.md)
./build.sh <slug>
```

Ra `<slug>_music.mp4` (Facebook Reels + YouTube Shorts) và `<slug>_mute.mp4` (TikTok).
Chuyển vào `../render/` khi xong. Khoảng 2,5 phút cho video 32 giây.

## 3. Chrome — đăng bài

Claude Code dùng **chính extension Claude in Chrome**, cùng bộ tool với Cowork:

```bash
claude --chrome
```

- Cần extension bản **1.0.36+**
- Phải đăng nhập bằng `/login` — **không chạy với API key** hay token dài hạn
- Gõ `/chrome` trong phiên để kiểm tra kết nối, cấp quyền site, chọn browser
- Dùng đúng profile Chrome đang đăng nhập → cookie Facebook/TikTok/YouTube có sẵn

Mọi gotcha trong `me-tech-plan.md` mục 5 (paste ClipboardEvent, Add sound TikTok, bài TikTok đã hẹn không sửa được lịch) áp dụng y nguyên.

## 4. Chạy tự động hằng ngày — chia đôi quy trình

Claude Code chạy headless được:

```bash
claude -p "chạy daily Mê Tech, dừng trước bước đăng" \
  --permission-mode acceptEdits --permission-prompts none --output-format json
```

Lên lịch thì có ba đường: `/schedule` (Cloud Routines, tối thiểu 1 giờ, chạy trên cloud không cần máy bật), Scheduled Tasks trong app Claude desktop (chạy nền trên máy, tối thiểu 1 phút), hoặc `launchd`/`cron` tự viết. Tài liệu chính thức có nhắc launchd/cron nhưng **không có hướng dẫn cụ thể**.

> ⚠️ **Đừng lên lịch cho bước đăng bài.**
> Tài liệu của Claude Code **không nói gì** về việc `--chrome` có chạy được cùng `-p` (headless) hay không — trang Chrome không nhắc headless, trang headless không nhắc Chrome. Khả năng cao là treo hoặc lỗi "extension not connected", và cơ chế duyệt quyền site không có đường pre-approve cho chạy nền.
>
> Mà thật ra cũng không nên: nhịp mới là 2 bài/ngày **có Thiện duyệt nội dung trước khi đăng**.

**Cách chia đúng:**

| Phần | Chạy thế nào |
|---|---|
| Research tin + viết copy + render ảnh + render video + TTS | headless được, lên lịch thoải mái — không đụng browser |
| Thiện duyệt | trong chat |
| Đăng / hẹn giờ lên 3 nền tảng | phiên tương tác, `claude --chrome` |

Tức là: cron gọi `claude -p` lúc sáng để chuẩn bị sẵn bài, đến lúc bạn rảnh thì mở phiên tương tác, xem, duyệt, đăng.

## 5. Key API

Để trong `me-tech/.env` (đã có trong `.gitignore`). **Không commit key lên git**, kể cả repo riêng.

```
FPT_API_KEY=...
GOOGLE_TTS_KEY=...
```

## 6. Bàn giao ngữ cảnh

Claude Code không thấy lịch sử chat của Cowork. Nhưng `CLAUDE.MD` → `AGENTS.MD` → `INDEX.md` đã trỏ sẵn tới `me-tech/`, nên phiên mới chỉ cần đọc theo đường đó là nắm đủ. Gõ **"chạy daily Mê Tech"**.
