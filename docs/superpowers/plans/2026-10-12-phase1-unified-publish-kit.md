# Phase 1: Unified Publish Kit & Meta Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thống nhất quy trình đọc metadata (`meta.json`) và lõi xuất bản dùng chung cho cả 3 kênh (`me-tech`, `thien-tran`, `tam-an-lac`), loại bỏ hoàn toàn việc sinh file rác `meta_<slug>.py`, bổ sung chế độ `--dry-run` kiểm thử an toàn trước khi bấm đăng thật.

**Architecture:** 
Xây dựng module lõi `ops/publish/` (hoặc `core-publish/`) tập trung hoá việc nạp metadata từ file tĩnh `meta.json` trong thư mục `content/<slug>/`. Giữ tương thích ngược 100% với cấu trúc `meta.py` hiện tại ở cả 3 kênh. Cung cấp CLI `publish.py` hỗ trợ `--channel`, `--slug`, `--platform`, `--at`, `--dry-run`.

**Tech Stack:** Python 3.10+, Playwright (CDP connection), unittest.

**Spec:** Kế hoạch quy hoạch Phase 1 được chốt từ phiên Brainstorming ngày 12/10/2026.

---

## Global Constraints
- **Preserve CDP Sessions:** Tuyệt đối không gọi `launch_persistent_context` hay `pkill Chrome`. Chỉ kết nối qua `connect_over_cdp` tới các cổng đã mở (`9333`, `9444`, `9555`).
- **Backward Compatibility:** Các script hiện tại (`yt.py`, `tt.py`, `fb.py`, `fb_profile.py`) khi `from meta import VIDEO, YT_TITLE, ...` phải tiếp tục chạy trơn tru mà không cần sửa đổi logic nội bộ.
- **Append-Only Logs:** Không sửa đổi lịch sử các file `logs/*.md`.

## Review Focus
1. Xử lý trường hợp bài chỉ có `meta.json` mà không có `meta_<slug>.py`.
2. Xử lý trường hợp fallback ngược lại bài cũ chỉ có `meta_<slug>.py`.
3. Kiểm tra tính hợp lệ của đường dẫn `VIDEO` (tồn tại file mp4 thật trên đĩa, dung lượng > 0).
4. Độ dài metadata: YT_TITLE <= 100 ký tự (không emoji), TT_CAPTION <= 150 ký tự, FB_CAPTION đầy đủ.
5. Chế độ `--dry-run`: kết nối CDP, mở tab kiểm tra login & kênh đúng mà KHÔNG upload hay bấm nút Post.

---

### Task 1: Module MetaLoader hỗ trợ chuẩn `meta.json` và Backward Compatibility

**Files:**
- Create: `ops/publish/meta_loader.py`
- Test: `ops/publish/tests/test_meta_loader.py`

**Interfaces:**
- Produces: `load_meta(channel: str, slug: str, content_dir: str = None) -> MetaData`
  ```python
  @dataclass
  class MetaData:
      video_path: str
      yt_title: str
      yt_desc: str
      fb_caption: str
      tt_caption: str
      slug: str
      channel: str
  ```

- [x] **Step 1: Viết test kiểm tra nạp `meta.json` và fallback `meta_<slug>.py`**
- [x] **Step 2: Chạy test để xác nhận test FAIL (chưa có code)**
- [x] **Step 3: Triển khai `MetaLoader` trong `ops/publish/meta_loader.py`**
- [x] **Step 4: Chạy test để xác nhận PASS 100%**
- [x] **Step 5: Commit `feat(publish): add unified MetaLoader supporting meta.json and legacy fallback`**

---

### Task 2: Cấu hình Kênh Tập Trung (`channels.json`)

**Files:**
- Create: `ops/publish/channels.json`
- Create: `ops/publish/config.py`
- Test: `ops/publish/tests/test_config.py`

