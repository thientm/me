import os
import re
from brain.personas import PERSONA_METECH, PERSONA_TAMANLAC
from brain.templates import get_template_reply

def format_prompt(comment_text: str, channel: str, video_title: str = "") -> str:
    system_persona = PERSONA_TAMANLAC if channel == "tamanlac" else PERSONA_METECH
    prompt = f"""{system_persona}
Ngữ cảnh video: "{video_title if video_title else 'Video trên kênh'}"
Bình luận của người xem: "{comment_text}"

Hãy viết một câu phản hồi đúng tinh thần trên, tối đa 40 từ:"""
    return prompt

def clean_reply(text: str) -> str:
    # Bỏ ngoặc kép bao quanh nếu có
    res = text.strip()
    if res.startswith('"') and res.endswith('"'):
        res = res[1:-1].strip()
    if res.startswith("'") and res.endswith("'"):
        res = res[1:-1].strip()
        
    # Loại bỏ tiền tố xưng danh nếu LLM sinh
    prefixes = [
        "Mê Tech:", "Mê Tech :", "Tâm An Lạc:", "Tâm An Lạc :",
        "Ad:", "Admin:", "Trả lời:", "Phản hồi:"
    ]
    for p in prefixes:
        if res.startswith(p):
            res = res[len(p):].strip()
            
    return res

def generate_smart_reply(comment_text: str, channel: str, video_title: str = "", fallback_only: bool = False) -> str:
    if fallback_only:
        return get_template_reply(channel, "question")

    # Kiểm tra biến môi trường GEMINI_API_KEY nếu có
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return get_template_reply(channel, "question")

    try:
        import urllib.request
        import json

        prompt = format_prompt(comment_text, channel, video_title)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": 100,
                "temperature": 0.7
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            raw_text = body["candidates"][0]["content"]["parts"][0]["text"]
            return clean_reply(raw_text)
    except Exception:
        return get_template_reply(channel, "question")
