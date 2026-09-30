# Tâm An Lạc - Rules and Guidelines

Brand Name: Tâm An Lạc
Theme: Buddhism, Dharma, peaceful meditation teachings.
Target Audience: Normal middle and high age (35-65+).

## Visual Rules
- **Text**: Show text larger (approx 78px) for readability.
- **Effects**: No artificial geometric overlays or harsh effects (no HTML halos). Visuals must be completely serene, natural, and calm. Use AI-generated images with natural lighting (e.g., god rays).
- **Animation**: Use GSAP for buttery-smooth Ken Burns zooms and text cross-dissolves. Ken Burns zoom should be slightly faster (e.g., ~7.8% zoom over 12s).
- **Safezone**: Follow standard 9:16 safezones (Y: 1050px to 1420px approx) to ensure compatibility across YouTube Shorts, TikTok, and Facebook Reels.

## Audio & Outro Rules
- **Voice**: Use TTS preset `Thiền Tâm Đức` (Northern, meditative storytelling).
- **Outro**: Silent outro optimized for looping across 3 platforms. No TTS reading channel name or CTA. Use a temple bell/chime to trigger a seamless loop.

## Publishing & Platforms
The automated publishing scripts should use the local isolated Chrome profile (`chrome_profile/`) to maintain logged-in sessions for these platforms:
- **YouTube Shorts**: https://www.youtube.com/@tamanlac.youtube
- **TikTok**: https://www.tiktok.com/@tamanlac.tiktok
- **Facebook Reels**: https://www.facebook.com/tamanlac.fb

## Content Rules — chốt 30.09.2026 (Thiện)
- **Không giảng nội dung kinh.** Không đọc nguyên văn kệ/kinh, không dùng lời dịch Hán-Việt cổ ("Ý dẫn đầu các pháp", "phẩm Song Yếu"…), không nêu tên kinh hay số kệ trong lời đọc — người nghe 35–65+ thấy khó hiểu, lướt qua.
- **Nói về lời dạy của Phật bằng lời đời thường**: một bài học sống (buông bỏ, nhẫn nhịn, biết đủ, lời nói, giận dữ, cha mẹ, vô thường…), kể bằng một tình huống quen thuộc (gia đình, công việc, tuổi già, con cái), rồi một điều làm được ngay hôm nay.
- Mạch 30–45s: câu mở chạm đúng nỗi lòng người nghe (≤2 giây, dạng câu hỏi hoặc tình huống) → điều Phật dạy, nói giản dị → ví dụ đời thường → một việc nhỏ để thực hành → chuông.
- **Không bịa lời Phật.** Mỗi bài phải dựa trên một lời dạy có thật; nguồn (kinh, kệ, bản dịch) chỉ ghi ở `script.json` → `"source"` và mô tả YouTube, **không đọc trong video**. Không có nguồn chắc chắn thì nói "lời Phật dạy về…" ở dạng khái quát, không dựng câu trích dẫn.
- Không hứa hẹn tâm linh (phước báu, đổi vận, chữa bệnh), không so sánh tôn giáo, không chính trị.

