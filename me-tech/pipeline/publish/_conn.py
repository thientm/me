"""Kết nối tới Chrome hồ sơ Mê Tech đang chạy sẵn ở cổng 9333."""
from playwright.sync_api import sync_playwright

PORT = 9333

def connect():
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    return pw, b, b.contexts[0]

def page(ctx, match=None):
    for p in ctx.pages:
        if match is None or match in p.url:
            return p
    return ctx.new_page()
