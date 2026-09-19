"""Đăng lên TikTok Studio. KHÔNG chọn nhạc TikTok — video đã có nhạc nền."""
import argparse, datetime as dt, sys
sys.path.insert(0, ".")
from _conn import confirm_schedule, connect, require_login
from meta import VIDEO, TT_CAPTION

_ap = argparse.ArgumentParser(); _ap.add_argument("--at"); _ap.add_argument("--finish", action="store_true")
_args = _ap.parse_known_args()[0]
AT, FINISH = _args.at, _args.finish
if FINISH:
    AT = None
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

if AT:
    # TikTok Studio có sẵn "Schedule" ở mục "When to post"
    q.get_by_text("Schedule", exact=True).first.click()
    q.wait_for_timeout(3500)
    print("== o hen gio TikTok ==")
    ins = q.locator("input")
    for i in range(min(ins.count(), 10)):
        e = ins.nth(i)
        try:
            if e.is_visible():
                print(" ", i, repr(e.get_attribute("placeholder") or e.get_attribute("aria-label")),
                      "=", repr(e.input_value()))
        except Exception:
            pass
    q.screenshot(path="_scratch/tt_sched.png")
    # TikTok: radio "Schedule" là input ẩn, click vào nó không ăn — phải click
    # đúng phần tử hiện trên màn. Chưa dò ra selector ổn định, nên dừng ở đây
    # và nhờ người bật tay, thay vì bấm Post nhầm thành đăng ngay.
    raise SystemExit(
        "⏸ TikTok: bật 'Schedule' và chọn giờ bằng tay trên composer đang mở,\n"
        "   rồi chạy:  python3 tt.py --finish")

q.get_by_role("button", name="Post", exact=True).first.click()
q.wait_for_timeout(8000)
# TikTok hỏi "Continue to post?" khi check chưa xong
try:
    pn = q.get_by_role("button", name="Post now", exact=True)
    if pn.count() and pn.first.is_visible():
        pn.first.click()
        print("da bam Post now")
except Exception as e:
    print("khong co hop xac nhan:", e)
q.wait_for_timeout(25000)
q.screenshot(path="_scratch/tt_done.png")
print("url:", q.url)
print(q.inner_text("body")[:700])
pw.stop()
