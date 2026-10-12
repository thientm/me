import os
import shutil
import glob
from typing import Dict, Any, List

def check_environment() -> Dict[str, Any]:
    """Check system requirements for video rendering:
    - ffmpeg
    - uv
    - Font BeVietnamPro-Bold
    - Chromium
    - Pipeline python environment
    """
    checks: Dict[str, bool] = {}
    issues: List[str] = []

    # 1. ffmpeg
    has_ffmpeg = shutil.which("ffmpeg") is not None
    checks["ffmpeg"] = has_ffmpeg
    if not has_ffmpeg:
        issues.append("Thiếu công cụ 'ffmpeg' trong PATH (cài đặt: brew install ffmpeg)")

    # 2. uv
    has_uv = shutil.which("uv") is not None
    checks["uv"] = has_uv
    if not has_uv:
        issues.append("Thiếu công cụ 'uv' trong PATH (cài đặt: brew install uv)")

    # 3. Font BeVietnamPro-Bold
    home = os.path.expanduser("~")
    font_path = os.path.join(home, "Library", "Fonts", "BeVietnamPro-Bold.ttf")
    has_font = os.path.exists(font_path)
    checks["font"] = has_font
    if not has_font:
        issues.append(f"Chưa cài font 'Be Vietnam Pro Bold' tại: {font_path}")

    # 4. Playwright Chromium
    chrome_dir = os.path.join(home, "Library", "Caches", "ms-playwright")
    chrome_matches = glob.glob(os.path.join(chrome_dir, "chromium*")) if os.path.exists(chrome_dir) else []
    has_chrome = len(chrome_matches) > 0 or os.path.exists(chrome_dir)
    checks["chromium"] = has_chrome
    if not has_chrome:
        issues.append("Playwright Chromium chưa được tải vào cache ms-playwright")

    # 5. Virtualenv python
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    venv_py = os.path.join(repo_root, "me-tech", "pipeline", ".venv", "bin", "python")
    has_venv = os.path.exists(venv_py)
    checks["venv"] = has_venv
    if not has_venv:
        issues.append(f"Không tìm thấy Python .venv chuẩn tại: {venv_py}")

    ok = len(issues) == 0

    return {
        "ok": ok,
        "checks": checks,
        "issues": issues
    }
