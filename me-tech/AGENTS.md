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
| Facebook Reels | 08:00 / 12:00 / 20:00 | qua **Business Suite**, tư cách Page, Public · **luôn bật Share to Facebook story** (chốt 25.09.2026, `fb.py` tự bật và chặn Share nếu chưa bật) · **không** bật dịch giọng Meta AI (bỏ 26.09.2026 — Meta giới hạn số lượt, hết lượt là kẹt cả bài) |
| YouTube Shorts | cùng khung | cùng file, không xuất lại |
| TikTok | lệch 30 phút | cùng file · **không chọn nhạc TikTok**, giữ Original sound |

Đăng bằng Playwright nối CDP vào hồ sơ Chrome riêng `~/.me-tech-browser`.
Cách mở, các selector và **toàn bộ bẫy đã gặp**: `pipeline/publish/README.md`.
Caption từng nền tảng: `pipeline/publish/meta.py`.

### 5 · Ghi log
1 dòng/bài vào `logs/{YYYY-MM}.md`. Sau 24h cập nhật reach/views.
- **Soát Facebook trước khi ghi log** (chốt 25.09.2026): mở bài trong Business Suite,
  xác nhận **Share to Facebook story = bật**.
  Dòng log FB phải ghi `story ✓`; thiếu thì ghi rõ và báo Thiện.
  Nhãn trạng thái phải sạch — thấy **"Failed to publish"** thì bài chưa lên, dù đã có dòng.
- Sau 24h ghi thêm bài đó có nhãn **High-quality creative** của Facebook không
  (`HQ ✓` / `HQ ✗`) — xem mục "Nhãn High-quality creative" bên dưới.

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
| Khung **đăng** | **08:00 · 12:00 · 20:00** | xem "Vì sao 3 khung" ở dưới |
| Khung **dựng** | **07:00 · 11:00 · 19:00** | trước giờ đăng 1 tiếng, tác vụ định kỳ tự chạy |
| Thứ tự đăng | **YouTube → TikTok → Facebook** | ít lỗi nhất trước, hỏng thì hỏng ở cái cuối |

**Sáu cổng tự động — đừng gỡ:**

1. `validate.py` — soát file nội dung **trước** TTS (1 giây thay vì 100)
2. `build.py` — **dừng** nếu độ dài ngoài 32–38s (dùng `--tts-only` để sửa nhanh gấp 3)
3. `safezone.py` — **chặn** nếu >2% mực rơi vào vùng bị UI che
4. `_conn.confirm_schedule()` — **không cho bấm** nút hẹn giờ khi ô giờ còn trống
5. `validate.py` — **chặn** bài không có trạm `shot` nào (xem "Ảnh dẫn nguồn là bắt buộc")
6. `fb.py` — **không bấm Share** khi chưa bật share story

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

Ảnh nguồn để ở **`pipeline/shots/`** — chỉ nằm trên máy, **không commit** (chốt 25.09.2026,
xem "Chạy trên nhiều máy"). Tin daily đăng xong là hết giá trị, không có nhu cầu dựng lại bài cũ.

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
| **Chart / bảng số liệu có sẵn trên trang nguồn** (benchmark, giá, điểm-theo-chi-phí) | Chart tự vẽ lại rồi ghi là của hãng |

**Trang nguồn có chart số liệu thì ưu tiên chụp chart** (chốt 30.09.2026): một trạm
`shot` dẫn đúng chart đó, `focus`/`hl` vào cột hay điểm đang được đọc, `src` như mọi ảnh
nguồn. Chart thật của hãng đáng tin và dễ hiểu hơn một đoạn chữ nêu số. Chụp khổ
`--phone`; chart ngang quá hẹp ở 430px thì chụp khổ rộng hơn rồi cắt riêng khối chart.

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

- **3 khung/ngày: 08:00 · 12:00 · 20:00**, dựng trước mỗi khung 1 tiếng
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


## Chạy trên nhiều máy — chốt 25.09.2026

