# Real Estate & Property Plan

> Lưu trữ lộ trình pháp lý, giấy tờ, và kế hoạch tài chính tổng thể cho các dự án bất động sản.

## Dự án đang thực hiện (Active)

### Dự án 01: Sang tên và lên thổ cư đất ở quê (Linked to G-01)

**Thông tin thửa đất**
- Vị trí: đất sau ga Yên Viên, gần cửa hàng Duy LiNing, gần đình làng Vân — thuộc xã Yên Viên cũ, nay là xã Phù Đổng.
- Phân vị trí theo bảng giá đất: Vị trí 2 (VT2), giảm 20% do cách mặt đường >500m.
- Giá theo Bảng giá đất Hà Nội 2026 (NQ 52/2025/NQ-HĐND, hiệu lực 1/1/2026): **38tr/m²** — đã xác nhận qua luật sư tra cứu (2026-08-03).

#### 1. Lộ trình pháp lý & Thủ tục
| Bước | Trạng thái | Ngày cập nhật | Ghi chú |
|---|---|---|---|
| 1. Ký hợp đồng tặng cho tại phòng công chứng | Chưa bắt đầu | | |
| 2. Nộp hồ sơ đăng ký sang tên tại VP Đăng ký đất đai / Bộ phận một cửa | Chưa bắt đầu | | |
| 3. Đóng thuế, phí (TNCN, lệ phí trước bạ - nếu không được miễn) | Chưa bắt đầu | | |
| 4. Nhận sổ đỏ mang tên mình | Chưa bắt đầu | | |
| 5. Nộp đơn xin chuyển mục đích sử dụng đất sang thổ cư + bản vẽ trích lục | Chưa bắt đầu | | |
| 6. Đóng tiền sử dụng đất khi lên thổ cư | Chưa bắt đầu | | |

> Trạng thái dùng: `Chưa bắt đầu` / `Đang làm` / `Chờ (bên ngoài)` / `Xong`. Cập nhật cột Ngày + Ghi chú mỗi khi trạng thái đổi; không xoá lịch sử, chỉ ghi đè trạng thái hiện tại (bảng này là snapshot, không phải log).

#### 2. Kế hoạch tài chính & Trả góp
*Dòng tiền thực tế hàng tháng (trả nợ, tích luỹ...) ghi ở `finance/logs/{YYYY-MM}.md`, mỗi entry liên quan tới dự án này gắn tag `[G-01]` trong `note` để dễ lọc. Mục này chỉ ghi tổng quan/mục tiêu.*
- **Tổng ngân sách dự kiến:** ~3 tỷ (nếu vay đủ để làm sớm)
- **Vốn tự có:** ~2.4 tỷ
  - 1.3 tỷ: Tiền bố mẹ cho (đang gửi tiết kiệm kỳ hạn 1 tháng).
  - 705 triệu: Tiền cá nhân (đang để tại Techcombank).
  - ~400 triệu: Đang nằm trong Crypto (có plan tracking cơ cấu riêng).
- **Số tiền cần vay:** 0 - 0.6 tỷ (chưa chốt, tuỳ quyết định — xem Research & Đánh giá bên dưới)
- **Kế hoạch vay:** 
  - Vay ai / Ngân hàng nào:
  - Lãi suất:
  - Thời hạn:
  - Số tiền trả góp dự kiến hàng tháng: (điền số tiền - sau đó update sang `finance/cashflow.md`)
- **Tích luỹ trước khi nộp hồ sơ:**
  - Mục tiêu cần có trước bước nộp hồ sơ/đóng thuế: (điền số tiền)
  - Hiện có: (điền số tiền, cập nhật khi có log tháng mới ở `finance/logs/`)

#### 3. Research & Đánh giá
*Ghi phát hiện/quyết định research vào đây khi có, kèm ngày. Không xoá mục cũ, thêm mục mới bên dưới nếu có cập nhật/đổi ý.*

**Phương án vay**
- 2026-08-03: Đang ở bước lên kế hoạch. Vốn tự có sẵn 2.4 tỷ; cần thêm ~0.6 tỷ nếu vay đủ 3 tỷ. Chiến lược thời điểm/vay phụ thuộc diễn biến khung giá đất khu vực (hiện tại mức 38):
  - Nếu khung giá đất biến động tăng thêm nhiều → vay đủ 3 tỷ, làm sớm để tránh thuế/lệ phí bị tính theo khung giá mới cao hơn.
  - Nếu khung giá đất không biến động nhiều → delay sang đầu năm sau (~sau Tết): vẫn phải vay, nhưng vay ít hơn — nhờ (1) lãi gửi tiết kiệm từ khoản 2.4 tỷ trong lúc chờ, (2) có thêm khoản thưởng Tết bổ sung vào vốn.
  - Chưa chốt phương án; phụ thuộc kết quả research khung giá đất (xem "Việc cần chốt" bên dưới).

