#!/usr/bin/env python3
"""Tắt SẠCH Chrome của một kênh khi làm xong kênh đó (luật 30.09.2026).

    python3 close_browser.py 9444        # thien-tran
    python3 close_browser.py 9555        # tam-an-lac
    python3 close_browser.py 9333        # me-tech — chỉ khi cả 3 kênh xong khung (FB 2 kênh kia cũng đi qua đây)

Gửi lệnh CDP `Browser.close` — Chrome tự lưu cookie và thoát như bấm Cmd+Q. KHÔNG pkill
(19.09.2026 pkill đã làm mất sạch đăng nhập). Bài đã hẹn giờ nằm trên máy chủ nền tảng,
tắt Chrome không ảnh hưởng.

Không tắt khi: job khác giữ build.lock (<20 phút), hoặc (với 9333) có fb9333.lock.
"""
import json
import os
import sys
import time
import urllib.request

RUN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".run")


def fresh(name, secs):
    p = os.path.join(RUN, name)
    return os.path.exists(p) and time.time() - os.path.getmtime(p) < secs


def main():
    port = int(sys.argv[1])
    own = "--own-lock" in sys.argv
    # build.lock là khoá của job me-tech — chỉ chặn Chrome me-tech (9333), không chặn 9444/9555
    if port == 9333 and not own and fresh("build.lock", 1200):
        sys.exit("[X] có job đang giữ build.lock — không tắt Chrome")
    if port == 9333 and fresh("fb9333.lock", 1800):
        sys.exit("[X] kênh khác đang đăng FB qua 9333 (fb9333.lock) — không tắt")
    try:
        ws = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3).read())["webSocketDebuggerUrl"]
    except Exception:
        print(f"[OK] cổng {port}: Chrome đã tắt sẵn")
        return
    # Playwright connect_over_cdp lỗi khi Chrome 0 tab → mở 1 tab trống trước
    try:
        tabs = [t for t in json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=3).read()) if t.get("type") == "page"]
        if not tabs:
            urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT"), timeout=3)
    except Exception:
        pass
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        try:
            b.new_browser_cdp_session().send("Browser.close")
        except Exception:
            pass
    for _ in range(10):
        time.sleep(1)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
        except Exception:
            print(f"[OK] cổng {port}: đã tắt Chrome sạch (Browser.close)")
            return
    sys.exit(f"[X] cổng {port}: Chrome chưa tắt sau 10s — để nguyên, KHÔNG pkill")


if __name__ == "__main__":
    try:
        import playwright  # noqa: F401
    except ModuleNotFoundError:
        _py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline", ".venv", "bin", "python")
        os.execv(_py, [_py] + sys.argv)
    main()
