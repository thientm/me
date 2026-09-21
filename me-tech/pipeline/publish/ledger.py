#!/usr/bin/env python3
"""So dang bai - chong dang trung cho CA BA nen tang.

    python3 ledger.py            # xem da dang gi
    python3 ledger.py --forget hacktron-openai:tiktok

Vi sao can: 21.09.2026 YouTube co hai ban cong khai trung nhau. yt.py da co
cong chan doi chieu tieu de ngay tren kenh (chac chan nhat), nhung Facebook va
TikTok thi khong doc nguoc lai duoc de dang. So nay la lop chan thu hai, chay
o may, khong phu thuoc giao dien nen tang.

Khoa = <ten file video>:<nen tang>. Mot video chi dang mot lan moi nen tang.
Muon dang lai that -> `--force` (hoac xoa dong bang --forget).
"""
import json
import os
import sys
import datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.abspath(os.path.join(HERE, "..", "..", "logs", "posted.json"))


def _load():
    try:
        with open(PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(d):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2, sort_keys=True)


def slug(video):
    return os.path.splitext(os.path.basename(video))[0]


def key(video, platform):
    return "%s:%s" % (slug(video), platform)


def seen(video, platform):
    return _load().get(key(video, platform))


def record(video, platform, note=""):
    d = _load()
    d[key(video, platform)] = {
        "luc": dt.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "ghi_chu": note,
    }
    _save(d)


def guard(video, platform, force=False):
    """Goi NGAY DAU moi script dang. Da co trong so -> thoat, khong dang lai."""
    hit = seen(video, platform)
    if hit and not force:
        print("[X] SO DANG BAI: %s da len %s luc %s"
              % (slug(video), platform, hit.get("luc", "?")))
        print("    Khong dang lai. That su muon dang lai thi them --force.")
        sys.exit(0)
    if hit and force:
        print("[!] --force: dang lai %s tren %s du so da ghi %s"
              % (slug(video), platform, hit.get("luc", "?")))


def main():
    if "--forget" in sys.argv:
        k = sys.argv[sys.argv.index("--forget") + 1]
        d = _load()
        if d.pop(k, None) is None:
            print("khong co khoa:", k)
            return 1
        _save(d)
        print("da xoa:", k)
        return 0
    d = _load()
    if not d:
        print("so trong:", PATH)
        return 0
    print("so dang bai -", PATH)
    for k in sorted(d):
        print("  %-42s %s" % (k, d[k].get("luc", "?")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
