# Auto Engagement Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng hệ thống tự động hoá thả tim, like và trả lời bình luận (Auto Reaction & Reply) đa nền tảng (YouTube, TikTok, Facebook) cho Mê Tech và Tâm An Lạc qua giao thức Chrome CDP.

**Architecture:** Kiến trúc module hoá gồm Bộ điều phối (Runner/Lock checker), Sổ lưu trạng thái (Ledger chống trùng), Bộ não xử lý (Rule filter + Template rotation + LLM fallback), và các Adapters Playwright CDP tương tác nền tảng (Studio Inboxes).

**Tech Stack:** Python 3.11+, Playwright (CDP connection), pytest, Gemini API / agy subprocess.

**Spec:** `docs/superpowers/specs/2026-10-12-auto-engagement-bot-design.md`

## Global Constraints
- Chrome CDP ports: 9333 (Mê Tech & FB quản trị), 9555 (Tâm An Lạc).
- Chạy nền tuyệt đối (`quiet mode`), không pop-up cướp chuột người dùng.
- Tự động dừng/hoãn nếu tồn tại `.run/build.lock` hoặc `fb9333.lock`.
- Giới hạn tốc độ: Tối đa 5–8 reply và 15–20 like/lần chạy; delay ngẫu nhiên 4–10s giữa các thao tác.
- TDD: Mọi module logic độc lập đều có test với mock dữ liệu trước khi ghép vào CDP adapter.

## Review Focus
1. Bình luận bị xử lý trùng lặp do lỗi ghi đĩa ledger -> Kiểm tra lock file và đọc ghi atomic JSON.
2. Xung đột lock với pipeline dựng/đăng video làm rớt session -> Kiểm tra lock trước khi mở context CDP.
3. Kẹt popup / dialog trên giao diện Studio -> Đặt timeout 8–10s cho mọi selector.
4. AI sinh câu trả lời quá dài (>40 từ) hoặc văn mẫu PR -> Guardrail cắt gọn và format chuẩn persona.
5. Kênh sai nhận diện (nhầm kênh Mê Tech sang giọng Tâm An Lạc) -> Strict mapping channel-persona qua Enum/config.

---

### Task 1: Sổ theo dõi tương tác (Engagement Ledger) & Lock Checker

**Files:**
- Create: `me-tech/ops/engagement/ledger.py`
- Create: `me-tech/ops/engagement/lock.py`
- Test: `me-tech/ops/engagement/tests/test_ledger_and_lock.py`

**Interfaces:**
- Produces:
  - `class EngagementLedger`:
    - `has(comment_id: str) -> bool`
    - `record(comment_id: str, author: str, actions: list[str], reply_text: str = "") -> None`
    - `save() -> None`
  - `check_conflicts(lock_paths: list[str]) -> bool`
  - `class EngagementLock`:
    - `acquire() -> bool`
    - `release() -> None`

- [ ] **Step 1: Viết test cho Ledger và Lock**

```python
# me-tech/ops/engagement/tests/test_ledger_and_lock.py
from me-tech.ops.engagement.ledger import EngagementLedger
from me-tech.ops.engagement.lock import check_conflicts, EngagementLock

def test_ledger_record_and_has(tmp_path):
    ledger_file = tmp_path / "ledger.json"
    ledger = EngagementLedger(str(ledger_file))
    assert not ledger.has("yt:123")
    ledger.record("yt:123", "User A", ["heart", "like"], "Thanks!")
    ledger.save()
    
    # Reload
    new_ledger = EngagementLedger(str(ledger_file))
    assert new_ledger.has("yt:123")

def test_lock_conflict_detection(tmp_path):
    build_lock = tmp_path / "build.lock"
    build_lock.touch()
    assert check_conflicts([str(build_lock)]) is True
```

- [ ] **Step 2: Chạy test để xác nhận FAIL**

