"""Đăng Reel lên Page Mê Tech qua Meta Business Suite.

Đăng bằng business.facebook.com chứ KHÔNG phải facebook.com/reels/create —
đường kia đăng nhầm sang trang cá nhân.
"""
import argparse, datetime as dt, re, sys
sys.path.insert(0, ".")
from _conn import confirm_schedule, connect, require_login
from meta import VIDEO, FB_CAPTION

import ledger

_ap = argparse.ArgumentParser(); _ap.add_argument("--at")
_ap.add_argument("--force", action="store_true")
_a = _ap.parse_known_args()[0]
AT, FORCE = _a.at, _a.force
ledger.guard(VIDEO, "facebook", FORCE)
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

# Chốt 25.09.2026 (Thiện): mỗi reel đều share lên story.
# Có thể Facebook nhớ sau lần bật đầu, nhưng không tin — lần nào cũng đọc lại, tắt thì bật.
# 26.09.2026 Thiện bỏ luật dịch giọng Meta AI (Meta giới hạn số lượt, hết lượt là kẹt cả bài).
story = q.get_by_role("switch", name="Share to Facebook story").first
if story.get_attribute("aria-checked") != "true":
    story.click()
    q.wait_for_timeout(1500)
ok_story = story.get_attribute("aria-checked") == "true"
print("Share to story:", ok_story)
if not ok_story:
    q.screenshot(path="_scratch/fb_toggles.png")
    pw.stop()
    sys.exit("[X] story chua bat - KHONG bam Share. Xem _scratch/fb_toggles.png")

if AT:
    # fb.py KHONG dien o ngay, chi dien gio/phut -> chi hen duoc TRONG NGAY.
    # 22.09.2026 fb_photo.py dinh dung loi nay: 30 bai don vao mot ngay.
    if WHEN.date() != dt.date.today():
        pw.stop()
        sys.exit("[X] fb.py chi hen duoc TRONG NGAY (muon %s, hom nay %s)."
                 % (WHEN.strftime("%d/%m"), dt.date.today().strftime("%d/%m")))
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
                     # O ngay KHONG co aria-label, chi co placeholder.
                     {"ngày": "input[placeholder='dd/mm/yyyy']",
                      "giờ": "input[aria-label='hours']",
                      "phút": "input[aria-label='minutes']"},
                     # NGAY phai co trong `want`. O nao khong neu thi chi bi
                     # kiem khac rong — ma o ngay luon khac rong.
                     {"ngày": WHEN.strftime("%d %B %Y"),
                      "giờ": WHEN.strftime("%H"), "phút": WHEN.strftime("%M")})
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
ledger.record(VIDEO, "facebook", ("hen " + AT) if AT else "dang ngay")
pw.stop()
