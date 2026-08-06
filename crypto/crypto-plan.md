# Crypto Portfolio Plan

> Kế hoạch cơ cấu, theo dõi và tối ưu danh mục Crypto.
> Nhật ký giao dịch và thay đổi cấu trúc nằm ở `logs/{YYYY-MM}.md`. Review định kỳ nằm ở `reviews/`.

## 1. Thông tin dòng vốn
- **Tổng vốn gốc (initial):** 650,000,000 VND
- **Giá trị hiện tại (2026-08-04):** ~414,100,000 VND (Đang tạm lỗ ~236 triệu / -36%)
- **Mục tiêu đầu tư:** Quỹ dự phòng thanh khoản **bắt buộc phải rút (cash-out) để làm sổ đỏ**. Không phải danh mục hold dài hạn.
- **Time Horizon:** Cực ngắn. Deadline nộp hồ sơ sổ đỏ là **Đầu tháng 11/2026** (Chỉ còn khoảng 3 tháng).
- **Khẩu vị rủi ro:** Cực kỳ thận trọng. Ưu tiên bảo toàn số vốn >400tr hiện có để kịp đắp vào tiền làm sổ đỏ BĐS, không được phép để hao hụt thêm quá sâu.

## 2. Target Allocation & Tình trạng hiện tại (Snapshot 2026-08-04)

| Tài sản | Tỷ trọng | Phân loại | Định hướng xử lý (Chuẩn bị cash-out) |
|---|---|---|---|
| **BTC** | 64.53% | Coin dây sống | Tỷ trọng lớn nhất, an toàn nhất danh mục hiện tại. Canh các nhịp giá hồi phục từ nay đến T10/2026 để xả dần sang VND/USDT. |
| **BNSOL** | 25.74% | Altcoin / Staking | Rủi ro biến động cao hơn BTC. Cần theo dõi sát hệ sinh thái Solana, ưu tiên chốt lời/cắt lỗ dứt khoát sớm để đưa về an toàn. |
| **USDC** | 5.13% | Stablecoin | Tiền mặt có sẵn. Giữ nguyên không mua thêm Altcoin, sẵn sàng quy đổi P2P sang VND. |
| **ONDO** | 4.58% | RWA Altcoin | Tỷ trọng nhỏ nhưng độ rủi ro cao, thanh lý dần khi được giá. |
| **BNB** | 0.01% | Coin lẻ sàn | Dùng làm phí giao dịch (Dust). |

## 3. Nguyên tắc & Chiến lược tối ưu (Optimization Strategy)
Vì toàn bộ số tiền này **được dùng làm quỹ dự trữ làm sổ đỏ (deadline T11/2026)**, chiến lược sẽ thiên về **phòng thủ & rút lui (Exit Strategy)** thay vì tối ưu lợi nhuận:
- **Tái cơ cấu (Rebalancing):** KHÔNG nạp thêm tiền mới để gồng lỗ (tránh rủi ro kẹt vốn). KHÔNG mua thêm các Altcoin rủi ro cao.
- **Chiến lược Rút vốn (Take profit / Exit):** 
  - Đặt sẵn các lệnh Limit bán (Sell) ở các mốc giá cao để chốt dần BTC và BNSOL từ nay cho đến hết tháng 10/2026.
  - Phân bổ rút dần ra VND (P2P) theo từng đợt, tránh đợi đến sát deadline T11/2026 mới xả một cục (đề phòng thị trường dump sập đúng lúc cần tiền).
- **Chiến lược Cắt lỗ (Stop loss):** Phải xác định một mốc "Hard Stop" cho danh mục (Ví dụ: Nếu tổng tài sản tụt xuống dưới 380 triệu thì bắt buộc cắt máu cash-out toàn bộ ra VND để đảm bảo không bị thiếu hụt tiền làm BĐS).

## 4. Nhật ký giao dịch gần nhất
- **2026-08-04:** Khởi tạo danh mục. Vốn 650tr -> Còn 414tr. Cơ cấu: 64.5% BTC, 25.7% BNSOL, 5.1% USDC, 4.6% ONDO. Xác định phương hướng cash-out toàn bộ phục vụ Dự án 01 BĐS.

