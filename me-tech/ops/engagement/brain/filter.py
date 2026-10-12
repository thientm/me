import re

SPAM_KEYWORDS = [
    "zalo", "tele", "t.me", "kiếm tiền", "nhận quà", "lừa đảo", "đm", "vl",
    "http://", "https://", "ib riêng", "liên hệ 0", "chứng khoán", "kèo", "đầu tư lãi"
]

TAMANLAC_GREETINGS = [
    "a di đà phật", "nam mô", "quán thế âm", "bình an", "an lạc",
    "chúc", "cầu an", "tịnh tâm", "hoan hỷ", "bồ tát", "cảm ơn kênh"
]

METECH_GREETINGS = [
    "hay quá", "tuyệt", "hóng", "đỉnh", "ủng hộ", "chúc kênh",
    "thả tim", "quá đã", "chất lượng", "cảm ơn ad", "cảm ơn bạn"
]

QUESTION_PATTERNS = [
    r"\?", r"không\b", r"sao\b", r"làm thế nào", r"thế nào", r"như thế nào",
    r"xin hỏi", r"cho mình hỏi", r"cài đặt", r"dùng được", r"ở đâu", r"giá bao nhiêu"
]

def classify_comment(text: str, channel: str) -> str:
    cleaned = text.strip().lower()
    
    # 1. Check Spam & Toxic
    for kw in SPAM_KEYWORDS:
        if kw in cleaned:
            return "spam"

    # 2. Check Question (Cần AI/LLM suy nghĩ)
    for q in QUESTION_PATTERNS:
        if re.search(q, cleaned):
            return "question"

    # 3. Check Greeting / Compliment
    if channel == "tamanlac":
        for kw in TAMANLAC_GREETINGS:
            if kw in cleaned:
                return "greeting"
    elif channel == "metech":
        for kw in METECH_GREETINGS:
            if kw in cleaned:
                return "greeting"

    return "neutral"
