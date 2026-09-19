"""Đăng Reel lên Page Mê Tech qua Meta Business Suite.

Đăng bằng business.facebook.com chứ KHÔNG phải facebook.com/reels/create —
đường kia đăng nhầm sang trang cá nhân.
"""
import argparse, datetime as dt, re, sys
sys.path.insert(0, ".")
from _conn import confirm_schedule, connect, require_login
from meta import VIDEO, FB_CAPTION

_ap = argparse.ArgumentParser(); _ap.add_argument("--at")
AT = _ap.parse_known_args()[0].at
if AT:
    _h, _m = (int(x) for x in AT.split(":"))
    WHEN = dt.datetime.now().replace(hour=_h, minute=_m, second=0, microsecond=0)
    if WHEN <= dt.datetime.now() + dt.timedelta(minutes=20):
        WHEN += dt.timedelta(days=1)
    print("hen:", WHEN.strftime("%d/%m/%Y %H:%M"))

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

if AT:
    # Business Suite có sẵn "Schedule" ở bước Share
    q.get_by_text("Schedule", exact=True).first.click()
    q.wait_for_timeout(3000)
    print("== o hen gio ==")
    ins = q.locator("input")
    for i in range(min(ins.count(), 16)):
        e = ins.nth(i)
        try:
            if e.is_visible():
                print(" ", i, repr(e.get_attribute("aria-label") or e.get_attribute("placeholder")),
                      "=", repr(e.input_value()))
        except Exception:
            pass
    for lab, val in (("hours", WHEN.strftime("%H")), ("minutes", WHEN.strftime("%M"))):
        f = q.locator(f"input[aria-label='{lab}']").first
        f.click()
        q.keyboard.press("Meta+a"); q.keyboard.press("Delete")
        f.type(val, delay=110)
        q.wait_for_timeout(900)
    # LUẬT: đọc lại rồi mới được bấm. Bấm khi ô giờ trống = Facebook tự lấy now+1h.
    confirm_schedule(q,
                     {"ngày": "input[aria-label='dd/mm/yyyy']",
                      "giờ": "input[aria-label='hours']",
                      "phút": "input[aria-label='minutes']"},
                     {"giờ": WHEN.strftime("%H"), "phút": WHEN.strftime("%M")})
    q.screenshot(path="_scratch/fb_sched.png")

# nút Share thật nằm cuối danh sách (đầu danh sách là tab "Share")
bt = q.get_by_role("button")
tgt = None
for i in range(bt.count()):
    e = bt.nth(i)
    try:
        lab = (e.get_attribute("aria-label") or e.inner_text() or "").strip()
        if e.is_visible() and lab == ("Schedule" if AT else "Share"):
            tgt = e
    except Exception:
        pass
if tgt is None:
    raise SystemExit("❌ khong tim thay nut " + ("Schedule" if AT else "Share"))
tgt.click()
print("da bam", "Schedule" if AT else "Share", "— DUNG dieu huong tab nay")
q.wait_for_timeout(45000)
q.screenshot(path="_scratch/fb_done.png")
pw.stop()
