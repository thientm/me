# Mê Tech — Plan vận hành kênh nội dung AI

Kênh: Facebook Page **Mê Tech** (facebook.com/mecongnghe40) + **TikTok** (TikTok Studio).
Định vị: "AI dễ hiểu" — tin AI tiếng Việt, ngắn gọn, luôn có góc ứng dụng thực tế, mỗi bài ít nhất 1 ảnh.

> File này là bán tĩnh. Chỉ sửa khi chiến lược/nhịp đăng thật sự đổi.
> Log từng bài đã đăng: `me-tech/logs/{YYYY-MM}.md` (append-only).

---

## 1. Nhịp đăng — RULE CỨNG

**2 bài/ngày mỗi nền tảng. Tối đa. Cách nhau tối thiểu 8 tiếng.**

| Khung | Facebook | TikTok |
|---|---|---|
| Trưa | 12:00 | 12:30 |
| Tối | 21:00 | 21:30 |

- **Không đăng khung 00:00–06:00.** Reach gần như bằng 0.
- Không có tin đủ hay thì **đăng 1 bài**, hoặc **nghỉ**. Không lấp chỗ.
- Cùng một tin thì đăng cả 2 nền tảng, lệch 30 phút, nội dung viết lại riêng cho từng nơi.

### Vì sao — bằng chứng ngày 16/09/2026
Hôm đó chạy 1 bài/giờ, 18 bài/ngày trên Facebook và 20 bài trên TikTok. Kết quả:

| | Số bài | Reach/bài (FB) | Tổng reach ngày |
|---|---|---|---|
| 15/09 | 6 | 20 – 47 | ~195 |
| 16/09 | 12 (tới 11:00) | 3 – 20 | ~118 |

Đăng gấp đôi, tổng reach **giảm ~40%**. TikTok còn nặng hơn: 12 bài đăng trong ngày, **0 view** toàn bộ, trong khi bài ngày trước đó đều đạt 130–206 view. Một bài bị khoá về "Only me" (kẹt review).

Ba cơ chế: (1) tự cạnh tranh — cùng một tệp follower nhỏ bị chia nhỏ; (2) nhịp đều tăm tắp 24/24 trông như bot, kích hoạt bộ lọc spam; (3) đốt nội dung — mỗi ngày chỉ có 2–3 tin AI thật sự đáng đăng.

### Vấn đề gốc chưa giải quyết
**Follows = 0 trên toàn bộ bài, suốt 90 ngày.** Reach 20–47 với 0 follow, 0 share nghĩa là nội dung tới được người đọc nhưng không giữ được ai. Giảm tần suất chỉ hết bị bóp — không tự sinh ra follower. Việc kế tiếp phải làm: thử format khác (video/reels thay vì ảnh tĩnh), CTA rõ hơn, và chọn tin theo mức độ liên quan tới người Việt thay vì theo độ nóng của tin quốc tế.

---

## 2. Quy trình chạy một ngày (daily)

Gõ với agent: *"chạy daily Mê Tech"*. Agent làm theo đúng thứ tự sau.

1. **Đọc log** `me-tech/logs/{YYYY-MM}.md` (và tháng trước nếu cần) → nắm chủ đề đã đăng.
2. **Research** tin AI 24–48h qua. Chọn theo thứ tự ưu tiên:
   - có góc ứng dụng được cho người Việt bình thường (tiền, công việc, lừa đảo, học hành)
   - có con số cụ thể, kiểm chứng được
   - chưa nằm trong log
3. **Chống trùng**: `grep -i "<từ khoá>" me-tech/logs/*.md`. Trùng chủ đề → bỏ, trừ khi có diễn biến mới thật sự (khi đó ghi rõ "cập nhật của <bài cũ>" trong log).
4. **Viết copy** 2 phiên bản: Facebook (dài hơn, có bullet, CTA câu hỏi cuối) và TikTok (title ngắn + description có hashtag).
5. **Render ảnh** (xem mục 4). Không cần browser.
6. **Gửi Thiện duyệt** copy + ảnh trong chat. Chờ OK.
7. **Đăng / hẹn giờ** đúng khung giờ ở mục 1.
8. **Ghi log** ngay sau khi đăng — 1 dòng/bài vào `me-tech/logs/{YYYY-MM}.md`.
9. Sau 24h: cập nhật reach/views vào dòng log tương ứng (đây là ngoại lệ duy nhất được sửa dòng cũ — chỉ điền số liệu, không sửa nội dung).