Luồng có thể chạy ở nhiều máy, **git là đường đồng bộ duy nhất**. Video `render/*.mp4`
không vào git (nặng), nên **một bài dựng → đăng trọn trên MỘT máy**; máy khác không
tiếp tục dở dang được. Đăng xong thì file của bài đó hết giá trị.

| Commit | Chỉ để trên máy (`.gitignore`) |
|---|---|
| `logs/*.md`, **`logs/posted.json`** — chống trùng giữa các máy | `pipeline/content/<slug>.json` |
| code `pipeline/`, `publish/*.py`, `pronounce.json`, `uv.lock`… | `publish/meta_<slug>.py` |
| `AGENTS.md`, `me-tech-plan.md`, `reviews/` | `publish/ACTIVE` — con trỏ bài đang chọn của riêng máy đó |
| mẫu: `content/lawzero.json`, `_roundup-template.json`, `_schema-cu/`, `publish/meta.py` | `pipeline/shots/*.png`, `_scratch/`, `render/`, `.venv/`, `.work/` |

**Hai luật cứng:**
1. **`git pull` trước khi chọn tin; đăng xong commit + push `logs/` ngay** (chỉ `me-tech/logs/`
   và file luật/code mình sửa, không kéo theo mục khác). Lớp chặn trùng 1 (`posted.json`)
   chỉ có tác dụng khi nó được đồng bộ kịp.
2. **Mỗi lúc chỉ MỘT máy chạy tác vụ định kỳ.** Hai máy cùng chạy 19:02 thì cả hai thấy
   "chưa có bài" rồi cùng đăng — lớp 2 (quét kênh) chỉ cứu được YouTube.

File trên máy dọn được sau ~7 ngày (bài đã có dòng log + đủ 3 khoá trong `posted.json`).

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

Phút nhảy 5 một nấc → ba khung chốt 08:00 · 12:00 · 20:00 đều đặt được.
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

**22.09.2026 — `fb_verify.py` báo "chưa thấy" cho một bài ĐÃ hẹn đúng.** Danh sách
`scheduled_posts` **phân trang**: hôm đó có 30 thẻ ảnh trong hàng đợi, nên bài reel
hẹn 08:00 không được vẽ ra, `inner_text("body")` đếm được 0. Cổng trả mã `1`, mà mã
`1` nghĩa là "chạy fb.py để đăng" — tin theo là **upload lần nữa**. Đã vá: lọc bằng ô
`Search by ID or caption` trước khi đếm. Luật chung: cổng đọc một danh sách dài thì
phải lọc trước, "không thấy trong màn hình đầu" **không phải** là "chưa có".

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

## Nhãn "High-quality creative" của Facebook — chỉ là ĐẦU VÀO, không phải mục tiêu

Ghi 25.09.2026, lúc Thiện hỏi có dùng nhãn này để cải tiến được không.

Business Suite gắn nhãn này cho một số reel. Rê chuột vào thì Facebook tự giải thích:
*"Posts with visually engaging content are more likely to capture attention and drive
engagement"*, kèm nút **Boost** ngay bên dưới. Tức là nó chấm **phần hình**, và gắn với
việc mời chạy quảng cáo. Nó không phải điểm chất lượng chung cho cả ba nền tảng.

Số liệu lúc 25.09 13:15, 19 reel:

| Nhóm | Có nhãn |
|---|---|
| Không có trạm `shot` (18–21/09) | **0/7** |
| Có `shot`, không có lưới `data` | 1/7 (hacktron) |
| Có `shot` + lưới `data` | **3/5** (mimo, grok, alibaba — trượt: opus55, gpt6) |

Nhãn **không đi cùng kết quả**:

| | Reach | Giữ 3s (3s views ÷ views) | Xem trung bình |
|---|---|---|---|
| 4 bài có nhãn | 13 – 361 (Alibaba chỉ 13) | 18 – 27% | 3 – 7s |
| bài không nhãn, cùng thời kỳ | 16 – 253 | 25 – 35% (R&D Index 35%, GLM 31%) | 2 – 8s |