## Quy trình một bài (tạm, tới khi gộp engine — xem kế hoạch gộp 29.09.2026)
Lịch: 3 khung như me-tech — 08:00, 12:00, 20:00 (dựng trước ~2 tiếng). Orchestrator giao cho một sub-agent mỗi khung.
1. **Nội dung:** chép `content/002_y_dan_dau/` sang `content/<NNN>_<slug>/`, viết lại `script.json` (luật ở trên, `voice` = "Thiền Tâm Đức"), `meta.json` (yt_title, yt_desc có nguồn, tt_caption, fb_caption, fb_tags). `scene.html` chép từ bài trước — cue chữ lấy từ `window.TIMING`. **Ảnh: sinh MỚI cho từng bài** (luật gốc: ảnh AI, ánh sáng tự nhiên) bằng `../me-tech/pipeline/.venv/bin/python render_pipeline/gen_images.py <slug> "<cảnh 1>" "<cảnh 2>" "<cảnh 3>"` → `content/<slug>/img_{1,2,3}.jpg` (1080x1920), scene.html trỏ `url('img_1.jpg')`…; mỗi cảnh tả đúng nội dung câu đang đọc; sổ `logs/images.json` — không dùng lại ảnh đã dùng.
2. **Dựng:** `cd tam-an-lac && SSL_CERT_FILE=../me-tech/pipeline/ca-bundle.pem ../me-tech/pipeline/.venv/bin/python render_pipeline/build.py <slug>` → `content/<slug>/video.mp4`. Soát: câu mở ≤2s, 30–45s, contact sheet (chữ 78px, Y 1050–1420, ≤3 dòng).
3. **Đăng YT + TT** bằng bộ script me-tech đã chép ở `_pubkit/a/publish/` (cổng 9555, kênh `UCjEteQMJ4zzFV9_iKvChpvA`):
   - `./open_browser.sh` (gọi `me-tech/ops/open_chrome.py`, mở nền không cướp chuột) nếu 9555 tắt → `python3 ../me-tech/ops/fresh_browser.py 9555` → `python3 ../me-tech/ops/whois.py 9555 --yt UCjEteQMJ4zzFV9_iKvChpvA --tt tamanlac.tiktok` (sai thì DỪNG).
   - `cp content/<slug>/video.mp4 _pubkit/<slug>.mp4`; viết `_pubkit/a/publish/meta_<slug>.py` (VIDEO tuyệt đối tới bản chép, YT_TITLE không emoji, YT_DESC, FB_CAPTION = fb_caption + tags, TT_CAPTION); ghi slug vào `_pubkit/a/publish/ACTIVE`.
   - `cd _pubkit/a/publish && PY=../../../../me-tech/pipeline/.venv/bin/python`: `$PY yt.py [--at HH:MM]` → `$PY yt_verify.py`; `$PY tt.py [--at HH:MM]` (tự bấm "Got it") → `$PY tt_verify.py`. Đọc MÃ THOÁT.
4. **Đăng FB** qua Chrome me-tech 9333 (tài khoản thientm quản lý Page): cùng thư mục, `$PY fb.py [--at HH:MM]` → `$PY fb_verify.py` (bản chép của me-tech fb.py, `ASSET` = Page Tâm An Lạc, nối 9333 qua `_conn_fb.py`). Giữ khoá `mkdir ../me-tech/.run/fb9333.lock` trong lúc đăng FB, xong `rmdir`. **Không** chạy fresh_browser trên 9333, không bấm Switch profile.
5. **Log:** thêm entry vào `logs/<YYYY-MM>.md` (append-only). Sổ chống trùng: `_pubkit/logs/posted.json`.
- **Xong kênh là tắt Chrome** (chốt 30.09.2026): đăng + verify xong → `python3 ../me-tech/ops/close_browser.py 9555` (CDP Browser.close, không pkill). Không tự tắt 9333 — orchestrator tắt khi cả 3 kênh xong.

## Ảnh AI — Antigravity CLI `agy` (30.09.2026)
- `gen_images.py` gọi `agy -p` (công cụ `generate_image`, model ảnh `gemini-3.1-flash-image`), tự dừng agy khi ảnh ghi xong (agy không tự thoát).
- **Quota tài khoản hiện tại rất thấp: ~1 ảnh / ~5 giờ** (lỗi 429 RESOURCE_EXHAUSTED "You have exhausted your capacity on this model"). Script báo `[X] HẾT QUOTA … reset sau …` ngay.
- Khi hết quota (TẠM, chờ Thiện chốt cách xử lý): dùng ảnh AI đã sinh trước mà **chưa dùng trong 7 ngày** theo `logs/images.json`; không có thì dùng `templates/buddha_*.jpg` và ghi rõ "ảnh dùng lại (hết quota agy)" trong log bài.
