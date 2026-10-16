import datetime as dt
from typing import Dict, Any

def get_brainstorm_prompt(channel: str, topic: str) -> str:
    """Generate specialized brainstorming prompt according to channel identity and superpowers."""
    if channel == "me-tech":
        return f"""[Superpower: Brainstorming] Mê Tech — Đề tài: "{topic}"
Nhiệm vụ: Phát triển kịch bản video ngắn (32–38s) theo định vị "Công nghệ dễ hiểu, gần với đời mình".
Người xem: người Việt 18–40, dùng điện thoại hằng ngày, KHÔNG làm IT.
0. Nhóm đề tài (khoá "cat", xem me-tech/AGENTS.md "Định vị 2.0"):
   - Chọn 1 trong: dien-thoai, canh-giac, dang-tien, xe, vi-sao, tuong-lai, ai-dung-ngay, tech-viet.
   - Không quá 2 bài liền cùng nhóm — tra 3 dòng log gần nhất.
   - Phép thử: giải thích cho mẹ/em mình trong 1 câu được không? Không được thì đổi góc.
1. Phân tích cốt lõi:
   - "Cái này liên quan gì tới tôi?" — người xem dùng, tránh, hay mua được gì?
   - Mỗi con số đặt cạnh một thứ quen (ly cà phê, chiếc Vision, lương tháng). Tối đa 1 thuật ngữ, giải thích ngay.
2. Brainstorm Hook (Bắt buộc):
   - Đưa ra 3 phương án câu mở đầu (Hook) ≤10 từ, thời lượng nói ≤2.5s.
   - Câu 1 nhắc thứ người xem đã biết hoặc đang có; không mở bằng tên hãng/tên model.
3. Cấu trúc kịch bản:
   - Phân bổ 4-6 câu liền mạch, chuẩn bị từ khoá hot và số liệu trực quan.
   - Câu áp chót là câu hỏi mở trả lời được bằng một ý, để kéo comment.
   - Đối soát nhật ký me-tech/logs/*.md để đảm bảo không trùng góc khai thác."""

    elif channel == "thien-tran":
        return f"""[Superpower: Brainstorming] Thiện Trần — Đề tài: "{topic}"
Nhiệm vụ: Phát triển bài phân tích chuyên sâu (32–38s) theo chuẩn High-Signal Filter:
1. Tam giác phân tích:
   - FACT (Sự thật / Số liệu gốc): Số liệu benchmark, giá bán, chi phí API, tuyên bố kỹ thuật chính thức.
   - INFERENCE (Suy luận logic): Rút ra kết luận gì về xu hướng ngành? Đâu là chiếc bẫy chi phí hoặc giới hạn thật?
   - OPINION (Góc nhìn của Thiện): Lời khuyên thẳng thắn, bóc trần Hype vs Substance (ai hưởng lợi, ai trả tiền).
2. Brainstorm Hook:
   - Đưa ra 3 phương án câu mở đầu ≤10 từ (≤2.5s), sắc bén, phản biện trực diện định kiến đám đông.
3. Lựa chọn Trạm Shot:
   - Chọn 1 biểu đồ/benchmark/bảng dữ liệu đắt giá nhất làm bằng chứng xác thực.
   - Đối soát nhật ký thien-tran/logs/*.md chống trùng chủ đề."""

    elif channel == "tam-an-lac":
        return f"""[Superpower: Brainstorming] Tâm An Lạc — Đề tài: "{topic}"
Nhiệm vụ: Phát triển bài thiền ngắn (30–45s, giọng Thiền Tâm Đức):
1. Điểm chạm nỗi lòng:
   - Nỗi lo âu, áp lực công việc, mệt mỏi cuộc sống hoặc những tranh cãi chấp nhặt hàng ngày.
2. Soi chiếu lời Phật dạy:
   - Trích dẫn tinh thần mộc mạc từ lời Phật dạy qua Kinh Pháp Cú hoặc kinh điển đời thường (an trú hiện tại, biết buông xả).
3. Brainstorm 3 Prompt Hình Ảnh (Tránh trùng tam-an-lac/logs/images.json):
   - Prompt 1: Không gian tĩnh lặng, chén cơm, giọt nước, bóng nắng.
   - Prompt 2: Đức Phật / Bồ Tát tĩnh toạ giữa thiên nhiên (chỉ rõ phong cách tranh, chất liệu ánh sáng).
   - Prompt 3: Sự buông bỏ, tâm an, nụ cười nhẹ nhõm."""

    else:
        raise ValueError(f"Unknown channel: {channel}")

def generate_scaffold(channel: str, slug: str, title: str) -> Dict[str, Any]:
    """Generate blank compliant JSON scaffold for a given channel."""
    today_str = dt.date.today().strftime("%d.%m.%Y")
    
    if channel in ("me-tech", "thien-tran"):
        brand_name = "MÊ TECH" if channel == "me-tech" else "THIỆN TRẦN"
        outro_data = {
            "mark": "Mê Tech" if channel == "me-tech" else "Thiện Trần",
            "handle": "mecongnghe40" if channel == "me-tech" else "thientranx"
        }
        return {
            "slug": slug,
            "voice": "Xuân Vĩnh" if channel == "me-tech" else "Adam bựa",
            "brand": brand_name,
            "kicker": f"NEWS · {today_str}",
            "date": today_str,
            "gap": 0.24,
            "gap_group": 0.6,
            "lead_in": 0.4,
            "tail": 2.2,
            "speed": 1.1,
            "outro": outro_data,
            "hook": 1,
            **({"cat": ""} if channel == "me-tech" else {}),
            "segments": [
                {
                    "id": "hook",
                    "group": "intro",
                    "mode": "say",
                    "say": title,
                    "plain": title,
                    "words": title.split(),
                    "weights": [1] * len(title.split()),
                    "hot": [0]
                },
                {
                    "id": "outro",
                    "group": "outro",
                    "mode": "outro",
                    "words": [],
                    "weights": []
                }
            ]
        }
    elif channel == "tam-an-lac":
        return {
            "slug": slug,
            "voice": "Thiền Tâm Đức",
            "source": "Lời Phật dạy về chánh niệm và an lạc.",
            "lead_in": 0.1,
            "gap": 0.75,
            "tail": 3.6,
            "segments": [
                {
                    "id": "s1",
                    "text": title
                }
            ]
        }
    else:
        raise ValueError(f"Unknown channel: {channel}")
