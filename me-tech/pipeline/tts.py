#!/usr/bin/env python3
"""Render voiceover theo TỪNG đoạn và xuất timing.json.

Đây là nguồn sự thật của cả pipeline: độ dài thật của từng đoạn giọng đọc
quyết định timeline animation, chứ không phải ngược lại.

    python tts.py content/gemini-live.json [outdir]

Xuất ra outdir:
    <slug>.vo.wav    giọng đọc đã nối, 48kHz mono
    <slug>.timing.json  {slug, total, lead_in, tail, segments:[{id,scene,start,end,...}]}
"""
import json, sys, os, re, time, unicodedata, difflib
import numpy as np
from vieneu import Vieneu

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))

# --- từ điển phát âm: sửa từ viết tắt TRƯỚC khi đưa vào model
_PRON = {k: v for k, v in json.load(open(os.path.join(HERE, "pronounce.json"), encoding="utf-8")).items()
         if not k.startswith("_")}
_PRON_RE = [(re.compile(r"(?<![0-9A-Za-zÀ-ỹ])" + re.escape(k) + r"(?![0-9A-Za-zÀ-ỹ])"), v)
            for k, v in sorted(_PRON.items(), key=lambda kv: -len(kv[0]))]

def spell(text):
    for rx, v in _PRON_RE:
        text = rx.sub(v, text)
    return text

def syllables(text):
    return len([w for w in text.replace(",", " ").replace(":", " ").split() if w.strip(".!?")])

# --- tầng kiểm chứng: cho máy nghe lại rồi so với text gốc
_ASR = None
def _asr():
    global _ASR
    if _ASR is None:
        from faster_whisper import WhisperModel
        print("  … nạp Whisper (lần đầu hơi lâu)", flush=True)
        _ASR = WhisperModel("small", device="cpu", compute_type="int8")
    return _ASR

# Whisper ghi số bằng CHỮ SỐ ("82 6") còn kịch bản viết bằng CHỮ ("tám mươi hai phẩy sáu"),
# nên bỏ hết phần số ở cả hai bên rồi mới so — kiểm tra từ ngữ, không kiểm tra con số.
_NUM = set("khong mot hai ba bon nam sau bay tam chin muoi tram nghin ngan trieu ty phay phan linh le lam tu".split())

def _strip_numbers(t):
    return " ".join(w for w in t.split() if not w.isdigit() and w not in _NUM)

def _norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9 ]+", " ", t.replace("đ", "d"))
    return " ".join(t.split())

def check(path, expected):
    """Trả (đạt, tỉ lệ từ, độ giống, text nghe được)."""
    segs, _ = _asr().transcribe(path, language="vi", beam_size=1)
    heard = _norm(" ".join(x.text for x in segs))
    want = _norm(expected)
    if not want:
        return True, 1.0, 1.0, heard
    h2, w2 = _strip_numbers(heard), _strip_numbers(want)
    if not w2:
        return True, 1.0, 1.0, heard
    wr = len(h2.split()) / max(len(w2.split()), 1)
    sr = difflib.SequenceMatcher(None, w2, h2).ratio()
    return (wr >= 0.78 and sr >= 0.50), wr, sr, heard

def _tmp_wav(a, path):
    import wave
    pcm = (np.clip(a, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def render_segment(tts, text, voice, opts, tries=3, verify=False):
    """Sinh nhiều lần rồi chọn bản đạt — model là ngẫu nhiên, một lần có thể cụt đuôi."""
    exp = syllables(text) / 4.3
    best, best_score, log, heard = None, -1.0, [], ""
    _w = os.path.join(HERE, ".work"); os.makedirs(_w, exist_ok=True)
    tmp = os.path.join(_w, "_check.wav")
    for k in range(tries):
        a = np.asarray(tts.infer(text, voice=voice, **opts), dtype=np.float32)
        d = len(a) / SR
        if verify:
            _tmp_wav(a, tmp)
            ok, wr, sr, heard = check(tmp, text)
            log.append(f"{d:.2f}s/{wr:.2f}")
            if ok:
                return a, d, exp, k + 1, log, "", heard
            score = min(wr, 1.0) + sr
        else:
            ratio = d / exp if exp else 1.0
            log.append(f"{d:.2f}s")
            if 0.85 <= ratio <= 1.40:
                return a, d, exp, k + 1, log, "", heard
            score = -abs(ratio - 1.0)
        if score > best_score:
            best, best_score = (a, d), score
    a, d = best
    if os.path.exists(tmp): os.remove(tmp)
    return a, d, exp, tries, log, "  ⚠ KHÔNG BẢN NÀO ĐẠT", heard

def main():
    global VERIFY
    VERIFY = "--no-verify" not in sys.argv
    cpath = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    outdir = args[0] if args else "../render/vo"
    os.makedirs(outdir, exist_ok=True)
    c = json.load(open(cpath, encoding="utf-8"))
    slug, voice = c["slug"], c["voice"]
    gap, lead_in, tail = c.get("gap", .3), c.get("lead_in", .6), c.get("tail", 2.0)

    tts = Vieneu()
    defaults = {}
    defaults.update(c.get("tts_opts", {}))
    parts, timing, cursor = [], [], lead_in
    parts.append(np.zeros(int(lead_in * SR), dtype=np.float32))

    for i, s in enumerate(c["segments"]):
        t0 = time.time()
        opts = dict(defaults); opts.update(s.get("opts", {}))
        said = spell(s["say"])
        a, dur, exp, tries, log, flag, heard = render_segment(tts, said, voice, opts, verify=VERIFY)
        timing.append({"id": s["id"], "scene": s["scene"],
                       "start": round(cursor, 3), "end": round(cursor + dur, 3),
                       "dur": round(dur, 3), "show": s["show"]})
        print(f"  [{i+1:2}/{len(c['segments'])}] {s['id']:<6} {dur:5.2f}s  thử {tries}x {log}  {time.time()-t0:4.1f}s{flag}", flush=True)
        if flag and heard:
            print(f"           nghe được: «{heard}»", flush=True)
        parts.append(a)
        cursor += dur
        if i < len(c["segments"]) - 1:
            parts.append(np.zeros(int(gap * SR), dtype=np.float32))
            cursor += gap

    parts.append(np.zeros(int(tail * SR), dtype=np.float32))
    total = cursor + tail

    vo = np.concatenate(parts)
    peak = float(np.abs(vo).max()) or 1.0
    vo = (vo / peak * 0.89 * 32767).astype("<i2")
    import wave
    wp = os.path.join(outdir, f"{slug}.vo.wav")
    with wave.open(wp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(vo.tobytes())

    manifest = {"slug": slug, "voice": voice, "total": round(total, 3),
                "lead_in": lead_in, "gap": gap, "tail": tail,
                "date_label": c.get("date_label", ""), "segments": timing}
    tp = os.path.join(outdir, f"{slug}.timing.json")
    json.dump(manifest, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{wp}\n{tp}\ntotal {total:.2f}s")

if __name__ == "__main__":
    main()
