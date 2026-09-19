#!/usr/bin/env python3
"""Soát file nội dung TRƯỚC khi chạy TTS.

Lý do tồn tại: 19.09.2026 mất ba vòng dựng lại (mỗi vòng ~100 giây) chỉ vì
độ dài lệch khỏi khoảng chốt, và suýt ra video hỏng vì `data.stages[].at`
trỏ ra ngoài mảng `words` sau khi rút gọn câu. Cả hai lỗi đó đều phát hiện
được trong một giây nếu soát trước.

    python3 validate.py content/<slug>.json
"""
import json, sys

MODES = {"say", "data", "step", "outro"}

# Hiệu chỉnh từ ba bài đã dựng thật (lawzero · glm53 · rnd-index):
# 136–141 âm tiết ↔ 36,6–37,6 giây → 0,268 giây/âm tiết, sai số ±3%.
SEC_PER_SYL = 0.268
TARGET = (32.0, 38.0)


def syllables(seg):
    w = seg.get("weights")
    return sum(w) if w else len(seg["words"])


def check(path):
    d = json.load(open(path, encoding="utf-8"))
    err, warn = [], []
    segs = d["segments"]

    for k in ("slug", "brand", "kicker", "date", "outro"):
        if k not in d:
            err.append(f"thiếu khoá gốc '{k}'")

    ids = [s["id"] for s in segs]
    if len(set(ids)) != len(ids):
        err.append("id câu bị trùng")

    for i, s in enumerate(segs):
        tag = f"câu[{i}] {s.get('id', '?')}"
        if s.get("mode") not in MODES:
            err.append(f"{tag}: mode '{s.get('mode')}' không hợp lệ")
        if len(s["words"]) != len(s.get("weights") or s["words"]):
            err.append(f"{tag}: words {len(s['words'])} ≠ weights {len(s.get('weights', []))}")
        for h in s.get("hot", []):
            if h >= len(s["words"]):
                err.append(f"{tag}: hot {h} vượt quá {len(s['words'])} chữ")
        if not s.get("say", "").strip():
            err.append(f"{tag}: thiếu 'say'")

    if segs[-1].get("mode") != "outro":
        err.append("câu cuối phải là mode 'outro'")

    # group phải liền khối — cách quãng là máy quay lia đi rồi lia về
    seen, prev = set(), None
    for s in segs:
        g = s["group"]
        if g != prev:
            if g in seen:
                err.append(f"group '{g}' bị cắt quãng rồi quay lại")
            seen.add(g); prev = g
    modes = {}
    for s in segs:
        modes.setdefault(s["group"], set()).add(s["mode"])
    for g, m in modes.items():
        if len(m) > 1:
            err.append(f"group '{g}' trộn nhiều mode: {sorted(m)}")

    # mốc số liệu phải trỏ đúng vào một câu mode 'data'
    for j, st in enumerate(d.get("data", {}).get("stages", [])):
        si, wi = st["at"]
        if si >= len(segs):
            err.append(f"data.stages[{j}].at: câu {si} không tồn tại")
        elif wi >= len(segs[si]["words"]):
            err.append(f"data.stages[{j}].at: chữ {wi} vượt quá {len(segs[si]['words'])} "
                       f"chữ của câu '{segs[si]['id']}'")
        elif segs[si]["mode"] != "data":
            err.append(f"data.stages[{j}].at trỏ vào câu '{segs[si]['id']}' mode "
                       f"'{segs[si]['mode']}', phải là 'data'")

    for g, m in modes.items():
        if "step" in m:
            cards = next((s.get("cards") for s in segs if s["group"] == g and s.get("cards")), None)
            n = sum(1 for s in segs if s["group"] == g)
            if cards and len(cards) != n and not any(s.get("splitAt") for s in segs if s["group"] == g):
                warn.append(f"group '{g}': {len(cards)} thẻ nhưng {n} câu — cần 'splitAt'")

    syl = sum(syllables(s) for s in segs)
    est = syl * SEC_PER_SYL
    lo, hi = int(TARGET[0] / SEC_PER_SYL), int(TARGET[1] / SEC_PER_SYL)
    ngroups = len({s["group"] for s in segs})

    print(f"  {len(segs)} câu · {ngroups} trạm · {syl} âm tiết")
    print(f"  ước lượng {est:.1f}s (khoảng chốt {TARGET[0]:.0f}–{TARGET[1]:.0f}s "
          f"↔ {lo}–{hi} âm tiết)")
    if not lo + 4 <= syl <= hi - 4:
        d_syl = (lo + 6) - syl if syl < lo else syl - (hi - 6)
        warn.append(f"số âm tiết sát mép — {'thêm' if syl < lo else 'bớt'} khoảng "
                    f"{abs(d_syl)} âm tiết cho chắc")
    if not 5 <= ngroups <= 7:
        warn.append(f"{ngroups} trạm — nhắm 5–7 trạm cho bài ~35 giây")

    for w in warn:
        print(f"  ⚠ {w}")
    for e in err:
        print(f"  ✗ {e}")
    return not err


if __name__ == "__main__":
    print("── soát nội dung")
    sys.exit(0 if check(sys.argv[1]) else 1)