---

## 3. Chống đăng trùng

Log là nguồn sự thật duy nhất. Trước khi chốt tin:

```bash
grep -i "gemini\|openai\|<từ khoá>" me-tech/logs/*.md
```

Quy ước: cột **Chủ đề** viết đủ tên riêng (công ty + sản phẩm) để grep ăn được. Không viết chung chung kiểu "tin AI mới".

---

## 4. Thông số ảnh

Ảnh **vẽ bằng code**, không phải ảnh AI sinh ra. Render HTML/canvas → PNG bằng headless Chromium, không cần browser của Thiện.

- **Facebook**: 1 ảnh cover `1080x1350`
- **TikTok**: carousel 3 slide `1080x1920` — (1) hook, (2) danh sách số liệu, (3) lưu ý + CTA
  - Nội dung phải nằm trong khoảng **y 220 – 1500** để tránh UI TikTok che
- Font: **Be Vietnam Pro** (tải từ Google Fonts, cài vào `~/.fonts`, `fc-cache -f`)
- Nền tối, accent xanh `#4F9CFF` → tím `#7C5CFF`, số liệu màu vàng `#FFC978`
- Footer mọi ảnh: logo tròn "MT" + "MÊ TECH"

---

## 5. Ghi chú kỹ thuật từng nền tảng

### Facebook (Meta Business Suite)
- Đăng với tư cách **Page**, audience Public.
- Caption: dán bằng **một sự kiện `paste` ClipboardEvent tổng hợp** — giữ nguyên xuống dòng, 1 thao tác thay vì ~25 lần gõ từng dòng.
- Ảnh: inject `File` vào file input của composer.
- Hẹn giờ: Post settings → Scheduling options → nhập Date + Time → "Schedule for later" → "Schedule".
- **Sửa lịch được**: bài đã hẹn → click vào bài → panel Post details → `...` → **Reschedule Post** → đổi ngày giờ. Không cần xoá.

### TikTok (TikTok Studio)
- Upload ở tab **photo**, ảnh vào **file input ĐẦU TIÊN** (cái có thuộc tính `multiple`).
- Title: set qua native value setter.
- Description (DraftJS): dán bằng **một `paste` ClipboardEvent**. Gõ từng dòng với phím Return liên tiếp đã từng làm crash TikTok Studio.
- **Nhạc nền: bắt buộc mọi bài.** "Add sound" → click ô search trong modal (toạ độ đổi mỗi lần, phải dò lại) → gõ query → **Enter** (không Enter thì autocomplete che kết quả) → "Use" một track. Query chạy được: "lofi chill background", "chill instrumental vlog". Mỗi bài một track khác nhau.
- Nhạc **không thêm/đổi được sau khi đã đăng**. Bài đã đăng chỉ sửa được caption, cover, location, privacy, comment settings — và caption/cover chỉ 1 lần/ngày, trong vòng 7 ngày.
- **Bài đã hẹn giờ KHÔNG sửa được** ("Scheduled posts cannot be edited"). Menu `...` chỉ có Delete và Download. Muốn đổi lịch = xoá rồi upload lại. → **Hẹn giờ TikTok phải chắc ngay từ đầu.**
- Bài mới thường vào "Content under review", privacy khoá "Only me" cho tới khi duyệt xong. Thường tự mở trong vài giờ.
- Analytics của TikTok **trễ 2–3 ngày**. Số view ở danh sách Posts thì cập nhật gần như realtime — lấy số ở đó.

### Chung
- **Đồng hồ**: sandbox của agent từng lệch vài tiếng so với giờ thật. Luôn đọc giờ thật bằng `new Date()` chạy trong tab browser trước khi hẹn giờ bất cứ thứ gì.
- Browser: dùng Chrome của Thiện qua extension. Trong lúc agent chạy thì **không đụng vào cửa sổ Chrome đó** — tab bị cướp focus. Mỗi bài mất 3–6 phút.

