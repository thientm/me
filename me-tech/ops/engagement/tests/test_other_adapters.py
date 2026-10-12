import pytest
from adapters.fb_business import FacebookBusinessAdapter
from adapters.tt_studio import TikTokStudioAdapter

def test_adapter_instantiation():
    fb = FacebookBusinessAdapter(port=9333)
    tt = TikTokStudioAdapter(port=9333)
    assert fb.port == 9333
    assert tt.port == 9333

def test_fb_batch_process_mock():
    fb = FacebookBusinessAdapter(port=9333)
    comments = [
        {"id": "fb1", "author": "Trần Bình", "text": "A Di Đà Phật"},
        {"id": "fb2", "author": "Spammer", "text": "inbox kiếm tiền online zalo"}
    ]
    results = fb.process_comments_batch(comments, channel="tamanlac", dry_run=True)
    assert len(results) == 2
    assert results[0]["action_taken"] == ["like", "reply"]
    assert results[1]["action_taken"] == ["skip_spam"]

def test_tt_batch_process_mock():
    tt = TikTokStudioAdapter(port=9555)
    comments = [
        {"id": "tt1", "author": "Lan Huong", "text": "Kênh hay quá ạ"}
    ]
    results = tt.process_comments_batch(comments, channel="metech", dry_run=True)
    assert len(results) == 1
    assert results[0]["action_taken"] == ["heart", "reply"]