Nên đọc là:
- **Gợi ý yếu** là ảnh nguồn thật + lưới số liệu làm Facebook thấy hình "bắt mắt".
  Hai thứ đó vốn đã là luật (ảnh nguồn bắt buộc, `data` cho câu có số), nên **không
  có việc gì mới phải làm vì nhãn này**.
- **Đừng tối ưu cho nhãn.** Nó không kéo reach hay giữ chân trên chính Facebook,
  và không có gì cho thấy TikTok/YouTube dùng tiêu chí tương tự.
- **Mẫu còn quá nhỏ và bị lẫn thời gian**: cả 4 nhãn đều rơi vào bài 21–23/09, còn
  chưa rõ Facebook gắn nhãn sau bao lâu (bài 24–25/09 có thể chưa được chấm).
  Cứ ghi `HQ ✓/✗` ở mốc 24h, đủ ~20 bài mới xét lại cùng đợt xếp hạng 5 kiểu móc.

Chỉ số chung cho cả ba nền tảng vẫn là **giữ 3s FB** và **APV YT** (xem "Câu móc").

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

### Câu móc — chốt 24.09.2026

Tuần đầu làm video (`reviews/2026-09-w4-review.md`): chỉ **25%** view Facebook
giữ quá giây thứ 3, APV YouTube ~55% so với ~70% của Shorts. Câu đầu kiểu
"X vừa ra Y" bắt người xem đợi mới biết có gì cho mình.

**Ba luật cứng — `validate.py` chặn:**

1. Câu 1 **≤ 10 chữ, ≤ 2 giây**, đọc được ngay khung hình đầu
2. **Không mở bằng tên hãng** — tên hãng để câu 2, làm phần "giải thích"
3. Câu 1 phải **đúng với nguồn từng chữ**. Chỗ nào hụt thì câu 2 bù ngay,
   không đợi tới trạm "NÓI CHO ĐÚNG". Kênh là "AI dễ hiểu": được sốc, được
   gây tò mò, **không được sai** — bị lừa ở giây thứ 5 thì mất uy tín lâu hơn
   cái lợi một lượt lướt

**Năm kiểu móc** — khai `"hook": <1–5>` ở khoá gốc file nội dung:

| # | Kiểu | Cơ chế | Mẫu |
|---|---|---|---|
| 1 | Con số sốc | con số ngược với điều người xem nghĩ | "Rẻ hơn Claude 11 lần. Mà ngang sức." |
| 2 | Chuyện khó tin | nghe như phim | "Một AI vừa tự hack ba công ty thật." |
| 3 | Nói vào người xem | "bạn" + việc của bạn | "Giờ nói một câu, ChatGPT tự làm ra file." |
| 4 | Bỏ lửng | nêu kết quả, giấu nguyên nhân | "Ba người vào được máy của OpenAI. Không phá gì cả." |
| 5 | Đảo ngược | hãng nói A, thực tế B | "Chip mạnh nhất Trung Quốc. Nhưng chưa ai được mua." |

Chọn kiểu hợp với tin, không ép. Tin nào cũng hợp nhiều kiểu thì **xoay vòng**
— tra kiểu của 3 bài gần nhất trong log, chọn kiểu khác.

**Đo — bắt buộc:** dòng log mỗi bài ghi `móc: kiểu N · "<câu 1>"`. Sau 24h điền
thêm `giữ 3s FB: x%` (3-second views ÷ views, trong Business Suite) và `APV YT: y%`.
Mốc so: **25%** và **~55%**. Sau ~10 bài xếp hạng 5 kiểu, kiểu nào thua cả
hai mốc thì bỏ khỏi bảng.

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


## Chạy tự động — tác vụ định kỳ

Chốt 21.09.2026. Một tác vụ định kỳ chạy **07:00 · 11:00 · 19:00** (cron UTC
`0 0,4,12 * * *`), mỗi lần dựng một bài và hẹn đăng vào khung sau đó **một tiếng**:
**08:00 · 12:00 · 20:00**.