---

## 5. Lộ trình Exit theo tháng (Milestone)

Mục tiêu: Rút toàn bộ ~414 triệu ra VND trước deadline T11/2026. Chia thành 3 giai đoạn, mỗi giai đoạn có mục tiêu rút cụ thể.

| Giai đoạn | Thời gian | Mục tiêu rút (VND) | Ưu tiên xả | Ghi chú |
|---|---|---|---|---|
| **Giai đoạn 1: Dọn rìa** | T8/2026 | ~80 - 100tr | ONDO (toàn bộ), USDC (toàn bộ), BNSOL (một phần) | Xả hết các vị thế nhỏ/rủi ro cao trước. USDC convert P2P ngay, không cần chờ. |
| **Giai đoạn 2: Thu gọn** | T9/2026 | ~130 - 150tr | BNSOL (còn lại), BTC (bắt đầu xả dần) | Sau GĐ1, danh mục chỉ còn BTC thuần. Bắt đầu DCA-out BTC theo tuần. |
| **Giai đoạn 3: Dứt điểm** | T10/2026 | ~180 - 200tr (Phần còn lại) | BTC (toàn bộ còn lại) | Chậm nhất **25/10/2026** phải cash-out xong 100%. Buffer 1 tuần trước deadline nộp hồ sơ sổ đỏ. |

> **Nguyên tắc**: Số tiền mục tiêu rút mỗi giai đoạn là **tối thiểu**. Nếu thị trường pump mạnh → xả nhiều hơn mục tiêu, đẩy nhanh tiến độ. Nếu thị trường đi ngang/giảm nhẹ → vẫn xả đúng kế hoạch, không chờ đợi.

## 6. Playbook vận hành định kỳ

### 6.1 Weekly Check — Mỗi Thứ 2 đầu tuần

Checklist thực hiện mỗi tuần (ước tính ~15 phút):

