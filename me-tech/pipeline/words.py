#!/usr/bin/env python3
"""Gán mốc thời gian cho TỪNG CHỮ hiển thị.

Whisper cho word timestamps trên chính file giọng đọc. Với câu tiếng Việt
thuần, số chữ nghe được thường khớp số chữ kịch bản -> map 1:1.
Khi lệch (do đọc chữ viết tắt kiểu "gi pi ti"), rơi về chia đều theo độ dài
chữ trong khoảng [start, end] của đoạn -- vẫn đúng nhịp vì biên đoạn là thật.

    python demo/words.py demo/astra.timing.json demo/astra.vo.wav demo/data.js
"""
import json, sys

def whisper_words(wav):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language="vi", beam_size=1, word_timestamps=True)
    out = []
    for s in segs:
        for w in (s.words or []):
            out.append({"t": w.word.strip(), "a": float(w.start), "b": float(w.end)})
    return out


def spread(words, a, b):
    """Chia đều theo trọng số độ dài chữ -- chỉ dùng khi không nghe được gì."""
    wt = [max(len(w), 2) for w in words]
    tot = sum(wt)
    out, cur = [], a
    for w, k in zip(words, wt):
        d = (b - a) * k / tot
        out.append({"w": w, "a": round(cur, 3), "b": round(cur + d, 3)})
        cur += d
    return out


def warp(script, inside, a, b, weights=None):
    """Kéo dãn theo nhịp nói THẬT.

    Whisper tách chữ viết tắt thành nhiều token nên số lượng hiếm khi khớp
    kịch bản. Thay vì bỏ đi, ta dựng một hàm đơn điệu
    (tỉ lệ ký tự đã đọc -> thời điểm thật) từ các mốc whisper, rồi chiếu
    vị trí ký tự của từng chữ kịch bản qua hàm đó. Nhờ vậy chỗ giọng đọc
    chậm lại hay ngắt hơi vẫn được phản ánh đúng.
    """
    hz = sum(max(len(h["t"]), 1) for h in inside)
    xs, ys, cum = [0.0], [max(a, inside[0]["a"])], 0
    for h in inside:
        k = max(len(h["t"]), 1)
        xs.append(cum / hz); ys.append(max(a, h["a"]))
        cum += k
        xs.append(cum / hz); ys.append(min(b, h["b"]))
    xs.append(1.0); ys.append(b)
    for i in range(1, len(ys)):                      # ép đơn điệu
        ys[i] = max(ys[i], ys[i - 1])

    def at(f):
        for i in range(1, len(xs)):
            if f <= xs[i]:
                span = xs[i] - xs[i - 1]
                r = 0 if span <= 0 else (f - xs[i - 1]) / span
                return ys[i - 1] + r * (ys[i] - ys[i - 1])
        return ys[-1]

    # "weights" = số âm tiết mà chữ hiển thị đó đại diện khi đọc lên.
    # Cần vì chữ trên hình ("35") ngắn hơn hẳn lời đọc ("ba mươi lăm").
    sw = list(weights) if weights else [max(len(w), 2) for w in script]
    sz = sum(sw)
    out, cum = [], 0
    for w, k in zip(script, sw):
        f0 = cum / sz; cum += k; f1 = cum / sz
        out.append({"w": w, "a": round(at(f0), 3), "b": round(at(f1), 3)})
    return out


def main():
    tim, wav, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    man = json.load(open(tim, encoding="utf-8"))
    heard = whisper_words(wav)

    segs = []
    for s in man["segments"]:
        a, b = s["start"], s["end"]
        script = s["show"]["words"]
        wts = s["show"].get("weights")
        inside = [h for h in heard if a - 0.2 <= (h["a"] + h["b"]) / 2 <= b + 0.2]
        if len(inside) == len(script) and not wts:
            ws = [{"w": script[i],
                   "a": round(max(a, inside[i]["a"]), 3),
                   "b": round(min(b, inside[i]["b"]), 3)} for i in range(len(script))]
            src = f"whisper 1:1 ({len(inside)} chữ)"
        elif inside:
            ws = warp(script, inside, a, b, wts)
            src = f"whisper kéo dãn (nghe {len(inside)} / hiện {len(script)})"
        else:
            ws = spread(script, a, b)
            src = "chia đều (không nghe được chữ nào)"
        print(f"  {s['id']}  {a:5.2f}-{b:5.2f}  {src}")
        segs.append({"id": s["id"], "scene": s["scene"], "start": a, "end": b,
                     "plain": s["show"]["plain"], "words": ws})

    data = {"total": man["total"], "voice": man["voice"], "segments": segs}
    open(dst, "w", encoding="utf-8").write(
        "window.TL = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    json.dump(data, open(dst.replace(".js", ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{dst}  total {man['total']:.2f}s")

if __name__ == "__main__":
    main()
