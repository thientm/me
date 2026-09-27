import os
import wave
import json
import numpy as np
from vieneu import Vieneu

SR = 48000
OUT_DIR = "/Users/thientm/Documents/GitHub/me/thien-tran/render/vo"
os.makedirs(OUT_DIR, exist_ok=True)

# 3 segments
SEGMENTS = [
    {
        "id": "s1",
        "text": "Nếu có người mang rác đến tặng bạn, bạn có nhận không? Chắc chắn là không. Bạn không nhận, thì đống rác đó, vẫn thuộc về người mang đến."
    },
    {
        "id": "s2",
        "text": "Lời chê bai, sự cay nghiệt của người đời cũng như vậy. Người gieo khẩu nghiệp tự gánh quả báo. Bạn không bận lòng, thì tâm bạn mãi thanh tịnh như hoa sen."
    },
    {
        "id": "s3",
        "text": "Đỉnh cao của sự buông bỏ, không phải là trả đũa, mà là bình thản mỉm cười và bước tiếp."
    }
]

def save_wav(audio_data, path, sample_rate=SR):
    peak = float(np.abs(audio_data).max()) or 1.0
    pcm = (audio_data / peak * 0.90 * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm.tobytes())

def main():
    print("Khởi tạo Vieneu TTS với giọng 'Thiền Tâm Đức'...", flush=True)
    tts = Vieneu()
    
    parts = []
    # 0.5s lead in
    parts.append(np.zeros(int(0.5 * SR), dtype=np.float32))
    
    timing = []
    cursor = 0.5
    
    for i, seg in enumerate(SEGMENTS):
        print(f"Đang sinh đoạn {i+1}: {seg['text'][:40]}...", flush=True)
        a = tts.infer(seg["text"], voice="Thiền Tâm Đức")
        dur = len(a) / SR
        timing.append({
            "id": seg["id"],
            "start": round(cursor, 3),
            "end": round(cursor + dur, 3),
            "dur": round(dur, 3),
            "text": seg["text"]
        })
        parts.append(a)
        cursor += dur
        # Add 0.55s gap between scenes
        gap = 0.55
        parts.append(np.zeros(int(gap * SR), dtype=np.float32))
        cursor += gap

    # Add 2.5s tail for outro & temple bell
    tail = 2.8
    parts.append(np.zeros(int(tail * SR), dtype=np.float32))
    total_dur = cursor + tail

    vo = np.concatenate(parts)

    # Load temple bell and mix at cursor (end of speech)
    bell_path = "/Users/thientm/Documents/GitHub/me/thien-tran/render/vo/temple_bell.wav"
    if os.path.exists(bell_path):
        with wave.open(bell_path, 'rb') as bw:
            bdata = np.frombuffer(bw.readframes(bw.getnframes()), dtype=np.int16).astype(np.float32) / 32767.0
        bell_idx = int((cursor - 0.2) * SR)
        blen = min(len(bdata), len(vo) - bell_idx)
        if blen > 0:
            vo[bell_idx:bell_idx + blen] += bdata[:blen] * 0.70

    out_wav = os.path.join(OUT_DIR, "viral_buddha.vo.wav")
    save_wav(vo, out_wav)
    
    out_tim = os.path.join(OUT_DIR, "viral_buddha.timing.json")
    manifest = {
        "slug": "viral_buddha",
        "voice": "Thiền Tâm Đức",
        "total": round(total_dur, 2),
        "segments": timing
    }
    with open(out_tim, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Hoàn thành! Audio dài {total_dur:.2f}s: {out_wav}", flush=True)

if __name__ == "__main__":
    main()
