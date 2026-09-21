#!/usr/bin/env python3
"""Dang mot video len ca ba nen tang bang mot lenh.

    python3 post.py                 dang ngay
    python3 post.py --at 21:00      hen gio (ca ba deu ho tro hen gio san)
    python3 post.py --only tiktok   chay lai mot nen tang bi loi
    python3 post.py --force         bo qua so chong trung (hiem khi can)

Hen gio dung tinh nang CO SAN cua tung nen tang, khong phai cron chay luc 21h.
Ly do: cron doi may phai thuc, Chrome phai con dang nhap, va mang phai thong
dung thoi diem do. Hen bang nen tang thi dat xong la xong, tat may cung chay.

Sau moi nen tang deu KIEM CHUNG LAI thay vi tin cu bam - 19.09 YouTube nhan
cu bam Publish nhung video van nam o Draft, khong kiem thi khong biet.

CHONG DANG TRUNG - ba lop, dung go lop nao:
  1. ledger.py   so o may: mot video chi len mot lan moi nen tang
  2. yt.py       doi chieu tieu de ngay tren kenh truoc khi upload
  3. *_verify.py doc lai sau khi dang, dem so ban trung

File nay PHAI doc MA THOAT cua script con, khong doc chu in ra. 21.09.2026
phien tu dong doan tinh trang tu chu -> upload lai -> hai ban cong khai trung.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
STEPS = {"youtube": "yt.py", "facebook": "fb.py", "tiktok": "tt.py"}
VERIFY = {"youtube": "yt_verify.py", "facebook": "fb_verify.py", "tiktok": None}

# Y nghia ma thoat cua *_verify.py - xem dau moi file verify
V_OK, V_MISSING, V_DRAFT, V_DUP = 0, 1, 2, 3


def run(script, args=()):
    return subprocess.run([PY, os.path.join(HERE, script), *args], cwd=HERE).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", help="gio hen hom nay, dang HH:MM (gio may)")
    ap.add_argument("--only", choices=list(STEPS), action="append")
    ap.add_argument("--force", action="store_true",
                    help="bo qua so chong trung - chi dung khi that su muon dang lai")
    a = ap.parse_args()

    which = a.only or list(STEPS)
    extra = (["--at", a.at] if a.at else []) + (["--force"] if a.force else [])
    ok, fail, warn = [], [], []

    for w in which:
        head = w.upper() + ("  (hen " + a.at + ")" if a.at else "")
        print("\n%s\n>> %s\n%s" % ("=" * 52, head, "=" * 52))

        rc = run(STEPS[w], extra)
        if rc == 2:
            fail.append(w)
            print("[!] %s: moi la Draft - chay %s, DUNG upload lai" % (w, "yt_finish.py"))
            continue
        if rc != 0:
            fail.append(w)
            print("[X] %s loi (ma %d)" % (w, rc))
            continue

        v = VERIFY[w]
        if not v:
            ok.append(w)
            continue

        vrc = run(v)
        if vrc == V_OK:
            ok.append(w)
        elif vrc == V_DUP:
            warn.append(w)
            print("[X] %s: DANG TRUNG tren nen tang - bao Thien xoa bot,"
                  " TUYET DOI khong chay lai" % w)
        elif vrc == V_DRAFT:
            fail.append(w)
            print("[!] %s: con nam o Draft - chay yt_finish.py" % w)
        else:
            fail.append(w)
            print("[ ] %s: kiem chung khong thay bai" % w)

    print("\n" + "=" * 52)
    print("[OK] xong:", ", ".join(ok) or "khong co")
    if warn:
        print("[X]  TRUNG:", ", ".join(warn), "- can nguoi xoa bot bang tay")
    if fail:
        print("[X]  loi :", ", ".join(fail))
        print("     chay lai rieng: python3 post.py --only %s%s"
              % (fail[0], (" --at " + a.at) if a.at else ""))
    return 1 if (fail or warn) else 0


if __name__ == "__main__":
    sys.exit(main())
