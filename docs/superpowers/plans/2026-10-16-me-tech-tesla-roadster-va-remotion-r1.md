# Kế hoạch chạy trên Mac: bài Tesla Roadster bay + Remotion R1

> **Tài liệu**: Runbook thực thi
> **Ngày lập**: 16.10.2026
> **Máy chạy**: Mac của Thiện (cần mạng HuggingFace cho TTS/Whisper, Chrome hồ sơ Mê Tech để đăng)
> **Bối cảnh**: Bài thử đầu tiên của định vị 2.0 "Công nghệ dễ hiểu, gần với đời mình"
> (`me-tech/me-tech-plan.md` mục 0). Kịch bản + caption đã soạn và qua `validate.py` trong phiên cloud.
>
> Câu lệnh cho Claude Code trên Mac: **"làm theo docs/superpowers/plans/2026-10-16-me-tech-tesla-roadster-va-remotion-r1.md"**

Phần A làm trước và **phải xong trong hôm nay**. Phần B chỉ bắt đầu sau khi A đã hẹn đăng xong.

---

## Phần A — Đăng bài Tesla Roadster hôm nay (pipeline cũ)

| File | Trạng thái |
|---|---|
| `me-tech/pipeline/content/tesla-roadster-bay.json` | ✅ kịch bản, 13 câu · 7 trạm · 146 âm tiết · ~35,6s · `cat: xe` · móc kiểu 2 |
| `me-tech/content/tesla-roadster-bay/meta.json` | ✅ caption YouTube / Facebook / TikTok |
| `me-tech/pipeline/shots/tesla-roadster.png` | ❌ chưa có — cloud bị chặn tesla.com |

### A0 · Đồng bộ
```bash
cd ~/Documents/me && git pull origin master
cd me-tech/pipeline && ./run.sh --doctor
```

### A1 · 🛑 Chốt 1 — Thiện duyệt kịch bản
Kịch bản đã gửi Thiện trong phiên cloud. Nếu Thiện chưa trả lời "duyệt" thì in bảng
`say` của 13 câu ra và **dừng chờ**. Sửa chữ ở đây, chạy lại `python3 validate.py content/tesla-roadster-bay.json`.

### A2 · Chụp ảnh nguồn + kiểm sự thật
```bash
.venv/bin/python capture.py https://www.tesla.com/roadster shots/tesla-roadster.png --phone
```
- **Bắt buộc mở ảnh ra xem**: trang phải nêu **2028** (năm sản xuất). Có thì dùng.
- Không có 2028 → tìm trang/bài đăng chính chủ của Tesla nêu 2028 (tesla.com, X @Tesla),
  chụp lại, sửa `src` trong trạm `src1`. Không tìm được → đổi câu `src1` cho khớp đúng điều
  trang nói, chạy lại validate.
- Soát thêm trên trang: tiền cọc **$250,000** cho bản Thrust, bản **Rocket** chỉ theo lời mời.
  Lệch với kịch bản → sửa kịch bản, báo Thiện.
- Đo toạ độ pixel trong ảnh rồi điền vào câu `src1`:
  `"view"` (tiêu đề trang), `"focus"` (đoạn nêu 2028), `"hl"` (dòng nêu 2028). Cách đo: `AGENTS.md` mục "Ảnh dẫn nguồn".

### A3 · Dựng
```bash
./run.sh content/tesla-roadster-bay.json --preview
```
Các cổng phải qua: validate · độ dài 32–38s · Whisper từng câu · safezone ≤2%.
Hay gặp: "Rốt-xtơ", "Xpây-ếch", "Xmít-xô-ni-ần", "Vi-sần" bị Whisper báo lệch → nghe lại,
đọc đúng thì bỏ qua, sai thì sửa `say` hoặc thêm vào `pronounce.json`.

### A4 · 🛑 Chốt 2 — Thiện duyệt video
Gửi `render/tesla-roadster-bay.preview.mp4`. Nghe kỹ: "không phẩy tám mốt giây",
"hai trăm năm mươi nghìn đô", câu hỏi cuối.

### A5 · Đăng
- Khung: **20:00** hôm nay (TikTok 20:30). Đã lỡ thì khung kế tiếp còn trống.
- Thứ tự: **YouTube → TikTok → Facebook**. Caption lấy từ `meta.json` (`python3 use.py tesla-roadster-bay`).
- Facebook: bật **Share to Facebook story**. TikTok: Original sound.
- Mọi quy tắc + bẫy: `me-tech/AGENTS.md` mục 4 và `pipeline/publish/README.md`.