Run: `pytest me-tech/ops/engagement/tests/test_ledger_and_lock.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Cài đặt `EngagementLedger` và `EngagementLock`**

Tạo `me-tech/ops/engagement/ledger.py` và `me-tech/ops/engagement/lock.py` hỗ trợ atomic file write và kiểm tra `.run/*.lock`.

- [ ] **Step 4: Chạy lại test để xác nhận PASS**

Run: `pytest me-tech/ops/engagement/tests/test_ledger_and_lock.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add me-tech/ops/engagement/ledger.py me-tech/ops/engagement/lock.py me-tech/ops/engagement/tests/test_ledger_and_lock.py
git commit -m "feat(engagement): add ledger and lock safety modules"
```

---

### Task 2: Rule Filter & Template Rotation (Brain)

**Files:**
- Create: `me-tech/ops/engagement/brain/filter.py`
- Create: `me-tech/ops/engagement/brain/templates.py`
- Test: `me-tech/ops/engagement/tests/test_brain_rules.py`

**Interfaces:**
- Produces:
  - `classify_comment(text: str, channel: str) -> str` (Trả về: "spam", "greeting", "question", "neutral")
  - `get_template_reply(channel: str, category: str, author: str = "") -> str`

- [ ] **Step 1: Viết test cho Rule Filter & Template**

```python
# me-tech/ops/engagement/tests/test_brain_rules.py
from me-tech.ops.engagement.brain.filter import classify_comment
from me-tech.ops.engagement.brain.templates import get_template_reply

def test_classify_spam():
    assert classify_comment("Inbox zalo 098xxx nhận quà", "metech") == "spam"
    assert classify_comment("Đm lừa đảo", "tamanlac") == "spam"

def test_classify_greeting():
    assert classify_comment("A Di Đà Phật", "tamanlac") == "greeting"
    assert classify_comment("Video hay quá ad ơi", "metech") == "greeting"

def test_template_rotation_differs():
    t1 = get_template_reply("tamanlac", "greeting")
    t2 = get_template_reply("tamanlac", "greeting")
    assert isinstance(t1, str) and len(t1) > 0
```

- [ ] **Step 2: Chạy test để xác nhận FAIL**

Run: `pytest me-tech/ops/engagement/tests/test_brain_rules.py -v`
Expected: FAIL

- [ ] **Step 3: Cài đặt `filter.py` và `templates.py`**

Triển khai regex và keyword sets cho lọc spam/toxic; xây dựng danh mục template phong phú cho Mê Tech & Tâm An Lạc.

- [ ] **Step 4: Chạy test để xác nhận PASS**

Run: `pytest me-tech/ops/engagement/tests/test_brain_rules.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add me-tech/ops/engagement/brain/filter.py me-tech/ops/engagement/brain/templates.py me-tech/ops/engagement/tests/test_brain_rules.py
git commit -m "feat(engagement): add rule filter and template rotation"
```

---

### Task 3: Persona Prompts & LLM Generation

**Files:**
- Create: `me-tech/ops/engagement/brain/personas.py`
- Create: `me-tech/ops/engagement/brain/llm_reply.py`
- Test: `me-tech/ops/engagement/tests/test_llm_reply.py`

**Interfaces:**
- Produces:
  - `generate_smart_reply(comment_text: str, channel: str, video_title: str = "") -> str`

- [ ] **Step 1: Viết test với Mock LLM**

```python
# me-tech/ops/engagement/tests/test_llm_reply.py
from me-tech.ops.engagement.brain.llm_reply import format_prompt, clean_reply

def test_prompt_formatting():
    prompt = format_prompt("Tool này free không?", "metech", "Top 5 AI 2026")
    assert "Mê Tech" in prompt
    assert "tối đa 40 từ" in prompt

def test_clean_reply_guardrail():
    raw = ' "Chào bạn! Tool này có gói miễn phí nhé. Hãy thử ngay! " '
    cleaned = clean_reply(raw)
    assert cleaned == "Chào bạn! Tool này có gói miễn phí nhé. Hãy thử ngay!"
```

- [ ] **Step 2: Chạy test để xác nhận FAIL**

Run: `pytest me-tech/ops/engagement/tests/test_llm_reply.py -v`
Expected: FAIL

- [ ] **Step 3: Cài đặt `personas.py` và `llm_reply.py`**

Tích hợp gọi LLM qua Gemini API hoặc agy command với cơ chế fallback nếu offline.

- [ ] **Step 4: Chạy test để xác nhận PASS**

Run: `pytest me-tech/ops/engagement/tests/test_llm_reply.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add me-tech/ops/engagement/brain/personas.py me-tech/ops/engagement/brain/llm_reply.py me-tech/ops/engagement/tests/test_llm_reply.py
git commit -m "feat(engagement): add persona definitions and llm reply generator"
```

---

### Task 4: Base Adapter & YouTube Studio Adapter (`yt_studio.py`)

**Files:**
- Create: `me-tech/ops/engagement/adapters/base.py`
- Create: `me-tech/ops/engagement/adapters/yt_studio.py`
- Test: `me-tech/ops/engagement/tests/test_yt_adapter_dryrun.py`

**Interfaces:**
- Produces:
  - `class BaseAdapter`:
    - `connect_cdp(port: int)`
    - `random_delay(min_s: float, max_s: float)`
  - `class YouTubeStudioAdapter(BaseAdapter)`:
    - `scan_and_engage(channel_id: str, dry_run: bool = False, limit_replies: int = 5) -> dict`

- [ ] **Step 1: Viết test cho cấu trúc Adapter & parse comment card**

```python
# me-tech/ops/engagement/tests/test_yt_adapter_dryrun.py
from me-tech.ops.engagement.adapters.yt_studio import parse_comment_element_mock

def test_parse_comment():
    mock_data = {"id": "c1", "author": "Nam", "text": "Clip hay quá"}
    res = parse_comment_element_mock(mock_data)
    assert res["id"] == "c1"
```

- [ ] **Step 2: Chạy test để xác nhận FAIL**

Run: `pytest me-tech/ops/engagement/tests/test_yt_adapter_dryrun.py -v`
Expected: FAIL

- [ ] **Step 3: Cài đặt `base.py` và `yt_studio.py`**

Kết nối CDP Playwright, điều hướng tới `studio.youtube.com/channel/<ID>/comments/inbox`, tương tác Creator Heart, Like và Reply.

- [ ] **Step 4: Chạy test để xác nhận PASS**

Run: `pytest me-tech/ops/engagement/tests/test_yt_adapter_dryrun.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add me-tech/ops/engagement/adapters/base.py me-tech/ops/engagement/adapters/yt_studio.py me-tech/ops/engagement/tests/test_yt_adapter_dryrun.py
git commit -m "feat(engagement): add base adapter and youtube studio adapter"
```

---

### Task 5: Facebook Business Suite & TikTok Studio Adapters

**Files:**
- Create: `me-tech/ops/engagement/adapters/fb_business.py`
- Create: `me-tech/ops/engagement/adapters/tt_studio.py`
- Test: `me-tech/ops/engagement/tests/test_other_adapters.py`

**Interfaces:**
- Produces:
  - `class FacebookBusinessAdapter(BaseAdapter)`:
    - `scan_and_engage(asset_id: str, dry_run: bool = False, limit_replies: int = 5) -> dict`
  - `class TikTokStudioAdapter(BaseAdapter)`:
    - `scan_and_engage(dry_run: bool = False, limit_replies: int = 5) -> dict`

- [ ] **Step 1: Viết test mock cho FB & TikTok**

```python
# me-tech/ops/engagement/tests/test_other_adapters.py
from me-tech.ops.engagement.adapters.fb_business import FacebookBusinessAdapter
from me-tech.ops.engagement.adapters.tt_studio import TikTokStudioAdapter

def test_adapter_instantiation():
    fb = FacebookBusinessAdapter(port=9333)
    tt = TikTokStudioAdapter(port=9333)
    assert fb.port == 9333
    assert tt.port == 9333
```

- [ ] **Step 2: Chạy test để xác nhận FAIL**

Run: `pytest me-tech/ops/engagement/tests/test_other_adapters.py -v`
Expected: FAIL

- [ ] **Step 3: Cài đặt `fb_business.py` và `tt_studio.py`**

Xử lý selector trên Meta Business Suite Inbox (`fb_comments`) và TikTok Studio (`tiktokstudio/comment`).

- [ ] **Step 4: Chạy test để xác nhận PASS**

Run: `pytest me-tech/ops/engagement/tests/test_other_adapters.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add me-tech/ops/engagement/adapters/fb_business.py me-tech/ops/engagement/adapters/tt_studio.py me-tech/ops/engagement/tests/test_other_adapters.py
git commit -m "feat(engagement): add facebook business and tiktok studio adapters"
```

---

### Task 6: CLI Runner & Chế độ Dry-Run

**Files:**
- Create: `me-tech/ops/engagement/runner.py`
- Test: `me-tech/ops/engagement/tests/test_runner_cli.py`

**Interfaces:**
- Produces:
  - CLI: `python3 -m me-tech.ops.engagement.runner [--channel metech|tamanlac] [--dry-run]`

- [ ] **Step 1: Viết test cho CLI arguments và routing**

```python
# me-tech/ops/engagement/tests/test_runner_cli.py
from me-tech.ops.engagement.runner import parse_args

def test_runner_args():
    args = parse_args(["--channel", "metech", "--dry-run", "--limit", "3"])
    assert args.channel == "metech"
    assert args.dry_run is True
    assert args.limit == 3
```

- [ ] **Step 2: Chạy test để xác nhận FAIL**

Run: `pytest me-tech/ops/engagement/tests/test_runner_cli.py -v`
Expected: FAIL

- [ ] **Step 3: Cài đặt `runner.py`**

Tập hợp kiểm tra lock, khởi tạo ledger, kết nối CDP theo cấu hình kênh, gọi adapters tương ứng, ghi log kết quả.

- [ ] **Step 4: Chạy test để xác nhận PASS**

Run: `pytest me-tech/ops/engagement/tests/test_runner_cli.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add me-tech/ops/engagement/runner.py me-tech/ops/engagement/tests/test_runner_cli.py
git commit -m "feat(engagement): add cli runner with dry-run support"
```

---

### Task 7: Thiết lập Lịch trình Tự động (Launchd / Cron Schedule)

**Files:**
- Create: `me-tech/ops/engagement/cron_schedule.sh`
- Create: `me-tech/ops/engagement/com.me.engagement.plist`
- Test: Chạy thử trực tiếp `cron_schedule.sh --dry-run`

- [ ] **Step 1: Tạo script wrapper `cron_schedule.sh`**

Chạy lần lượt cho Mê Tech và Tâm An Lạc, ghi log vào `~/Library/Logs/engagement_bot.log`.

- [ ] **Step 2: Tạo launchd plist chạy vào các khung giờ vàng**

Lịch: 08:30, 12:30, 16:30, 20:30 hàng ngày.

- [ ] **Step 3: Chạy thử nghiệm thực tế script với cờ `--dry-run`**

Run: `bash me-tech/ops/engagement/cron_schedule.sh --dry-run`
Expected: Thoát mã 0, log ghi nhận quét thành công và in ra các bình luận mẫu được chọn reply.

- [ ] **Step 4: Commit**

```bash
git add me-tech/ops/engagement/cron_schedule.sh me-tech/ops/engagement/com.me.engagement.plist
git commit -m "feat(engagement): add launchd service and cron automation scripts"
```
