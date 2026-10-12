# Phase 2: Unified Render Engine & Pre-flight Validator

> **Mục tiêu**: Thống nhất giao diện và quy trình dựng video giữa 3 kênh (`me-tech`, `thien-tran`, `tam-an-lac`), giải quyết triệt để việc trùng lặp mã nguồn giữa `me-tech/pipeline/` và `core-video-engine/`, đồng thời cung cấp công cụ kiểm thử trước khi render (`--dry-run` & `--doctor`) để phát hiện lỗi kịch bản, thiếu ảnh hoặc thiếu font trong < 1 giây thay vì phải đợi 2 phút dựng video hỏng.

---

## Kiến Trúc Tổng Thể

```
ops/render/
├── __init__.py
├── config.py           # Định nghĩa engine type và đường dẫn cho từng kênh
├── validator.py        # Soát lỗi kịch bản & assets (motion_deck vs zen_meditation)
├── doctor.py           # Kiểm tra môi trường (ffmpeg, Playwright, fonts, TTS cache)
├── cli.py              # CLI thống nhất: python3 -m ops.render.cli --channel <ch> --slug <slug> [--dry-run]
└── tests/
    ├── __init__.py
    ├── test_validator.py
    ├── test_doctor.py
    └── test_cli.py
```

---

## Danh Sách Task & Kế Hoạch Triển Khai

### Task 1: Render Configuration & Channel Mapping
- **Files**:
  - Create: `ops/render/config.py`
  - Test: `ops/render/tests/test_config.py`
- **Interfaces**:
  - `get_render_config(channel: str, slug: str, root_dir: Optional[str] = None) -> RenderSpec`
  - `me-tech`: engine `motion_deck`, content `me-tech/pipeline/content/{slug}.json`, out `me-tech/render/{slug}.mp4`
  - `thien-tran`: engine `motion_deck`, content `thien-tran/content/{slug}.json`, out `thien-tran/render/{slug}.mp4`
  - `tam-an-lac`: engine `zen_meditation`, content `tam-an-lac/content/{slug}/script.json`, out `tam-an-lac/content/{slug}/video.mp4`
- [x] **Step 1: Viết test cho `ops/render/config.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/render/config.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(render): add channel render configuration mapping`**

---

### Task 2: Pre-flight Content & Asset Validator
- **Files**:
  - Create: `ops/render/validator.py`
  - Test: `ops/render/tests/test_validator.py`
- **Interfaces**:
  - `validate_motion_deck(content_path: str, shots_dir: str) -> Tuple[List[str], List[str], float]` (errors, warnings, est_duration)
    - Soát: hook < 10 từ, mảng `words` == `weights`, mode `shot` phải có ảnh tồn tại trong `shots/` và có `src`, outro hợp lệ, thời lượng ước lượng (32s-38s).
  - `validate_zen_meditation(content_path: str, content_dir: str) -> Tuple[List[str], List[str], float]`
    - Soát: `script.json` có `voice`, `segments`, tồn tại ảnh thiền `img_*.jpg`, thời lượng ước lượng (30s-45s).
- [x] **Step 1: Viết test kiểm tra validator với dữ liệu hợp lệ và không hợp lệ**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/render/validator.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(render): add pre-flight content and asset validator`**

---

### Task 3: Environment Doctor Module
- **Files**:
  - Create: `ops/render/doctor.py`
  - Test: `ops/render/tests/test_doctor.py`
- **Interfaces**:
  - `check_environment() -> Dict[str, Any]`
    - Kiểm tra `ffmpeg` trong PATH
    - Kiểm tra `uv` trong PATH
    - Kiểm tra Python `.venv` có các thư viện cần thiết (`vieneu`, `playwright`, `numpy`, `scipy`)
    - Kiểm tra Font chữ (`BeVietnamPro-Bold.ttf`)
    - Kiểm tra Playwright Chromium cache
- [x] **Step 1: Viết test cho `ops/render/doctor.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/render/doctor.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(render): add environment doctor healthcheck`**

---

### Task 4: Unified Render CLI với Chế độ `--dry-run` & `--doctor`
- **Files**:
  - Create: `ops/render/cli.py`
  - Test: `ops/render/tests/test_cli.py`
- **Interfaces**:
  - Lệnh: `python3 -m ops.render.cli --channel <name> --slug <slug> [--dry-run] [--doctor] [--skip-tts]`
  - Khi `--dry-run`:
    - Chạy validator tương ứng cho channel.
    - Chạy doctor kiểm tra tài nguyên.
    - In bảng báo cáo chi tiết, trả về exit code 0 nếu hợp lệ, exit code 1 nếu có lỗi chặn.
  - Khi render thật:
    - Chạy dry-run kiểm tra trước. Nếu fail, dừng ngay.
    - Kích hoạt engine tương ứng.
- [x] **Step 1: Viết test cho `ops/render/cli.py`**
- [x] **Step 2: Chạy test xác nhận FAIL**
- [x] **Step 3: Triển khai `ops/render/cli.py`**
- [x] **Step 4: Chạy test xác nhận PASS**
- [x] **Step 5: Commit `feat(render): add unified render CLI with dry-run support`**

---

### Task 5: Đồng Bộ `me-tech/pipeline` sang dùng Engine Lõi & Dry-Run Thực Tế 3 Kênh
- **Files**:
  - Cập nhật tương thích ngược: `me-tech/pipeline/run.sh`
  - Chạy dry-run kiểm thử trên:
    - `me-tech`: `quinnipiac-ai-trust-crisis`
    - `thien-tran`: `multi_agent_token_burn_myth`
    - `tam-an-lac`: `038_bua_trua_dau_tuan`
- [x] **Step 1: Cập nhật `run.sh` của `me-tech` để kết nối vào `ops.render.cli`**
- [x] **Step 2: Chạy dry-run thực tế trên 3 kênh**
- [x] **Step 3: Đối soát exit code 0 và báo cáo cho User**
- [x] **Step 4: Commit `feat(render): complete Phase 2 unified render engine`**
