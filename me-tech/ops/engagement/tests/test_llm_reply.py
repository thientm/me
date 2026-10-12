import pytest
from brain.llm_reply import format_prompt, clean_reply, generate_smart_reply

def test_prompt_formatting():
    prompt = format_prompt("Tool này có bản free không ad?", "metech", "Top 5 AI 2026")
    assert "Mê Tech" in prompt
    assert "tối đa 40 từ" in prompt
    assert "Tool này có bản free không ad?" in prompt

    prompt_tml = format_prompt("Làm sao để bớt giận dữ?", "tamanlac", "Chữ Nhẫn")
    assert "Tâm An Lạc" in prompt_tml
    assert "không hứa hẹn tâm linh" in prompt_tml

def test_clean_reply_guardrail():
    raw = ' "Chào bạn! Tool này có gói miễn phí nhé. Hãy thử ngay! " '
    cleaned = clean_reply(raw)
    assert cleaned == "Chào bạn! Tool này có gói miễn phí nhé. Hãy thử ngay!"

    # Loại bỏ tiền tố xưng hô thừa do bot sinh
    raw_with_prefix = "Mê Tech: Chào bạn, bản này hoàn toàn miễn phí nhé!"
    cleaned_prefix = clean_reply(raw_with_prefix)
    assert cleaned_prefix == "Chào bạn, bản này hoàn toàn miễn phí nhé!"

def test_generate_smart_reply_fallback(monkeypatch):
    # Khi offline hoặc không có API key, fallback trả về template an toàn
    reply = generate_smart_reply("Công cụ này dùng thế nào?", "metech", fallback_only=True)
    assert isinstance(reply, str)
    assert len(reply) > 0