### A6 · Ghi log
Một dòng vào `me-tech/logs/2026-10.md`, cột Ghi chú **mở đầu bằng** `cat: xe ·`, rồi
`móc: kiểu 2 · "Ô tô này vừa bay qua cả hàng xe" (<giây>s)`, `story ✓`, ảnh nguồn.
Sau 24h: reach/view, giữ 3s FB, APV YT, **số comment** (đo luật câu hỏi cuối).

### Xong phần A khi
- [ ] 3 nền tảng hẹn/đăng, 3 script verify thoát 0, mỗi nền tảng đúng 1 bản
- [ ] Dòng log có `cat: xe`
- [ ] `git commit` log + `pronounce.json` (nếu sửa) + kịch bản (nếu sửa), push master

---

## Phần B — Remotion R1 (thử song song, KHÔNG đăng)

Mục tiêu: dựng lại **đúng bài Tesla** bằng Remotion từ cùng giọng đọc, để so với bản pipeline cũ.
Thiết kế & bảng skill: `me-tech/me-tech-plan.md` mục 0.6.

**Luật**: viết code Remotion **qua skill `remotion-best-practices`** (đã cài ở `.claude/skills/`).
Không dùng ElevenLabs (bỏ qua `voiceover.md`). Không gỡ cổng nào của pipeline cũ.

### B1 · Khung dự án — skill `remotion-create`
- Thư mục `me-tech/remotion/`, TypeScript, composition `MeTech` 1080×1920 @30fps.
- Thêm `node_modules/`, `out/` của nó vào `.gitignore`.
- Font Be Vietnam Pro (skill `remotion-markup` › `google-fonts.md`).

### B2 · Nối dữ liệu có sẵn — `parameters.md` + `calculate-metadata.md`
Đầu vào (đã sinh ở bước A3, không tạo lại giọng):
- `pipeline/content/tesla-roadster-bay.json` — kịch bản (Zod schema theo đúng cấu trúc này)
- `render/vo/tesla-roadster-bay.vo.wav` + `.timing.json` — giọng + mốc từng câu
- `pipeline/.work/data.json` — mốc **từng chữ** do `words.py` sinh

Script `remotion/scripts/prep.ts <slug>`: chép 3 file vào `remotion/public/<slug>/`.
`calculateMetadata` đọc `timing.json.total` → `durationInFrames`. Độ dài do giọng quyết định.

### B3 · Hình — `remotion-captions`, `text-highlights.md`, `transitions.md`, `sfx.md`
- Mỗi `group` là một trạm. Chữ sáng theo giọng từng chữ (đổi `data.json` sang kiểu `Caption`).
- Chữ trong `hot` → `<Highlight>`/`<Circle>` của `@remotion/rough-notation`.
- Lia giữa trạm: tối đa 1150 px/s, 0,85–1,80s (giữ thông số đã chốt).
- Trạm `shot`: ảnh `shots/tesla-roadster.png`, zoom view → focus → vệt hl, ghi `src`.
- Bảng màu, dòng thương hiệu, outro: theo `pipeline/scene.html :root` — cùng nhận diện.
- Nhạc nền: dùng `bed.wav` của `music.py`, không thêm nhạc ngoài.

### B4 · Render + cổng — `remotion-render`
```bash
cd me-tech/remotion
npx remotion render MeTech ../render/tesla-roadster-bay.remotion.mp4 --props=...
mkdir -p /tmp/rm-frames && ffmpeg -i ../render/tesla-roadster-bay.remotion.mp4 -vf fps=2.5 /tmp/rm-frames/%04d.png
cd ../pipeline && .venv/bin/python -c "import safezone; safezone.check('/tmp/rm-frames', every=1)"
```
Phải qua safezone ≤2%.

### B5 · Duyệt
Gửi Thiện cả hai bản cạnh nhau (`tesla-roadster-bay.preview.mp4` và `.remotion.mp4`) kèm
3 khung hình so sánh. **Không đăng bản Remotion**. Thiện quyết có chuyển R2 không.

### Xong phần B khi
- [ ] `remotion/` render được bài Tesla, chữ khớp giọng, qua safezone
- [ ] Commit `me-tech/remotion/` (không có `node_modules`, `out`, file mp4), push master
- [ ] Tick "Remotion R1" trong `me-tech/me-tech-plan.md` mục 0.8

---

## Nguồn sự thật đã dùng cho kịch bản (16.10.2026)

Bloomberg, TechCrunch, CNN, Not a Tesla App, The Next Web, Engadget, Edmunds, InsideEVs,
Yahoo Autos; chuyên gia Smithsonian Roger Connor (qua CNN): "We are literally talking about hopping".
Số 0,81s là đồng hồ tại sự kiện của Tesla, chưa có đo độc lập. Tỷ giá dùng ~26.000 đ/USD,
Vision ~32 triệu.
