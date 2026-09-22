#!/usr/bin/env python3
"""Kiem chung bai Facebook theo DUNG cau mo dau cua FB_CAPTION.

    python3 fb_verify.py            # lay moc tu meta.FB_CAPTION
    python3 fb_verify.py "chuoi"

Ma thoat - script goi no PHAI doc ma nay:
    0  thay dung mot ban          -> xong
    1  khong thay                 -> chua len, chay fb.py
    3  thay nhieu hon mot ban     -> dang trung, bao Thien xoa bot

Ban cu cua file nay do chuoi "chu tri mot phan tu" cua mot bai thang truoc,
nen no bao "khong thay" cho MOI bai moi - tuc la chua bao gio kiem chung gi.
Moc phai lay tu meta.py, dung bao gio go cung.

Bai HEN GIO khong nam o tab published_posts -> doc them tab scheduled.
"""
import sys
sys.path.insert(0, ".")
from _conn import connect

ASSET = "403727472998689"
TABS = {
    "da dang": "https://business.facebook.com/latest/posts/published_posts?asset_id=" + ASSET,
    "hen gio": "https://business.facebook.com/latest/posts/scheduled_posts?asset_id=" + ASSET,
}


def norm(s):
    return " ".join((s or "").split()).strip().lower()


def anchor(caption):
    """Cau dau tien cua caption, cat ~60 ky tu - du dac trung, du ngan de khong
    bi Facebook cat mat khi hien thi rut gon."""
    first = [l for l in caption.split("\n") if l.strip()][0]
    return first.strip()[:60]


def main():
    if len(sys.argv) > 1:
        want_raw = sys.argv[1]
    else:
        from meta import FB_CAPTION
        want_raw = anchor(FB_CAPTION)
    want = norm(want_raw)
    print("-- doi chieu moc: <<%s>>" % want_raw)

    pw, b, ctx = connect()
    total = 0
    try:
        p = ctx.new_page()
        p.set_default_timeout(60000)
        for name, url in TABS.items():
            p.goto(url, wait_until="domcontentloaded")
            p.wait_for_timeout(14000)
            # Danh sach nay PHAN TRANG: 22.09.2026 co 30 the anh trong hang doi,
            # bai reel hen 08:00 khong duoc ve ra -> doc body tho tra ve 0 cho
            # mot bai DA hen dung. Phai loc bang o Search truoc khi dem.
            try:
                box = p.get_by_placeholder("Search by ID or caption")
                if box.count():
                    box.first.click()
                    box.first.fill(want_raw[:30])
                    p.wait_for_timeout(9000)
                else:
                    print("   [!] khong thay o Search - dem tren ca trang")
            except Exception as e:
                print("   [!] o Search loi (%s) - dem tren ca trang" % e)
            body = norm(p.inner_text("body"))
            n = body.count(want)
            total += n
            print("   %-8s: %d" % (name, n))
    finally:
        pw.stop()

    if total > 1:
        print("   [X] THAY %d BAN - co the dang trung. BAO Thien kiem tra." % total)
        return 3
    if total == 1:
        print("   [OK] dung mot ban.")
        return 0
    print("   [ ] chua thay - chay fb.py de dang.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
