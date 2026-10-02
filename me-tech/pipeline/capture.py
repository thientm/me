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
ap.add_argument("--phone", action="store_true",
                help="chụp ở khổ điện thoại — trang tự xuống dòng ngắn, chữ mới đọc được trong video dọc")
ap.add_argument("--scroll", action="store_true",
                help="cuộn hết trang trước khi chụp — trang hiện chữ dần khi cuộn tới (vd microsoft.ai) chụp --full ra trống")
ap.add_argument("--sel", help="chỉ chụp một phần tử (CSS selector), ví dụ đoạn văn đang dẫn")
a = ap.parse_args()

prof = tempfile.mkdtemp(prefix="metech-capture-")
with sync_playwright() as pw:
    # LÝ DO CÓ --phone: chụp ở khổ 1400px rồi thu vào khung 1080 thì chữ thân bài
    # chỉ còn ~5px thật trên điện thoại — không ai đọc được, ảnh thành đồ trang trí.
    # Khổ điện thoại làm trang xuống dòng ~40 ký tự, thu vào khung vẫn đọc được.
    vp = {"width": 430, "height": 932} if a.phone else {"width": a.w, "height": a.h}
    kw = {}
    if a.phone:
        kw = dict(is_mobile=True, has_touch=True,
                  user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
                             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
    ctx = pw.chromium.launch_persistent_context(
        user_data_dir=prof, headless=True,
        viewport=vp, device_scale_factor=3, **kw)
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
    if a.scroll:
        h = p.evaluate("document.body.scrollHeight")
        for y in range(0, h, 400):
            p.evaluate(f"window.scrollTo(0,{y})"); p.wait_for_timeout(250)
        p.evaluate("window.scrollTo(0,0)"); p.wait_for_timeout(1500)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if a.sel:
        el = p.locator(a.sel).first
        el.scroll_into_view_if_needed()
        p.wait_for_timeout(600)
        el.screenshot(path=a.out)
        box = el.bounding_box()
        print("phần tử:", a.sel, "->", {k: round(v) for k, v in box.items()} if box else None)
    else:
        p.screenshot(path=a.out, full_page=a.full)
    print("title:", p.title()[:100])
    print("url  :", p.url)
    print("ảnh  :", a.out)
    ctx.close()
