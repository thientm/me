"""Nối tới Chrome hồ sơ Mê Tech đang chạy sẵn ở cổng 9333.

LUẬT CỨNG — đọc trước khi sửa file này:

  Chỉ được `connect_over_cdp` vào một Chrome ĐÃ chạy sẵn.
  TUYỆT ĐỐI không `launch_persistent_context` lên ~/.me-tech-browser,
  và không `pkill` nó.

Ngày 19.09.2026 đã mất sạch phiên đăng nhập cả ba nền tảng vì phạm luật này.
Bằng chứng: bảng cookie chỉ còn 15 dòng (hồ sơ Chrome thường của Thiện có ~1,2 MB),
tức là các dòng bị XOÁ chứ không phải không giải mã được. Cùng buổi sáng đó có hai
lần `launch_persistent_context` lên đúng thư mục này (một lần còn giả lập iPhone) và
một lần `pkill`; Chrome ghi lại `exit_type: Crashed`. Hôm trước không hề khởi động
lại hồ sơ — chỉ nối CDP — nên không mất gì.

Muốn đo giao diện di động thì tạo hồ sơ vứt đi riêng, đừng đụng hồ sơ này.
"""
import sys
import urllib.request
from playwright.sync_api import sync_playwright

PORT = 9333
PROFILE = "~/.me-tech-browser"

LAUNCH = (
    '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" '
    f'--user-data-dir="$HOME/.me-tech-browser" --remote-debugging-port={PORT} '
    '--no-first-run --no-default-browser-check &'
)


def alive():
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
        return True
    except Exception:
        return False


def connect():
    if not alive():
        sys.exit(
            f"❌ Chrome hồ sơ Mê Tech chưa chạy ở cổng {PORT}.\n"
            f"   Mở bằng tay rồi chạy lại:\n\n   {LAUNCH}\n\n"
            "   ĐỪNG để script tự mở — tự mở bằng Playwright là mất phiên đăng nhập."
        )
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    return pw, b, b.contexts[0]


def require_login(ctx, which):
    """Kiểm tra đăng nhập TRƯỚC khi upload, để hỏng thì hỏng sớm và nói rõ lý do."""
    probe = {
        "youtube": ("https://studio.youtube.com/", "accounts.google.com"),
        "facebook": ("https://business.facebook.com/latest/home", "loginpage"),
        "tiktok": ("https://www.tiktok.com/tiktokstudio/upload", "/login"),
    }[which]
    p = ctx.new_page()
    p.goto(probe[0], wait_until="domcontentloaded", timeout=60000)
    p.wait_for_timeout(6000)
    if probe[1] in p.url:
        sys.exit(f"❌ {which}: hồ sơ chưa đăng nhập. Đăng nhập trong cửa sổ Chrome rồi chạy lại.")
    print(f"✅ {which}: còn đăng nhập")
    return p


def quit_browser():
    """Đóng SẠCH. Không bao giờ pkill."""
    import subprocess
    subprocess.run(["osascript", "-e", 'quit app "Google Chrome"'], check=False)
