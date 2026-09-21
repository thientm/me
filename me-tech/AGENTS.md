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

## Chốt lại — mọi quyết định đã khoá

Sửa bất kỳ dòng nào dưới đây thì phải **đo được lý do**, đừng đổi theo cảm tính.

| Hạng mục | Chốt | Vì sao |
|---|---|---|
| Độ dài | **32–38 giây** | vùng giao của cả ba nền tảng, một file đăng cả ba |
| Tốc độ đọc | **×1,10** (`"speed"`) | dùng `atempo` nên không the giọng; ngân sách 131–155 âm tiết |
| Số trạm | **5–7** | 12–13 câu, máy quay chỉ lia giữa trạm |
| Neo máy quay | **(505, 925)** | tâm dải nội dung, không phải tâm khung |
| `FIT` | **1150** | dải nội dung y 350→1500, dưới dòng thương hiệu |
| Bề ngang trạm | **830px** | 850 an toàn − 10px hở mỗi bên |
| Tốc độ lia | **1150 px/s**, 0,85–1,80s | bản cũ ~3.000 px/s bị chê nhức mắt |
| `HOLD` | **0,40s** | không rời trạm trước khi chữ cuối sáng xong |
| Vùng an toàn | **x 80–930 · y 250–1500** | đo thật trên Short của kênh, không lấy theo blog |
| Ngưỡng cổng | **2%** mực bị UI che | `safezone.py` chặn build nếu vượt |
| Ảnh dẫn nguồn | **≥1 trạm `shot` mỗi bài** | `validate.py` chặn; bỏ thì phải khai `no_shot` |
| Khung đăng | **07:45 · 12:30 · 21:00** | xem "Vì sao 3 khung" ở dưới |

**Năm cổng tự động — đừng gỡ:**

1. `validate.py` — soát file nội dung **trước** TTS (1 giây thay vì 100)
2. `build.py` — **dừng** nếu độ dài ngoài 32–38s (dùng `--tts-only` để sửa nhanh gấp 3)
3. `safezone.py` — **chặn** nếu >2% mực rơi vào vùng bị UI che
4. `_conn.confirm_schedule()` — **không cho bấm** nút hẹn giờ khi ô giờ còn trống
5. `validate.py` — **chặn** bài không có trạm `shot` nào (xem "Ảnh dẫn nguồn là bắt buộc")

**Bốn luật nội dung:**

- Luôn có một trạm **"NÓI CHO ĐÚNG"** nêu điều chưa kiểm chứng
- Hình phải **tả đúng thứ đang nói** — không có gì để vẽ thì bỏ trống, đừng dán icon cho đủ
- **Mỗi bài phải có ít nhất một trạm `shot`** dẫn ảnh chụp trang gốc
- Ảnh dẫn nguồn chỉ chụp **nguồn gốc** (`--phone`), bắt buộc ghi `src` trên màn hình

**Ba bẫy đã trả giá:**

- `pkill` / `launch_persistent_context` lên `~/.me-tech-browser` → **mất sạch đăng nhập**
- Tin cú bấm mà không kiểm lại → YouTube **đăng trùng 2 bản công khai**
- Upload lại mà không báo → để **rác trên kênh** cho Thiện tự phát hiện

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

**Chuỗi bước** (`mode: "flow"`) — khai `"nodes": [{"t","d"}, ...]`. Các hộp sáng dần
theo lời, có mũi tên nối. Dùng khi nội dung thật sự là "từ A sang B sang C"
(leo thang quyền, chuỗi sự kiện). **Không** dùng để trang trí — nội dung không có
thứ tự thì dùng `step`.

### Ảnh dẫn nguồn là BẮT BUỘC, không phải tuỳ chọn

**Mỗi bài phải có ít nhất một trạm `mode: "shot"`** — chụp CHÍNH TRANG GỐC rồi dẫn
trong video. Đây là thứ trực quan nhất trong cả bài, và là bằng chứng nhìn thấy
được rằng nguồn có thật.

