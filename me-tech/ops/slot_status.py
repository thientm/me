#!/usr/bin/env python3
"""Khung HH:00 hôm nay đã có bài chưa — đọc logs/posted.json, không mở trình duyệt.

    python3 slot_status.py 20      -> in 1 dòng, mã thoát:
      0  done              đủ youtube + tiktok + facebook
      1  none              chưa có nền tảng nào
      2  partial <slug> <thiếu,…>

Một khoá tính cho khung khi ghi ngày hôm nay và:
  - ghi_chu "hen HH:.." khớp giờ khung (TikTok lệch 30 phút vẫn khớp), hoặc
  - "dang ngay" ghi từ 1 tiếng trước giờ khung trở về sau (đăng trễ vẫn tính).
"""
import datetime as dt, json, pathlib, sys

PLAT = ("youtube", "tiktok", "facebook")
slot = int(sys.argv[1])
today = dt.date.today()
led = json.loads((pathlib.Path(__file__).parent.parent / "logs/posted.json").read_text())

hits = {}
for key, v in led.items():
    slug, _, plat = key.rpartition(":")
    if plat not in PLAT:
        continue
    try:
        luc = dt.datetime.strptime(v.get("luc", ""), "%d.%m.%Y %H:%M")
    except ValueError:
        continue
    if luc.date() != today:
        continue
    note = v.get("ghi_chu", "")
    if note.startswith("hen "):
        ok = note[4:6] == f"{slot:02d}"
    else:
        ok = luc >= dt.datetime.combine(today, dt.time(max(slot - 1, 0)))
    if ok:
        hits.setdefault(slug, set()).add(plat)

best = max(hits.items(), key=lambda kv: len(kv[1]), default=None)
if best and len(best[1]) == 3:
    print("done", best[0]); sys.exit(0)
if best:
    print("partial", best[0], ",".join(p for p in PLAT if p not in best[1])); sys.exit(2)
print("none"); sys.exit(1)