- [ ] **Snapshot giá trị:** Chụp/ghi lại tổng giá trị danh mục (VND). So với tuần trước tăng/giảm bao nhiêu %.
- [ ] **Kiểm tra tiến độ exit:** Đã rút được bao nhiêu VND so với milestone tháng này? Đang đúng tiến độ hay chậm?
- [ ] **Đánh giá thị trường (5 phút):**
  - BTC tuần qua tăng hay giảm? Có tin tức macro lớn nào không? (Fed, CPI, ETF flow...)
  - SOL / Altcoin có biến động bất thường không?
  - Sentiment chung: Tham lam (Greed) hay Sợ hãi (Fear)?  → Check [Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [ ] **Quyết định action tuần này:**
  - Có đặt lệnh bán (Limit Sell) mới không? Ở mốc giá nào?
  - Có cần Market Sell ngay (nếu đang pump mạnh) không?
  - Có cần kích hoạt Hard Stop (nếu port < 380 triệu) không?
- [ ] **Ghi log:** Append kết quả vào `logs/{YYYY-MM}.md` với format:
  ```
  ## Tuần DD/MM - DD/MM
  - Tổng port: XXX triệu | Tuần trước: XXX triệu | Δ: +/-X%
  - Đã rút trong tuần: XXX triệu VND
  - Tổng đã rút luỹ kế: XXX / 414 triệu (XX%)
  - Action: [Mô tả lệnh đã đặt / đã khớp / điều chỉnh]
  - Nhận định tuần tới: [Canh xả thêm / Giữ nguyên / Cảnh giác]
  ```

### 6.2 Monthly Review — Đầu mỗi tháng (T9/2026, T10/2026)

Checklist review sâu hơn (ước tính ~30 phút):

- [ ] **Tổng kết tháng vừa qua:**
  - Giá trị đầu tháng vs cuối tháng.
  - Tổng VND đã rút thành công trong tháng. So với milestone đã vượt/chưa đạt?
  - Cơ cấu danh mục còn lại: bao nhiêu % BTC, bao nhiêu % Altcoin, bao nhiêu % Stablecoin?
- [ ] **Review chiến lược — Có cần điều chỉnh không?**
  - Nếu rút **nhanh hơn kế hoạch** → Tốt, giảm áp lực tháng sau. Có thể linh hoạt hơn (canh giá tốt hơn trước khi xả phần còn lại).
  - Nếu rút **chậm hơn kế hoạch** → Cảnh báo! Cần tăng tốc xả hàng tháng tới, thậm chí Market Sell không cần canh giá.
  - Mốc Hard Stop (380 triệu) có cần điều chỉnh không? (Ví dụ nếu đã rút được 100tr rồi thì port chỉ còn ~314tr, mốc Hard Stop cũng nên hạ theo phần còn lại).
- [ ] **Research macro tháng tới:**
  - Có sự kiện lớn nào sắp tới? (FOMC, CPI, ETF deadline, Solana unlock schedule...)
  - Tỷ giá P2P USDT/VND có biến động không? (Ảnh hưởng trực tiếp số VND thực nhận khi rút).
- [ ] **Cập nhật file:**
  - Sửa mục "Giá trị hiện tại" ở Section 1.
  - Sửa bảng cơ cấu ở Section 2 (nếu tỷ trọng thay đổi nhiều).
  - Ghi review vào `reviews/{tháng}-review.md`.

### 6.3 Trigger-based Actions — Kích hoạt bất kỳ lúc nào

Ngoài lịch tuần/tháng, các tình huống sau **kích hoạt hành động ngay lập tức** bất kể đang ở tuần nào:

| Trigger | Hành động | Lý do |
|---|---|---|
| **BTC pump >10% trong tuần** | Xả 30-50% lượng BTC đang giữ | Tranh thủ thanh khoản cao, giá tốt — không tham. |
| **BNSOL/ONDO pump >15%** | Market Sell toàn bộ vị thế đó | Altcoin pump mạnh thường kéo theo dump nhanh. Cơ hội thoát hàng hiếm có. |
| **Tổng port < 380 triệu** | **EMERGENCY: Market Sell ALL → VND** | Hard Stop. Bảo vệ vốn tối thiểu cho BĐS. Không bàn cãi, không chờ đợi. |
| **Tổng port > 450 triệu** | Xả ngay phần vượt (>414tr) về USDC/VND | Lock lại phần "lãi bất ngờ", đưa về safe zone. Phần còn lại tiếp tục theo kế hoạch. |
| **Tin xấu macro lớn** (FED tăng lãi suất đột ngột, sàn bị hack...) | Đánh giá ngay trong 1h, nếu port giảm >5% → xả 50% ngay | Không chờ "hồi phục", vì deadline là cố định (T11/2026). |

## 7. Quy trình Weekly Deep Review (khi có Agent hỗ trợ)

> Quy trình này dành cho agent. Section 6 là checklist thao tác tay của bạn — hai phần bổ trợ nhau, không thay thế nhau.
>
> **Về cách chạy research ở bước 7.2:** nếu tool hỗ trợ subagent → chạy 4 nhóm song song rồi tổng hợp. Nếu không → làm tuần tự theo thứ tự 1→4. Trong mọi trường hợp, Nhóm 4 phải được đọc sau cùng khi tổng hợp, vì nhóm này có quyền phủ quyết.

### 7.0 Khi nào chạy

- **Mặc định:** mỗi Thứ 2 đầu tuần.
- **Chạy ngay, không chờ Thứ 2**, nếu có bất kỳ điều nào sau đây:
  - BTC biến động >10% trong tuần (tăng hoặc giảm)
  - BNSOL hoặc ONDO biến động >15%
  - TTS (xem 7.3) tụt dưới 400tr, hoặc vượt 450tr
  - Tin macro lớn: Fed đổi lãi suất đột ngột, sàn bị hack, tin siết pháp lý crypto tại VN
  - Còn dưới 14 ngày tới deadline 25/10/2026

### 7.1 Bước 1 — Thu thập input

1. Đọc file này để nắm chiến lược, milestone (Section 5) và cơ cấu danh mục (Section 2).
2. Đọc `crypto/logs/{YYYY-MM}.md` gần nhất — tiến độ rút và action đã thực hiện.
3. Đọc `real-estate/real-estate-plan.md` mục "Kế hoạch tài chính & Trả góp" — lấy số liệu vốn/vay hiện hành.
4. Hỏi user 3 câu:
   - Tổng giá trị crypto hiện tại? (hoặc chụp màn hình Binance)
   - Đã rút được bao nhiêu VND kể từ lần review trước?
   - Có giao dịch nào ngoài kế hoạch không?
5. Tự tính: TTS, % luỹ kế đã rút, số ngày còn tới 25/10/2026, trạng thái tiến độ (theo 7.3).

### 7.2 Bước 2 — Research 4 nhóm yếu tố

Mỗi nhóm trả lời đúng các câu hỏi của nhóm đó, dùng nguồn được liệt kê, và kết luận theo đúng định dạng output — để so sánh được giữa các tuần.

**Nhóm 1 — Vĩ mô toàn cầu**
- Hỏi: Tuần/tháng tới có FOMC không (lịch 2026: 15-16/9, 27-28/10, 8-9/12)? Kỳ vọng lãi suất trên CME FedWatch (hiện 3.50-3.75%)? CPI/PCE mới nhất? DXY tăng hay giảm? Nasdaq/S&P tuần qua? Có sự kiện địa chính trị lớn?
- Nguồn: federalreserve.gov (lịch họp), CME FedWatch, TradingEconomics, Yahoo Finance
- Output: `risk-on` / `risk-off` / `neutral` + 1-2 câu lý do

**Nhóm 2 — Vĩ mô crypto**
- Hỏi: Dòng tiền ETF BTC tuần qua (inflow/outflow bao nhiêu)? Fear & Greed hiện tại và xu hướng 7 ngày? BTC dominance tăng hay giảm (tăng = altcoin yếu)? Có tin quy định lớn (SEC, ETF)?
- Nguồn: alternative.me/crypto/fear-and-greed-index, Coinglass, CoinMarketCap
- Output: sentiment tổng thể + có tin nào đủ lớn để đổi kế hoạch không

**Nhóm 3 — Vi mô từng tài sản**
- BTC: giá, %Δ tuần, vị trí so EMA20/50/200, RSI, vị trí trong chu kỳ (tham chiếu: đỉnh $126k T10/2025 → đáy $60.8k T6/2026)
- BNSOL: giá SOL, tỷ lệ quy đổi BNSOL/SOL có bị discount không, thanh khoản khi redeem, lịch unlock SOL, dòng ETF SOL
- ONDO: giá, lịch unlock (áp lực bán mang tính hệ thống), TVL, tin sector RWA
- USDC: không research, chỉ đọc số dư
- Nguồn: Binance spot, TradingView, Coinglass, token unlock trackers
- Output: mỗi coin một dòng — momentum `tăng`/`giảm`/`ngang` + lý do ưu tiên xả trước (nếu có)

**Nhóm 4 — Pháp lý VN + kênh rút tiền** ⚠️
- Hỏi: VN có quy định mới về tài sản số / sàn được cấp phép / siết P2P? Tỷ giá USDT/VND trên Binance P2P so với tuần trước? Spread và thanh khoản merchant? Có tin ngân hàng block tài khoản giao dịch P2P?
- Nguồn: VnExpress, CafeF, Thư viện pháp luật, Binance P2P
- Output: `kênh rút THÔNG` / `TẮC NGHẼN` / `RỦI RO` + tỷ giá + cảnh báo

> **Quyền phủ quyết của Nhóm 4:** nếu Nhóm 4 báo `RỦI RO`, kết quả này override toàn bộ tính toán giá của Nhóm 1-3, kích hoạt override ưu tiên 1 ở mục 7.3. Lý do: giá coin đẹp mà không chuyển được thành VND trước 25/10 thì vô nghĩa — và rủi ro này không thể "chờ hồi phục" như rủi ro giá.

Kết thúc bước này, tổng hợp Nhóm 1-3 thành **điều kiện thị trường**:
- `THUẬN LỢI` — risk-on, momentum tăng, F&G >60
- `TRUNG TÍNH` — tín hiệu hỗn hợp
- `BẤT LỢI` — risk-off, momentum giảm, F&G <40

### 7.3 Bước 3 — Decision Matrix

**Định nghĩa TTS (Tổng tài sản dự án) = VND đã rút + giá trị crypto còn lại.**
Mọi ngưỡng trong mục này đo trên TTS, vì đây là con số trả lời đúng câu hỏi "còn đủ tiền làm sổ đỏ không". Không đo trên riêng phần crypto — phần đã rút ra VND là tiền đã an toàn, không còn chịu rủi ro giá.

**Trục 1 — Sàn tiến độ bắt buộc (luỹ kế đã rút ra VND):**

| Mốc | Tối thiểu | Quy ra VND |
|---|---|---|
| 31/8/2026 | ≥20% | ~83tr |
| 30/9/2026 | ≥55% | ~228tr |
| 25/10/2026 | 100% | ~414tr |

Trạng thái: **CHẬM** (dưới sàn) / **ĐÚNG** (đạt sàn, vượt dưới 10 điểm phần trăm) / **NHANH** (vượt sàn từ 10 điểm phần trăm trở lên).
*Ví dụ tại mốc 30/9 (sàn 55%): rút được 50% → CHẬM; 55-64% → ĐÚNG; ≥65% → NHANH.*

**Matrix:**

| | THUẬN LỢI | TRUNG TÍNH | BẤT LỢI |
|---|---|---|---|
| **CHẬM** | Market sell bù đủ sàn + xả thêm 10-15% crypto còn lại | Market sell bù đủ sàn ngay, không canh giá | Market sell bù đủ sàn ngay. Không chờ hồi. |
| **ĐÚNG** | Xả thêm 10-20% crypto còn lại bằng limit ở giá cao | Xả đúng sàn tuần này, limit sát giá thị trường | Xả đúng sàn, ưu tiên market sell phần altcoin |
| **NHANH** | Limit giá cao, kiên nhẫn chờ khớp | Giữ nhịp, xả nhỏ giọt theo tuần | Xả đúng sàn — không lấy "đang nhanh" làm cớ dừng |

*Mọi tỷ lệ % trong bảng tính trên **giá trị crypto còn lại tại thời điểm review**, không phải trên 414tr gốc. "Bù đủ sàn" = rút thêm cho đủ mức luỹ kế tối thiểu của mốc gần nhất.*

> **Nguyên tắc xuyên suốt: cột BẤT LỢI không bao giờ có nghĩa là "dừng bán".** Đây chính là cái bẫy đã đưa danh mục từ 650tr xuống 414tr — giảm → chờ hồi → giảm tiếp.

**Thứ tự ưu tiên xả:** ONDO → USDC (convert luôn) → BNSOL → BTC. Rủi ro cao và thanh khoản kém đi trước; BTC giữ lại sau cùng vì an toàn nhất và thanh khoản tốt nhất, xả lúc nào cũng được.

**Override — đè lên toàn bộ matrix:**

| Điều kiện | Hành động | Ưu tiên |
|---|---|---|
| Còn <14 ngày tới 25/10 | Market sell ALL, bất kể giá | 1 |
| Nhóm 4 báo RỦI RO kênh rút | Market sell ALL → VND trong 24h | 1 |
| TTS < 380tr | Market sell ALL → VND | 2 |
| TTS > 450tr | Xả ngay phần vượt 414tr, lock về VND | 3 |
| BTC pump >10%/tuần | Xả 30-50% BTC đang giữ | 4 |
| BNSOL/ONDO pump >15% | Market sell toàn bộ vị thế đó | 4 |

### 7.4 Bước 4 — Đối chiếu kế hoạch BĐS

```
Vốn tự có dự phóng tại T11/2026
  = 1.3 tỷ (bố mẹ, tiết kiệm)
  + 705tr (cá nhân, Techcombank)
  + TTS crypto thực tế          ← thay cho giả định 400tr
  + 35tr × số tháng còn lại tới T11
  + lãi tiết kiệm ước tính

Số cần vay = 3 tỷ − Vốn tự có dự phóng
Δ = Số cần vay − 433tr (mức đã chốt ở Phương án C)
Ảnh hưởng timeline = Δ ÷ 35tr/tháng → dịch mốc hết nợ T1/2028
```

Ngưỡng cảnh báo:
- **Δ > +50tr** → nêu rõ mốc hết nợ bị lùi bao lâu; cảnh báo nếu chạm/vượt mốc cưới đầu 2028.
- **Số cần vay > 500tr** → cờ đỏ: cấu trúc vay đang giả định 50% vay 0% lãi từ người thân. Cần kiểm tra phần 0% có scale lên được không, hay phải vay ngân hàng toàn bộ phần vượt (lãi 7%, đội chi phí).

### 7.5 Bước 5 — Ghi log

Append vào `crypto/logs/{YYYY-MM}.md` theo đúng format sau (không sửa entry cũ):

```
## Tuần DD/MM - DD/MM (Deep Review)

### Input
- TTS: XXXtr (VND đã rút XXXtr + crypto còn lại XXXtr) | Tuần trước: XXXtr | Δ: ±X%
- Tiến độ luỹ kế: XXX/414tr (XX%) | Sàn yêu cầu: XX% → CHẬM/ĐÚNG/NHANH
- Còn XX ngày tới 25/10

### Research
- N1 vĩ mô toàn cầu: risk-on/off/neutral — [lý do]
- N2 vĩ mô crypto: [F&G, ETF flow, dominance]
- N3 vi mô: BTC [...] | BNSOL [...] | ONDO [...]
- N4 pháp lý VN/P2P: THÔNG/TẮC/RỦI RO | tỷ giá XXX
→ Điều kiện thị trường: THUẬN LỢI/TRUNG TÍNH/BẤT LỢI

### Quyết định
- Ô matrix: [tiến độ] × [thị trường]
- Override kích hoạt: [không / tên override]
- Action: [lệnh cụ thể: coin nào, bao nhiêu, market hay limit ở giá nào]
- Judgment call: [nếu có — nêu rõ]

### Đối chiếu BĐS
- Vốn tự có dự phóng T11/2026: X.XXX tỷ
- Cần vay: XXXtr (kế hoạch 433tr, Δ: ±XXtr)
- Mốc hết nợ: T1/2028 → [giữ nguyên / lùi X tháng]
```

### 7.6 Ngoại lệ & Judgment call

Áp dụng khi gặp tình huống mà matrix và override đều không cover (black swan, sự cố sàn, thay đổi hoàn cảnh cá nhân, tin chưa có tiền lệ). Quy tắc:

1. **Phải nói rõ đây là judgment call** — không được trình bày như thể đang theo rule có sẵn.
2. **Mặc định nghiêng về bảo toàn vốn** — lưỡng lự giữa bán và giữ thì chọn bán. Deadline cứng, sai lầm không còn thời gian sửa.
3. **Nêu rõ đánh đổi** — chọn phương án này thì đang từ bỏ điều gì.
4. **Ghi vào log** để tuần sau cân nhắc nâng thành rule chính thức.

**3 nguyên tắc bất biến — không judgment call nào được phép vi phạm:**
- Không bao giờ khuyến nghị **nạp thêm tiền mới** vào crypto.
- Không bao giờ khuyến nghị **mua lại/DCA** để gỡ lỗ.
- Không bao giờ **dời deadline 25/10** để chờ giá tốt hơn.

Ba điều này chốt cứng vì chúng là những quyết định mà bản thân lúc đang lỗ sẽ dễ bị cám dỗ nhất — và cũng chính là cơ chế đã đưa 650tr xuống 414tr.
