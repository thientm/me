import os
import json
import glob
import re
import datetime as dt
from typing import List, Tuple, Optional

MODES = {"say", "data", "step", "shot", "flow", "outro"}
SEC_PER_SYL = 0.268

def validate_motion_deck(content_path: str, shots_dir: Optional[str] = None) -> Tuple[List[str], List[str], float]:
    """Validate content file and assets for motion deck engine (me-tech, thien-tran).
    Returns: (errors, warnings, estimated_duration)
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(content_path):
        return [f"Content file not found: {content_path}"], [], 0.0

    try:
        with open(content_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON format in {content_path}: {e}"], [], 0.0

    # Kiểm tra các trường bắt buộc cấp gốc
    for key in ("slug", "brand", "kicker", "date", "outro"):
        if key not in data:
            errors.append(f"Thiếu khoá gốc '{key}'")

    segs = data.get("segments", [])
    if not segs:
        errors.append("Không có phân đoạn ('segments') nào")
        return errors, warnings, 0.0

    # Kiểm tra trùng lặp ID phân đoạn
    ids = [s.get("id") for s in segs if "id" in s]
    if len(set(ids)) != len(ids):
        errors.append("ID phân đoạn bị trùng lặp")

    total_syl = 0

    for i, s in enumerate(segs):
        tag = f"Phân đoạn [{i}] {s.get('id', '?')}"
        mode = s.get("mode")

        if mode not in MODES:
            errors.append(f"{tag}: mode '{mode}' không hợp lệ (phải thuộc {MODES})")

        words = s.get("words", [])
        weights = s.get("weights")

        if weights is not None and len(words) != len(weights):
            errors.append(f"{tag}: số lượng words ({len(words)}) ≠ weights ({len(weights)})")

        if mode != "outro":
            if not s.get("say", "").strip():
                errors.append(f"{tag}: thiếu nội dung thoại 'say'")
            total_syl += sum(weights) if weights else len(words)

        if mode == "shot":
            shot_file = s.get("shot")
            if not shot_file:
                errors.append(f"{tag}: mode 'shot' nhưng không khai báo 'shot' (tên file ảnh)")
            elif shots_dir:
                shot_path = os.path.join(shots_dir, shot_file)
                if not os.path.exists(shot_path):
                    errors.append(f"{tag}: Không tìm thấy file ảnh dẫn nguồn: {shot_file}")
            
            if not s.get("src"):
                errors.append(f"{tag}: mode 'shot' có ảnh nhưng thiếu 'src' (nguồn trích dẫn)")

    # Kiểm tra câu đầu (Hook)
    first_seg = segs[0]
    first_words = first_seg.get("words", [])
    if len(first_words) > 10:
        warnings.append(f"Hook mở đầu hơi dài ({len(first_words)} từ > khuyến nghị ≤10 từ)")

    # Kiểm tra câu cuối
    if segs[-1].get("mode") != "outro":
        errors.append("Phân đoạn cuối cùng bắt buộc phải là mode 'outro'")

    est_duration = round(total_syl * SEC_PER_SYL + 2.5, 2)
    if not (30.0 <= est_duration <= 45.0):
        warnings.append(f"Thời lượng ước tính ({est_duration}s) nằm ngoài chuẩn tối ưu (32–38s)")

    return errors, warnings, est_duration

def validate_zen_meditation(content_path: str, content_dir: Optional[str] = None) -> Tuple[List[str], List[str], float]:
    """Validate content file and assets for zen meditation engine (tam-an-lac).
    Returns: (errors, warnings, estimated_duration)
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(content_path):
        return [f"Script file not found: {content_path}"], [], 0.0

    try:
        with open(content_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON format in {content_path}: {e}"], [], 0.0

    for key in ("slug", "voice", "segments"):
        if key not in data:
            errors.append(f"Thiếu khoá gốc '{key}'")

    segs = data.get("segments", [])
    if not segs:
        errors.append("Không có phân đoạn ('segments') nào")
        return errors, warnings, 0.0

    total_words = 0
    for i, s in enumerate(segs):
        tag = f"Phân đoạn [{i}] {s.get('id', '?')}"
        text = s.get("text", "")
        if not text.strip():
            errors.append(f"{tag}: nội dung text trống")
        total_words += len(text.split())

    # Kiểm tra hình ảnh minh họa trong thư mục content_dir
    c_dir = content_dir or os.path.dirname(content_path)
    if os.path.exists(c_dir):
        images = [f for f in os.listdir(c_dir) if f.lower().endswith((".jpg", ".jpeg", ".png")) and f.startswith("img_")]
        if not images:
            errors.append(f"Thiếu hình ảnh minh hoạ (img_*.jpg) trong thư mục {c_dir}")
    else:
        errors.append(f"Thư mục nội dung không tồn tại: {c_dir}")

    lead_in = data.get("lead_in", 0.5)
    gap = data.get("gap", 0.55)
    tail = data.get("tail", 2.8)
    est_duration = round(lead_in + total_words * 0.28 + gap * max(0, len(segs) - 1) + tail, 2)

    if not (28.0 <= est_duration <= 50.0):
        warnings.append(f"Thời lượng ước tính ({est_duration}s) nằm ngoài khoảng lý tưởng (30–45s)")

    # Kiểm tra chống trùng lặp câu mở đầu (Anti-monotony Hook & Keyword Check)
    first_seg_text = segs[0].get("text", "").strip() if segs else ""
    if first_seg_text:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        now_month = dt.datetime.now().strftime("%Y-%m")
        log_path = os.path.join(root_dir, "tam-an-lac", "logs", f"{now_month}.md")
        if os.path.exists(log_path):
            try:
                with open(log_path, "r", encoding="utf-8") as lf:
                    log_content = lf.read()
                recent_hooks = re.findall(r'Mở:\s*["“]([^"”]+)["”]', log_content)
                if recent_hooks:
                    last_3 = recent_hooks[-3:]
                    first_words = first_seg_text.split()[:2]
                    prefix = " ".join(first_words).lower()
                    for prev_hook in last_3:
                        prev_prefix = " ".join(prev_hook.split()[:2]).lower()
                        if prefix == prev_prefix and len(prefix) > 4:
                            warnings.append(
                                f"Trùng lặp cấu trúc mở đầu: '{prefix}' đã xuất hiện ở bài gần nhất ('{prev_hook}'). "
                                f"Bắt buộc đổi mới theo quy tắc Hook Diversity trong tam-an-lac/AGENTS.md."
                            )
                            break
            except Exception:
                pass

    return errors, warnings, est_duration
