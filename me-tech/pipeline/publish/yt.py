import argparse, datetime as dt, sys
sys.path.insert(0, ".")
from _conn import connect, require_login
from meta import VIDEO, YT_TITLE, YT_DESC

import ledger

_ap = argparse.ArgumentParser(); _ap.add_argument("--at")
_ap.add_argument("--force", action="store_true")
_a = _ap.parse_known_args()[0]
AT, FORCE = _a.at, _a.force
ledger.guard(VIDEO, "youtube", FORCE)   # lop chan 1: so o may, khong can mo trinh duyet
if AT:
    _h, _m = (int(x) for x in AT.split(":"))
    _when = dt.datetime.now().replace(hour=_h, minute=_m, second=0, microsecond=0)
    if _when <= dt.datetime.now():
        _when += dt.timedelta(days=1)
    AT_DAY = _when.day
    AT_HHMM = _when.strftime("%I:%M %p").lstrip("0")
    print("hen:", _when.strftime("%d.%m.%Y"), AT_HHMM)

CH = "UCnElgDX9q_AYGdFc2oDuWUA"
pw, b, ctx = connect()
require_login(ctx, 'youtube').close()

# === CONG CHAN DANG TRUNG - dung go ===
# 21.09.2026 kenh co HAI ban cong khai trung nhau vi mot lan chay lai.
# Truoc khi upload, doi chieu tieu de voi kenh. Da co -> thoat, khong upload.
from yt_verify import scan as _scan
_pub, _draft = _scan(YT_TITLE, ctx) if not FORCE else ([], [])
if _pub or _draft:
    print("[X] DA CO TREN KENH: Published=%d Draft=%d" % (len(_pub), len(_draft)))
    print("    Tieu de: <<%s>>" % YT_TITLE[:70])
    if _pub:
        print("    -> Da dang roi. KHONG upload lai. Xong.")
    else:
        print("    -> Moi la Draft. Chay yt_finish.py, KHONG upload lai.")
    pw.stop()
    sys.exit(0 if _pub else 2)
print("[OK] chua co tren kenh - tien hanh upload.")

p = ctx.pages[0] if ctx.pages else ctx.new_page()
p.set_default_timeout(120000)

def dismiss():
    for lab in ["Continue", "Tiep tuc", "Got it", "Da hieu"]:
        try:
            btn = p.get_by_role("button", name=lab, exact=False)
            if btn.count() and btn.first.is_visible():
                btn.first.click()
                p.wait_for_timeout(1200)
        except Exception:
            pass

p.goto("https://studio.youtube.com/channel/%s/videos/upload?d=ud" % CH,
       wait_until="domcontentloaded")
p.wait_for_timeout(9000)
dismiss()
p.wait_for_timeout(2000)
print("url:", p.url)

p.locator("input[type=file]").first.set_input_files(VIDEO)
print("da chon file")

p.wait_for_selector("#title-textarea #textbox", timeout=120000)
p.wait_for_timeout(3000)
dismiss()

t = p.locator("#title-textarea #textbox").first
t.click()
p.keyboard.press("Meta+a")
p.keyboard.press("Delete")
t.type(YT_TITLE, delay=6)
p.wait_for_timeout(600)

d = p.locator("#description-textarea #textbox").first
d.click()
d.type(YT_DESC, delay=3)
p.wait_for_timeout(600)

p.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first.click()
p.wait_for_timeout(1000)
print("tieu de:", t.inner_text()[:150])

# Next x3
for i in range(3):
    p.click("#next-button")
    p.wait_for_timeout(2500)
    print("next", i + 1)

p.wait_for_selector("tp-yt-paper-radio-button[name='PUBLIC']", timeout=60000)

if AT:
    # Hẹn giờ bằng tính năng sẵn có của YouTube, không phải cron lúc 21h.
    # Phần hẹn giờ nằm SAU nút mở rộng, không hiện sẵn.
    p.locator("#second-container-expand-button").first.click()
    p.wait_for_timeout(2500)
    # NGÀY: lịch dạng calendar, phải BẤM ô ngày — gõ chữ vào là bị backdrop chặn
    p.locator("#datepicker-trigger").first.click()
    p.wait_for_timeout(1800)
    p.locator("ytcp-date-picker").get_by_text(str(AT_DAY), exact=True).first.click()
    p.wait_for_timeout(2000)
    # GIỜ
    tb = p.locator("#time-of-day-container input").first
    tb.click()
    p.wait_for_timeout(600)
    p.keyboard.press("Meta+a"); p.keyboard.press("Delete")
    tb.type(AT_HHMM, delay=45)
    p.wait_for_timeout(1200)
    p.keyboard.press("Enter")
    p.wait_for_timeout(2000)
    print("da dat:", repr(tb.input_value()))
else:
    p.locator("tp-yt-paper-radio-button[name='PUBLIC']").first.click()
    p.wait_for_timeout(1500)

p.screenshot(path="_scratch/yt_before_publish.png")
db = p.locator("#done-button").first
print("nut:", db.inner_text().strip())
print(p.inner_text("ytcp-uploads-dialog")[:700])

db.click()
p.wait_for_timeout(14000)
sh = p.locator("ytcp-video-share-dialog")
print("== KET QUA ==")
print(sh.first.inner_text()[:400] if sh.count() else p.inner_text("body")[:300])
ledger.record(VIDEO, "youtube", ("hen " + AT) if AT else "dang ngay")
pw.stop()
