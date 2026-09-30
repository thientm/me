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

LOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".run", "build.lock")


def call(port, path, method="GET"):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", method=method)
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.read().decode()


def main():
    port = int(sys.argv[1])
    own = "--own-lock" in sys.argv   # job đang giữ khoá tự gọi thì được dọn
    if not own and os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 1200:
        sys.exit("[X] có job đang giữ khoá build.lock — không dọn tab")
    try:
        tabs = [t for t in json.loads(call(port, "/json/list")) if t.get("type") == "page"]
    except Exception:
        sys.exit(f"[X] Chrome chưa chạy ở cổng {port}")
    keep = json.loads(call(port, "/json/new?about:blank", "PUT"))["id"]
    for t in tabs:
        call(port, f"/json/close/{t['id']}")
    print(f"[OK] cổng {port}: đóng {len(tabs)} tab, còn 1 tab trống ({keep[:8]})")


if __name__ == "__main__":
    main()