- 2026-08-03 (đánh giá tài chính chi tiết A/B/C): Input xác nhận — vay cấu trúc 50% 0% lãi / 50% lãi 7%/năm, vay 1 năm đáo hạn, trả 35tr/tháng ưu tiên phần 7% trước (tối ưu lãi), lãi tiết kiệm giả định 4.5%/năm kỳ hạn 3 tháng (private bank — quốc doanh chỉ ~2.6-2.9%), thưởng Tết 50tr. Điểm mấu chốt: 35tr/tháng là dòng tiền có sẵn từ bây giờ — nếu chưa vay thì dùng để **tích luỹ vốn** thay vì trả nợ, nên các phương án delay không chỉ hưởng lãi tiết kiệm + thưởng Tết mà còn hưởng thêm tích luỹ chủ động này.

  | Phương án | Bắt đầu | Cần vay | Tổng lãi vay | Hết nợ hoàn toàn |
  |---|---|---|---|---|
  | A. Làm ngay | T8/2026 | 600tr | ~8.7tr | ~T2/2028 |
  | C. Chờ 4 tháng | T11/2026 (tích luỹ T8-T11, chưa có thưởng Tết) | ~433tr | ~4.7tr | ~T1/2028 |
  | B. Chờ hết Tết | T2/2027 (tích luỹ T8-T1 + thưởng Tết) | ~321tr | ~2.7tr | ~T12/2027 |

  - Thuần tài chính: B tối ưu nhất (ít lãi vay nhất, hết nợ sớm nhất theo lịch thực tế — vì khoản vay nhỏ hơn nhiều bù lại cả thời gian chờ). A kém nhất về tài chính nhưng chắc chắn nhất về giá đất (không phải chờ đợi gì).
  - **Phát hiện quan trọng nhất, làm thay đổi cách nhìn về "an toàn"**: Rủi ro bảng giá đất không nằm ở *ngày nộp hồ sơ*, mà nằm ở **ngày cơ quan nhà nước ra quyết định cho phép chuyển mục đích sử dụng đất (bước 5)** — đây mới là thời điểm áp giá đất tính "tiền sử dụng đất" (bước 6, khoản chi phí lớn nhất, nhạy giá đất nhất). Bảng giá đất điều chỉnh hằng năm có hiệu lực từ 1/1. Nên: bắt đầu sớm hơn (vd. tháng 11 thay vì tháng 2) **chỉ thực sự né được rủi ro nếu toàn bộ quy trình đến lúc có quyết định chuyển mục đích hoàn tất trước 31/12/2026** — nếu xử lý hồ sơ ở địa phương mất >2 tháng (khá phổ biến ở VN cho thủ tục chuyển mục đích), thì bắt đầu tháng 11 hay tháng 2 không khác biệt về mặt né rủi ro giá đất, và lúc đó nên quay lại chọn theo tài chính thuần tuý (ưu tiên B).
  - Chưa chốt: cần biết thời gian xử lý thực tế bước 2-5 tại địa phương (xem "Việc cần chốt" bên dưới) mới chọn được giữa A/B/C.

**Việc cần chốt (Open)**
- [ ] Research & chốt khung giá đất khu vực — kết quả quyết định: làm sớm (vay đủ 3 tỷ) hay delay qua Tết (vẫn vay, nhưng ít hơn). *(mở từ 2026-08-03)*
  - 2026-08-03: Đã research xong phần cơ chế/luật (xem chi tiết ở mục "Thủ tục pháp lý & chi phí" bên dưới). Còn thiếu: tra đúng Phụ lục (theo vị trí thửa đất) kèm Nghị quyết 52/2025/NQ-HĐND để xác nhận chính xác mức áp cho thửa đất của mình (hiện mới biết mặt bằng chung khu vực Gia Lâm, chưa khớp đúng thửa). Task vẫn mở.
  - 2026-08-03 (update): Đã xác nhận qua luật sư — thửa đất thuộc Vị trí 2 (VT2), giảm 20% do xa mặt đường >500m → đúng 38tr/m² (xem "Thông tin thửa đất" ở đầu mục). Phần xác minh con số coi như xong; task này giờ chỉ còn phần **quyết định** vay đủ 3 tỷ làm sớm hay delay qua Tết — chưa chốt.
  - 2026-08-03 (cross-check độc lập, không qua luật sư): Đã tự tra lại **cơ chế** — khớp đúng luật: VT2 = thửa giáp ngõ/ngách ≥3.5m (đúng định nghĩa NQ 52/2025/NQ-HĐND); quy định giảm 20% cho khoảng cách ≥500m so với đường chính là có thật, tìm thấy nguyên văn khớp. Xã Phù Đổng thuộc Khu vực giá đất số 8 (cùng Thuận An, Gia Lâm, Bát Tràng). **Không tự verify lại được con số gốc VT2 khu vực 8** vì không truy cập được file Phụ lục PDF/Excel chính thức (các nguồn online đều 403 hoặc chỉ có bản dự thảo/tóm tắt). → Kết luận: cơ chế luật sư dùng là đúng luật, nhưng con số 38tr cuối cùng vẫn dựa vào việc tin luật sư đã tra đúng file gốc, chưa tự đối chiếu số học được.
