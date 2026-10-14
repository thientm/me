import sys
import datetime as dt
import re
sys.path.insert(0, ".")
from _conn import connect
from meta import VIDEO, YT_TITLE
import ledger

pw, b, ctx = connect()
pages = [x for x in ctx.pages if "studio.youtube.com" in x.url]
if not pages:
    p = ctx.new_page()
    p.goto("https://studio.youtube.com/channel/UCvoMD_dBm8z1i-Zd8Pwu7mQ/videos/short", wait_until="domcontentloaded")
    p.wait_for_timeout(10000)
else:
    p = pages[0]
p.set_default_timeout(90000)

ed = p.get_by_text("Edit draft", exact=True)
if not ed.count():
    print("Khong thay Edit draft tren tab hien tai, dang dieu huong toi danh sach shorts...")
    p.goto("https://studio.youtube.com/channel/UCvoMD_dBm8z1i-Zd8Pwu7mQ/videos/short", wait_until="domcontentloaded")
    p.wait_for_timeout(8000)
    ed = p.get_by_text("Edit draft", exact=True)

if not ed.count():
    print("Van khong thay Edit draft. Kiem tra xem co dialog upload dang mo khong...")
    dlg = p.locator("ytcp-uploads-dialog")
    if not dlg.count():
        print("Khong co ytcp-uploads-dialog hay Edit draft")
        pw.stop()
        sys.exit(1)
else:
    print("Thay nut Edit draft, dang bam...")
    ed.first.click()
    p.wait_for_timeout(8000)

for i in range(5):
    p.wait_for_timeout(2000)
    if p.locator("tp-yt-paper-radio-button[name='PUBLIC']").count() and p.locator("tp-yt-paper-radio-button[name='PUBLIC']").first.is_visible():
        print("Da toi buoc Visibility!")
        break
    nb = p.locator("#next-button").first
    for _ in range(15):
        if nb.is_visible() and not nb.get_attribute("disabled") and nb.get_attribute("aria-disabled") != "true":
            break
        p.wait_for_timeout(2000)
    nb.click()
    p.wait_for_timeout(3000)
    print("clicked next", i + 1)

p.wait_for_selector("tp-yt-paper-radio-button[name='PUBLIC']", timeout=60000)

# Mở Schedule
exp = p.locator("#second-container-expand-button").first
if exp.is_visible():
    exp.click()
    p.wait_for_timeout(2500)

today_day = str(dt.date.today().day)
p.locator("#datepicker-trigger").first.click()
p.wait_for_timeout(1800)
p.locator("ytcp-date-picker").get_by_text(today_day, exact=True).first.click()
p.wait_for_timeout(2000)

tb = p.locator("#time-of-day-container input").first
tb.click()
p.wait_for_timeout(600)
p.keyboard.press("Meta+a")
p.keyboard.press("Delete")
tb.type("8:00 PM", delay=45)
p.wait_for_timeout(1200)
p.keyboard.press("Enter")
p.wait_for_timeout(2000)
print("Da dat gio:", repr(tb.input_value()))

p.screenshot(path="_scratch/yt_sched_2000.png")
db = p.locator("#done-button").first
print("Nut done:", db.inner_text().strip(), "| disabled:", db.get_attribute("disabled"))
db.click()
p.wait_for_timeout(14000)
sh = p.locator("ytcp-video-share-dialog")
print("== KET QUA ==")
print(sh.first.inner_text()[:400] if sh.count() else p.inner_text("body")[:300])

ledger.record(VIDEO, "youtube", "hen 20:00")
print("[OK] YouTube Shorts scheduled at 20:00!")
pw.stop()