---

## 6. Số liệu tham chiếu (tính tới 16/09/2026)

| | Facebook | TikTok |
|---|---|---|
| Reach/views mỗi bài, nhịp bình thường | 20 – 47 reach | 130 – 206 views |
| Bài tốt nhất từng có | 80 reach (31/08, "dev chỉ CRUD") | 206 views (15/09, iOS 27/Siri) |
| Follows sinh ra | **0** | — |
| Share | 0 | 0 |

Mốc để biết đã thoát bóp sau khi giảm tần suất: **reach Facebook về lại 40–60/bài** trong 3–4 ngày.

---

## 7. Video / Reel — định dạng chính từ 17/09/2026

Ảnh tĩnh chỉ với tới ~1–2% follower. Reel / Short được đẩy ra ngoài tệp follower — đúng thứ page đang thiếu (0 follow suốt 90 ngày).

### Nhịp thử nghiệm
- **Khung tối 21:00 → reel**, khung trưa 12:00 giữ ảnh như cũ.
- Chạy 5 ngày rồi so reach khung tối với mốc cũ: **47** (15/09 22:00) và **39** (15/09 23:02).
- Cùng cách chọn tin, chỉ khác format — đủ sạch để đọc kết quả.

### Một render, ba nền tảng
`me-tech/pipeline/` dựng video 9:16 từ animation HTML → frames → ffmpeg. Đọc `pipeline/README.md` để sửa nội dung.

| File | Đăng ở đâu | Nhạc |
|---|---|---|
| `<slug>_music.mp4` | Facebook Reels + YouTube Shorts | nhạc tự soạn nhúng sẵn (`music.py`) |
| `<slug>_mute.mp4` | TikTok | không audio → chọn sound native lúc upload |

Vì sao chia đôi: thư viện nhạc **không** phải yếu tố xếp hạng của YouTube Shorts, và Facebook Page bị giới hạn bản quyền nên có khi không có bài nào để chọn. Riêng TikTok thì mỗi sound có **trang riêng** — đó là một cửa khám phá thật, đáng giữ. Audio gốc không bị TikTok phạt; sound trending cho cú hích 1–3 tuần rồi tắt.

**Bẫy chết người**: bản `_mute` mà quên bấm "Add sound" trên TikTok thì video im lặng hoàn toàn → retention về 0. Bước bắt buộc trong checklist.

### Thông số
- 1080x1920, 30fps, H.264 high + AAC 48kHz, `+faststart`
- Độ dài mặc định **32 giây** (25–35s là khoảng đã chốt)
- Nội dung trong vùng an toàn **y 220 – 1500**
- Giữ file **dưới 20MB** để `device_commit_files` đẩy về máy được (cap 20MB/file). CRF 21 + maxrate 4500k cho ra ~13MB/32s.
- Video build xong nằm ở `me-tech/render/` (đã cho vào `.gitignore`, không commit binary)

### Giới hạn tần suất của từng nền tảng
- YouTube Shorts: **1–5/ngày an toàn, 10+ thường bị bóp reach**. Cùng một bài học với Facebook và TikTok — đừng bơm.

### Ảnh minh hoạ ngoài
Chỉ dùng nguồn có license rõ, xếp theo độ an toàn:
1. Đồ hoạ tự dựng (biểu đồ, so sánh, timeline) — an toàn tuyệt đối, tạo chất riêng
2. Newsroom chính chủ — Google blog, OpenAI, NASA (ảnh NASA gần như toàn bộ là public domain)
3. Wikimedia Commons — check license từng ảnh, ghi credit
4. Unsplash / Pexels
5. Screenshot giao diện sản phẩm tự chụp

**Không lấy ảnh trong bài báo.** Content ID trên YouTube và Rights Manager trên Facebook bắt được, và càng rủi ro nếu sau này bật kiếm tiền. Mỗi ảnh ngoài ghi nguồn + license vào log.

---

## 8. Bối cảnh đang dang dở (cập nhật 16/09/2026)