**Interfaces:**
- Produces: `get_channel_config(channel: str) -> ChannelConfig`
  - `cdp_port`: 9333, 9444, 9555
  - `fb_cdp_port`: 9333 (dùng chung cho Facebook)
  - `yt_channel_id`: `UCnElgDX9q_AYGdFc2oDuWUA`, `UCvoMD_dBm8z1i-Zd8Pwu7mQ`, `UCjEteQMJ4zzFV9_iKvChpvA`
  - `tt_username`: `me-tech`, `thientranx`, `tamanlac.tiktok`
  - `fb_type`: `page_business_suite` (Mê Tech, Tâm An Lạc) hoặc `personal_profile` (Thiện Trần)
  - `fb_asset_id`: Mê Tech Page id, Tâm An Lạc Page id

- [x] **Step 1: Viết test kiểm tra cấu hình 3 kênh**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Tạo `channels.json` và `config.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(publish): add centralized channel configuration`**

---

### Task 3: Nâng cấp `meta.py` tại 3 Kênh để chuyển sang dùng `MetaLoader`

**Files:**
- Modify: `me-tech/pipeline/publish/meta.py`
- Modify: `thien-tran/_pubkit/a/publish/meta.py`
- Modify: `tam-an-lac/_pubkit/a/publish/meta.py`
- Test: `ops/publish/tests/test_compat_meta.py`

**Interfaces:**
- Giữ nguyên các biến module xuất khẩu: `VIDEO`, `YT_TITLE`, `YT_DESC`, `FB_CAPTION`, `TT_CAPTION`, `SLUG`.
- Tự động ưu tiên đọc `content/<slug>/meta.json` trước; nếu không có thì đọc `meta_<slug>.py`.

- [x] **Step 1: Viết test đối soát với các bài hiện hành (đảm bảo output khớp 100% với biến cũ)**
- [x] **Step 2: Cập nhật `meta.py` của `me-tech`, `thien-tran`, `tam-an-lac`**
- [x] **Step 3: Chạy test đối soát xác nhận PASS**
- [x] **Step 4: Commit `refactor(publish): upgrade meta.py across 3 channels to use MetaLoader`**

---

### Task 4: Unified Publisher CLI với Chế độ `--dry-run`

**Files:**
- Create: `ops/publish/cli.py`
- Test: `ops/publish/tests/test_cli.py`

**Interfaces:**
- Lệnh: `python3 -m ops.publish.cli --channel <name> --slug <slug> [--platform all|yt|tt|fb] [--at HH:MM] [--dry-run]`
- Chế độ `--dry-run`:
  1. Kiểm tra tồn tại video mp4.
  2. Đo độ dài tiêu đề & caption theo chuẩn từng nền tảng.
  3. Kiểm tra kết nối tới Chrome CDP port tương ứng.
  4. Quét trạng thái kênh (`whois` / channel verification) để chắc chắn đang kết nối đúng tài khoản.
  5. Báo cáo kết quả sẵn sàng mà KHÔNG thực hiện thao tác upload file hay bấm submit.

- [x] **Step 1: Viết unit tests cho CLI và dry-run flag**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/publish/cli.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(publish): add unified publisher CLI with dry-run support`**

---

### Task 5: Dry-Run Verification Thực Tế & Báo Cáo

**Files:**
- Verify các bài gần nhất:
  - Mê Tech: `quinnipiac-ai-trust-crisis`
  - Thiện Trần: `multi_agent_token_burn_myth`
  - Tâm An Lạc: `038_bua_trua_dau_tuan`

- [x] **Step 1: Tạo mẫu `meta.json` cho cả 3 bài thử nghiệm**
- [x] **Step 2: Chạy Dry-Run CLI trên cả 3 kênh với cờ `--dry-run`**
- [x] **Step 3: Đối soát output và xác nhận exit code 0**
- [x] **Step 4: Lập báo cáo kết quả chi tiết cho User và đề xuất commit chốt Phase 1**
