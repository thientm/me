# Đăng bài — Playwright trên hồ sơ Chrome riêng

Hồ sơ riêng `~/.me-tech-browser` (đã đăng nhập sẵn FB Mê Tech · TikTok Mê Tech ·
YouTube "Mê Tech vn"). Chạy song song được với Chrome cá nhân vì khác `user-data-dir`.

## ⛔ Chỉ nối CDP. Không bao giờ tự mở hồ sơ này bằng Playwright.

**19.09.2026 — mất sạch phiên đăng nhập cả ba nền tảng.** Điều tra:

| Bằng chứng | Kết luận |
|---|---|
| Bảng cookie còn **15 dòng** (hồ sơ Chrome thường của Thiện: ~1,2 MB) | các dòng bị **xoá**, không phải không giải mã được |
| `Default/Preferences` → `exit_type: Crashed` | Chrome bị giết cứng bằng `pkill` |
| 18.09: chỉ `connect_over_cdp`, không khởi động lại hồ sơ lần nào → không mất gì | |
| 19.09: hai lần `launch_persistent_context` lên đúng thư mục này (một lần giả lập iPhone) + một lần `pkill` | đây là thứ mới xuất hiện |

Không tách bạch được 100% giữa `launch_persistent_context` và `pkill`, nhưng cả hai
đều bị cấm từ nay, vì bản sửa giống nhau:

- Chrome mở **một lần bằng tay**, để nguyên đó. Script chỉ `connect_over_cdp` vào
- `_conn.connect()` **thoát ngay** nếu cổng 9333 chưa sống — không tự mở thay
- Cần đóng thì `_conn.quit_browser()` (osascript quit), **không `pkill`**
- Muốn đo giao diện di động → tạo hồ sơ vứt đi riêng, đừng đụng `~/.me-tech-browser`
- Mỗi script đăng gọi `require_login()` trước khi upload, hỏng thì hỏng sớm và nói rõ

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

## Hẹn giờ

Cả ba nền tảng đều có hẹn giờ sẵn — dùng cái đó, **không** dựng cron chạy lúc 21h
(cron đòi máy phải thức, Chrome phải còn đăng nhập, mạng phải thông đúng lúc).

```bash
python3 post.py --at 21:00        # cả ba
python3 post.py --only youtube --at 21:00
```

| Nền tảng | Tình trạng script | Ghi chú |
|---|---|---|
| YouTube | ✅ tự động được | Phần hẹn giờ nằm sau `#second-container-expand-button`. Ngày phải **bấm ô trong lịch**, gõ chữ là bị backdrop chặn. |
| Facebook | ⚠ điền được, cần kiểm | Ô `hours`/`minutes` ở bước Share. Bấm Schedule khi còn trống → FB tự lấy **now+1h**. |
| TikTok | ❌ phải bật tay | Radio `input[value=schedule]` là input ẩn, click không ăn; chưa dò ra phần tử hiện đúng. `tt.py --at` dừng lại nhờ người bật, rồi `python3 tt_finish.py`. |

### Luật cứng

`_conn.confirm_schedule()` **đọc lại** ngày/giờ trên giao diện trước khi cho bấm nút
hẹn. Trống hoặc sai thì thoát, không bấm.

> 19.09.2026: bấm Schedule trên Facebook lúc ô giờ còn trống → bài bị hẹn 16:02
> thay vì 21:00, phải nhờ Thiện vào sửa tay. Cùng ngày, YouTube nhận cú bấm
> Publish nhưng video vẫn nằm ở Draft. **Không bao giờ tin cú bấm — luôn đọc lại.**

### Script dò selector

Vứt vào `_scratch/` (đã gitignore). Đừng để lẫn ở thư mục gốc — 19.09 để rơi vãi
13 file dò dẫm ra ngoài.
