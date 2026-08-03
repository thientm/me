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

## 7. Quy trình khi Agent hỗ trợ review

Mỗi khi bạn nhờ tôi review (hàng tuần hoặc hàng tháng), tôi sẽ thực hiện theo quy trình sau:

1. **Đọc file này** (`crypto-plan.md`) để nắm chiến lược hiện tại và milestone.
2. **Đọc log gần nhất** (`logs/{YYYY-MM}.md`) để biết tiến độ rút vốn và action đã thực hiện.
3. **Hỏi bạn 3 câu nhanh:**
   - Tổng giá trị port hiện tại? (hoặc bạn chụp screenshot)
   - Đã rút được bao nhiêu VND kể từ lần review trước?
   - Có giao dịch nào đặc biệt (mua/bán ngoài kế hoạch) không?
4. **Đưa ra đánh giá:**
   - Tiến độ exit so với milestone: Đúng / Nhanh / Chậm.
   - Gợi ý action cụ thể cho tuần/tháng tới.
   - Cảnh báo nếu có rủi ro (giá giảm sâu, chậm tiến độ, sát deadline...).
5. **Cập nhật log** và điều chỉnh plan nếu cần.
