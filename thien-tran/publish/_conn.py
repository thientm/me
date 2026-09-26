"""Nối tới Chrome hồ sơ Thiện Trần đang chạy sẵn ở cổng 9444.

LUẬT CỨNG:
  Chỉ được `connect_over_cdp` vào Chrome ĐÃ chạy sẵn qua `open_browser.sh`.
  TUYỆT ĐỐI không `launch_persistent_context` trực tiếp hay `pkill` nó để tránh hỏng cookie.
"""
import os
import sys
import urllib.request
from playwright.sync_api import sync_playwright

PORT = 9444


def alive():
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
        return True
    except Exception:
        return False


def connect():
    if not alive():
        sys.exit(
            f"❌ Chrome hồ sơ Thiện Trần chưa chạy ở cổng {PORT}.\n"
            f"   Mở bằng lệnh: ./thien-tran/publish/open_browser.sh\n\n"
            "   ĐỪNG để script tự mở — mở bằng tay giữ phiên đăng nhập vĩnh viễn."
        )
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    return pw, b, b.contexts[0]


def require_login(ctx, which):
    """Kiểm tra đăng nhập TRƯỚC khi upload, để hỏng thì hỏng sớm và nói rõ lý do."""
    probe = {
        "youtube": ("https://studio.youtube.com/", "accounts.google.com"),
        "facebook": ("https://www.facebook.com/thientm?locale=vi_VN", "login"),
        "tiktok": ("https://www.tiktok.com/tiktokstudio/upload", "/login"),
    }[which]
    p = ctx.new_page()
    p.goto(probe[0], wait_until="domcontentloaded", timeout=60000)
    url = p.url
    p.close()
    if probe[1] in url:
        sys.exit(
            f"❌ Chưa đăng nhập {which.upper()}.\n"
            f"   Mở Chrome ở cổng {PORT}, đăng nhập tay vào {probe[0]} rồi chạy lại."
        )
