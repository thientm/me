# Phase 3: Content Brainstorming, Pipeline Orchestrator & Quality Gates

> **Mục tiêu**: Thiết lập bộ điều phối quy trình tự động (`ops.orchestrator`) tích hợp các superpowers (`brainstorming`, `writing-plans`, `verification-before-completion`) cho 3 kênh trong 3 khung giờ (`08:00`, `12:00`, `20:00`), thiết lập 2 trạm kiểm soát chất lượng (**Gate 1: Duyệt kịch bản**, **Gate 2: Duyệt video & pre-publish**) với cờ `--dry-run` kiểm thử toàn diện.

---

## Kiến Trúc Tổng Thể

```
ops/orchestrator/
├── __init__.py
├── slot.py            # Kiểm tra trạng thái khung giờ 08:00, 12:00, 20:00 trên cả 3 kênh
├── brainstorm.py      # Bộ khung sinh gợi ý ý tưởng & kịch bản chuẩn cho từng kênh
├── gates.py           # Quản lý Gate 1 (Kịch bản & Assets) và Gate 2 (Video & Publish Ready)
├── cli.py             # CLI điều phối: python3 -m ops.orchestrator.cli [--slot 08|12|20] [--dry-run]
└── tests/
    ├── __init__.py
    ├── test_slot.py
    ├── test_brainstorm.py
    ├── test_gates.py
    └── test_cli.py
```

---

## Danh Sách Task & Kế Hoạch Triển Khai

### Task 1: Multi-Channel Slot Status Checker
- **Files**:
  - Create: `ops/orchestrator/slot.py`
  - Test: `ops/orchestrator/tests/test_slot.py`
- **Interfaces**:
  - `check_channel_slot(channel: str, slot: int, root_dir: Optional[str] = None) -> Dict[str, Any]`
  - `check_all_slots(slot: Optional[int] = None, root_dir: Optional[str] = None) -> Dict[str, Dict[str, Any]]`
  - Trạng thái: `done` (đủ 3 platform), `partial` (thiếu platform), `none` (chưa có bài).
- [x] **Step 1: Viết test cho `ops/orchestrator/slot.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/orchestrator/slot.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(orchestrator): add multi-channel slot status checker`**

---

### Task 2: Brainstorm Template & Prompt Generator
- **Files**:
  - Create: `ops/orchestrator/brainstorm.py`
  - Test: `ops/orchestrator/tests/test_brainstorm.py`
- **Interfaces**:
  - `get_brainstorm_prompt(channel: str, topic: str) -> str`:
    - `me-tech`: 3 góc khai thác thực tế "AI dễ hiểu", 3 hook <10 từ, phân tích ứng dụng thực tế.
    - `thien-tran`: Tam giác FACT vs INFERENCE vs OPINION, bóc trần Hype vs Substance, hook ≤2.5s, trạm shot chart/benchmark.
    - `tam-an-lac`: Nỗi lòng chạm cảm xúc, liên hệ lời Phật dạy mộc mạc, prompt 3 ảnh tránh trùng `images.json`.
  - `generate_scaffold(channel: str, slug: str, title: str) -> dict`: Sinh khung JSON kịch bản chuẩn.
- [x] **Step 1: Viết test cho `ops/orchestrator/brainstorm.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/orchestrator/brainstorm.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(orchestrator): add channel-specific brainstorm and scaffold generators`**

---

### Task 3: Quality Gates Module (Gate 1 & Gate 2)
- **Files**:
  - Create: `ops/orchestrator/gates.py`
  - Test: `ops/orchestrator/tests/test_gates.py`
- **Interfaces**:
  - `evaluate_gate1(channel: str, slug: str, root_dir: Optional[str] = None) -> GateResult`:
    - Kiểm tra cấu trúc kịch bản, độ dài hook, mảng weights, tồn tại ảnh dẫn nguồn hoặc ảnh thiền qua `ops.render.validator`.
  - `evaluate_gate2(channel: str, slug: str, platform: str = "all", root_dir: Optional[str] = None) -> GateResult`:
    - Kiểm tra video mp4 đã render xong, kiểm tra độ dài tiêu đề/caption qua `ops.publish.cli`.
- [x] **Step 1: Viết test cho `ops/orchestrator/gates.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/orchestrator/gates.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(orchestrator): add quality gates verification module`**

---

### Task 4: Unified Orchestrator CLI với Chế độ `--dry-run`
- **Files**:
  - Create: `ops/orchestrator/cli.py`
  - Test: `ops/orchestrator/tests/test_cli.py`
- **Interfaces**:
  - Lệnh: `python3 -m ops.orchestrator.cli [--slot 08|12|20] [--channel <name>] [--dry-run]`
  - Xuất bảng điều phối tổng thể 3 kênh: Trạng thái slot, Gate 1, Gate 2, và cảnh báo cần hành động.
- [x] **Step 1: Viết test cho `ops/orchestrator/cli.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/orchestrator/cli.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(orchestrator): add unified orchestrator CLI with dry-run support`**

---

### Task 5: Dry-Run Verification Thực Tế & Báo Cáo
- **Files**:
  - Chạy dry-run kiểm thử trên cả 3 kênh cho slot hiện tại.
  - Cập nhật tài liệu và báo cáo kết quả cho người dùng.
- [x] **Step 1: Chạy dry-run kiểm thử thực tế trên 3 kênh**
- [x] **Step 2: Đối soát exit code 0**
- [x] **Step 3: Lập báo cáo chi tiết và đề xuất commit chốt Phase 3**
