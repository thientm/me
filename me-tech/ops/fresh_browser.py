#!/usr/bin/env python3
"""Dọn tab trước khi bắt đầu một phiên làm việc trên Chrome của một kênh (luật 30.09.2026).

    python3 fresh_browser.py 9333        # me-tech   (FB cả ba kênh cũng đi qua đây)
    python3 fresh_browser.py 9444        # thien-tran
    python3 fresh_browser.py 9555        # tam-an-lac

Mở một tab trống rồi đóng MỌI tab khác. Chỉ đóng tab qua CDP — không tắt Chrome,
không pkill, nên phiên đăng nhập không bị đụng.

Chỉ chạy lúc BẮT ĐẦU phiên. Không chạy khi job khác đang giữ khoá (me-tech/.run/build.lock
mới hơn 20 phút) — tab soạn bài của job đó có thể đang "Publishing", và *_finish.py
cần tab đang mở. Luôn chừa lại một tab: Chrome 0 tab thì connect_over_cdp báo
"Browser context management is not supported".
"""
import json
import os
import sys
import time
import urllib.request

try:
    import playwright  # noqa: F401
except ModuleNotFoundError:  # python3 hệ thống → chạy lại bằng venv của me-tech (cần playwright để mở tab nền)
    _py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline", ".venv", "bin", "python")
    if os.path.exists(_py):
        os.execv(_py, [_py] + sys.argv)

LOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".run", "build.lock")


def call(port, path, method="GET"):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", method=method)
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.read().decode()


def main():
    port = int(sys.argv[1])
    own = "--own-lock" in sys.argv   # job đang giữ khoá tự gọi thì được dọn
    # build.lock là khoá của job me-tech — chỉ chặn Chrome me-tech (9333), không chặn 9444/9555
    if port == 9333 and not own and os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 1200:
        sys.exit("[X] có job đang giữ khoá build.lock — không dọn tab")
    # FB của thien-tran / tam-an-lac cũng đăng qua Chrome me-tech: đang giữ khoá này là đang có tab soạn bài
    fb = os.path.join(os.path.dirname(LOCK), "fb9333.lock")
    if port == 9333 and os.path.exists(fb) and time.time() - os.path.getmtime(fb) < 1800:
        sys.exit("[X] kênh khác đang đăng FB qua 9333 (fb9333.lock) — không dọn tab")
    try:
        tabs = [t for t in json.loads(call(port, "/json/list")) if t.get("type") == "page"]
    except Exception:
        sys.exit(f"[X] Chrome chưa chạy ở cổng {port}")
    # tab trống mở NỀN + thu nhỏ cửa sổ — /json/new bật Chrome lên trước mặt (cướp chuột)
    keep = quiet_blank_tab(port)
    for t in tabs:
        call(port, f"/json/close/{t['id']}")
    print(f"[OK] cổng {port}: đóng {len(tabs)} tab, còn 1 tab trống ({keep[:8]})")


def quiet_blank_tab(port):
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:   # python3 hệ thống không có playwright → mở kiểu cũ
        return json.loads(call(port, "/json/new?about:blank", "PUT"))["id"]
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline", "publish"))
    from _conn import quiet
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        quiet(b, b.contexts[0])
        s = b.new_browser_cdp_session()
        return s.send("Target.createTarget", {"url": "about:blank", "background": True})["targetId"]


if __name__ == "__main__":
    main()
