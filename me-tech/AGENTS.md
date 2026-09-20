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
| Facebook Reels | 12:00 / 21:00 | qua **Business Suite**, tư cách Page, Public |
| YouTube Shorts | cùng khung | cùng file, không xuất lại |
| TikTok | lệch 30 phút | cùng file · **không chọn nhạc TikTok**, giữ Original sound |

Đăng bằng Playwright nối CDP vào hồ sơ Chrome riêng `~/.me-tech-browser`.
Cách mở, các selector và **toàn bộ bẫy đã gặp**: `pipeline/publish/README.md`.
Caption từng nền tảng: `pipeline/publish/meta.py`.

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

**Ảnh dẫn nguồn** (`mode: "shot"`) — chụp CHÍNH TRANG GỐC rồi dẫn trong video.

```bash
python capture.py <url> ../render/shots/<tên>.png --phone   # hồ sơ vứt đi, không đụng me-tech-browser
```

**Luôn chụp `--phone`.** Chụp khổ máy tính rồi thu vào khung 1080 thì chữ thân bài
chỉ còn **5 px thật** trên điện thoại — đó là ảnh trang trí, không phải trích dẫn.
Khổ điện thoại làm trang xuống dòng ~40 ký tự, đẩy vào đúng đoạn thì chữ đạt ~32 px.

Khai trong câu:

```json
"shot":  "<tên>.png",
"src":   "domain/đường-dẫn · ngày",
"view":  [x, y, w, h],   ô mở đầu — tiêu đề + tác giả, để thấy là trang thật
"focus": [x, y, w, h],   ô chốt — ĐÚNG đoạn đang dẫn, đây là chỗ phải đọc được
"hl":    [x, y, w, h]    vệt tô sáng chạy qua dòng then chốt
```

Toạ độ tính bằng pixel trong file ảnh. Hai nhịp: mở ra cả trang (0,55s) → đẩy vào
đoạn đang dẫn (1,30s) → vệt tô sáng chạy qua (0,70s). Ô kính 830×430.

| Được chụp | Không được chụp |
|---|---|
| Blog chính hãng, hồ sơ toà án, trang tài liệu, bảng đo chính thức | **Ảnh trong bài báo** — có giấy phép của hãng tin |
| Chỉ phần đang được dẫn (tiêu đề, đoạn nêu số) | Cả bài, hay phần hướng dẫn kỹ thuật |

`validate.py` chặn nếu có `shot` mà thiếu `src` — ảnh dẫn nguồn **bắt buộc** ghi xuất xứ
trên màn hình. Ảnh rộng 740px (không phải 830): để full width thì trạm cao quá,
đuôi chữ rơi xuống dải caption.

Phiên hiện tại **không có công cụ sinh ảnh AI**. Bài nào không có nguồn để chụp thì
dùng hình vẽ bằng nét, đừng chèn ảnh kho cho có.

**Hình vẽ bằng nét** — khai `"icon"` ở câu đầu của trạm. Hình được **vẽ dần** trong
0,7 giây ngay trước chữ đầu tiên, cùng nhịp với chữ ăn theo giọng.

Có sẵn: `bolt` `chip` `lock` `key` `eye` `spread` `doc` `clock` `warn` `model`
`building` `question` `chat` `stop`

Luật: **hình phải tả đúng thứ đang nói**, không phải trang trí. Không logo, không
hình thương hiệu. Trạm nào không có thứ để vẽ thì bỏ trống — thà thiếu hình còn hơn
dán một cái icon vô nghĩa cho đủ.

**Tốc độ đọc** — khai `"speed"` ở gốc file (1.10 = nhanh hơn 10%). Dùng `atempo`
nên không đổi cao độ. Khoảng lặng `gap`/`gap_group` vẫn giữ đúng nghĩa: con số ghi
ra là con số nghe thấy. Ngân sách âm tiết giãn theo: ×1,10 thì khoảng chốt là
131–155 âm tiết thay vì 119–141.

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

**Luật cứng về thời điểm lia** — máy quay **không bao giờ** rời một trạm trước khi
chữ cuối của trạm đó đã sáng xong và đứng yên thêm `HOLD` = 0,40 giây.
Thà tới trạm sau muộn còn hơn cắt mất đuôi câu.
Ranh giới giữa hai trạm dùng `gap_group` = 0,60s (thay vì `gap` = 0,24s giữa các câu
trong cùng trạm) để cú lia diễn ra trong khoảng lặng, không ăn vào lời nói.

> Lỗi đã từng mắc: neo máy quay vào lúc câu *sau* bắt đầu, rồi để thời gian lia
> ăn ngược vào câu *đang* nói → cả 6 trạm đều bắt đầu trôi **trước khi chữ cuối
> kịp sáng**. Nếu sửa lại chỗ này, đo lại bằng bảng "chữ cuối tắt / lia bắt đầu".

---

## Vùng an toàn 3 nền tảng — chốt 19.09.2026

Đo bằng cách mở chính Short của kênh trên Chrome giả lập iPhone rồi lấy toạ độ thật
của từng nút, quy về hệ 1080×1920 — **không lấy theo blog** (các blog lệch nhau nhiều).

```
        x 80 ─────────────── 930
 y 250  ┌──────────────────────┐   trên y<250 : logo · tìm kiếm · tab For You
        │                      │   dưới y>1500: username + caption + tên nhạc
        │   TẤT CẢ NỘI DUNG    │                (Facebook Reels ngặt nhất: 420px)
 y 900  │ ─ ─ ─ ─ ─ ─ ─┐       │   x>930 khi y>900: cột like/bình luận/chia sẻ
        │              │ cột   │                   — cột này KHÔNG chạy hết khung,
 y1500  └──────────────┴───────┘                     trên y=900 vẫn dùng được
```

Ba mốc trong `scene.html` giữ cho nội dung nằm đúng hộp này:

| Hằng | Giá trị | Vì sao |
|---|---|---|
| neo máy quay | `(505, 925)` | tâm **dải nội dung** — không phải tâm khung `(540, 960)`, cũng không phải tâm vùng an toàn `(505, 875)`: dòng thương hiệu chiếm y 276–345, neo cao hơn thì đầu trạm đè lên nó |
| `FIT` | `1150` | dải cho nội dung: y 350→1500 |
| bề ngang trạm · `r.wmax` | `830` | 850 an toàn − 10px hở mỗi bên cho nhoè JPEG |

HUD: thương hiệu + ngày ở `top:276px`, kicker `top:318px`, thanh tiến độ `top:254px`.
Chân khung không còn gì — chỗ đó bị caption che 100%.

`safezone.py` chạy tự động cuối bước dựng: đếm % mực rơi ngoài hộp, ngưỡng **2%**.
Nó **bỏ qua khung đang lia** — lúc máy quay chạy thì hai trạm cùng quét qua vùng chết,
đếm vào là sai; chỉ đo khung đứng yên vì đó mới là lúc người xem phải đọc được.

> Bài 18/09 có **16% mực bị UI che**, dải y 250–500 thì trống 0,02%. Sau khi sửa: **0,86%**.

Chưa tính quảng cáo. Nếu boost bài thì Facebook ăn tới 670px đáy — lúc đó hạ `BOT`
xuống 1250 trong `safezone.py` và viết câu ngắn lại.

---

**Đừng đụng vào** trong `scene.html` nếu không có lý do đo được:
`SPEED=1150` px/giây · `MV_MIN/MAX` 0,85–1,80 giây mỗi cú lia · easing `eSine` ·
`HOLD=0,40` · chữ chạy trước giọng 0,08s.
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
