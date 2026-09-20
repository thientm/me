#!/usr/bin/env python3
"""Chụp ảnh NGUỒN GỐC để dẫn trong video.

    python capture.py <url> <đường-dẫn-ảnh-ra> [--h 900] [--crop 0,0,1400,900]

Luật (đừng nới):
- Chỉ chụp NGUỒN GỐC: blog chính hãng, hồ sơ toà án, trang tài liệu, bảng đo
  chính thức. KHÔNG chụp ảnh trong bài báo — AGENTS.md cấm, và đó là ảnh có
  giấy phép của hãng tin.
- Chỉ lấy đúng phần đang được dẫn (tiêu đề, đoạn nêu con số), không lấy cả bài.
- Trên video luôn phải có dòng ghi xuất xứ đi kèm (khai "src" ở trạm mode 'shot').

Dùng HỒ SƠ VỨT ĐI, không bao giờ đụng ~/.me-tech-browser.
"""
import argparse, os, tempfile
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("url")
ap.add_argument("out")
ap.add_argument("--w", type=int, default=1400)
ap.add_argument("--h", type=int, default=900)
ap.add_argument("--wait", type=int, default=6000)
ap.add_argument("--full", action="store_true")
a = ap.parse_args()

prof = tempfile.mkdtemp(prefix="metech-capture-")
with sync_playwright() as pw:
    ctx = pw.chromium.launch_persistent_context(
        user_data_dir=prof, headless=True,
        viewport={"width": a.w, "height": a.h}, device_scale_factor=2)
    p = ctx.pages[0] if ctx.pages else ctx.new_page()
    p.set_default_timeout(60000)
    p.goto(a.url, wait_until="domcontentloaded")
    p.wait_for_timeout(a.wait)
    # dẹp banner cookie che mất nội dung
    for t in ("Accept", "Accept all", "I agree", "Got it", "Đồng ý"):
        try:
            b = p.get_by_role("button", name=t, exact=False)
            if b.count() and b.first.is_visible():
                b.first.click(); p.wait_for_timeout(800); break
        except Exception:
            pass
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    p.screenshot(path=a.out, full_page=a.full)
    print("title:", p.title()[:100])
    print("url  :", p.url)
    print("ảnh  :", a.out)
    ctx.close()