- [x] Xác nhận thời gian xử lý thực tế bước 2-5 (đặc biệt bước 5 — chuyển mục đích sử dụng đất) tại VP đăng ký đất đai/UBND xã Phù Đổng, hoặc hỏi luật sư — để biết bắt đầu tháng nào thì kịp có quyết định chuyển mục đích **trước 31/12/2026** (né được rủi ro bảng giá đất 2027). Nếu xử lý mất >2 tháng, phương án bắt đầu tháng 11 không còn né được rủi ro này, nên ưu tiên tài chính (phương án B, chờ tới T2/2027). *(mở từ 2026-08-03)*
  - 2026-08-04 (update): Luật sư xác nhận thời gian xử lý tối đa là **1 đến 2 tháng**. → **Chốt chọn Phương án C (Nộp hồ sơ đầu Tháng 11/2026)**: Đảm bảo có Quyết định trước 31/12/2026 để khóa giá 38tr/m² (né rủi ro tăng giá 2027), đồng thời tối ưu thêm được 4 tháng tích luỹ (T8-T11/2026) ~175tr vốn tự có, giảm tiền vay xuống còn ~433tr. Hết nợ hoàn toàn vào T1/2028.
  - 2026-08-06 (cảnh báo, chưa đổi quyết định): Phương án C có biên an toàn gần bằng 0 — trường hợp xử lý 2 tháng thì quyết định rơi đúng 1/1/2027, mốc bảng giá đất mới có hiệu lực. Cân nhắc dời lên đầu T10/2026. Xem chi tiết ở mục "⚠️ Rủi ro thời điểm" bên dưới.
