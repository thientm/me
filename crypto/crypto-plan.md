# Crypto Portfolio Plan

> Kế hoạch cơ cấu, theo dõi và tối ưu danh mục Crypto.
> Nhật ký giao dịch và thay đổi cấu trúc nằm ở `logs/{YYYY-MM}.md`. Review định kỳ nằm ở `reviews/`.

## 1. Thông tin dòng vốn
- **Tổng vốn gốc (initial):** 650,000,000 VND
- **Giá trị hiện tại (2026-09-18 11:10, đo từ giá spot + P2P realtime):** **$19.498 ≈ 504.200.000 VND** (P2P 25.860; tạm lỗ ~146tr / −22,4%). **BTC 0,15931 ($77.253) = 318,3tr · SOL 55,28 ($104,49) = 149,4tr · stables $1.415 = 36,6tr.** Cơ cấu: BTC 63,1% · SOL 29,6% · stables 7,3%. Tiến độ rút VND **0%**. Còn **43 ngày** tới 31/10, **23 ngày** tới override #1 (11/10).
  - 🔄 **Cổng swap SOL→BTC ĐANG MỞ, CHƯA THỰC HIỆN.** SOL/BTC = **0,0013529 = 97,8% biên độ 90 ngày** (đỉnh 90 ngày 0,0013593, chỉ còn +0,5%), vượt ngưỡng 85% ở mục 7.3. Swap là **quyền chọn**, không bắt buộc, và **không bao giờ thay thế tranche**. Nếu làm: 55,28 SOL → ~0,074 BTC.
  - ~~Snapshot cũ 2026-09-07: $19.965 ≈ 515,1tr, BTC 63,71% · SOL 29,19% · USDT 3,61% · USDC 3,48%.~~
  - *(lịch sử, đã hết hiệu lực từ 07/09)* ⚠️ **BNSOL không phải 1:1 với SOL**: giá spot BNSOL/USDT = $101,90 vs SOL $90,36 → **1,1277 SOL/BNSOL** (rewards staking tích luỹ, tỷ lệ chỉ tăng). Mọi lần định giá trước đây quy BNSOL theo giá SOL đều **thiếu ~13%**.
  - *(lịch sử)* ✅ **Không cần Standard Redemption 4 ngày** — có cặp spot BNSOL/USDT (vol $2,56M/24h), bán trực tiếp, phí taker 0,1%.
- **⏰ DEADLINE MỚI: 31/10/2026** *(đổi 2026-08-21 bổ sung 2)*. User có **kênh bán USDT trao tay**, không qua P2P/ngân hàng → không bị NĐ 284 ép về 1/9. Deadline thật là lúc cần tiền đóng tiền sử dụng đất (~T11). **31/10 vừa là hạn an toàn cho dòng tiền, vừa trùng đỉnh mùa vụ** (T10 trung vị +15,6%, dương 7/9 năm).
  - 🎯 **Chiến lược đang chạy (từ 18/09/2026): Decision Matrix v2.1 ở mục 7.3** — glidepath theo số lượng coin + band TTS + stop thật. Không còn trục "điều kiện thị trường", không dùng dự báo hướng giá để đổi kích thước hay thời điểm tranche.
    - ~~Chiến lược 25/08: trailing stop 10-12% + ladder $80k/$88k/$98k~~ — thay bằng glidepath 18/09. Ladder giá không còn là cơ chế chính; nó chỉ tồn tại ở vế "bán thêm khi giá cao" của Trục 2.
  - *Cách tính % trailing:* `max(12%, 3×ATR14/giá)` từ đỉnh nhịp — thị trường êm thì giữ 12%, biến động phình thì stop tự nới theo ATR để không bị quét bởi nhiễu thường nhật. **Stop phải là lệnh thật trên sàn, không phải "để ý trong đầu".**
  - ~~🔴 **RED ALERT 505tr** *(user đặt 04/09/2026)*~~ — **ĐÃ BỎ ngày 18/09/2026 theo quyết định của user.** Lý do: rule nổ liên tục 11 ngày (08→18/09) mà **chưa một lần được thực thi**; một chuông kêu mãi không ai dậy thì nó dạy thói quen bỏ qua chuông và làm hỏng cả rule khác. Vùng 470-515tr nay do **band ở mục 7.3 Trục 2** phụ trách (dải giữa = bán đúng lịch).
  - **Hard floor 440tr** — thủng thì bán sạch ngay, không bàn.
  - ⚠️ Trao tay **vẫn cấu thành "giao dịch"** theo Điều 9 NĐ 284, chỉ khó bị phát hiện hơn; dấu vết chuyển sang bước nộp tiền mặt vào bank → giữ chứng từ nguồn tiền.
- ~~**Deadline cũ: 1/9/2026 — MỐC PHÁP LÝ**~~ *(hạ xuống thành khuyến nghị, không còn ràng buộc)*. **NĐ 284/2026/NĐ-CP Điều 9 khoản 1**: *"Phạt tiền từ 30.000.000 đến 50.000.000 đồng đối với **nhà đầu tư trong nước** giao dịch tài sản mã hóa không thông qua tổ chức cung cấp dịch vụ do Bộ Tài chính cấp phép."* Đây là mức áp **trực tiếp cho cá nhân** (không chia đôi), không có ngoại lệ cho việc tự bán tài sản của mình.
  - 🔴 **Sau 1/9 có thể KHÔNG CÒN kênh hợp pháp nào**: chưa sàn nào được cấp phép (dự kiến Q3/2026), và Binance **không thể** được cấp phép (NQ 05/2025 yêu cầu doanh nghiệp VN, vốn ≥10.000 tỷ, ≥65% vốn nội).
  - ✅ **Nắm giữ KHÔNG bị phạt**, chỉ *giao dịch* mới bị (UBCKNN 05/06/2026) → phương án dự phòng hợp pháp là giữ nguyên và chờ sàn nội, nhưng **tiền kẹt vô thời hạn** và gap BĐS phình lên ~1,1 tỷ.
  - Override ưu tiên 1 (`<14 ngày → market sell ALL`) **đang có hiệu lực**. Chốt hạn nội bộ cho phần coin→USDT: **27/08** (trước keynote Jackson Hole của Warsh 28/08).
