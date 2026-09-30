# Thiện Trần — Kênh Thương Hiệu Cá Nhân (AI & Tech Insight)

> **Đây là luồng làm việc chính thức cho kênh Thiện Trần.**
> Bất kỳ AI nào làm việc trong thư mục này đều phải tuân thủ nghiêm ngặt các quy tắc dưới đây.

## 1. CỐT LÕI NỘI DUNG (THE MISSION)
- **Định vị**: Kênh phân tích tín hiệu cao (High-Signal Filter), không phải máy đọc báo.
- **Tiêu chuẩn (Quality Gate)**:
  - Tách biệt rõ ràng: **FACT** (Sự thật/Số liệu) vs **INFERENCE** (Suy luận) vs **OPINION** (Góc nhìn).
  - Phải trả lời được: Điều này tạo ra thay đổi thực tế gì? Ai bị ảnh hưởng? Hype vs Substance là gì?
  - Bỏ qua: Tin đồn vô căn cứ, tin PR sáo rỗng của công ty, thông báo không mang lại giá trị thực tế.

## 2. QUY TẮC DỰNG VIDEO (RENDER ENGINE)
- **Cấu trúc JSON**:
  - `hook` phải < 10 từ. Đi thẳng vào vấn đề.
  - Phải có ít nhất 1 trạm `mode: "shot"` kèm ảnh chụp màn hình chứng minh (Fact).
  - **Trang nguồn có chart/bảng số liệu (benchmark, giá, chi phí…) thì ưu tiên chụp chart** làm trạm `shot` (focus/hl vào cột/điểm đang nói, ghi `src`) — chốt 30.09.2026. Không tự vẽ lại chart rồi gán cho hãng.
  - Hai trạm liên tiếp dùng chung 1 ảnh thì đều phải dùng `mode: "shot"`.
  - Mảng `words` và `weights` phải luôn bằng nhau.
  - Outro luôn là: `{"mark": "Thiện Trần", "socials": [{"platform": "facebook", "handle": "/thientm"}, {"platform": "tiktok", "handle": "/thientranx"}, {"platform": "youtube", "handle": "/thientm"}]}`
- **Tuyệt đối KHÔNG SỬA CẤU TRÚC `scene.html`**: Mọi layout, camera, safezone đã được căn chỉnh 100%. Chỉ được phép đổi màu biến CSS (`--ink`, `--now`, `--was`, `--paper`) nếu cần.

## 3. QUY TẮC ĐĂNG BÀI (PUBLISHING PIPELINE)
- **Tuyệt đối không chạy Headless**: TikTok và FB sẽ shadowban nếu phát hiện headless bot.
- **Bảo mật Profile**: Dữ liệu duyệt web lưu tại `~/.thien-tran-browser`. Không bao giờ lưu trong git.
- **Khởi động**: Luôn dùng `./thien-tran/publish/open_browser.sh` để mở Chrome qua cổng `9444`.
- **Tối ưu SEO 3 Nền tảng**:
  - **YouTube Shorts**: Tiêu đề có từ khoá tìm kiếm, mô tả dài, giàu ngữ nghĩa.
  - **TikTok**: Gọn gàng, 1 câu + 3-4 hashtag cốt lõi.
  - **Facebook Cá nhân**: Đăng qua `facebook.com/reels/create`, ngắt đoạn thoáng mắt, dùng 2-3 emoji định vị (💡, 🚀).

## 4. BÀI HỌC GIAO DIỆN NỀN TẢNG (UI QUIRKS LỊCH SỬ)
- **YouTube**: Lệnh gõ phím `.type()` gây ra lỗi giật lag nhảy chữ (race condition), dẫn đến tiêu đề rác. LUÔN LUÔN dùng `.fill()` cho `#title-textarea` và `#description-textarea`. Không dùng link `?d=ud` vì YouTube hay giấu nút, hãy tìm nút bằng lệnh `p.get_by_role("button", name=re.compile(r"create", re.I))`.
- **Facebook**: 
  - Nút xuất bản chính thức mang tên **"Post"** (hoặc Đăng). Tránh click nhầm vào nút thả xuống "Scheduling options Publish now". Dùng `re.compile(r"^(Post|Publish|Đăng)$", re.I)`.
  - **LƯU Ý QUAN TRỌNG VỀ QUYỀN RIÊNG TƯ (AUDIENCE)**: Facebook cá nhân hay bị mặc định trạng thái `Only me` (Chỉ mình tôi). Kịch bản upload FB cần (và phải) kiểm tra nút Audience ở bước cuối và chuyển sang `Public` (Công khai) trước khi bấm Post.