- [ ] **Hỏi luật sư: hệ số K có bị tính chồng lên bảng giá 2026 không?** Đang có tranh luận rằng bảng giá đất 2026 vốn đã bao gồm hệ số K, nếu cơ quan thuế áp thêm K lần nữa khi tính tiền sử dụng đất thì số phải nộp **tăng thêm 1-1.5 lần**. Đây là rủi ro tính toán (không liên quan việc điều chỉnh bảng giá 2027) nhưng độ lớn tác động rất cao — phải làm rõ trước khi nộp hồ sơ. *(mở từ 2026-08-06)*
- [ ] **Hỏi luật sư: có được giảm 70% tiền sử dụng đất khi chuyển lên thổ cư không?** Có quy định áp dụng từ 1/1/2026 về việc giảm 70% tiền sử dụng đất cho một số trường hợp chuyển mục đích ([VOV](https://vov.vn/kinh-te/bat-dong-san/tu-112026-truong-hop-nao-duoc-giam-70-tien-su-dung-dat-khi-chuyen-len-tho-cu-post1256789.vov)). Chưa rõ thửa đất của mình có thuộc diện được giảm không — nếu có thì đây là khoản tiết kiệm rất lớn, đủ để đổi cả bài toán vay. *(mở từ 2026-08-06)*

**Thủ tục pháp lý & chi phí (thuế TNCN, lệ phí trước bạ, điều kiện lên thổ cư ở địa phương...)**
- 2026-08-03: Research khung giá đất / bảng giá đất (để đánh giá rủi ro tăng giá cho quyết định vay ở trên):
  - Luật Đất đai 2024 (hiệu lực 1/8/2024) **bỏ hẳn "khung giá đất"** cũ (cơ chế Chính phủ ban hành trần/sàn 5 năm/lần theo Luật Đất đai 2013). Mức 4.5tr/m² trước đây ở khu vực mình là theo khung cũ này, áp dụng đến hết 31/12/2025.
  - Từ 1/1/2026, Hà Nội áp dụng **"Bảng giá đất lần đầu"** theo Nghị quyết 52/2025/NQ-HĐND (HĐND TP thông qua 26/11/2025), xây dựng theo **nguyên tắc thị trường** (không còn bị khung giá đất cũ khống chế trần), chia theo vị trí VT1-VT4 (theo tên đường/mặt đường) + hệ số điều chỉnh cho nhà nhiều mặt tiền, giảm giá theo khoảng cách tới đường chính. → Đây là nguồn gốc mức 38tr đang thấy.
  - **Kết luận sơ bộ**: mức tăng 4.5tr → 38tr chủ yếu do **đổi hẳn phương pháp luận một lần** (chuyển từ khung giá đất bị khống chế thấp hơn thị trường nhiều năm, sang bảng giá theo thị trường), không phải biến động thị trường thông thường của 1 năm — bản chất giống "one-time reset" hơn là bước đầu của một chuỗi tăng dồn dập.
  - **Cơ chế điều chỉnh sau 2026**: Luật quy định bảng giá đất áp dụng/điều chỉnh **hàng năm** (khác chu kỳ 5 năm cũ), nhưng Nghị quyết 52/2025 không quy định mức tăng tự động — mỗi lần điều chỉnh vẫn cần UBND TP trình HĐND TP xem xét, quyết nghị lại. Không có cơ chế leo thang tự động.
  - **2 yếu tố khiến rủi ro tăng tiếp vẫn thật, không chỉ lý thuyết**:
    1. Giá rao bán thị trường thực tế quanh Yên Viên hiện ~50-70tr/m² (mặt đường thương mại 70-120tr/m²) — cao hơn nhiều so với 38tr bảng giá NN → dù đã "nhảy" ~8 lần, bảng giá vẫn thấp hơn thị trường, còn dư địa điều chỉnh tăng tiếp theo đúng nguyên tắc thị trường của luật mới.
    2. Gia Lâm đang tái cơ cấu hành chính (vận hành mô hình mới từ 1/7/2025, gộp còn 17 đơn vị cấp xã) và có định hướng lên quận — chất xúc tác riêng có thể khiến giá khu vực này tăng nhanh hơn mặt bằng chung trong các đợt điều chỉnh tới.
  - **Nguồn**: [cafef.vn - Từ 1/8 Luật Đất đai bỏ khung giá đất](https://cafef.vn/tu-1-8-luat-dat-dai-bo-khung-gia-dat-bang-gia-dat-lan-dau-duoc-ap-dung-tu-1-1-2026-188240716105310487.chn), [luatvietnam.vn - Bỏ khung giá đất ảnh hưởng thế nào đến người dân](https://luatvietnam.vn/dat-dai-nha-o/bo-khung-gia-dat-anh-huong-nhu-the-nao-den-nguoi-dan-567-96754-article.html), [luatvietnam.vn - Nghị quyết 52/2025/NQ-HĐND](https://luatvietnam.vn/dat-dai/nghi-quyet-52-2025-nq-hdnd-ha-noi-bang-gia-dat-lan-dau-ap-dung-tu-01-01-2026-420193-d2.html), [thanhuyhanoi.vn - Gia Lâm hoàn tất sắp xếp đơn vị hành chính](https://thanhuyhanoi.vn/tin-tuc/huyen-gia-lam/huyen-gia-lam-hoan-tat-sap-xep-don-vi-hanh-chinh-san-sang-van-hanh-mo-hinh-moi-tu-2025-50018267.html).
  - **Đã xác minh (update 2026-08-03)**: 38tr/m² là đúng cho thửa đất của mình — luật sư tra cứu xác nhận thửa thuộc Vị trí 2 (VT2), giảm 20% do cách mặt đường >500m. Chi tiết vị trí: xem "Thông tin thửa đất" ở đầu mục Dự án 01.

**Thị trường BĐS Hà Nội (research 2026-08-06)**
- **Chung cư HN: KHÔNG có sóng thoát hàng — mới ở mức dấu hiệu sớm.**
  - Thứ cấp Q2/2026 ~60tr/m² (CBRE), **giảm 3% QoQ — lần đầu giảm kể từ cuối 2022**; tăng YoY co còn 13% (đỉnh 2024-25 là 26%).
  - Hấp thụ toàn thị trường Q2/2026 chỉ 68% nguồn cung mới (trước đây thường >90%); riêng dự án mở bán mới giảm 3 quý liên tiếp, còn ~50%.
  - Nhưng **sơ cấp vẫn tăng mạnh**: ~95tr/m², +12% QoQ, +21% YoY. Phân khúc <60tr/m² đã biến mất khỏi nguồn cung mới.
  - Chuyên gia (VnBusiness, CafeBiz) nói phần lớn là **"cắt lãi" chứ không phải cắt lỗ thật**. Thị trường đang phân hoá (sơ cấp cao cấp neo/tăng, thứ cấp dùng đòn bẩy chịu áp lực), chưa phải khủng hoảng.
  - Nguồn cung: H1/2026 mở bán 16.600 căn; dự báo 2026-2027 khoảng 35.000-40.000 căn/năm.
- **Dự phóng giá chung cư 2027:** CBRE/One Mount — đà tăng chậm lại, vẫn tăng 2 chữ số nhưng thấp hơn hẳn mức 24-25%/năm trước. ABS Research: neo cao ~100-102tr/m² xuyên 2026-2027. *(Có một luồng nói giá giảm 15-30% giai đoạn 2027-2029, nhưng KHÔNG xác minh được tổ chức nào đứng sau — coi là ý kiến thiểu số chưa kiểm chứng, không phải dự báo chủ đạo.)*
- **Đất nền vùng ven — quan trọng hơn chung cư đối với dự án này:**
  - Bảng giá đất nhà nước 2026 tại **Đông Anh, Gia Lâm, Thanh Trì tăng 20-26%** so với trước.
  - Long Biên tăng ổn định 8-12%/năm, thanh khoản tốt nhất. Gia Lâm/Đông Anh dư địa cao hơn nhưng rủi ro lớn hơn (nhiều khu đã "tăng đón đầu" mạnh 2021-2022).
  - Động lực chính là quy hoạch **14 cây cầu qua sông Hồng/sông Đuống** + hạ tầng, không phải sốt ảo.
  - *Chưa xác minh: không có số liệu định lượng về dòng tiền dịch chuyển chung cư ↔ đất nền.*
- **Kết luận cho quyết định của mình:** diễn biến chung cư **không đủ mạnh để làm căn cứ hành động**. Đất nền vùng ven vẫn trong xu hướng tăng, tức áp lực tăng bảng giá đất 2027 **không giảm đi**. Thời điểm nộp hồ sơ nên quyết theo tiến độ pháp lý, không theo tâm lý thị trường chung cư.
- **Nguồn**: [Tuổi Trẻ - chung cư HN rao cắt lỗ](https://tuoitre.vn/chung-cu-ha-noi-rao-cat-lo-ca-ti-dong-van-kho-ban-ap-luc-lai-vay-lau-ngay-100260707064935522.htm), [VnExpress - CBRE tốc độ tăng giá giảm một nửa](https://vnexpress.net/cbre-toc-do-tang-gia-chung-cu-cu-o-ha-noi-giam-mot-nua-5094899.html), [CafeBiz - thực chất là cắt lãi](https://cafebiz.vn/bat-dong-san-cat-lo-tran-lan-chuyen-gia-noi-thang-nhieu-noi-thuc-chat-chi-dang-cat-lai-176260726104540397.chn), [CafeF - dự báo giá chung cư 2026-2027](https://cafef.vn/du-bao-bat-ngo-ve-dien-bien-gia-chung-cu-ha-noi-tphcm-trong-giai-doan-2026-2027-188260802065633487.chn), [Dân Việt - bảng giá đất HN 2026 17 khu vực](https://danviet.vn/bang-gia-dat-ha-noi-2026-tu-ranh-gioi-hanh-chinh-den-17-khu-vuc-dinh-gia-thuc-te-d1373856.html).

**Cập nhật 2026-08-07 (deep-dive sóng thoát hàng — câu hỏi riêng: có nên chờ mua chung cư năm sau 2027?)**
- **Case cắt lỗ cụ thể (mới hơn, cho thấy điều chỉnh sâu hơn nhận định tháng 7)**: Nguyễn Xiển 6.2→4 tỷ (-35%), Kim Văn-Kim Lũ 3.9→2.4 tỷ (-38%), 19T Kiến Hưng 4.4→2.8 tỷ (-36%), Ngoại Giao Đoàn 110-120→75-80tr/m² (-30%), Dương Nội -1.2 tỷ, một case lỗ >1.5 tỷ **so với giá hợp đồng gốc** (lỗ thật, không chỉ "cắt lãi" như nhận định tháng 7). Nguyên nhân: áp lực thanh toán 45% giá trị HĐ còn lại khi bàn giao + hết ân hạn gốc + lãi vay 12-16%/năm (thả nổi lên 15-16%) đè nặng nhà đầu tư đòn bẩy cao. Tập trung dự án sắp bàn giao, phía Đông (dọc Đại lộ Thăng Long) và Tây/Tây Nam.
- **Điểm mấu chốt cho câu hỏi "chờ mua năm sau"**: đây là hiện tượng ở **thị trường thứ cấp** (nhà đầu tư kẹt dòng tiền bán lại). **Sơ cấp** (căn hộ mới từ chủ đầu tư) **vẫn tăng** — ~95tr/m², +12% QoQ, dự báo khu trung tâm +10-13%/năm trong 2026. → Nếu mục tiêu là mua căn mới/chủ đầu tư, chờ không có cơ sở giá sẽ giảm. Nếu mục tiêu là mua lại từ NĐT đang cần thoát hàng, ở đúng khu vực/phân khúc bị stress, cơ hội là thật và "quá trình điều chỉnh chưa dừng lại" theo chuyên gia.
- **Lịch sử 2011-2013 (giảm tới 50%, về giá 2006) có lặp lại không**: đa số chuyên gia được trích dẫn cho là **không** — bản chất khác nhau: 2011-2013 là dư cung + đóng băng tín dụng toàn hệ thống; hiện tại cung khan hiếm hơn, chi phí đất/xây tăng mạnh nâng giá sàn sơ cấp, thị trường được đánh giá "đang trên đà phục hồi" chứ không đóng băng.
- **Dự báo 2027 phân hoá 3 nhóm** (đã xác minh nguồn — cập nhật lại ghi chú "chưa xác minh" ở mục dự báo phía trên):
  1. CBRE/One Mount (mainstream): vẫn tăng, chậm lại về hai chữ số → dài hạn ~3-5%/năm. Không dự báo giảm.
  2. Phạm Đức Toản (TGĐ EZ Property): giá "sẽ phải giảm" do 298 dự án gỡ vướng đồng loạt khởi công 2026-2027 tăng cung — không đưa số % cụ thể.
  3. Nguyễn Anh Quê (Chủ tịch G6 Group — nguồn đã xác định, không còn là ý kiến ẩn danh): đi ngang hết 2025 → vào chu kỳ giảm dài, đáy 2028-2030, giảm **15-30%** (có nơi nói 10-30%) từ đỉnh Q4/2024. Bi quan nhất trong số có tên tuổi, nhưng vẫn thiểu số so với CBRE/Savills.
- **Trả lời trực tiếp**: không nguồn nào (kể cả bi quan nhất) dự báo giá **về lại** mức trước sốt hoặc giảm sâu kiểu 2011-2013 (50%). Cơ sở thực tế nhất để "chờ giá giảm mua năm sau" là nhắm vào **thứ cấp đang cắt lỗ** ở khu vực/dự án cụ thể đang bị stress đòn bẩy, không phải chờ mặt bằng giá chung cư đảo chiều.
- **Nguồn**: [VnExpress - Sóng thoát hàng chung cư sắp bàn giao](https://vnexpress.net/song-thoat-hang-chung-cu-sap-ban-giao-5104548.html), [Dân Trí - cắt lỗ cả tỷ đồng mỗi căn](https://dantri.com.vn/bat-dong-san/chung-cu-ha-noi-ha-nhiet-nhieu-nguoi-ban-cat-lo-ca-ty-dong-moi-can-20260807014428157.htm), [CafeF - dự báo bất ngờ giai đoạn 2026-2027](https://cafef.vn/du-bao-bat-ngo-ve-dien-bien-gia-chung-cu-ha-noi-tphcm-trong-giai-doan-2026-2027-188260802065633487.chn), [CafeF - Phạm Đức Toản: giá sẽ phải giảm](https://cafef.vn/sep-bds-khang-dinh-nam-2026-2027-nguon-cung-tang-manh-gia-chung-cu-ha-noi-se-phai-giam-188260122102146633.chn), [NguoiQuanSat - lịch sử đáy có lặp lại](https://nguoiquansat.vn/thi-truong-bds-ha-noi-den-het-nam-2025-lich-su-roi-vao-day-co-lap-lai-169525.html), [Stockbiz - Nguyễn Anh Quê dự báo giảm 15-30%](https://stockbiz.vn/tin-tuc/bat-dong-san-tinh-se-bat-dau-sot-vao-quy-32026-gia-chung-cu-ha-noi-se-ha-khoang-15-30-vao-giai-doan-2027-2029/27089754).

**⚠️ Rủi ro thời điểm — Phương án C có thể KHÔNG còn biên an toàn (2026-08-06)**
- **Cơ sở pháp lý bắt buộc**: Điều 159 khoản 3 Luật Đất đai 2024 quy định UBND cấp tỉnh **hàng năm** phải trình HĐND quyết định điều chỉnh bảng giá đất, công bố áp dụng **từ 1/1 năm sau**. Đây là nghĩa vụ bắt buộc, không phải tuỳ chọn.
- **Tiền lệ**: NQ 52/2025 được HĐND thông qua **26/11/2025**, hiệu lực 1/1/2026. → Bảng giá 2027 nhiều khả năng được trình/thông qua **khoảng tháng 10-11/2026**, hiệu lực 1/1/2027.
- **Chưa có tiền lệ bảng giá đất năm sau thấp hơn năm trước.**
- **Vấn đề với Phương án C**: nộp hồ sơ đầu T11/2026 + thời gian xử lý 1-2 tháng (luật sư xác nhận) → quyết định chuyển mục đích rơi vào khoảng **1/12/2026 đến 1/1/2027**. Trường hợp xấu (2 tháng) **rơi đúng mốc bảng giá 2027 có hiệu lực**. Tức Phương án C đang có biên an toàn gần bằng 0, không phải "đảm bảo trước 31/12" như đã chốt ngày 04/08.
- **Liên hệ chéo với domain crypto**: nếu chốt cash-out crypto trước 1/9/2026 (do Nghị định 284 — xem `crypto/logs/2026-08.md`), thì tiền đã sẵn sàng từ đầu tháng 9. Nghĩa là **có thể bắt đầu thủ tục đất sớm hơn T11**, ví dụ đầu T10, để quyết định rơi vào T11-T12/2026 — an toàn trước 1/1/2027. Ràng buộc pháp lý crypto lại vô tình mở ra cơ hội giảm rủi ro cho dự án đất.
- *Chưa xác minh: tính tới đầu 8/2026 chưa tìm thấy dự thảo, phát ngôn lãnh đạo TP hay lộ trình cụ thể nào về bảng giá đất 2027. Chỉ xác nhận được nghĩa vụ pháp lý phải điều chỉnh hàng năm.*

**Khác**
- 2026-08-04: Đánh giá sự đồng bộ với mục tiêu cá nhân (Hôn nhân). Đối tác (nữ, sinh năm 2000 - Canh Thìn) phạm Kim Lâu năm 2027 (28 tuổi mụ), hết Kim Lâu vào năm 2028 (29 tuổi mụ). Do đó bắt buộc phải cưới sau Tết Âm lịch 2028 (sang năm Mậu Thân). Mốc thời gian này **khớp hoàn hảo 100% với Phương án C**: Hết nợ hoàn toàn vào Tháng 1/2028 (sát Tết). Bước sang năm 2028 vừa cầm sổ đỏ chính chủ, vừa sạch nợ, vừa đẹp tuổi cưới.

### Dự án 02: Mua nhà ở cho bản thân (chung cư hoặc đất) — đang ngắm

> **Trạng thái đầu vào**: thông tin cung cấp rời rạc dần theo thời gian, không phải 1 lần đủ hết. Mục này là nơi chắt lọc/tổng hợp để nhìn ra bài toán quyết định, không phải log thô — cập nhật liên tục, không xoá mục cũ, chỉ thêm entry mới có ngày khi có input/research mới.

#### 1. Bài toán cần quyết
- Mua nhà ở riêng, đang cân nhắc giữa **3 chung cư** (Vinhomes Smart City, Hope Residence, Le Grand Jardin) và **1 lựa chọn đất nền** (Việt Hưng, Long Biên — phải bán một phần đất quê ở Dự án 01 sau khi ra sổ để có tiền mua).
- Tiêu chí đã biết tính đến giờ: **gần bố mẹ** (ưu tiên khu Long Biên/Việt Hưng/Phúc Đồng/Sài Đồng), có cơ hội mua rẻ nếu đúng lúc "sóng thoát hàng", pháp lý an toàn (sang tên bình thường, không vướng ràng buộc).
- Còn thiếu (xem "Việc cần chốt"): ngân sách tổng, mua để ở hay đầu tư, mốc thời gian mong muốn, có gắn với sự kiện khác không (vd. mốc cưới 2028 như Dự án 01).

#### 2. Các lựa chọn đang so sánh (research 2026-08-07)

| Lựa chọn | Vị trí | Giá hiện tại | Tình trạng thị trường | Pháp lý / rủi ro |
|---|---|---|---|---|
| Vinhomes Smart City | Tây Mỗ, Nam Từ Liêm — xa Long Biên/bố mẹ | Thứ cấp 3-5 tỷ/căn, cắt lỗ từ 2,4 tỷ, rẻ hơn thị trường 300-500tr ở một số căn | **Sóng thoát hàng rõ nhất trong 4 lựa chọn** — CĐT đã hết quỹ sơ cấp, hầu hết giao dịch là thứ cấp cắt lỗ | Sổ đỏ đầy đủ, giao dịch thông thường |
| Hope Residence | Phúc Đồng, Long Biên — gần | Giá gốc: NOXH ~16tr/m², thương mại ~22-25tr/m². Giá thứ cấp rao hiện tại **55,5-77,1tr/m²** (gấp 3,5-4,5 lần giá gốc) | **Không phải cắt lỗ — đang tăng vọt** do khan hiếm suất NOXH (93% dự án là NOXH, 1.397/1.504 căn; 107 căn còn lại là thương mại) | ⚠️ **Cần xác minh trước khi đi xa hơn**: bàn giao cuối 2025, luật cấm chuyển nhượng NOXH trong 5 năm đầu (trừ bán cho người đủ điều kiện mua NOXH khác) → nếu đang xem là suất NOXH mà chưa đủ 5 năm, giao dịch trên thị trường nhiều khả năng qua **ủy quyền/vi bằng** — không sang tên ngay, không thế chấp vay bình thường, rủi ro tranh chấp. Cần hỏi rõ môi giới: NOXH hay 1/107 căn thương mại. |
| Le Grand Jardin (Sài Đồng/Phúc Đồng, CĐT Handico3/BRG) | Long Biên — gần | Bàn giao thô 3PN ~2,3-2,6 tỷ; căn góc 97-106m² ~2,9-3,3 tỷ (1 listing ghi 77m²/6,5 tỷ — nghi outlier, cần kiểm tra thực tế khi xem) | Đã bàn giao xong, ổn định — không có áp lực "sóng thoát hàng do đến hạn thanh toán" như 2 dự án trên | Đã có sổ hồng, sang tên bình thường — rủi ro thấp nhất trong 3 chung cư |
| Đất nền Việt Hưng | Long Biên — gần nhất | ~171tr/m² (lô 63m², ngõ, mặt tiền 4,1m, phố Ngô Gia Tự) đến 250-270tr/m² (mặt phố/view công viên — outlier cao). Lô nhỏ 60-63m² trong ngõ đã **~10-10,8 tỷ** | Khu đã đô thị hoá hoàn chỉnh, giá ổn định neo cao, không phải thị trường đang cắt lỗ | Sổ đỏ, nhưng **vấn đề là tài chính**: đắt gấp 3-5 lần đất quê Phù Đổng cùng m² (38tr/m² bảng giá NN). Một lô nhỏ nhất đã vượt xa tổng ngân sách hiện có của Dự án 01 (~3 tỷ) — cần bán đất quê + có thêm vốn khác mới đủ. |

**Kết luận sơ bộ (2026-08-07)**:
- Chỉ Smart City đang có làn sóng cắt lỗ đúng nghĩa để "chờ mua rẻ"; nhưng vị trí mâu thuẫn với tiêu chí gần bố mẹ.
- Hope Residence và Le Grand Jardin đáp ứng vị trí, nhưng Hope Residence đang tăng giá (không giảm) và có rủi ro pháp lý NOXH cần làm rõ trước; Le Grand Jardin an toàn pháp lý nhất nhưng không có động lực giảm giá thêm.
- Đất nền Việt Hưng đáp ứng vị trí tốt nhất nhưng khoảng cách tài chính với ngân sách hiện có là vấn đề lớn nhất, chưa tính được chính xác vì thiếu diện tích thửa đất quê.
- **Nguồn**: [Batdongsan - Bảng giá Smart City cắt lỗ T5/2026](https://batdongsan.com.vn/ban-can-ho-chung-cu-phuong-tay-mo-vinhomes-smart-city/bang-gia-cap-nhat-t5-2026-gia-cat-lo-view-ep-san-so-ban-gap-lh-pr45732109), [Canhovinhomes - giá cắt lỗ từ 2,4 tỷ T7/2026](https://canhovinhomes.info/gia-mua-ban-chuyen-nhuong-can-ho-chung-cu-vinhomes-smart-city/), [Batdongsan - Hope Residence giá bán T1/2026](https://batdongsan.com.vn/du-an-nha-o-xa-hoi-long-bien/hope-residence-pj3744), [Vietnammoi - NOXH Long Biên giá 16tr/m2](https://vietnammoi.vn/ha-noi-cho-mo-ban-hon-300-can-noxh-gia-16-trieum2-20255419937824.htm), [Thuvienphapluat - tổng quan Hope Residence Phúc Đồng](https://thuvienphapluat.vn/phap-luat-nha-dat/tong-quan-du-an-hope-residence-phuc-dong-ha-noi-1577.html), [Homedy - Le Grand Jardin Sài Đồng](https://homedy.com/ban-can-ho-le-grand-jardin-sai-dong), [Dandautu - Le Grand Jardin tiến độ](https://dandautu.vn/du-an/le-grand-jardin-sai-dong), [Mogi - nhà đất Việt Hưng T2/2026](https://mogi.vn/ha-noi/quan-long-bien/mua-nha-dat/duong-viet-hung-long-bien-sid13657).

#### 3. Việc cần chốt (Open)
- [ ] **Diện tích thực tế thửa đất quê Phù Đổng** (Dự án 01) — cần để tính bán 1 phần thu về bao nhiêu, đủ mua bao nhiêu m² đất Việt Hưng. *(mở từ 2026-08-07)*
- [ ] **Xác minh căn Hope Residence đang xem là suất NOXH hay 1 trong 107 căn thương mại** — quyết định rủi ro pháp lý (ủy quyền/vi bằng) có chấp nhận được không. *(mở từ 2026-08-07)*
- [ ] **Ngân sách tổng dự kiến cho quyết định này** — vốn tự có, có vay không, độc lập hay dùng chung nguồn với ngân sách Dự án 01? *(mở từ 2026-08-07)*
- [ ] **Timeline mong muốn** — chờ đến khi nào, có gắn với mốc nào khác không (vd. mốc cưới 2028)? *(mở từ 2026-08-07)*
- [ ] Kiểm tra thực tế outlier giá 77m²/6,5 tỷ ở Le Grand Jardin khi đi xem — có thể là loại căn khác (villa/shophouse) trong cùng khu, không đại diện mặt bằng chung. *(mở từ 2026-08-07)*

## Lưu trữ dự án cũ (Completed)
- (Chưa có)
