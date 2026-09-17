#!/usr/bin/env python3
"""Biến file nội dung thành cấu hình hình cho scene.html.

Gom các câu liên tiếp cùng `group` thành MỘT trạm trên mặt phẳng. Máy quay
chỉ lia giữa các trạm, không lia theo từng câu — đó là lý do 11 câu vẫn chỉ
có 6 cú lia.

    python deck.py content/lawzero.json .work/deck.js
"""
import json, sys

MODES = {"say", "data", "step", "outro"}


def groups(segs):
    """Gom câu liên tiếp cùng group (hoặc cùng mode nếu không khai group)."""
    out = []
    for i, s in enumerate(segs):
        key = s.get("group") or f"_{i}"
        mode = s.get("mode", "say")
        if mode not in MODES:
            raise SystemExit(f"câu {s['id']}: mode '{mode}' không hợp lệ ({', '.join(sorted(MODES))})")
        if out and out[-1]["key"] == key:
            if out[-1]["mode"] != mode:
                raise SystemExit(f"group '{key}' trộn hai mode khác nhau")
            out[-1]["segs"].append(i)
        else:
            out.append({"key": key, "mode": mode, "segs": [i],
                        "lab": s.get("lab", ""), "cards": s.get("cards"),
                        "splitAt": s.get("splitAt")})
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    c = json.load(open(src, encoding="utf-8"))
    segs = c["segments"]

    if segs[-1].get("mode") != "outro":
        raise SystemExit("câu cuối phải là mode 'outro' — cảnh kết dùng chung")

    deck = {
        "brand": c.get("brand", "MÊ TECH"),
        "kicker": c.get("kicker", ""),
        "date": c.get("date", ""),
        "outro": c.get("outro", {"mark": "Mê Tech", "handle": "mecongnghe40"}),
        "data": c.get("data"),
        "hot": [s.get("hot", []) for s in segs],
        "groups": groups(segs),
    }
    open(dst, "w", encoding="utf-8").write(
        "window.DECK = " + json.dumps(deck, ensure_ascii=False, indent=1) + ";\n")

    n = len(deck["groups"])
    print(f"  {len(segs)} câu → {n} trạm → {n-1} cú lia")
    for g in deck["groups"]:
        print(f"    {g['mode']:<5} {g['key']:<10} câu {[segs[i]['id'] for i in g['segs']]}")


if __name__ == "__main__":
    main()