Tác vụ **bị buộc vào máy của Thiện** (cần Chrome hồ sơ Mê Tech ở cổng 9333 và
pipeline ở `/Users/thien.tm/Documents/me/me-tech`) và chạy ở chế độ **tự duyệt** —
không dừng lại hỏi ai. Nên mọi cổng an toàn trong file này phải còn nguyên: không
có ai ngồi đó để bắt lỗi thay.

Một tiếng đệm là để **có chỗ hỏng mà sửa**, không phải để làm cho nhanh. Một bài
mất ~30 phút, còn lại là biên an toàn.

### Chrome chạy nền, không cướp chuột — `ops/open_chrome.py` (30.09.2026)

Thiện chốt: Chrome kênh không được nháy lên trước mặt khi Thiện đang dùng máy. Mở Chrome
**chỉ** bằng `python3 me-tech/ops/open_chrome.py <9333|9444|9555>` (mở nền + thu nhỏ).
`_conn.connect()` và `whois.py` tự thu nhỏ và mở tab nền. Chi tiết: `pipeline/publish/README.md`.

### Mở browser là dọn tab trước — `ops/fresh_browser.py` (30.09.2026)

Thiện chốt: mỗi lần mở lại một Chrome để làm việc, **tắt hết tab đang mở trước**.
Tab cũ (composer FB các ngày trước, trang Studio, trang đọc tin) làm script bắt nhầm
tab và che hộp thoại. Chạy ngay sau khi giữ khoá, trước bước chụp nguồn/đăng bài:

```bash
python3 ops/fresh_browser.py 9333 --own-lock   # me-tech; 9444 thien-tran; 9555 tam-an-lac
```

Script mở một tab trống rồi đóng các tab khác qua CDP — **không** tắt Chrome, không pkill.
Hai ngoại lệ: không dọn khi job khác đang giữ khoá (tab soạn bài của nó có thể đang
"Publishing"), và không dọn giữa chừng một lần đăng — `*_finish.py` cần tab đang mở.

**Xong kênh là tắt Chrome kênh đó** (chốt 30.09.2026): đăng + verify xong →
`python3 ops/close_browser.py <cổng> --own-lock`. Gửi CDP `Browser.close` (như Cmd+Q,
cookie được lưu) — **không** pkill. Bài hẹn giờ nằm trên máy chủ nền tảng, tắt Chrome
không ảnh hưởng. Chrome me-tech 9333 chỉ tắt khi **cả 3 kênh** xong khung, vì FB của
thien-tran và tam-an-lac cũng đi qua nó (script tự chặn khi còn `fb9333.lock`).

### Giám sát viên — `ops/watchdog.sh` (26.09.2026)

Tác vụ định kỳ chạy **trong** một session Claude: session bận/treo hay máy ngủ thì nó
trễ (25–26/09 trễ 30–45 phút liền ba lần) và không lịch nào trong cùng session gỡ được.
Giám sát viên chạy **ngoài** Claude bằng launchd, lúc HH:40 · HH:55 · 10 phút sau giờ đăng:

1. `ops/slot_status.py <giờ>` đọc `posted.json` — khung đủ 3 nền tảng thì thôi
2. tiến trình pipeline chạy >30 phút → TERM/KILL (không đụng Chrome)
3. `.run/build.lock` được chạm trong 20 phút → job khác đang chạy, thôi.
   **Job nào đang dựng/đăng cũng phải giữ khoá và `touch` nó ở mỗi bước**
4. còn lại → giữ khoá, mở Chrome nếu tắt, chạy `claude -p` (allowlist lệnh, tối đa 50 phút)
   để đăng nốt nền tảng thiếu hoặc dựng cả bài

Cài/gỡ: `ops/install.sh` / `ops/install.sh --remove` (Thiện tự cài). Chạy thử không
gọi Claude: `DRY=1 ops/watchdog.sh`. Log: `~/Library/Logs/metech-watchdog.log`.

### Thứ tự đăng: YouTube → TikTok → Facebook