- **🔑 Nguyên tắc thực thi: tách 2 quyết định.** *Coin → USDT* gỡ rủi ro giá, làm được tức thì → **làm ngay**. *USDT → VND* gỡ rủi ro pháp lý, bị chặn bởi AML (20-50tr/lệnh) → rải đều 11 ngày. Đừng giữ coin chờ theo tiến độ rút VND.
- **Mục tiêu đầu tư:** Quỹ dự phòng thanh khoản **bắt buộc phải rút (cash-out) để làm sổ đỏ**. Không phải danh mục hold dài hạn.
- **Time Horizon:** Cực ngắn. Deadline nộp hồ sơ sổ đỏ là **Đầu tháng 11/2026** (Chỉ còn khoảng 3 tháng).
- **Khẩu vị rủi ro:** Cực kỳ thận trọng. Ưu tiên bảo toàn số vốn >400tr hiện có để kịp đắp vào tiền làm sổ đỏ BĐS, không được phép để hao hụt thêm quá sâu.

## 2. Target Allocation & Tình trạng hiện tại (đo 2026-09-18 11:10)

| Tài sản | SL | Giá | Giá trị | Định hướng xử lý |
|---|---|---|---|---|
| **BTC** | **0,15931** | $77.253 | **318,3tr** (63,1%) | Glidepath 7.3 Trục 1 + ladder limit bán sẵn + stop-market **$75.900**. |
| **SOL** | **55,28** | $104,49 | **149,4tr** (29,6%) | Như BTC. Stop-market **$98,50**. Cổng swap sang BTC đang mở (97,8% biên 90 ngày) nhưng **chưa thực hiện**. |
| **Stables** (USDT+USDC) | ~$1.415 | — | **36,6tr** (7,3%) | **Rút ra VND ngay** — không chịu rủi ro giá, không lý do trì hoãn. |
| **BNB** | dust | — | — | Phí giao dịch. |

> **Quy tắc số lượng (thêm 07/09): số lượng coin dùng để tính port phải là số ĐO** (đọc từ app/số dư sàn, hoặc suy từ % phân bổ user chụp từ app) — **không bao giờ là số SUY từ cơ cấu cũ**. Bảng suy 21/08 từng lệch −11% ở BNSOL, gây báo sai port +3,7% (~20tr). Mỗi lần user báo số mới từ app → cập nhật bảng này, ghi ngày.
> ~~Snapshot 07/09: BTC 0,1593 · SOL 55,3 · USDT 721 · USDC 695.~~ ~~Snapshot 04/08: BTC 64,53% · BNSOL 25,74% · USDC 5,13% · ONDO 4,58%.~~

## 3. Nguyên tắc & Chiến lược tối ưu (Optimization Strategy)
Vì toàn bộ số tiền này **được dùng làm quỹ dự trữ làm sổ đỏ (deadline T11/2026)**, chiến lược sẽ thiên về **phòng thủ & rút lui (Exit Strategy)** thay vì tối ưu lợi nhuận:
- **Tái cơ cấu (Rebalancing):** KHÔNG nạp thêm tiền mới để gồng lỗ (tránh rủi ro kẹt vốn). KHÔNG mua thêm các Altcoin rủi ro cao.
- **Chiến lược Rút vốn (Take profit / Exit):** 
  - Bán theo **glidepath cố định** ở mục 7.3 Trục 1 (không còn "canh mốc giá cao để chốt dần" — cách đó đã chạy từ 04/08 và cho ra 0/12 lệnh được thực thi).
  - Phân bổ rút dần ra VND (P2P) theo từng đợt, tránh đợi đến sát deadline T11/2026 mới xả một cục (đề phòng thị trường dump sập đúng lúc cần tiền).
- **Rủi ro tập trung sàn (Platform risk):** 100% danh mục nằm trên Binance — một lần khoá tài khoản là mất quyền truy cập toàn bộ, đúng lúc pháp lý VN đang siết. Quy tắc giảm thiểu:
  - **USDT sau khi bán coin KHÔNG nằm ỳ trên sàn**: chuyển ra theo đúng nhịp kênh rút (P2P/trao tay) ngay khi có thể, mục tiêu số dư USDT trên sàn không vượt ~1 tuần khối lượng rút.
  - Bất kỳ dấu hiệu hạn chế tài khoản (yêu cầu KYC lại, treo rút, cảnh báo AML) → **kích hoạt ngay override N4 RỦI RO** (7.3), không chờ review.
  - Bật whitelist địa chỉ rút + 2FA; không dùng tài khoản Binance này cho bất kỳ hoạt động nào khác ngoài kế hoạch exit.
- **Chiến lược Cắt lỗ (Stop loss):** Phải xác định một mốc "Hard Stop" cho danh mục (Nếu tổng tài sản tụt xuống dưới 440 triệu thì bắt buộc cắt máu cash-out toàn bộ ra VND để đảm bảo không bị thiếu hụt tiền làm BĐS). *(Lịch sử: 380tr → 405tr ngày 07/08 → 440tr ngày 21/08. Tầng cảnh báo hiện hành: **band ở mục 7.3 Trục 2** → hard floor 440tr. RED ALERT 505tr đã bỏ ngày 18/09.)*

