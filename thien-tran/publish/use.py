#!/usr/bin/env python3
"""Chon bai se dang.

    python3 use.py                 xem dang chon bai nao + danh sach bai co san
    python3 use.py anthropic-ipo   chon bai
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACTIVE = os.path.join(HERE, "ACTIVE")


def have():
    return sorted(f[5:-3] for f in os.listdir(HERE)
                  if f.startswith("meta_") and f.endswith(".py"))


def main():
    cur = ""
    if os.path.exists(ACTIVE):
        cur = open(ACTIVE, encoding="utf-8").read().strip()

    if len(sys.argv) < 2:
        print("dang chon:", cur or "(chua chon)")
        import ledger
        for s in have():
            done = [p for p in ("youtube", "facebook", "tiktok")
                    if ledger.seen(s + ".mp4", p)]
            print("  %-22s %s" % (s, ("da len: " + ", ".join(done)) if done else "chua dang"))
        return 0

    slug = sys.argv[1]
    if slug not in have():
        print("[X] khong co meta_%s.py" % slug)
        print("    co san:", ", ".join(have()))
        return 1
    with open(ACTIVE, "w", encoding="utf-8") as f:
        f.write(slug + "\n")
    print("[OK] dang chon:", slug)
    from meta import VIDEO, YT_TITLE
    print("     video:", os.path.basename(VIDEO))
    print("     tieu de:", YT_TITLE[:70])
    return 0


if __name__ == "__main__":
    sys.exit(main())
