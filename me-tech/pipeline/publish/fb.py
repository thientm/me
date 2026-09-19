"""Đăng Reel lên Page Mê Tech qua Meta Business Suite.

Đăng bằng business.facebook.com chứ KHÔNG phải facebook.com/reels/create —
đường kia đăng nhầm sang trang cá nhân.
"""
import re, sys
sys.path.insert(0, ".")
from _conn import connect, require_login
from meta import VIDEO, FB_CAPTION

ASSET = "403727472998689"          # Page Mê Tech

pw, b, ctx = connect()
require_login(ctx, 'facebook').close()
q = ctx.new_page()
q.set_default_timeout(120000)

q.goto("https://business.facebook.com/latest/reels_composer/?asset_id=" + ASSET,
       wait_until="domcontentloaded")
q.wait_for_timeout(10000)
print("url:", q.url)

# "Add video" mở hộp chọn file, không có input[type=file] sẵn trong DOM
with q.expect_file_chooser() as fc:
    q.get_by_text("Add video", exact=True).first.click()
fc.value.set_files(VIDEO)
print("da chon file, cho upload…")
for _ in range(30):
    q.wait_for_timeout(3000)
    if "100%" in q.inner_text("body"):
        break
print("upload xong")

# mô tả — gõ từng dòng, Shift+Enter để xuống dòng trong contenteditable
tb = q.get_by_role("textbox").first
tb.click()
q.wait_for_timeout(500)
for i, line in enumerate(FB_CAPTION.split("\n")):
    if i:
        q.keyboard.press("Shift+Enter")
    q.keyboard.type(line, delay=4)
q.wait_for_timeout(1500)
print("mo ta:", tb.inner_text()[:90])

# nhãn nút Facebook có ký tự zero-width ở cuối -> khớp bằng regex
for step in ("Create", "Edit"):
    q.get_by_role("button", name=re.compile(r"^\s*Next\s*$")).last.click()
    q.wait_for_timeout(9000)
    print("qua buoc", step)

t = q.inner_text("body")
print("Original sound giữ nguyên:", "Original audio" in t)
print("Public:", "Public" in t)

# nút Share thật nằm cuối danh sách (đầu danh sách là tab "Share")
bt = q.get_by_role("button")
tgt = None
for i in range(bt.count()):
    e = bt.nth(i)
    try:
        if e.is_visible() and (e.get_attribute("aria-label") or e.inner_text() or "").strip() == "Share":
            tgt = e
    except Exception:
        pass
tgt.click()
print("da bam Share — dang publish, DUNG dieu huong tab nay")
q.wait_for_timeout(45000)
q.screenshot(path="_scratch/fb_done.png")
pw.stop()