## 4. Nhật ký giao dịch gần nhất
- **2026-08-04:** Khởi tạo danh mục. Vốn 650tr -> Còn 414tr. Cơ cấu: 64.5% BTC, 25.7% BNSOL, 5.1% USDC, 4.6% ONDO. Xác định phương hướng cash-out toàn bộ phục vụ Dự án 01 BĐS.
- **2026-08-11:** User xác nhận **chưa bán gì**. Chốt deadline nội bộ 1/9, bỏ thứ tự "BTC bán cuối", chuyển sang xả song song.
- **2026-08-21:** Nhịp tăng mạnh (BTC +15,5%/3 ngày), TTS ~472,5tr, **3 override cùng kích hoạt** → quyết định bán dứt điểm. Bác đề xuất "vay bù để giữ coin chờ nhịp lớn" (vi phạm 2/3 nguyên tắc bất biến; để về bờ 650tr cần thêm +37,6%). Vẫn **chưa xác nhận đã bán**.
- **2026-09-05→07:** Bán ONDO (~$721 USDT). Redeem BNSOL → SOL ~55,3. Port đo từ app: $19.965 ≈ 515,1tr.
- **2026-09-08→18:** Port thủng 505tr rồi 500tr (đáy 482,5tr ngày 16/09). CPI 11/09 và FOMC 17/09 đi qua, dots cứng nhưng giá không sập; port hồi về **504,3tr ngày 18/09**.
- **2026-09-18:** Plan lên **v2.1**. (1) **Bỏ RED ALERT 505tr**, hoà vào band Trục 2. (2) **Nới glidepath** 25/25/25/25 → **15/20/30/35** back-loaded, theo quyết định của user *(agent phản đối — mục 7.3)*. (3) Thêm **ladder bán sẵn** L1/L2/L3 làm đối trọng. **Danh mục vẫn BTC 0,15931 + SOL 55,28 — chưa bán gì, chưa swap gì.** Tiến độ rút VND **0%**, 0/12 khuyến nghị bán được thực thi.

---

## 5. Lộ trình Exit — Glidepath v2.1  *(thay bảng milestone T8/T9/T10, 18/09/2026)*

Bảng cũ (3 giai đoạn T8 → T9 → T10, mục tiêu ~414tr, hạn 25/10) đã hết giá trị: nó lập khi port còn 414tr và trước khi có override 11/10. **Lịch thi hành duy nhất là bảng dưới**, cơ chế đầy đủ ở mục 7.3.

Đơn vị là **số lượng coin**, không phải giá trị VND — giá trị dao động, số lượng thì không. Gốc: **0,15931 BTC + 55,28 SOL** (đo 18/09).

| Ngày | Bán | BTC | SOL | ≈VND @$77.253/$104,49 | Luỹ kế |
|---|---|---|---|---|---|
| **18/09** | toàn bộ stables | — | — | 36,6tr | 36,6tr (7,3%) |
| **24/09** | 15% | 0,023897 | 8,292 | 70,1tr | 106,7tr (21,2%) |
| **30/09** | 20% | 0,031862 | 11,056 | 93,5tr | **200,3tr (39,7%)** |
| **07/10** | 30% | 0,047793 | 16,584 | 140,3tr | 340,5tr (67,5%) |
| **11/10** | 35% (hết) | 0,055758 | 19,348 | 163,7tr | 504,2tr (100%) |

**Ladder bán sẵn — cơ chế bắt nhịp hồi.** Đặt **limit GTC ngay hôm nay**, không chờ. Lượng khớp được **trừ vào tranche xa nhất còn lại** (11/10 trước, rồi 07/10) — tổng vẫn 100%, không bán quá.

| Mức | TTS | BTC | SOL | Bán thêm | Trừ vào |
|---|---|---|---|---|---|
| **L1** | 515tr | **$79.034** | **$106,90** | 10% (0,015931 BTC + 5,528 SOL) | 11/10 |
| **L2** | 530tr | **$81.512** | **$110,25** | 15% (0,023897 BTC + 8,292 SOL) | 11/10 |
| **L3** | 545tr | **$83.990** | **$113,60** | 25% (0,039828 BTC + 13,820 SOL) | 07/10 |

> Nếu nhịp hồi đi tiếp, ladder khớp dần và **đuôi 11/10 tự teo từ 35% về 10% rồi 0%** — tức chính cái giá phải trả của việc nới sẽ được nhịp hồi trả lại. Nếu không hồi, ladder không khớp, glidepath chạy nguyên.

> ⚠️ **Cái giá của việc nới (18/09) — ghi để không quên khi nhìn lại:**
> - Luỹ kế 30/09 rơi từ **268tr (54%)** ở bản v2 xuống **200tr (40%)** — **thủng sàn tiến độ 228tr**. Sàn này coi như bỏ.
> - Đuôi 11/10 phình từ 25% lên **35%**: một cục lớn phải bán đúng ngày hạn cứng, bất kể giá hôm đó. Ladder ở trên là cơ chế duy nhất làm nó nhỏ lại.
> - Nới chỉ có lãi nếu giá **tăng** từ đây. Đi ngang thì không được gì; giảm thì mất đúng phần chênh.
> - **Agent phản đối quyết định này ngày 18/09** — lý do đầy đủ ở cuối mục 7.3. **User quyết giữ; agent thi hành.**

