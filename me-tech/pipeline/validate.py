#!/usr/bin/env python3
"""Soát file nội dung TRƯỚC khi chạy TTS.

Lý do tồn tại: 19.09.2026 mất ba vòng dựng lại (mỗi vòng ~100 giây) chỉ vì
độ dài lệch khỏi khoảng chốt, và suýt ra video hỏng vì `data.stages[].at`
trỏ ra ngoài mảng `words` sau khi rút gọn câu. Cả hai lỗi đó đều phát hiện
được trong một giây nếu soát trước.

    python3 validate.py content/<slug>.json
"""
import json, sys

MODES = {"say", "data", "step", "shot", "flow", "outro"}

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
        # ảnh dẫn nguồn mà không ghi xuất xứ là dùng ảnh người khác không ghi công
        if s.get("mode") == "shot" and s.get("shot") and not s.get("src"):
            err.append(f"{tag}: có 'shot' nhưng thiếu 'src' — ảnh dẫn nguồn BẮT BUỘC ghi xuất xứ")

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
            # n==1 + nhiều thẻ = trạm MỤC LỤC của bài điểm tin: hợp lệ, thẻ sáng
            # đều tay theo thời lượng câu (xem scene.html, rec.index)
            if cards and len(cards) != n and n != 1 \
                    and not any(s.get("splitAt") for s in segs if s["group"] == g):
                warn.append(f"group '{g}': {len(cards)} thẻ nhưng {n} câu — cần 'splitAt'")

    # ĐIỂM TIN NHANH — bài gộp nhiều tin, chốt riêng vì dễ hỏng theo kiểu riêng:
    # thiếu một trạm tin thì thẻ mục lục nói ba mà clip chỉ kể hai.
    if d.get("kind") == "roundup":
        idx = [s for s in segs if s["mode"] == "step"]
        if not idx:
            err.append("roundup: thiếu trạm mục lục (mode 'step') mở đầu")
        elif segs[0]["mode"] != "step":
            err.append("roundup: trạm mục lục phải là trạm ĐẦU TIÊN")
        else:
            ncards = len(idx[0].get("cards") or [])
            # trạm tin = mọi group trừ mục lục và outro
            nstory = len({s["group"] for s in segs}) - 2
            if ncards != nstory:
                err.append("roundup: mục lục %d thẻ nhưng %d trạm tin — phải bằng nhau"
                           % (ncards, nstory))
            if not 3 <= ncards <= 4:
                err.append("roundup: %d tin — chốt 3–4 tin, ít hơn thì đăng tin lẻ, "
                           "nhiều hơn thì không kịp đọc" % ncards)
        for g in {s["group"] for s in segs}:
            gs = [s for s in segs if s["group"] == g]
            if gs[0]["mode"] in ("step", "outro"):
                continue
            if not gs[0].get("lab"):
                err.append("roundup: trạm tin '%s' thiếu 'lab' — mỗi tin phải ghi nguồn" % g)

    # === CỔNG CÂU MÓC — đừng gỡ ===
    # 24.09.2026: tuần đầu video chỉ 25% view FB giữ quá giây 3. Luật câu móc
    # nằm ở AGENTS.md "Câu móc"; cổng này giữ cho nó khỏi lặng lẽ rơi như luật
    # ảnh dẫn nguồn từng rơi. Điểm tin nhanh bỏ qua: câu đầu của nó là mục lục.
    if d.get("kind") != "roundup":
        if d.get("hook") not in (1, 2, 3, 4, 5):
            err.append('thiếu "hook": <1–5> ở khoá gốc — kiểu câu móc, xem AGENTS.md "Câu móc"')
        h = segs[0]
        if len(h.get("words") or []) > 10:
            err.append("câu móc %d chữ — tối đa 10, đọc xong trong 2 giây"
                       % len(h["words"]))
        brand = (d.get("kicker") or "").split("·")[0].strip().lower()
        first = " ".join(h.get("words") or []).lower()
        if brand and first.startswith(brand):
            err.append("câu móc mở bằng tên hãng '%s' — để tên hãng sang câu 2" % brand)

    # === CỔNG ẢNH DẪN NGUỒN — đừng gỡ ===
    # 21.09.2026: 4/5 bài gần nhất KHÔNG có trạm 'shot' nào. Luật về ảnh dẫn
    # nguồn có trong AGENTS.md nhưng chỉ là MÔ TẢ cách làm, không cổng nào bắt
    # buộc — nên nó lặng lẽ rơi mất qua từng bài mà không ai báo. Cổng cũ chỉ
    # chặn "có shot mà thiếu src", tức là không có shot nào thì cho qua êm.
    # Ảnh chụp chính trang gốc là thứ trực quan nhất và là bằng chứng bài viết
    # có thật, nên mặc định BẮT BUỘC. Không có thì phải NÓI RÕ vì sao.
    nshot = sum(1 for s in segs if s.get("mode") == "shot")
    if not nshot and not d.get("no_shot"):
        err.append(
            "không có trạm 'shot' nào — mỗi bài phải dẫn ảnh chụp nguồn gốc.\n"
            "      Chụp:  .venv/bin/python capture.py <url> shots/<tên>.png --phone\n"
            "      Thật sự không có nguồn để chụp thì khai lý do ở khoá gốc:\n"
            '        "no_shot": "tin đồn rò rỉ, chưa có trang chính thức nào"')
    if d.get("no_shot"):
        warn.append("bỏ ảnh dẫn nguồn, lý do: %s" % d["no_shot"])
    if d.get("kind") == "roundup" and nshot and nshot < 2:
        warn.append("điểm tin nhanh mới có %d tin dẫn ảnh — nhắm mỗi tin một ảnh" % nshot)

    syl = sum(syllables(s) for s in segs)
    speed = float(d.get("speed", 1.0))
    est = syl * SEC_PER_SYL / speed
    lo = int(TARGET[0] / SEC_PER_SYL * speed)
    hi = int(TARGET[1] / SEC_PER_SYL * speed)
    ngroups = len({s["group"] for s in segs})

    print(f"  {len(segs)} câu · {ngroups} trạm · {syl} âm tiết"
          + (f" · tốc độ ×{speed:.2f}" if speed != 1.0 else ""))
    print(f"  ước lượng {est:.1f}s (khoảng chốt {TARGET[0]:.0f}–{TARGET[1]:.0f}s "
          f"↔ {lo}–{hi} âm tiết)")
    # so với NGƯỠNG CÓ ĐỆM, không phải lo/hi trần — so nhầm thì báo ngược chiều
    if syl < lo + 4:
        warn.append(f"số âm tiết sát mép dưới — thêm khoảng {(lo + 8) - syl} âm tiết cho chắc")
    elif syl > hi - 4:
        warn.append(f"số âm tiết sát mép trên — bớt khoảng {syl - (hi - 8)} âm tiết cho chắc")
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
