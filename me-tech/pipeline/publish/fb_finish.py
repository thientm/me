#!/usr/bin/env python3
"""Bam nut Schedule/Share cho composer Facebook DANG MO san.

    python3 fb_finish.py --at 12:30
    python3 fb_finish.py                # dang ngay

Dung khi fb.py da tai video, go mo ta, dat gio xong nhung dung lai o cong
`confirm_schedule` (hoac bi loi sau do). Chay lai fb.py se tai video LAN NUA
va bo lai mot composer bo hoang — dat hai ban nhap len Page. File nay xai lai
composer dang mo, nen khong sinh ban thua.

Van doc lai ngay/gio truoc khi bam, y het fb.py. Khong bao gio tin cu bam.
"""
import argparse
import datetime as dt
import sys
sys.path.insert(0, ".")
from _conn import confirm_schedule, connect
from meta import VIDEO

ap = argparse.ArgumentParser()
ap.add_argument("--at")
a = ap.parse_known_args()[0]
AT = a.at
if AT:
    _h, _m = (int(x) for x in AT.split(":"))
    WHEN = dt.datetime.now().replace(hour=_h, minute=_m, second=0, microsecond=0)
    if WHEN <= dt.datetime.now() + dt.timedelta(minutes=5):
        WHEN += dt.timedelta(days=1)
    print("hen:", WHEN.strftime("%d/%m/%Y %H:%M"))

pw, b, ctx = connect()
q = [p for p in ctx.pages if "reels_composer" in p.url]
if not q:
    pw.stop()
    sys.exit("[X] khong co composer Facebook nao dang mo. Chay fb.py truoc.")
q = q[-1]
q.set_default_timeout(60000)

t = q.inner_text("body")
print("Original sound giu nguyen:", "Original audio" in t)
print("Public:", "Public" in t)

if AT:
    confirm_schedule(q,
                     {"ngay": "input[placeholder='dd/mm/yyyy']",
                      "gio": "input[aria-label='hours']",
                      "phut": "input[aria-label='minutes']"},
                     {"ngay": WHEN.strftime("%d %B %Y"),
                      "gio": WHEN.strftime("%H"), "phut": WHEN.strftime("%M")})

want = "Schedule" if AT else "Share"
bt = q.get_by_role("button")
tgt = None
for i in range(bt.count()):
    e = bt.nth(i)
    try:
        lab = (e.get_attribute("aria-label") or e.inner_text() or "").strip()
        if e.is_visible() and lab == want:
            tgt = e          # nut that nam CUOI danh sach, dau danh sach la tab
    except Exception:
        pass
if tgt is None:
    pw.stop()
    sys.exit("[X] khong tim thay nut " + want)
tgt.click()
print("da bam", want, "- DUNG dieu huong tab nay")
q.wait_for_timeout(45000)
q.screenshot(path="_scratch/fb_done.png")

import ledger
ledger.record(VIDEO, "facebook", ("hen " + AT) if AT else "dang ngay")
print("da ghi so dang bai")
pw.stop()
