#!/usr/bin/env python3
"""Dat gio + bam nut tren composer TikTok. Dung chung cho tt.py va tt_finish.py.

    python3 tt_sched.py --at 21:00     # lam tren composer DANG MO
    python3 tt_sched.py                # dang ngay

BA CAI BAY DA TRA GIA O DAY, DUNG GO:

1. LOP PHU CHAN MOI CU BAM. Day la cai lam hong nhieu nhat.
   TikTok mo hop thoai bang mot lop phu `div.TUXModal-overlay` trum ca trang.
   Playwright bao: "TUXModal-overlay ... intercepts pointer events" roi thu
   lai 112 lan trong 60 giay va chet. Luc do NHIN man hinh thay nut ro rang,
   nen rat de tuong la sai selector — khong phai, la bi lop phu chan.
   => LUAT: goi `clear_overlay(q)` TRUOC MOI cu bam, khong phai sau.
   21.09.2026 doc `clear_dialog` sau cu bam submit -> mat nguyen khung 12:30.

2. O GIO khong go chu vao duoc, phai BAM trong bang chon:
       gio  .tiktok-timepicker-option-text.tiktok-timepicker-left
       phut .tiktok-timepicker-option-text.tiktok-timepicker-right
   Phut nhay 5 mot nac -> ba khung chot (07:45 · 12:30 · 21:00) deu dat duoc.
   (Ghi chu cu bao "radio Schedule la input an, click khong an" la SAI —
   get_by_text("Schedule").click() an binh thuong, mien la het lop phu.)

3. Hop thoai "Continue to post?" hien khi TikTok chua soat xong video.
   Cach dung: CHO hai muc Checks bao "No issues found" roi hay bam — bam
   truoc thi bi hoi, bam sau thi di thang. Con hien thi moi bam xac nhan.
"""
import re
import sys

DIALOG = "Continue to post?"
CHECK_OK = "No issues found"
OVERLAY = "div.TUXModal-overlay"


def overlay_on(q):
    try:
        return q.locator(OVERLAY).count() > 0 and q.locator(OVERLAY).first.is_visible()
    except Exception:
        return False


def clear_overlay(q, lan=6):
    """Don sach lop phu dang chan. Goi TRUOC moi cu bam."""
    for _ in range(lan):
        if not overlay_on(q):
            return True
        t = q.inner_text("body")
        if DIALOG in t:
            # Hop thoai that: xac nhan chu khong huy, vi minh dang muon dang.
            for name in ("Post now", "Schedule", "Continue", "OK"):
                btn = q.get_by_role("button", name=name, exact=True)
                if btn.count() and btn.last.is_visible():
                    print("   [lop phu] bam xac nhan:", name)
                    btn.last.click()
                    q.wait_for_timeout(5000)
                    break
            else:
                q.keyboard.press("Escape")
                q.wait_for_timeout(2000)
        else:
            # Lop phu la lich/bang chon dang mo -> dong lai.
            print("   [lop phu] dong bang dang mo")
            q.keyboard.press("Escape")
            q.wait_for_timeout(1500)
            if overlay_on(q):
                c = q.get_by_role("button", name="Cancel", exact=True)
                if c.count() and c.first.is_visible():
                    c.first.click()
                    q.wait_for_timeout(2000)
                else:
                    q.mouse.click(5, 5)
                    q.wait_for_timeout(1500)
    if overlay_on(q):
        q.screenshot(path="_scratch/tt_overlay_stuck.png")
        raise SystemExit("[X] TikTok: lop phu khong don duoc, xem "
                         "_scratch/tt_overlay_stuck.png")
    return True


def tap(q, loc, ten=""):
    """Bam mot phan tu, nhung don lop phu truoc da."""
    clear_overlay(q)
    loc.click(timeout=20000)
    if ten:
        print("   bam:", ten)