Xếp theo mức ít lỗi, đo từ thực tế 18–21.09:

| Nền tảng | Độ tin | Bẫy riêng |
|---|---|---|
| YouTube | cao nhất | hẹn giờ gốc, chạy phát ăn ngay; từng có cú Publish im lặng rơi về Draft → `yt_finish.py` |
| TikTok | vừa | `div.TUXModal-overlay` chặn cú bấm; phải chờ Checks xong rồi mới bấm |
| Facebook | thấp nhất | Business Suite trắng trang, ô giờ đọc ngược, hay phải `fb_finish.py` |

Làm cái chắc trước để nếu hết giờ hoặc hỏng thì **hỏng ở cái cuối**, không mất cả ba.
Đổi lại: nền tảng khó nhất nhận ít thời gian sửa nhất — chấp nhận, vì đằng nào
cũng còn ~50 phút đệm.

### Nếu không dựng được bài

Báo rõ vì sao rồi **dừng**. Đừng đăng bài kém chất lượng cho đủ khung — bài
sai nguồn thì ở lại trên kênh.

**Trễ giờ hay thiếu tin thì KHÔNG phải lý do bỏ khung** (Thiện chốt 26.09.2026, sau
khi hai khung 25/09 20:00 và 26/09 08:00 bị bỏ vì tác vụ chạy trễ). Tác vụ chạy trễ
thì vẫn dựng đủ cổng rồi **đăng ngay** khi xong; không có tin đủ nóng thì làm
**điểm tin nhanh**. Chỉ dừng khi cổng an toàn hỏng không sửa được.


## Thẻ ảnh Facebook — bộ thứ hai, KHÁC bộ video

Chốt 22.09.2026, khi Facebook giao nhiệm vụ 30 bài photo công khai trong tuần.

    cd pipeline
    .venv/bin/python card.py cards/thuong-xanh.json      # vẽ 30 thẻ → render/cards/
    cd publish
    ../.venv/bin/python fb_photo_batch.py --plan         # xem lịch
    ../.venv/bin/python fb_photo_batch.py                # xếp lịch thật

### Hai bảng màu, cố ý khác nhau — đừng hợp nhất

| | Video | Thẻ ảnh |
|---|---|---|
| Nền | mực ấm `#0E0D0B` | xanh đêm `#05070F` + gradient |
| Nhấn | hổ phách `#FFAE2B` | xanh `#4F9CFF` → tím `#7C5CFF`, số liệu vàng `#FFC978` |
| Khổ | 1080×1920 | 1080×1350 |
| Vì sao | chữ chạy theo giọng nên nền phải trầm, không giành mắt | đứng yên trong feed, phải bắt mắt mới có người dừng lại |

### Bẫy đã trả giá: 5 thẻ ra ảnh rỗng mà báo thành công

`card.py` vẽ cả 30 thẻ trên **cùng một trang** bằng `set_content`, mà
`set_content` dùng `document.write` nên **scope toàn cục không bị xoá** giữa các
lần. Khai `const D` ở tầng toàn cục thì từ thẻ thứ hai trở đi nổ
`Identifier 'D' has already been declared` **ngay dòng đầu** — thẻ ra đúng nền,
đúng logo, nhưng **không một chữ nào**.

Lỗi JS trong trang **không** làm `screenshot()` thất bại. Log báo đẹp, chỉ có
dung lượng file giống hệt nhau là dấu hiệu duy nhất. Chỉ mở ảnh ra xem mới thấy.

Hai cái chặn giờ đã có: script trong `card.html` **bọc trong hàm**, và `card.py`
bắt `pageerror` + đếm chữ trong `#title` và số `.row`, thẻ rỗng thì coi là hỏng.

Chữ tràn khung: co tiêu đề trước (82 → 52px), vẫn tràn thì co cả khối bằng
`transform: scale()` — giữ đúng tỉ lệ giữa các phần thay vì thu từng thứ một.

### Composer ảnh khác composer reel