Phần này ghi lại những quyết định **chưa chốt** để phiên sau — kể cả Claude Code mở từ trang trắng — không phải hỏi lại.

### Đang chờ quyết
- **Nhà cung cấp TTS tiếng Việt.** Đang cân giữa FPT.AI (free tier, giọng bản địa nhiều vùng miền) và Google Gemini TTS qua AI Studio (chất lượng cao, điều khiển ngữ điệu bằng prompt, ~vài trăm đồng/bài). Chưa nghe thử giọng nào.
- **Tone nhạc nền.** Thiện muốn hợp kênh IT/AI và để nhỏ. Bản hiện tại trong `music.py` là lo-fi Am7–Fmaj7–Cmaj7–G. Chưa chốt.
- **Reel Gemini 3.8 Live** đã dựng xong video (`render/gemini-live_*.mp4`) nhưng **chưa đăng** — Thiện muốn có voiceover rồi mới đăng.

### Đã thử và không dùng được
- **Chạy TTS offline trong sandbox Cowork**: bế tắc. Cài được thư viện nhưng trọng số model nằm trên HuggingFace, bị chặn egress. Piper, MMS-TTS, XTTS đều không tải được.
- **Gọi API TTS từ script trong Cowork**: bế tắc. `api.fpt.ai`, `vbee.vn`, `texttospeech.googleapis.com`, `generativelanguage.googleapis.com` đều bị gateway trả 403. Allowlist chỉ có pypi, npm, github. Chặn ở cả container cloud lẫn VM trên máy.
- **Google AI Studio trên browser**: tài khoản Thiện có gói AI Pro nhưng API key đang ở **Free tier** → mọi model (cả TTS lẫn Gemini 3 Flash) trả `permission denied`, UI báo "This model requires a paid API key". Muốn dùng phải bật billing cho project `gen-lang-client-...`.
- **Gọi API FPT.AI từ Chrome của Thiện**: đường này **thông** — đã test POST tới `api.fpt.ai/hmi/tts/v5`, trả 401 với key giả (tức là tới nơi, chỉ thiếu key thật). Là phương án dự phòng nếu không chuyển sang Claude Code.
- **Gói Google AI Pro**: không cho quyền lợi API nào. Google ghi rõ quyền lợi chỉ áp dụng trong giao diện web AI Studio.

### Quyết định đã chốt
- Chuyển phần dựng video + TTS sang **Claude Code trên Mac** (mạng không bị chặn). Xem `pipeline/SETUP.md`.
- Nhịp 2 bài/ngày, khung 12:00 và 21:00 (mục 1).
- Khung tối chuyển sang reel, khung trưa giữ ảnh tĩnh — để đo (mục 7).
- Không lấy ảnh từ bài báo (mục 7).
- Không lên lịch tự động cho bước đăng bài — Thiện duyệt nội dung trước khi đăng.

### Hàng đợi TikTok ngày 16/09
7 bài đã hẹn giờ 12:30–18:30 được **để chạy nốt** (TikTok không cho sửa lịch, chỉ cho xoá, và Thiện chọn không xoá). Từ 17/09 mới vào nhịp mới.

---

## 9. Quy trình đầy đủ một bài (chốt 17/09/2026)

Ba giai đoạn. Giai đoạn 1 làm ở đâu cũng được; giai đoạn 2 phải ở Claude Code trên Mac (Cowork bị chặn egress nên không chạy được TTS); giai đoạn 3 cần Chrome.

### Giai đoạn 1 — Nội dung

1. **Chống trùng**: `grep -i "<từ khoá>" me-tech/logs/*.md`. Trùng chủ đề thì bỏ, trừ khi có diễn biến mới thật sự.
2. **Research** tin AI 24–48h qua. Ưu tiên: có góc ứng dụng cho người Việt bình thường > có con số kiểm chứng được > chưa nằm trong log.
3. **Viết `pipeline/content/<slug>.json`.** Đây là file duy nhất phải soạn cho mỗi bài. Quy tắc:
   - **Mỗi câu = một nhịp hình.** Câu nào nói ra thì thứ tương ứng hiện lên màn hình.
   - Gom các câu cùng một khung hình vào chung `scene`.
   - **Không kết câu bằng từ viết tắt hoặc con số** — luôn có từ tiếng Việt đứng cuối.
   - Số viết bằng chữ trong `say` ("tám mươi hai phẩy sáu"), viết bằng số trong `show`.
   - Từ viết tắt cứ viết bình thường (`AI`, `API`) — `pronounce.json` lo phần đọc.