## 5. LUẬT TỐI ƯU TRẢI NGHIỆM NGƯỜI XEM (UX)
- **Outro tĩnh lặng**: Ở segment outro (cuối video), **TUYỆT ĐỐI KHÔNG ĐƯỢC CÓ KEY `say`**, `plain`, `words`, hay `weights`. Không để AI đọc tên kênh, không kêu gọi follow. Chỉ để mảng cấu trúc hình ảnh `{"id":"outro", "group":"...", "mode":"outro"}`. Hệ thống sẽ tự động chỉ chèn tiếng Chime (Sound effect) cực ngắn và hiển thị logo để tối ưu tính lặp lại (loop) của video trên Tiktok/Shorts.

## 6. QUY TRÌNH MỘT BÀI (tạm, tới khi gộp engine — kế hoạch gộp 29.09.2026)
Lịch: 3 khung như me-tech — 08:00, 12:00, 20:00 (dựng trước ~2 tiếng). Orchestrator giao cho một sub-agent mỗi khung.
1. **Tin:** AI/tech 24–48h, nguồn gốc chính thức; không trùng chủ đề đã đăng ở `logs/` (được trùng me-tech nhưng phải góc nhìn khác — FACT/INFERENCE/OPINION). Không chụp ảnh bài báo.
2. **Nội dung:** `content/<slug>.json` (voice "Adam bựa", brand "Thiện Trần", outro socials như mục 2). Học từ me-tech: câu 1 ≤10 chữ và **≤2,5 giây**, không mở bằng tên hãng; nhãn trạm đầu phải mang tin (không "TIN CHÍNH"); tên hãng/sản phẩm viết phiên âm trong `say` ("Ô-pen Ây Ai", "Flo-ri-đa", "Clâu", "Anh-thơ-píc"); 32–38s.
3. **Dựng:** `cd core-video-engine && SSL_CERT_FILE=../me-tech/pipeline/ca-bundle.pem ../me-tech/pipeline/.venv/bin/python build.py ../thien-tran/content/<slug>.json` → `render/<slug>.mp4`. Cổng Whisper/safezone phải qua; soát contact sheet.
4. **Đăng YT + TT** bằng bộ script me-tech ở `_pubkit/a/publish/` (cổng 9444, kênh `UCvoMD_dBm8z1i-Zd8Pwu7mQ`):
   - `publish/open_browser.sh` nếu 9444 tắt → `python3 ../me-tech/ops/fresh_browser.py 9444` → `python3 ../me-tech/ops/whois.py 9444 --yt UCvoMD_dBm8z1i-Zd8Pwu7mQ --tt thientranx` (sai thì DỪNG).
   - `cp render/<slug>.mp4 _pubkit/<slug>.mp4`; `_pubkit/a/publish/meta_<slug>.py` (VIDEO tuyệt đối, YT_TITLE không emoji); ghi slug vào `_pubkit/a/publish/ACTIVE`.
   - `$PY yt.py [--at HH:MM]` → `$PY yt_verify.py`; `$PY tt.py [--at HH:MM]` → `$PY tt_verify.py` (PY = me-tech venv). Đọc MÃ THOÁT.
5. **Đăng FB trang cá nhân** qua Chrome me-tech 9333 (đang đăng nhập thientm): `$PY fb_profile.py` (điền, chụp `_scratch/fb_profile_draft.png`) → soát ảnh (Public, caption đủ, không còn menu gợi ý hashtag, "safe to publish") → `$PY fb_profile.py --post` → xác nhận ở facebook.com/thientm/reels. Giữ khoá `mkdir ../me-tech/.run/fb9333.lock` trong lúc đăng, xong `rmdir`. Không chạy fresh_browser trên 9333. Lưu ý: URL tab tự đổi sang reel người khác dù hộp soạn vẫn mở — đừng tin URL.
6. **Log:** `logs/<YYYY-MM>.md` (append-only, một dòng/bài). Sổ chống trùng: `_pubkit/logs/posted.json`.
