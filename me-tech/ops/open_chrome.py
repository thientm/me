#!/usr/bin/env python3
"""Mở Chrome của một kênh ở chế độ nền, không cướp chuột (30.09.2026).

    python3 open_chrome.py 9333        # me-tech   (FB cả ba kênh cũng đi qua đây)
    python3 open_chrome.py 9444        # thien-tran
    python3 open_chrome.py 9555        # tam-an-lac

`open -gna` = mở phiên Chrome mới mà KHÔNG đưa lên trước mặt; mở xong thu nhỏ cửa sổ.
Chỉ mở Chrome thật với --user-data-dir của kênh — không launch_persistent_context,
không pkill (luật ở pipeline/publish/_conn.py). Chrome đang chạy sẵn thì chỉ thu nhỏ.
"""
import os
import subprocess
import sys
import time
import urllib.request

try:
    import playwright  # noqa: F401
except ModuleNotFoundError:  # python3 hệ thống → chạy lại bằng venv của me-tech
    _py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline", ".venv", "bin", "python")
    os.execv(_py, [_py] + sys.argv)
from playwright.sync_api import sync_playwright

ME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # thư mục repo
PROFILES = {
    9333: os.path.expanduser("~/.me-tech-browser"),
    9444: os.path.join(ME, "thien-tran", ".browser"),
    9555: os.path.join(ME, "tam-an-lac", "chrome_profile"),
}


def alive(port):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2)
        return True
    except Exception:
        return False


def main():
    port = int(sys.argv[1])
    if not alive(port):
        subprocess.run(["open", "-gna", "Google Chrome", "--args",
                        f"--user-data-dir={PROFILES[port]}", f"--remote-debugging-port={port}",
                        "--no-first-run", "--no-default-browser-check", "about:blank"], check=True)
        for _ in range(30):
            if alive(port):
                break
            time.sleep(1)
        else:
            sys.exit(f"[X] Chrome cổng {port} không lên sau 30s")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline", "publish"))
    from _conn import quiet
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        quiet(b, b.contexts[0])
    print(f"[OK] Chrome cổng {port} đang chạy (mở nền, không thu nhỏ — xem _conn.quiet)")


if __name__ == "__main__":
    main()