| | Reel (`reels_composer`) | Ảnh (`composer`) |
|---|---|---|
| Ô caption | có `role=textbox` | **không có** — là `contenteditable`, và có hai cái cùng `aria-label`, cái đầu **ẩn** |
| Chọn file | "Add video" | "Add photo/video" |

Cả hai đều mở hộp chọn file chứ không có `input[type=file]` sẵn trong DOM →
phải dùng `expect_file_chooser()`.

Ô ngày/giờ đọc ngược y hệt reel — dùng chung `_conn.confirm_schedule()`.

### Khung giờ ảnh: 09:30 · 11:00 · 14:00 · 16:30 · 18:30

Né hẳn ba khung video (08:00 · 12:00 · 20:00) để hai loại bài không giành chỗ
nhau trong feed.

`fb_photo_batch.py` **chạy lại được**: thẻ nào đã xếp đều nằm trong sổ đăng bài
(khoá `<slug>:facebook-photo`), chạy lại thì bỏ qua và đi tiếp từ chỗ hỏng.

### Nói thẳng về hiệu quả

Log của kênh: bài ảnh tĩnh đạt reach **20–47** và **0 follow suốt 90 ngày**,
trong khi video đạt ~206. Bộ thẻ này làm để **hoàn thành nhiệm vụ Facebook giao**,
không phải để kéo tương tác. Đừng lấy nó làm cớ quay lại đăng ảnh thay video.

Hết 30 thẻ mà tuần sau vẫn cần thì viết thêm vào `cards/thuong-xanh.json` —
đừng đăng lại thẻ cũ.


## Bẫy đã trả giá: 30 bài ảnh dồn vào MỘT ngày

22.09.2026. `fb_photo_batch.py` tính lịch đúng — 5 bài/ngày rải 6 ngày — và in
ra bảng lịch nhìn rất thuyết phục. Nhưng `fb_photo.py` khi điền lên giao diện
chỉ điền **giờ và phút**, **không bao giờ điền NGÀY**. Ô ngày giữ nguyên mặc
định là hôm đó. Kết quả: cả 30 bài lên trong ngày 22.09, chỉ rải trong 5 khung
giờ — đúng cái rủi ro "dồn dập dễ bị bóp reach" đã nêu ra khi chọn nhịp đăng.

**Vì sao cổng `confirm_schedule` không bắt được.** Nó *có* đọc ô ngày và in ra
màn hình `ngày: '22 September 2026'` — nhìn log thấy rất yên tâm. Nhưng ô nào
**không được nêu trong `want`** thì chỉ bị kiểm **khác rỗng**, mà ô ngày thì
nền tảng luôn điền sẵn hôm nay nên **luôn khác rỗng**. Cổng gật đầu cho một ô
chưa ai đụng tới.

Bài học chung, không riêng gì Facebook:

> Một cổng chỉ kiểm thứ được **nêu tên**. Đọc ra và in lên màn hình **không
> phải** là kiểm. Cổng nào nhận danh sách "cái cần kiểm" thì phải tự báo khi
> có cái không được nêu — nếu không, chỗ quên sẽ im lặng đi qua và trông y hệt
> như đã kiểm.

Ba chỗ đã vá:

1. `_conn.confirm_schedule()` **tự chặn** nếu có ô trong `fields` mà không có
   trong `want` — quên nêu là dừng, không phải lọt.
2. `fb.py` · `fb_photo.py` · `fb_finish.py` đều đưa **ngày** vào `want`.
3. `fb.py` và `fb_photo.py` **chặn hẳn** khi ngày cần hẹn khác hôm nay, vì cả
   hai đều chưa biết điền ô ngày (lịch dạng calendar, gõ chữ vào bị backdrop
   chặn — giống YouTube, xem `yt.py`).

**Còn thiếu:** phần chọn NGÀY trên lịch Facebook. Làm xong thì gỡ cổng (3) ở
trên, đừng gỡ (1) và (2). Trước khi làm xong, `fb_photo_batch.py` chỉ xếp được
lịch trong ngày — muốn rải nhiều ngày thì mỗi ngày chạy một lần.
