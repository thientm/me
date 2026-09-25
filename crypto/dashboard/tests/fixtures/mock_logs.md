# Log Giao dịch Crypto - Tháng 09/2026 (Mock Fixture)

## 2026-09-04: Cập nhật nhanh — port hồi phục, BTC lại trên $80k. Vẫn chưa bán gì.

### Input
- **User xác nhận: CHƯA BÁN GÌ** — tiến độ luỹ kế: **0%**.
- Tiền mặt đã rút: **0 VND**.
- Giá (Binance spot, 04/09): BTC $80.785 | SOL $103,33 | USDC $1,00
- Tỷ giá P2P: 25.802

### Trigger check
| Trigger | Trạng thái |
|---|---|
| Hard floor 540tr | Đang ở mức thử nghiệm |
| Tiến độ rút VND | 0% (0/13 khuyến nghị thực thi) |

## 2026-09-21: Review tuần — Đỉnh mới 532,7tr

### Input
- TTS: 532.700.000 VND (VND đã rút 0 VND + crypto 532,7tr)
- Tiến độ luỹ kế: 0 VND (0%)
- Lệnh thực thi: 0/13

## 2026-09-24: Review ngày — Binary Decision Point

### Input
- TTS: 550.643.256 VND (VND đã rút 0 VND + crypto 550,6tr)
- Tiến độ luỹ kế: 0 VND (0%) | Tranche 1 đến hạn: 24/09
- Còn 37 ngày tới 31/10/2026

### Research
- N1 vĩ mô: Risk neutral
- N2 crypto: BTC $84.262, SOL $115,72, P2P 25.930
- N4 pháp lý: Rủi ro kẹt P2P
→ Active Band: TAKE_PROFIT_540M

### Quyết định
- Action: Bán 50% coin (xả sạch 55,28 SOL + một phần BTC) và rút toàn bộ $1.415 Stables sang VND.

### Đối chiếu BĐS
- Vốn tự có: 2.555,6 triệu VND
- Cần vay: 544,4 triệu VND (so với trần 615tr: an toàn 70,6tr)
