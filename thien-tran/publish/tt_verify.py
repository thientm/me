#!/usr/bin/env python3
"""Kiem chung bai TikTok trong Content manager (ke ca ban DA HEN GIO).

    python3 tt_verify.py

Ma thoat: 0 = thay dung mot ban · 1 = khong thay · 3 = thay nhieu hon mot.

Truoc day TikTok khong co buoc kiem chung nao ca (VERIFY["tiktok"] = None),
nghia la neu cu bam Post im lang khong an thi khong ai biet.
"""
import sys
sys.path.insert(0, ".")
from _conn import connect


def norm(s):
    return " ".join((s or "").split()).strip().lower()


def main():
    from meta import TT_CAPTION
    want = norm(sys.argv[1] if len(sys.argv) > 1 else TT_CAPTION.split("#")[0][:40])
    print("-- doi chieu moc: <<%s>>" % want)
    pw, b, ctx = connect()
    try:
        p = ctx.new_page()
        p.set_default_timeout(60000)
        p.goto("https://www.tiktok.com/tiktokstudio/content",
               wait_until="domcontentloaded")
        p.wait_for_timeout(14000)
        n = norm(p.inner_text("body")).count(want)
    finally:
        pw.stop()
    print("   thay:", n)
    if n > 1:
        print("   [X] co the dang trung - bao Thien kiem tra.")
        return 3
    if n == 1:
        print("   [OK] dung mot ban.")
        return 0
    print("   [ ] chua thay - chay tt.py de dang.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
