# Thiện Trần — Kênh Thương Hiệu Cá Nhân (AI & Tech Insight)

> **Đây là luồng làm việc chính thức cho kênh Thiện Trần.**
> Bất kỳ AI nào làm việc trong thư mục này đều phải tuân thủ nghiêm ngặt các quy tắc dưới đây.

## 1. CỐT LÕI NỘI DUNG (THE MISSION)
- **Định vị**: Kênh phân tích tín hiệu cao (High-Signal Filter), không phải máy đọc báo.
- **Tiêu chuẩn (Quality Gate)**:
  - Tách biệt rõ ràng: **FACT** (Sự thật/Số liệu) vs **INFERENCE** (Suy luận) vs **OPINION** (Góc nhìn).
  - Phải trả lời được: Điều này tạo ra thay đổi thực tế gì? Ai bị ảnh hưởng? Hype vs Substance là gì?
  - Bỏ qua: Tin đồn vô căn cứ, tin PR sáo rỗng của công ty, thông báo không mang lại giá trị thực tế.

## 2. QUY TẮC DỰNG VIDEO (RENDER ENGINE)
- **Cấu trúc JSON**:
  - `hook` phải < 10 từ. Đi thẳng vào vấn đề.
  - Phải có ít nhất 1 trạm `mode: "shot"` kèm ảnh chụp màn hình chứng minh (Fact).
  - Hai trạm liên tiếp dùng chung 1 ảnh thì đều phải dùng `mode: "shot"`.
  - Mảng `words` và `weights` phải luôn bằng nhau.
  - Outro luôn là: `{"mark": "Thiện Trần", "socials": [{"platform": "facebook", "handle": "/thientm"}, {"platform": "tiktok", "handle": "/thientranx"}, {"platform": "youtube", "handle": "/thientm"}]}`
- **Tuyệt đối KHÔNG SỬA CẤU TRÚC `scene.html`**: Mọi layout, camera, safezone đã được căn chỉnh 100%. Chỉ được phép đổi màu biến CSS (`--ink`, `--now`, `--was`, `--paper`) nếu cần.

## 3. QUY TẮC ĐĂNG BÀI (PUBLISHING PIPELINE)
- **Tuyệt đối không chạy Headless**: TikTok và FB sẽ shadowban nếu phát hiện headless bot.
- **Bảo mật Profile**: Dữ liệu duyệt web lưu tại `~/.thien-tran-browser`. Không bao giờ lưu trong git.
- **Khởi động**: Luôn dùng `./thien-tran/publish/open_browser.sh` để mở Chrome qua cổng `9444`.
- **Tối ưu SEO 3 Nền tảng**:
  - **YouTube Shorts**: Tiêu đề có từ khoá tìm kiếm, mô tả dài, giàu ngữ nghĩa.
  - **TikTok**: Gọn gàng, 1 câu + 3-4 hashtag cốt lõi.
  - **Facebook Cá nhân**: Đăng qua `facebook.com/reels/create`, ngắt đoạn thoáng mắt, dùng 2-3 emoji định vị (💡, 🚀).

## 4. BÀI HỌC GIAO DIỆN NỀN TẢNG (UI QUIRKS LỊCH SỬ)
- **YouTube**: Lệnh gõ phím `.type()` gây ra lỗi giật lag nhảy chữ (race condition), dẫn đến tiêu đề rác. LUÔN LUÔN dùng `.fill()` cho `#title-textarea` và `#description-textarea`. Không dùng link `?d=ud` vì YouTube hay giấu nút, hãy tìm nút bằng lệnh `p.get_by_role("button", name=re.compile(r"create", re.I))`.
- **Facebook**: 
  - Nút xuất bản chính thức mang tên **"Post"** (hoặc Đăng). Tránh click nhầm vào nút thả xuống "Scheduling options Publish now". Dùng `re.compile(r"^(Post|Publish|Đăng)$", re.I)`.
  - **LƯU Ý QUAN TRỌNG VỀ QUYỀN RIÊNG TƯ (AUDIENCE)**: Facebook cá nhân hay bị mặc định trạng thái `Only me` (Chỉ mình tôi). Kịch bản upload FB cần (và phải) kiểm tra nút Audience ở bước cuối và chuyển sang `Public` (Công khai) trước khi bấm Post.
