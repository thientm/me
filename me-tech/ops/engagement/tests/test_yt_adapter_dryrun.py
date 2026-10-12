import pytest
from adapters.base import BaseAdapter
from adapters.yt_studio import YouTubeStudioAdapter, parse_comment_element_mock

def test_base_adapter_initialization():
    base = BaseAdapter(port=9333)
    assert base.port == 9333

def test_yt_parse_comment_element_mock():
    mock_raw = {
        "id": "comment_999",
        "author": "Nguyễn Văn A",
        "text": "Video rất hữu ích!",
        "video_title": "AI Short 2026"
    }
    parsed = parse_comment_element_mock(mock_raw)
    assert parsed["id"] == "comment_999"
    assert parsed["author"] == "Nguyễn Văn A"
    assert parsed["text"] == "Video rất hữu ích!"

def test_yt_studio_adapter_dryrun():
    adapter = YouTubeStudioAdapter(port=9333)
    # Test dry run execution logic with mock comments
    comments = [
        {"id": "c1", "author": "User 1", "text": "Video đỉnh quá ad"},
        {"id": "c2", "author": "User 2", "text": "Đm lừa đảo"}
    ]
    results = adapter.process_comments_batch(comments, channel="metech", dry_run=True)
    assert len(results) == 2
    assert results[0]["action_taken"] == ["heart", "like", "reply"]
    assert results[1]["action_taken"] == ["skip_spam"]