def wait_checks(q, giay=90):
    """Cho TikTok soat xong video. Soat xong thi bam nut khong bi hoi lai."""
    for i in range(giay // 3):
        if q.inner_text("body").count(CHECK_OK) >= 2:
            print("   checks xong sau ~%ds" % (i * 3))
            return True
        q.wait_for_timeout(3000)
    print("   [!] checks chua xong sau %ds - van bam, se xu ly hop thoai" % giay)
    return False


def set_time(q, when):
    """Bat Schedule va dat dung gio. Doc lai roi moi tra ve."""
    clear_overlay(q)
    tap(q, q.get_by_text("Schedule", exact=True).first, "Schedule")
    q.wait_for_timeout(3000)

    rad = q.locator("input[name='postSchedule'][value='schedule']").first
    if not rad.is_checked():
        raise SystemExit("[X] TikTok: khong bat duoc che do Schedule.")

    tf = q.locator("input.TUXTextInputCore-input")
    dfield, tfield = tf.nth(1), tf.nth(0)
    if dfield.input_value().strip() != when.strftime("%Y-%m-%d"):
        raise SystemExit("[X] TikTok: o ngay dang la %r, can %s. Chi ho tro hen TRONG NGAY."
                         % (dfield.input_value(), when.strftime("%Y-%m-%d")))

    tfield.click()
    q.wait_for_timeout(1500)
    for cls, val in ((".tiktok-timepicker-left", when.strftime("%H")),
                     (".tiktok-timepicker-right", when.strftime("%M"))):
        opt = q.locator(".tiktok-timepicker-option-text" + cls
                        ).filter(has_text=re.compile(r"^%s$" % val)).first
        opt.scroll_into_view_if_needed()
        opt.click()
        q.wait_for_timeout(1200)
    q.keyboard.press("Escape")
    q.wait_for_timeout(1500)

    got = tfield.input_value().strip()
    print("   o gio doc lai:", repr(got), "| ngay:", repr(dfield.input_value()))
    if got != when.strftime("%H:%M"):
        q.screenshot(path="_scratch/tt_sched_fail.png")
        raise SystemExit("[X] TikTok: o gio la %r, muon %s. KHONG bam."
                         % (got, when.strftime("%H:%M")))
    print("   [OK] ngay gio da dung")


def submit(q, at=None):
    """Cho soat xong, don lop phu, bam nut, roi don hop thoai neu no van hien."""
    want = "Schedule" if at else "Post"
    wait_checks(q)
    clear_overlay(q)
    btn = q.get_by_role("button", name=want, exact=True)
    if not btn.count():
        raise SystemExit("[X] khong thay nut " + want)
    tap(q, btn.last, want)
    q.wait_for_timeout(8000)
    clear_overlay(q)
    q.wait_for_timeout(14000)
    q.screenshot(path="_scratch/tt_done.png")


def main():
    import argparse, datetime as dt
    sys.path.insert(0, ".")
    ap = argparse.ArgumentParser()
    ap.add_argument("--at")
    a = ap.parse_known_args()[0]
    when = None
    if a.at:
        h, m = (int(x) for x in a.at.split(":"))
        when = dt.datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
        if when <= dt.datetime.now() + dt.timedelta(minutes=5):
            when += dt.timedelta(days=1)
        print("hen:", when.strftime("%d/%m/%Y %H:%M"))

    from _conn import connect
    from meta import VIDEO
    pw, b, ctx = connect()
    q = [p for p in ctx.pages if "tiktokstudio/upload" in p.url]
    if not q:
        pw.stop()
        sys.exit("[X] khong co composer TikTok nao dang mo. Chay tt.py truoc.")
    q = q[-1]
    q.set_default_timeout(45000)
    if when:
        set_time(q, when)
    submit(q, a.at)
    print("url:", q.url)
    import ledger
    ledger.record(VIDEO, "tiktok", ("hen " + a.at) if a.at else "dang ngay")
    print("da ghi so dang bai")
    pw.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
