# Đăng bài — Playwright trên hồ sơ Chrome riêng

Hồ sơ riêng `~/.me-tech-browser` (đã đăng nhập sẵn FB Mê Tech · TikTok Mê Tech ·
YouTube "Mê Tech vn"). Chạy song song được với Chrome cá nhân vì khác `user-data-dir`.

## Mở trình duyệt một lần, rồi mới chạy script

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --user-data-dir="$HOME/.me-tech-browser" \
  --remote-debugging-port=9333 --no-first-run --no-default-browser-check &
```

Script nối vào qua CDP (`_conn.py`), **không tự mở trình duyệt** — nhờ vậy phiên
đăng nhập giữ nguyên và Thiện nhìn được mọi thao tác.

## Bẫy đã gặp — đừng mắc lại

| Bẫy | Cách né |
|---|---|
| `setInputFiles` của Playwright dùng CDP nên file được coi là người chọn thật — extension nhét `File` object thì FB/TikTok **không đọc được** | luôn dùng Playwright, đừng dùng extension |
| Meta Business Suite: nút "Add video" mở hộp chọn file, **không có** `input[type=file]` sẵn | `expect_file_chooser()` |
| Nhãn nút Facebook có ký tự zero-width ở cuối (`"Next​"`) | khớp bằng regex, đừng `exact=True` |
| Toast "System dark mode is now off" chặn click | **đừng** xoá `.__fb-dark-mode` — nó bọc cả app, xoá là trắng trang. Bấm nút đóng toast, hoặc `click(force=True)` |
| Facebook đang "Publishing your post…" mà điều hướng tab đó đi chỗ khác | mở tab mới để kiểm tra, đừng đụng tab composer |
| YouTube Studio tự điều hướng (`themeRefresh`) ngay sau khi vào | chờ ~9s rồi mới thao tác; làm trọn luồng trong **một** script |
| YouTube: sau khi bấm Publish, `ytcp-video-share-dialog` che hết — trông như chưa đăng | đọc chính dialog đó để lấy link |
| TikTok hỏi "Continue to post?" khi check chưa xong | bấm "Post now" |
| TikTok: bài mới luôn ở "Content under review / Only me" một lúc | bình thường, tự mở công khai sau khi duyệt |

## Luật nội dung

- **TikTok: không chọn nhạc TikTok.** Video đã có nhạc nền, phải giữ "Original sound"
- Facebook đăng với tư cách **Page Mê Tech** (Business Suite, `asset_id=403727472998689`),
  không phải trang cá nhân — `facebook.com/reels/create` sẽ đăng nhầm sang cá nhân
- YouTube: kênh "Mê Tech vn" (`UCnElgDX9q_AYGdFc2oDuWUA`), Public, "không dành cho trẻ em"

`meta.py` giữ caption của từng nền tảng. `_scratch/` là script dùng một lần khi dò
selector — xoá được.
