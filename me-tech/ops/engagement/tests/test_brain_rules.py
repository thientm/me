import pytest
from brain.filter import classify_comment
from brain.templates import get_template_reply

def test_classify_spam():
    assert classify_comment("Inbox zalo 098xxx nhận quà ngay", "metech") == "spam"
    assert classify_comment("Đm lừa đảo", "tamanlac") == "spam"
    assert classify_comment("Tham gia nhóm tele kiếm tiền https://t.me/abc", "metech") == "spam"

def test_classify_greeting_tamanlac():
    assert classify_comment("A Di Đà Phật", "tamanlac") == "greeting"
    assert classify_comment("Nam mô Bồ Tát Quán Thế Âm", "tamanlac") == "greeting"
    assert classify_comment("Cầu chúc gia đình luôn bình an", "tamanlac") == "greeting"

def test_classify_greeting_metech():
    assert classify_comment("Video hay quá ad ơi!", "metech") == "greeting"
    assert classify_comment("Tuyệt vời quá kênh ơi 🔥", "metech") == "greeting"
    assert classify_comment("Hóng các video tiếp theo", "metech") == "greeting"

def test_classify_question():
    assert classify_comment("Công cụ này có dùng miễn phí được không bạn?", "metech") == "question"
    assert classify_comment("Làm sao cài được trên Mac vậy ad?", "metech") == "question"
    assert classify_comment("Làm thế nào để tâm bớt sân si ạ?", "tamanlac") == "question"

def test_template_rotation_differs():
    t1 = get_template_reply("tamanlac", "greeting")
    t2 = get_template_reply("tamanlac", "greeting")
    assert isinstance(t1, str) and len(t1) > 0
    assert isinstance(t2, str) and len(t2) > 0

    m1 = get_template_reply("metech", "greeting")
    assert isinstance(m1, str) and len(m1) > 0
