#!/usr/bin/env python3
"""Xep lich ca bo the anh len Facebook — 5 bai/ngay.

    python3 fb_photo_batch.py --plan     # chi in lich, khong dang
    python3 fb_photo_batch.py            # dang that

Nhiem vu Facebook tuan nay: 30 bai photo cong khai. 5 bai/ngay x 6 ngay.

Khung gio TRANH ba khung video (08:00 · 12:00 · 20:00) de hai loai bai khong
gianh cho nhau trong feed.

CHAY LAI DUOC: moi the da len lich deu nam trong so dang bai, chay lai thi
bo qua. Hong giua chung thi chay lai, no di tiep tu cho do.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
sys.path.insert(0, ".")
import ledger

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
PY = sys.executable

GIO = ["09:30", "11:00", "14:00", "16:30", "18:30"]   # tranh 08 · 12 · 20
MOI_NGAY = len(GIO)


def ke_hoach():
    d = json.load(open(os.path.join(PIPE, "cards", "thuong-xanh.json"),
                       encoding="utf-8"))
    cards = [c["slug"] for c in d["cards"]]
    hom_nay = dt.date.today()
    out = []
    for i, slug in enumerate(cards):
        ngay = i // MOI_NGAY
        gio = GIO[i % MOI_NGAY]
        khi = dt.datetime.combine(hom_nay + dt.timedelta(days=ngay),
                                  dt.time(*map(int, gio.split(":"))))
        out.append((slug, khi, ngay, gio))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true", help="chi in lich")
    ap.add_argument("--tu", type=int, default=0, help="bat dau tu the thu may")
    a = ap.parse_args()

    kh = ke_hoach()
    bay_gio = dt.datetime.now()

    print("── lịch %d thẻ · %d bài/ngày · tránh khung video 08:00 · 12:00 · 20:00"
          % (len(kh), MOI_NGAY))
    con_lai = []
    for i, (slug, khi, ngay, gio) in enumerate(kh):
        da = ledger.seen(slug + ".png", "facebook-photo")
        qua = khi <= bay_gio + dt.timedelta(minutes=15)
        trang_thai = ("đã xếp " + da["luc"]) if da else ("QUÁ GIỜ" if qua else "chờ")
        print("  %2d. %-20s %s  %s" % (i + 1, slug, khi.strftime("%d/%m %H:%M"), trang_thai))
        if not da and not qua and i >= a.tu:
            con_lai.append((slug, khi))

    if a.plan:
        print("\n%d thẻ chưa xếp." % len(con_lai))
        return 0
    if not con_lai:
        print("\nKhông còn thẻ nào cần xếp.")
        return 0

    print("\n── xếp %d thẻ, mỗi thẻ ~1,5 phút\n" % len(con_lai))
    ok, loi = [], []
    for slug, khi in con_lai:
        ngay = (khi.date() - dt.date.today()).days
        print("»", slug, khi.strftime("%d/%m %H:%M"), flush=True)
        r = subprocess.run([PY, os.path.join(HERE, "fb_photo.py"), slug,
                            "--at", khi.strftime("%H:%M"), "--day", str(ngay)],
                           cwd=HERE)
        (ok if r.returncode == 0 else loi).append(slug)
        if r.returncode:
            print("   [X] lỗi (mã %d) — bỏ qua, đi tiếp\n" % r.returncode, flush=True)
        # Facebook không thích bị dồn dập. Nghỉ giữa hai bài.
        import time; time.sleep(12)

    print("\n" + "=" * 52)
    print("[OK] xếp được %d thẻ" % len(ok))
    if loi:
        print("[X]  lỗi %d thẻ: %s" % (len(loi), ", ".join(loi)))
        print("     chạy lại file này, nó bỏ qua thẻ đã xếp và làm tiếp.")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
