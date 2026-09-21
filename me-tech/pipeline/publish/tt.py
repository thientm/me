"""Đăng lên TikTok Studio. KHÔNG chọn nhạc TikTok — video đã có nhạc nền."""
import argparse, datetime as dt, re, sys
sys.path.insert(0, ".")
from _conn import confirm_schedule, connect, require_login
from meta import VIDEO, TT_CAPTION

import ledger

_ap = argparse.ArgumentParser(); _ap.add_argument("--at"); _ap.add_argument("--finish", action="store_true")
_ap.add_argument("--force", action="store_true")
_args = _ap.parse_known_args()[0]
AT, FINISH, FORCE = _args.at, _args.finish, _args.force
if FINISH:
    AT = None
ledger.guard(VIDEO, "tiktok", FORCE)
if AT:
    _h, _m = (int(x) for x in AT.split(":"))
    WHEN = dt.datetime.now().replace(hour=_h, minute=_m, second=0, microsecond=0)
    if WHEN <= dt.datetime.now() + dt.timedelta(minutes=20):
        WHEN += dt.timedelta(days=1)
    print("hen:", WHEN.strftime("%d/%m/%Y %H:%M"))

pw, b, ctx = connect()
require_login(ctx, 'tiktok').close()
q = ctx.new_page()
q.set_default_timeout(120000)

q.goto("https://www.tiktok.com/tiktokstudio/upload?from=webapp", wait_until="domcontentloaded")
q.wait_for_timeout(10000)
q.locator("input[type=file]").first.set_input_files(VIDEO)
print("da chon file, cho upload…")
for _ in range(30):
    q.wait_for_timeout(3000)
    if "Uploaded" in q.inner_text("body"):
        break
print("upload xong")

ed = q.locator("div[contenteditable='true']").first
ed.click()
q.keyboard.press("Meta+a")
q.keyboard.press("Delete")
q.wait_for_timeout(500)
for tok in TT_CAPTION.split(" "):
    q.keyboard.type(tok, delay=10)
    if tok.startswith("#"):
        q.wait_for_timeout(350)
        q.keyboard.press("Escape")   # đóng menu hashtag, nếu không nó nuốt chữ sau
    q.keyboard.type(" ", delay=10)
q.wait_for_timeout(1500)
print("mo ta:", ed.inner_text()[:90])

t = q.inner_text("body")
print("Original sound giữ nguyên:", "Original sound" in t)

import tt_sched

if AT:
    tt_sched.set_time(q, WHEN)
    tt_sched.submit(q, AT)
    print("url:", q.url)
    ledger.record(VIDEO, "tiktok", "hen " + AT)
    pw.stop()
    sys.exit(0)

tt_sched.submit(q, None)
print("url:", q.url)
print(q.inner_text("body")[:500])
ledger.record(VIDEO, "tiktok", "dang ngay")
pw.stop()
