#!/usr/bin/env python3
"""Kiem chung bai YouTube theo DUNG TIEU DE, va dem ban trung.

    python3 yt_verify.py            # lay tieu de tu meta.YT_TITLE
    python3 yt_verify.py "tieu de"

Ma thoat - script goi no PHAI doc ma nay, dung doc chu:
    0  dung mot ban Published          -> xong, dung lam gi them
    1  khong tim thay                  -> chua dang, chay yt.py
    2  tim thay nhung la Draft         -> chay yt_finish.py, DUNG upload lai
    3  co NHIEU HON MOT ban Published  -> da dang trung, bao Thien xoa bot

Ly do ton tai: 21.09.2026 phien chay tu dong doc "dong moi nhat" thay vi doi
chieu tieu de, tuong chua dang nen upload lai -> hai ban CONG KHAI trung nhau
tren kenh. Khong bao gio quyet dinh upload lai dua tren "dong moi nhat".

`yt.py` goi `scan(title, ctx)` NGAY TRUOC khi upload va tu dung neu da co ban
Published/Draft trung tieu de - cong chan, khong chi la kiem chung sau.
"""
import sys
sys.path.insert(0, ".")

CH = "UCvoMD_dBm8z1i-Zd8Pwu7mQ"  # Kênh Thiện Trần


def norm(s):
    return " ".join((s or "").split()).strip().lower()


def scan(title, ctx=None):
    """Tra (pub, draft) khop DUNG tieu de.

    pub   = da cong khai HOAC da hen gio (ca hai deu la 'da xu ly xong, dung
            dang lai'). Dem chung mot ro vi quyet dinh dua tren chung giong
            nhau: co roi thi khong upload nua.
    draft = moi la ban nhap, phai chay yt_finish.py.

    ctx=None  -> tu noi CDP roi tu dong (dung khi chay doc lap)
    ctx san   -> dung lai phien dang mo (dung khi yt.py goi lam cong chan)
    """
    pw = None
    if ctx is None:
        from _conn import connect
        pw, _b, ctx = connect()
    p = ctx.new_page()
    try:
        p.set_default_timeout(60000)
        p.goto("https://studio.youtube.com/channel/%s/videos/short" % CH,
               wait_until="domcontentloaded")
        p.wait_for_timeout(12000)
        want = norm(title)
        pub, draft = [], []
        rows = p.locator("ytcp-video-row")
        for i in range(rows.count()):
            txt = rows.nth(i).inner_text()
            lines = [l.strip() for l in txt.split("\n") if l.strip()]
            if not any(want and want in norm(l) for l in lines):
                continue
            # 'Scheduled' la da xong viec cua minh -> tinh nhu da dang.
            # 'Draft' moi la chua xong. Doc theo thu tu nay, dung doi cho.
            if "Draft" in txt and "Scheduled" not in txt:
                draft.append(i)
            else:
                pub.append(i)
        return pub, draft
    finally:
        try:
            p.close()
        except Exception:
            pass
        if pw is not None:
            pw.stop()


def main():
    if len(sys.argv) > 1:
        title = sys.argv[1]
    else:
        from meta import YT_TITLE
        title = YT_TITLE
    print("-- doi chieu tieu de: <<%s>>" % title[:70])
    pub, draft = scan(title)
    print("   Published: %d   Draft: %d" % (len(pub), len(draft)))

    if len(pub) > 1:
        print("   [X] DANG TRUNG %d BAN CONG KHAI." % len(pub))
        print("       BAO Thien xoa bot. TUYET DOI KHONG upload them.")
        return 3
    if len(pub) == 1:
        extra = ("  [!] con %d ban nhap thua - bao Thien xoa." % len(draft)) if draft else ""
        print("   [OK] dung mot ban Published." + extra)
        return 0
    if draft:
        print("   [..] moi co ban Draft - chay yt_finish.py. DUNG upload lai.")
        return 2
    print("   [ ] chua thay - chay yt.py de dang.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