> **21.09.2026 — luật này đã lặng lẽ rơi mất.** Kiểm lại 5 bài gần nhất: chỉ
> `hacktron-openai` có trạm `shot`, 4 bài còn lại **không có ảnh nào**. Lý do:
> mục này chỉ **mô tả cách làm**, không cổng nào bắt buộc; cổng cũ chỉ chặn
> "có `shot` mà thiếu `src`", nên không có `shot` nào thì nó cho qua êm ru.
> Luật mà không có cổng thì chỉ là ghi chú — và ghi chú thì rơi.
> Giờ `validate.py` **chặn hẳn** bài không có trạm `shot`.

Thật sự không có nguồn để chụp (tin đồn rò rỉ, chưa hãng nào công bố) thì phải
**khai lý do** ở khoá gốc, chứ không được im lặng bỏ qua:

```json
"no_shot": "tin đồn rò rỉ, chưa có trang chính thức nào để chụp"
```

Ảnh nguồn nằm ở **`pipeline/shots/`** — đây là **đầu vào**, được commit.
Không để ở `render/shots/`: `render/` nằm trong `.gitignore`, để đó là mất ảnh,
mà mất ảnh thì **không dựng lại được bài cũ** (đã xảy ra với `hacktron-openai`).

```bash
cd pipeline
.venv/bin/python capture.py <url> shots/<tên>.png --phone   # hồ sơ vứt đi, không đụng me-tech-browser
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
dùng hình vẽ bằng nét, đừng chèn ảnh kho cho có — và nhớ khai `no_shot`.

**Bài điểm tin nhanh:** trạm tin dùng `mode: "shot"` được (thay cho `say`), nên
nhắm **mỗi tin một ảnh nguồn**. `validate.py` cảnh báo nếu bài `roundup` có ảnh
nhưng chỉ có một.

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

- **3 khung/ngày: 07:45 · 12:30 · 21:00.** Chỉ đăng khung nào có tin xứng đáng
- **Video 32–38 giây.** Vùng giao của cả ba nền tảng, một file đăng cả ba
- Không đăng 00:00–06:00
- Không đủ tin hay thì đăng 1 bài, hoặc nghỉ. **Không lấp chỗ**
- Không lấy ảnh từ bài báo

### Vì sao 3 khung, không phải 5–6

Đo trên chính số liệu Page ngày 21.09.2026 — video đã đủ 24h:

| đăng lúc | bài | reach |
|---|---|---|
| 18/09 17:33 | GLM-5.3 | 222 |
| 19/09 14:36 | R&D Index | 206 |
| 19/09 21:00 | Gemini đột nhập | 194 |
| 20/09 12:39 | Gemini 4 | 201 |

Chênh lệch cao nhất/thấp nhất chỉ **1,14 lần** — quá nhỏ để kết luận khung giờ nào
hơn. Reach dừng ở **~206, tức 2,1% của 9.600 người theo dõi**, bất kể giờ nào.

**Nút thắt không phải số khung giờ, mà là 2,1% đó.** Thêm khung chỉ tạo thêm bài
cùng chạm ~200 người, trong khi mỗi bài tốn >30 phút và mỗi lượt đăng đều có rủi ro
hỏng (đã gặp: YouTube đăng trùng 2 lần, Facebook composer trắng trang).

Điểm sáng duy nhất trong số liệu: **video reach gấp ~11 lần bài ảnh/chữ** (206 vs 19).

### Cách đo cho đúng

Đừng so reach thô — bài mới luôn thấp vì reach cộng dồn. **Chỉ so reach tại mốc 24h.**
Ghi vào `logs/` cột reach-24h cho mỗi bài, sau 2 tuần mới đủ mẫu để nói khung giờ nào hơn.

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


## Chống đăng trùng — ba lớp, đừng gỡ lớp nào

21.09.2026 kênh YouTube có **hai bản công khai trùng nhau**. Nguyên nhân: phiên
tự động đọc "dòng mới nhất" trên kênh thay vì đối chiếu tiêu đề, tưởng chưa đăng
nên upload lại. Ba lớp chặn hiện nay:

| Lớp | Ở đâu | Chặn được gì |
|---|---|---|
| 1. Sổ đăng bài | `publish/ledger.py` → `logs/posted.json` | chạy lại cùng một video, **không cần mở trình duyệt**, chặn trong 1 giây |
| 2. Đối chiếu kênh | `yt.py` gọi `yt_verify.scan()` **trước khi** upload | hai phiên chạy song song, hoặc sổ bị xoá |
| 3. Kiểm chứng sau | `yt_verify.py` · `fb_verify.py` · `tt_verify.py` | cú bấm im lặng không ăn, và đếm bản trùng |

Cùng ngày lớp 1 + lớp 2 đã **bắt được một lần chạy đôi thật**: một lệnh bị timeout
ở tầng công cụ nhưng vẫn chạy tiếp trên máy, lệnh thứ hai chạy đè lên. Không có
hai lớp này thì hôm đó lại thêm một bản trùng nữa.

`post.py` **đọc MÃ THOÁT**, không đọc chữ in ra:
`0` xong · `1` chưa thấy · `2` còn ở Draft · `3` đã trùng, người phải xoá bớt.

`--force` bỏ qua lớp 1 và 2. Chỉ dùng khi thật sự muốn đăng lại.

`fb_verify.py` cũ dò chuỗi `"chủ trì một phần tư"` gõ cứng từ một bài tháng trước,
nên nó báo "không thấy" cho **mọi** bài mới — tức là chưa bao giờ kiểm chứng gì.
Mốc phải lấy từ `meta.FB_CAPTION`, đừng bao giờ gõ cứng.

## Xếp hàng nhiều bài trong ngày

`publish/meta.py` giờ là **con trỏ**, không phải nơi gõ nội dung. Mỗi bài một file
`meta_<slug>.py`; chọn bài bằng `python3 use.py <slug>`, xem đang chọn gì và bài
nào đã lên nền tảng nào bằng `python3 use.py`. Trước đây mỗi lần đổi bài phải sửa
tay `meta.py` nên không chuẩn bị trước hai bài trong một ngày được.

## Hẹn giờ — ba nền tảng đều tự động được

Không dùng cron chờ tới giờ. Đặt lịch bằng tính năng sẵn có của nền tảng: đặt
xong là xong, tắt máy vẫn chạy.

### TikTok — lớp phủ chặn mọi cú bấm

Đây là cái làm hỏng nhiều nhất và khó nhìn ra nhất. TikTok mở hộp thoại bằng
`div.TUXModal-overlay` trùm cả trang; Playwright báo
`TUXModal-overlay ... intercepts pointer events` rồi thử lại 112 lần trong 60
giây và chết. Nhìn màn hình thì thấy nút rất rõ nên rất dễ tưởng sai selector.

> **Luật: gọi `tt_sched.clear_overlay(q)` TRƯỚC mỗi cú bấm, không phải sau.**
> 21.09 đặt sau cú bấm submit → mất nguyên khung 12:30.

Hộp "Continue to post?" hiện khi TikTok chưa soát xong video. Cách đúng là **chờ**
hai mục Checks báo "No issues found" rồi hãy bấm — bấm trước thì bị hỏi, bấm sau
thì đi thẳng. Còn hiện thì mới bấm xác nhận.

Ghi chú cũ *"radio Schedule là input ẩn, click không ăn nên phải bật tay"* là
**SAI**, và đã bắt làm tay ba tuần. `get_by_text("Schedule").click()` ăn bình
thường, miễn là hết lớp phủ. Ô giờ thì không gõ chữ vào được, phải **bấm** trong
bảng chọn:

    giờ   .tiktok-timepicker-option-text.tiktok-timepicker-left
    phút  .tiktok-timepicker-option-text.tiktok-timepicker-right

Phút nhảy 5 một nấc → ba khung chốt 07:45 · 12:30 · 21:00 đều đặt được.
Chỉ hẹn được **trong ngày**; khác ngày thì dừng hẳn, đừng đoán.

### Facebook — ô giờ đọc ngược

Ô ngày **không có** `aria-label`, chỉ có `placeholder='dd/mm/yyyy'`. Ô giờ/phút do
React điều khiển: `input_value()` trả về **rỗng** trong khi màn hình hiện rõ
"12 : 30" — chữ nằm ở thẻ cha. Nên `confirm_schedule` đọc ba cách theo thứ tự
`input_value` → `inner_text` → `parentElement.innerText`, và **rỗng không tính là
đọc được** (phải thử cách sau, đừng `break`). Thiếu bước này thì cổng báo TRỐNG
cho một lịch đã đặt đúng.

Mọi ô đọc lại đều để timeout **6 giây**, không để mặc định 120 — một ô biến mất là
treo bốn phút rồi mới chết.

`fb_finish.py` bấm nút cho composer **đang mở sẵn**, dùng khi fb.py dừng ở cổng
`confirm_schedule`. Chạy lại `fb.py` sẽ tải video LẦN NỮA và bỏ lại một composer
bỏ hoang trên Page.

### Chrome đóng hết cửa sổ thì không nối CDP được

Triệu chứng: cổng 9333 vẫn trả lời `/json/version`, nhưng `connect_over_cdp` chết
với `Protocol error (Browser.setDownloadBehavior): Browser context management is
not supported`, và `/json/list` rỗng. Nghĩa là Chrome còn sống nhưng **không còn
tab nào**. Không được mở lại hồ sơ bằng Playwright. Mở lại một tab bằng chính
DevTools:

```bash
curl -s -X PUT "http://127.0.0.1:9333/json/new?https://www.tiktok.com/tiktokstudio/content"
```

## Hai giây đầu — móc giữ người xem

Ở các trạm sau, chữ chưa đọc mờ 11% là đúng: người xem đang **nghe**, chữ chỉ đi
theo giọng. Trạm **đầu** thì ngược lại — người vừa lướt tới, chưa có gì để nghe,
mắt đọc trước tai. Hiện từng chữ một ở đó nghĩa là hai giây đắt nhất của clip gần
như trống.

- `.st.hook .w:not(.on)` sáng **56%** thay vì 11% → cả câu đọc được từ khung hình số 1
- trạm đầu **không có nhịp hiện ra** (`r.gi===0 → near=1`)
- nhãn trạm đầu mờ đi, nhường chỗ cho câu móc
- `hot` vẫn chạy theo giọng để mắt biết đang tới đâu

**Bẫy CSS đã trả giá:** `.st.hook .w` là **ba lớp**, đè cả `.w.on` lẫn `.w.hot.on`.
Viết thiếu `:not(.on)` thì vệt vàng tắt ngóm và cả câu xám đều — nhìn ảnh mới thấy,
đọc code không thấy.

Kéo theo một luật nội dung: `lab` của trạm đầu phải **mang tin**, đừng để
"TIN CHÍNH". `HAI NGHÌN TỶ ĐÔ` nói được điều gì đó; `TIN CHÍNH` thì không.

## Điểm tin nhanh — khi không đủ một tin đủ nóng

Ngày nào không có tin nào đủ sức đứng riêng thì gộp **3 tin** thành một bài, thay
vì bỏ khung. Chép `content/_roundup-template.json`, đặt `"kind": "roundup"`.

Cấu trúc: **trạm mục lục** (`mode: "step"`, 3 thẻ đánh số = 3 tiêu đề) → mỗi tin
một trạm `say` hai–ba câu, `lab` ghi nguồn → outro. 5 trạm, vẫn 32–38 giây.

Mục lục là chỗ giữ người: cả ba tiêu đề phải **đọc được ngay giây đầu** — đó chính
là lý do người ta ở lại. Nên thẻ mục lục có sàn độ sáng **0,62** (thẻ bước thường
là 0,30), và các thẻ sáng lên đều tay theo thời lượng câu thay vì bám `splitAt`
(trạm mục lục có nhiều thẻ nhưng chỉ **một** câu, `splitAt: null` — `scene.html`
nhận ra bằng `rec.index`).

`validate.py` soát riêng cho `roundup`: mục lục phải là trạm đầu, **số thẻ phải
bằng số trạm tin**, 3–4 tin, mỗi trạm tin phải có `lab`. Thiếu một trạm thì mục
lục nói ba mà clip chỉ kể hai — bắt trong một giây, thay vì phát hiện sau khi đăng.