**Không đổi, không thương lượng:**
- **11/10 là hạn cuối thật** (override #1: từ 11/10 còn <14 ngày tới 25/10 → market sell ALL). 25/10 chỉ là hạn dự phòng.
- **Hard floor 440tr** (≈ BTC $66.644 / SOL $90,14) → bán sạch ngay.
- **Stop-market thật BTC $75.900 · SOL $98,50** phải nằm trên sàn, không phải "để ý trong đầu".
- **Điều kiện thị trường chỉ được làm TĂNG tốc độ bán** (Trục 2) — không bao giờ làm giảm hay hoãn thêm lần nữa.

## 6. Playbook vận hành định kỳ

### 6.1 Weekly Check — Mỗi Thứ 2 đầu tuần

Checklist thực hiện mỗi tuần (ước tính ~15 phút):

- [ ] **Snapshot giá trị:** Chụp/ghi lại tổng giá trị danh mục (VND). So với tuần trước tăng/giảm bao nhiêu %.
- [ ] **Kiểm tra tiến độ exit:** Đã rút được bao nhiêu VND so với milestone tháng này? Đang đúng tiến độ hay chậm?
- [ ] **Đánh giá thị trường (5 phút):**
  - BTC tuần qua tăng hay giảm? Có tin tức macro lớn nào không? (Fed, CPI, ETF flow...)
  - Sentiment chung: Tham lam (Greed) hay Sợ hãi (Fear)?  → Check [Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [ ] **Quyết định action tuần này:**
  - Có đặt lệnh bán (Limit Sell) mới không? Ở mốc giá nào?
  - Có cần Market Sell ngay (nếu đang pump mạnh) không?
  - TTS đang ở band nào của Trục 2 (mục 7.3)? Có ô nào buộc tăng tranche không?
- [ ] **Ghi log:** Append kết quả vào `logs/{YYYY-MM}.md`. Dùng format chuẩn ở mục **7.5** — không dùng format riêng, tránh hai format song song gây khó so sánh giữa các tuần.

### 6.2 Monthly Review — Đầu mỗi tháng (T9/2026, T10/2026)

Checklist review sâu hơn (ước tính ~30 phút):

- [ ] **Tổng kết tháng vừa qua:**
  - Giá trị đầu tháng vs cuối tháng.
  - Tổng VND đã rút thành công trong tháng. So với milestone đã vượt/chưa đạt?
  - Cơ cấu danh mục còn lại: bao nhiêu % BTC, bao nhiêu % Altcoin, bao nhiêu % Stablecoin?
- [ ] **Review chiến lược — Có cần điều chỉnh không?**
  - Nếu rút **nhanh hơn kế hoạch** → tốt, nhưng **không được đổi thành lý do hoãn tranche sau**. Glidepath chỉ đi nhanh hơn, không đi chậm lại.
  - Nếu rút **chậm hơn kế hoạch** → Cảnh báo! Cần tăng tốc xả hàng tháng tới, thậm chí Market Sell không cần canh giá.
  - Mốc hard floor **440tr** và các band ở Trục 2 tính trên **TTS = VND đã rút + crypto còn lại**, nên không phải hạ theo phần còn lại khi đã rút được tiền.
- [ ] **Research macro tháng tới:**
  - Có sự kiện lớn nào sắp tới? (FOMC, CPI, ETF deadline, Solana unlock schedule...)
  - Tỷ giá P2P USDT/VND có biến động không? (Ảnh hưởng trực tiếp số VND thực nhận khi rút).
- [ ] **Cập nhật file:**
  - Sửa mục "Giá trị hiện tại" ở Section 1 và bảng số lượng ở Section 2 (bằng số ĐO từ sàn).
  - Ghi review vào `reviews/{tháng}-review.md`.

### 6.3 Trigger-based Actions — Kích hoạt bất kỳ lúc nào

Ngoài lịch tuần/tháng, các tình huống sau **kích hoạt hành động ngay lập tức** bất kể đang ở tuần nào:

| Trigger | Hành động | Lý do |
|---|---|---|
| **TTS chạm band Trục 2** (mục 7.3) | Theo đúng ô band: ≥530tr bán thêm 50% · 515-530tr tranche 15%→40% · 450-470tr tranche →40% · <450tr bán 60%/24h | Thay cho mọi trigger giá rời rạc cũ. Band chỉ làm **tăng** tốc độ bán. |
| **Tổng port < 440 triệu** | **EMERGENCY: Market Sell ALL → VND** | Hard floor (nâng 405→440 ngày 21/08). Bảo vệ vốn tối thiểu cho BĐS. Không bàn cãi, không chờ đợi. |
| **Giá thủng stop $75.900** | Lệnh stop-market trên sàn tự khớp | Stop là lệnh thật, không phải mức để cân nhắc. Ratchet lên mỗi thứ Năm, không bao giờ hạ. |
| **Dấu hiệu hạn chế tài khoản Binance** (KYC lại, treo rút, cảnh báo AML) | Kích hoạt override N4 RỦI RO ngay, không chờ review | Rủi ro kênh rút lớn hơn rủi ro giá. |
| **Tin xấu macro lớn** (FED tăng lãi suất đột ngột, sàn bị hack...) | Đánh giá ngay trong 1h, nếu port giảm >5% → xả 50% ngay | Không chờ "hồi phục", vì deadline là cố định (T11/2026). |

> ~~Các trigger đã bỏ ngày 18/09:~~ ~~"BTC pump >10%/tuần → xả 30-50%"~~ và ~~"BNSOL/ONDO pump >15%"~~ (không còn giữ BNSOL/ONDO) và ~~"Tổng port >450tr → xả phần vượt 414tr"~~ (mốc 414tr là số port cũ tháng 8, nay vô nghĩa) và ~~"🔴 TTS ≤505tr RED ALERT"~~ (nổ 11 ngày liên tiếp không được thực thi — xem mục 1). Tất cả đã được hệ band ở Trục 2 thay thế.

## 7. Quy trình Weekly Deep Review (khi có Agent hỗ trợ)

> Quy trình này dành cho agent. Section 6 là checklist thao tác tay của bạn — hai phần bổ trợ nhau, không thay thế nhau.
>
> **Về cách chạy research ở bước 7.2:** nếu tool hỗ trợ subagent → chạy 4 nhóm song song rồi tổng hợp. Nếu không → làm tuần tự theo thứ tự 1→4. Trong mọi trường hợp, Nhóm 4 phải được đọc sau cùng khi tổng hợp, vì nhóm này có quyền phủ quyết.

### 7.0 Khi nào chạy

- **Mặc định:** mỗi Thứ 2 đầu tuần.
- **Chạy ngay, không chờ Thứ 2**, nếu có bất kỳ điều nào sau đây:
  - BTC biến động >10% trong tuần (tăng hoặc giảm)
  - TTS (xem 7.3) rời khỏi dải giữa 470-515tr (Trục 2, mục 7.3)
  - Tin macro lớn: Fed đổi lãi suất đột ngột, sàn bị hack, tin siết pháp lý crypto tại VN
  - Còn dưới 14 ngày tới 25/10/2026 (tức từ 11/10 — override #1)
  - Một ngày tranche (24/09 · 30/09 · 07/10 · 11/10) đã trôi qua mà không có lệnh thật

### 7.1 Bước 1 — Thu thập input

1. Đọc file này để nắm chiến lược, milestone (Section 5) và cơ cấu danh mục (Section 2).
2. Đọc `crypto/logs/{YYYY-MM}.md` gần nhất — tiến độ rút và action đã thực hiện.
3. Đọc `real-estate/real-estate-plan.md` mục "Kế hoạch tài chính & Trả góp" — lấy số liệu vốn/vay hiện hành.
4. **Tự tính giá trị port, KHÔNG hỏi user**: lấy số lượng coin từ **bảng cơ cấu ĐO ở Section 2** (bản mới nhất, có ghi ngày đo), nhân giá spot Binance, quy VND theo tỷ giá P2P.
   **⚠️ QUY TẮC CỨNG: giá spot và tỷ giá P2P phải fetch REALTIME tại đúng thời điểm tính** (API ở block 7.2) — không tái sử dụng số của lần review trước, không dùng số cũ trong log kể cả cùng ngày, không ước lượng. Áp dụng cho MỌI lần quy đổi VND: deep review, check nhanh, cập nhật port, đối chiếu ngưỡng (hard floor 440tr, ladder...). Lý do: mọi ngưỡng quyết định đo bằng VND, tỷ giá lệch 1-2% là đủ đổi kết luận trigger; và đã từng sai 8% vì dùng số không tươi (06/08).
   Chỉ hỏi user 3 câu:
   - Đã rút được bao nhiêu VND kể từ lần review trước?
   - Có giao dịch nào ngoài kế hoạch không? (nếu có → cập nhật lại số lượng coin dùng để tính)
   - **Lệnh nào đang THẬT SỰ nằm trên sàn?** (trailing stop, ladder limit — liệt kê từng lệnh: loại, giá, khối lượng)
5. **Kiểm kê thực thi (BẮT BUỘC, làm trước khi phân tích):** đối chiếu mọi khuyến nghị của các review trước với câu trả lời câu 3. Phân biệt rõ ba trạng thái: `ĐÃ THỰC THI` / `CÓ LỆNH SỐNG TRÊN SÀN` / `CHỈ LÀ KHUYẾN NGHỊ TRÊN GIẤY`. **Khuyến nghị xuất hiện lần thứ 2 mà vẫn chưa thực thi → phải nêu bật ở ĐẦU output kèm câu hỏi trực tiếp "vì sao chưa làm / có quyết định KHÔNG làm không?"** — không được lặp lại khuyến nghị lần 3 như thể lần đầu. Lý do: từ 06/08 đến 04/09 có ≥6 lần khuyến nghị bán chưa được thực thi mà không lần nào bị chặn lại hỏi; chênh lệch kế hoạch–thực tế là rủi ro lớn nhất của toàn hệ thống, lớn hơn mọi sai số chỉ báo.
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
- SOL: giá, %Δ tuần, vị trí so EMA/MA50 tuần, **SOL/BTC và percentile 90 ngày** (cổng swap), funding + OI (đòn bẩy dẫn hay spot dẫn), lịch unlock, dòng ETF SOL
- ~~ONDO~~, ~~BNSOL~~: không còn nắm giữ (ONDO bán 05-07/09; BNSOL redeem 07/09).
- Stables: không research, chỉ đọc số dư
- Nguồn: Binance spot, TradingView, Coinglass, token unlock trackers
- Output: mỗi coin một dòng — momentum `tăng`/`giảm`/`ngang` + lý do ưu tiên xả trước (nếu có)

**Nhóm 4 — Pháp lý VN + kênh rút tiền** ⚠️
- Hỏi: VN có quy định mới về tài sản số / sàn được cấp phép / siết P2P? Tỷ giá USDT/VND trên Binance P2P so với tuần trước? Spread và thanh khoản merchant? Có tin ngân hàng block tài khoản giao dịch P2P?
- Nguồn: VnExpress, CafeF, Thư viện pháp luật, Binance P2P
- Output: `kênh rút THÔNG` / `TẮC NGHẼN` / `RỦI RO` + tỷ giá + cảnh báo

> **Quyền phủ quyết của Nhóm 4:** nếu Nhóm 4 báo `RỦI RO`, kết quả này override toàn bộ tính toán giá của Nhóm 1-3, kích hoạt override ưu tiên 1 ở mục 7.3. Lý do: giá coin đẹp mà không chuyển được thành VND trước 25/10 thì vô nghĩa — và rủi ro này không thể "chờ hồi phục" như rủi ro giá.

**📡 Nguồn API chuẩn (miễn phí, curl trực tiếp — dùng TRƯỚC khi cào web hay dùng nguồn tổng hợp):**

Mọi endpoint dưới đây thêm header `User-Agent: Mozilla/5.0`. Lưu ý môi trường: python `urllib` hay lỗi SSL trên máy này → tải bằng `curl` ra file rồi mới parse.

**Quy tắc tươi dữ liệu:** giá spot và tỷ giá P2P luôn fetch mới tại thời điểm sử dụng (xem quy tắc cứng ở 7.1 bước 4). Các dữ liệu chậm hơn (ETF flow, F&G, Altcoin Index, dominance) cập nhật theo ngày là đủ.

| Dữ liệu | Nhóm | Endpoint |
|---|---|---|
| Giá spot + klines (tính EMA/RSI/MACD/volume) | N3 | `api.binance.com/api/v3/ticker/price?symbols=[...]` · `api.binance.com/api/v3/klines?symbol=X&interval=1d\|4h\|1w&limit=N` |
| Funding rate + Open Interest (đo độ nóng đòn bẩy) | N3 | `fapi.binance.com/fapi/v1/fundingRate?symbol=X&limit=6` · `fapi.binance.com/futures/data/openInterestHist?symbol=X&period=1d&limit=10` |
| Order book depth (tường bid/ask quanh hỗ trợ/kháng cự) | N3 | `api.binance.com/api/v3/depth?symbol=X&limit=1000` — cộng dồn khối lượng theo dải giá 0,5-1%, tìm cụm lệnh lớn bất thường |
| **ETF BTC net flow theo ngày** (thay Coinglass/Farside vốn JS-rendered) | N2 | `api.coinmarketcap.com/data-api/v3/etf/overview/netflow/chart?category=btc&range=1m` |
| Fear & Greed — bản CMC (kèm btcPrice, btcVolume) | N2 | `api.coinmarketcap.com/data-api/v3/fear-greed/chart?start=<epoch giây>&end=<epoch giây>` ⚠️ truyền nhầm năm là lấy data năm cũ mà không báo lỗi |
| Fear & Greed — bản alternative.me (đối chiếu) | N2 | `api.alternative.me/fng/?limit=N` |
| Altcoin Season Index + altcoin mcap (đo breadth rotation) | N2 | `api.coinmarketcap.com/data-api/v3/altcoin-season/chart?start=<epoch>&end=<epoch>` |
| BTC dominance + stablecoin mcap (snapshot hiện tại) | N2 | `api.coinmarketcap.com/data-api/v3/global-metrics/quotes/latest` (endpoint `/dominance/chart` hay lỗi 500, đừng dựa vào) |
| **Tỷ giá USDT/VND realtime** (bắt buộc lấy MỚI NHẤT mỗi lần review/tính port) | N4 | Trang tham chiếu user chỉ định: [pricedancing.com USDT-VND chart](https://www.pricedancing.com/vi/Binance-P2P-USDT-VND-chart-ZqzaQWc) — chart của chính dữ liệu Binance P2P, xem trend/MA bằng mắt. Trang render JS + chống bot PoW nên agent KHÔNG tự đọc được (xác minh 06/08 & 04/09) → số realtime lấy qua **cùng nguồn gốc**: POST `p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search` body `{"page":1,"rows":10,"payTypes":[],"asset":"USDT","tradeType":"SELL","fiat":"VND","transAmount":"50000000"}` — giá ở `data[].adv.price`, lấy giá tốt nhất trong top ads. KHÔNG dùng nguồn tổng hợp (goonus/webgia — từng sai 8%). |

⚠️ Dominance của CMC (~59-60%) lệch hệ quy chiếu với TradingView (~56%) — chỉ so **trend trong cùng một nguồn**, không so chéo số tuyệt đối giữa hai nguồn (lỗi này từng gây khuyến nghị sai 19tr ngày 21/08).

Kết thúc bước này, tổng hợp Nhóm 1-3 thành **điều kiện thị trường**:
- `THUẬN LỢI` — risk-on, momentum tăng, F&G >60
- `TRUNG TÍNH` — tín hiệu hỗn hợp
- `BẤT LỢI` — risk-off, momentum giảm, F&G <40

### 7.3 Bước 3 — Decision Matrix  *(bản v2.1 — 18/09/2026 chiều; v2 viết sáng cùng ngày, v1 ở git history)*

> **Vì sao có v2 (sáng 18/09).** Bản v1 có trục "điều kiện thị trường" (THUẬN LỢI / TRUNG TÍNH / BẤT LỢI) — trục này đòi agent phán đoán hướng giá. Tuần 16-18/09 agent sai 3/3 lần liên tiếp cùng một hướng (khuyến nghị bán ở 482,5 / 493,5 / 493,4tr trong khi TTS lên 504,3tr; cây kịch bản FOMC lệch +45tr). Một trục mà đầu vào sai có hệ thống thì phải bỏ, không phải hiệu chỉnh.
> **Và vì sao là LÚC NÀY.** Toàn bộ rủi ro nhị phân đã đi qua: CPI 11/09 ✅, FOMC 17/09 ✅. FOMC kế tiếp ra quyết định 01:00 VN 29/10 — **sau** deadline. CPI 14/10 nằm **sau** override #1 (11/10). → Từ 18/09 tới hết kế hoạch **không còn sự kiện nhị phân nào cần chờ**. Lý do "chờ tin ra rồi tính" đã hết hiệu lực vĩnh viễn.
> **Vì sao có v2.1 (18/09).** User quyết **nới glidepath** vì BTC/SOL đang hồi (504,2tr, cao nhất từ 08/09). Ghi vào Trục 1 dưới dạng 15/20/30/35, kèm **ladder bán sẵn** làm đối trọng cho phần đuôi phình ra. **Agent đã phản đối vế nới** — lý do và cái giá ghi ở cuối mục này, không xoá. Danh mục **vẫn là BTC + SOL**; swap chỉ là quyền chọn đang mở.

**Định nghĩa TTS = VND đã rút + giá trị crypto còn lại.** Đo bằng VND vì nghĩa vụ cuối (tiền sử dụng đất) tính bằng VND; mọi lần đo dùng tỷ giá P2P realtime (quy tắc cứng 7.1 bước 4).

---

#### Trục 1 — GLIDEPATH: lịch bán cố định, không cần quyết định lại

Bán theo **số lượng coin cố định**, không theo giá trị VND. Gốc: **0,15931 BTC + 55,28 SOL** (đo 18/09).

| Ngày | Bán | BTC | SOL | ≈VND | Luỹ kế |
|---|---|---|---|---|---|
| **18/09** | toàn bộ stables | — | — | 36,6tr | 36,6tr (7,3%) |
| **24/09** | 15% | 0,023897 | 8,292 | 70,1tr | 106,7tr (21,2%) |
| **30/09** | 20% | 0,031862 | 11,056 | 93,5tr | 200,3tr (39,7%) |
| **07/10** | 30% | 0,047793 | 16,584 | 140,3tr | 340,5tr (67,5%) |
| **11/10** | 35% (hết) | 0,055758 | 19,348 | 163,7tr | 504,2tr (100%) |

- Tranche **back-loaded 15/20/30/35** *(v2.1, thay 25/25/25/25 của v2 — theo quyết định nới của user)*.
- Mỗi ngày tranche: đặt limit sát giá thị trường lúc mở phiên; **không khớp trước 20:00 VN thì market**, không dời sang hôm sau.
- **11/10 = hạn cuối thật** (override #1, và trước CPI 14/10). Mốc 25/10 chỉ còn là hạn dự phòng.
- Không có ô nào cho phép bán **ít hơn** hoặc **muộn hơn**. Việc nới đã dùng hết một lần rồi.

**Ladder bán sẵn (đặt limit GTC ngay 18/09)** — lượng khớp trừ vào tranche xa nhất còn lại (11/10 trước, rồi 07/10):

| Mức | TTS | BTC | SOL | Bán thêm |
|---|---|---|---|---|
| L1 | 515tr | $79.034 | $106,90 | 10% |
| L2 | 530tr | $81.512 | $110,25 | 15% |
| L3 | 545tr | $83.990 | $113,60 | 25% |

> Ladder là **Trục 2 biến thành lệnh thật**, không phải rule mới. Nó tồn tại vì vấn đề lớn nhất của kế hoạch này không phải chọn đúng ngưỡng mà là **0/12 khuyến nghị được thực thi** — lệnh GTC tự khớp, không cần ai quyết định lúc giá chạy.

#### Trục 2 — BANDS: trạng thái TTS chỉ được làm TĂNG tốc độ bán

Giá quy đổi tính trên danh mục thật (0,15931 BTC + 55,28 SOL + $1.415 stables, P2P 25.860), giả định hai coin dịch cùng tỷ lệ:

| Band | TTS | ≈ BTC / SOL | Hành động |
|---|---|---|---|
| 🟢 Lời bất ngờ | **≥530tr** | $81.512 / $110,25 | **Bán thêm 50% NGAY**, ngoài lịch *(ladder L2/L3 đã phủ một phần)* |
| 🟢 Trên dải | **515-530tr** | $79.034-81.512 | Tranche tuần đó **→ 40%** *(ladder L1 đặt ở đây)* |
| ⬜ **Dải giữa** | **470-515tr** | $71.600-79.034 | **Theo đúng lịch, không làm gì thêm** ← đang ở đây (504,2tr) |
| 🟠 Dưới dải | **450-470tr** | $68.296-71.600 | Tranche tuần đó **→ 40%** |
| 🔴 Cảnh báo | **<450tr** | <$68.296 / $92,37 | **Bán 60% crypto trong 24h** |
| ⛔ Hard floor | **<440tr** | <$66.644 / $90,14 | **Bán sạch ngay.** Không bàn. *(giữ nguyên từ 21/08)* |

> **Nguyên tắc trung tâm — thay cho mọi phán đoán hướng giá:**
> **Điều kiện thị trường chỉ được phép LÀM TĂNG lượng bán, không bao giờ làm giảm hoặc hoãn.**
> Giá lên → bán thêm (giá tốt). Giá xuống → bán thêm (bảo vệ sàn). Giá đi ngang → bán đúng lịch.
> Nhờ vậy kết cục không còn phụ thuộc việc agent đoán đúng hướng.
> *(RED ALERT 505tr đã bỏ ngày 18/09 — vùng đó nay nằm trong dải giữa.)*

#### Trục 3 — STOP THẬT (bắt buộc, không phải tuỳ chọn)

- Luôn có **stop-market GTC trên sàn** cho toàn bộ vị thế còn lại. Không có stop = vi phạm kế hoạch, không phải "đang cân nhắc".
- Đặt dưới đáy phiên Mỹ gần nhất, **ratchet lên mỗi thứ Năm, không bao giờ hạ xuống**.
- Mức hiện hành (18/09): **BTC $75.900 · SOL $98,50** (đáy phiên Mỹ 17/09: $76.000 / $98,47). Nếu cả hai khớp → TTS ≈ **496,5tr**.

#### Override — đè lên toàn bộ

| Điều kiện | Hành động | Ưu tiên |
|---|---|---|
| Nhóm 4 báo RỦI RO kênh rút (pháp lý/P2P/khoá TK) | Market sell ALL → VND trong 24h | 1 |
| Từ 11/10 (<14 ngày tới 25/10) | Market sell ALL, bất kể giá | 1 |
| TTS < 440tr | Market sell ALL → VND | 1 |
| Dấu hiệu hạn chế tài khoản Binance | Kích hoạt N4 ngay, không chờ review | 1 |

**Thứ tự xả trong mỗi tranche: SOL trước, BTC sau** — lý do **cấu trúc, không phải dự báo**: cầu ETF của SOL mỏng và đang cạn (**$153,9M tuần 28/08 → $6,2M tuần 04/09, −96%**; BTC hàng trăm triệu mỗi phiên), sổ lệnh mỏng hơn (bid/ask ±2% ≈ 0,7 vs 0,95), ATR ngày 4,06% vs 2,48%. *(Đính chính 18/09: SOL CÓ ETF — SEC công nhận SOL cho commodity trust 05/09/2026. Câu cũ "SOL không có cầu ETF" là sai về bản chất.)*

**Cổng swap SOL→BTC:** mở khi SOL/BTC **>85% biên độ 90 ngày**. Hiện **97,8%** (0,0013529; đỉnh 90 ngày 0,0013593) → **cổng đang mở, chưa thực hiện**. Được phép swap thay vì bán SOL, nhưng **không được dùng swap để thay thế tranche** — tranche vẫn phải bán đủ ra USDT.

#### Ba điều bản v2 CẤM agent làm *(giữ nguyên ở v2.1)*

1. **Không dùng dự báo hướng giá** (OI, funding, L/S, CVD, cây kịch bản, xác suất) làm lý do đổi kích thước hay thời điểm tranche. Các chỉ báo đó chỉ dùng để chọn **limit hay market trong ngày**, không bao giờ để hoãn.
2. **Không lặp lại một khuyến nghị đã bị bỏ qua như thể lần đầu.** Khuyến nghị chưa thực thi lần 2 → nêu ở đầu output kèm câu hỏi trực tiếp.
3. **Không đề xuất thêm ngưỡng/rule mới khi rule hiện có chưa từng được thực thi.** Từ 04/08 đến 18/09: 0/12 khuyến nghị bán được thực thi, 3 chuông cứng nổ và bị bỏ qua.

#### 📌 Bất đồng đã ghi nhận — việc nới glidepath (18/09)

**User quyết nới. Agent phản đối. Kế hoạch thi hành theo quyết định của user.** Lý do phản đối, ghi lại để đối chiếu về sau chứ không để tranh cãi tiếp:

- Giá hồi về 504,3tr **không phải thông tin mới về tương lai** — nó là dữ kiện về quá khứ 3 ngày. Nới vì giá hồi chính là vế "điều kiện thị trường làm giảm tốc độ bán" mà bản v2 viết cùng buổi sáng đã cấm.
- Luỹ kế 30/09 rơi **268tr → 200tr**, thủng sàn tiến độ 228tr.
- Đuôi 11/10 phình **25% → 35%**: một cục lớn phải bán đúng ngày hạn cứng, bất kể giá hôm đó.
- Bối cảnh: **tiến độ rút vẫn 0% sau 45 ngày, 0/12 khuyến nghị được thực thi.** Trong một hệ thống chưa từng thực thi rule nào, việc đầu tiên được thực thi lại là rule cho phép bán ít hơn.
- Đối trọng duy nhất với việc nới là **ladder bán sẵn** ở Trục 1. Nếu ladder không được đặt thành lệnh thật, việc nới trở thành "giữ nguyên và hy vọng" — không có cơ chế nào biến nhịp hồi thành tiền.

**Điều kiện để agent không nêu lại chuyện này:** tranche 24/09 được thực thi đúng hạn và đủ lượng. Nếu 24/09 trôi qua mà không có lệnh thật, agent phải nêu lại ở đầu mọi output (theo điều cấm số 2).

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
- Tiến độ luỹ kế: XXXtr (XX%) | Tranche đến hạn gần nhất: DD/MM → ĐÃ THỰC THI / CHƯA
- Còn XX ngày tới 11/10 (hạn cuối thật)

### Research
- N1 vĩ mô toàn cầu: risk-on/off/neutral — [lý do]
- N2 vĩ mô crypto: [F&G, ETF flow, dominance]
- N3 vi mô: BTC [...]
- N4 pháp lý VN/P2P: THÔNG/TẮC/RỦI RO | tỷ giá XXX
→ Band Trục 2: [tên band] | Stop hiện hành: $XX.XXX

### Quyết định
- Ô matrix: [tiến độ] × [thị trường]
- Override kích hoạt: [không / tên override]
- Action: [lệnh cụ thể: coin nào, bao nhiêu, market hay limit ở giá nào]
- Judgment call: [nếu có — nêu rõ]

### Đối chiếu BĐS
- Vốn tự có dự phóng T11/2026: X.XXX tỷ
- Cần vay: XXXtr (kế hoạch 433tr, Δ: ±XXtr)
- Mốc hết nợ: T1/2028 → [giữ nguyên / lùi X tháng]

### Kịch bản & Insight
- Xếp hạng vấn đề theo ĐỘ LỚN TÁC ĐỘNG TIỀN, không theo thứ tự phát hiện
- Bảng nhạy cảm: TTS thay đổi ra sao nếu tài sản lớn nhất ±5/10/15/20%
- 3-4 kịch bản, mỗi kịch bản có điều kiện kích hoạt rõ ràng và hành động tương ứng
- "Điều gì làm đổi khuyến nghị" — danh sách trigger kiểm chứng được
```

> **Vì sao bắt buộc có mục "Kịch bản & Insight":** bốn mục trên chỉ là bản ghi trạng thái — chúng trả lời "đang thế nào", không trả lời "nên làm gì và vì sao". Không có mục này thì review dễ sa vào việc phân tích kỹ những khoản nhỏ dễ đo (spread, phí, chiết khấu vài %) trong khi bỏ qua rủi ro lớn gấp cả chục lần nhưng khó đo (timing trên vị thế lớn nhất, rủi ro đuôi như khoá tài khoản). **Quy tắc: luôn xếp hạng theo số tiền, và luôn hỏi "cái gì lớn nhất mà mình chưa nhắc tới?"**

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