4. **Thiện duyệt kịch bản** trước khi dựng. Sửa chữ ở bước này rẻ hơn nhiều so với sau khi render.

### Giai đoạn 2 — Dựng

```bash
cd me-tech/pipeline
python build.py content/<slug>.json          # ~4 phút
python build.py content/<slug>.json --skip-tts   # đã có giọng, chỉ dựng lại hình
```

Chuỗi bên trong:

| Bước | Làm gì | Thời gian |
|---|---|---|
| `tts.py` | Đọc từng câu riêng, mỗi câu qua **cổng Whisper**, hỏng thì render lại (tối đa 3 lần). Xuất `vo.wav` + `timing.json` | ~25s |
| `render.py` | Đọc `timing.json` → sinh `video.html` → chụp ~1200 frame bằng Playwright | ~2,5 phút |
| `music.py` | Sinh nhạc nền đúng độ dài bài | ~5s |
| `ffmpeg` | Trộn, ducking, chuẩn hoá −14 LUFS, xuất 2 file | ~30s |

Ra `render/<slug>_music.mp4` và `render/<slug>_vo_only.mp4`.

5. **Thiện duyệt video.** Nghe kỹ câu cuối và các mốc số đếm.

### Giai đoạn 3 — Đăng

| Nền tảng | File | Ghi chú |
|---|---|---|
| **Facebook Reels** | `<slug>_music.mp4` | Đăng với tư cách Page, Public |
| **YouTube Shorts** | `<slug>_music.mp4` | Cùng file, không phải xuất lại |
| **TikTok** | `<slug>_vo_only.mp4` | **Bắt buộc bấm "Add sound"** — file này không có nhạc, quên là video im lặng dưới giọng đọc |

6. Khung giờ: **12:00 / 21:00** (mục 1). Reel dành cho khung tối.
7. **Ghi log ngay sau khi đăng** vào `logs/{YYYY-MM}.md`, 1 dòng/bài.
8. Sau 24h cập nhật reach/views vào dòng log đó.

### Thứ tự nhân quả — vì sao không được đảo

```
kịch bản  →  giọng đọc  →  timing.json  →  hình  →  ghép
                              ↑
                    nguồn sự thật duy nhất
```

Độ dài video **do kịch bản quyết định**, không đặt trước. Muốn video ngắn lại thì cắt bớt câu, không phải chỉnh timeline.

### Ba cổng kiểm soát tự động

| Cổng | Bắt được gì | Giới hạn đã biết |
|---|---|---|
| **Whisper** (`tts.py`) | Câu thiếu hẳn một mệnh đề | **Không đáng tin ở mức một chữ** — model small trên tiếng Việt hay "sửa" lời thành câu hợp lý. Clip ngắn dưới 1s thì nó bịa hẳn. |
| **Từ điển** (`pronounce.json`) | Từ viết tắt đọc sai / bị nuốt | Chỉ xử lý được từ đã có trong danh sách |
| **Ước lượng độ dài** | Chỉ còn dùng khi `--no-verify` | ±20%, từng báo oan 2 lần và bỏ sót 1 lần |

Tắt Whisper bằng `--no-verify` khi cần nhanh.

### Đã thử và loại bỏ

- **Vặn `repetition_penalty` / `babble_retries`**: chính nó gây cụt đuôi câu. Trả về mặc định thì tỉ lệ đạt lần đầu còn tốt hơn.
- **`afftdn` khử nhiễu giọng**: giọng TTS vốn sạch, chỉ làm mòn chi tiết.
- **Cho Whisper nghe riêng đuôi câu**: bịa 100%.
- **Đếm âm tiết bằng biên độ**: sai số ±2, không đủ tinh để bắt thiếu một chữ.
