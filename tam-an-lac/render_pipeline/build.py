import os
import sys
import shutil
import subprocess
import time
import json
import wave
import numpy as np
from vieneu import Vieneu
from playwright.sync_api import sync_playwright

# 29.09.2026: bỏ đường dẫn cứng /Users/thientm/... (máy cũ) — tính từ vị trí file.
# Dùng: python render_pipeline/build.py <slug>   (content/<slug>/script.json [+ scene.html])
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = sys.argv[1] if len(sys.argv) > 1 else "001_khau_nghiep"
OUT_DIR = os.path.join(ROOT, "content", SLUG)
HTML = os.path.join(OUT_DIR, "scene.html")
if not os.path.exists(HTML):
    HTML = os.path.join(ROOT, "templates", "scene.html")
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
AUDIO_WAV = os.path.join(OUT_DIR, "voice.wav")
OUTPUT_MP4 = os.path.join(OUT_DIR, "video.mp4")
SCRIPT = json.load(open(os.path.join(OUT_DIR, "script.json"), encoding="utf-8"))
VOICE = SCRIPT.get("voice", "Thiền Tâm Đức")

SR = 48000
FPS = 30
W, H = 1080, 1920

SEGMENTS = SCRIPT["segments"]


def synth_bell(sr=SR, dur=6.0):
    """Chuông chùa tự tổng hợp (không bản quyền). Máy này không có temple_bell.wav nào."""
    t = np.arange(int(dur * sr)) / sr
    out = np.zeros_like(t)
    for mult, amp, tau in [(1.0, 1.0, 3.2), (2.76, 0.45, 1.8), (5.40, 0.22, 0.9), (8.93, 0.10, 0.5)]:
        out += amp * np.sin(2 * np.pi * 196.0 * mult * t) * np.exp(-t / tau)
    out *= np.clip(t / 0.006, 0, 1) * (1 + 0.04 * np.sin(2 * np.pi * 1.3 * t))
    return (out / np.abs(out).max() * 0.55).astype(np.float32)

def save_wav(audio_data, path, sample_rate=SR):
    peak = float(np.abs(audio_data).max()) or 1.0
    pcm = (audio_data / peak * 0.90 * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm.tobytes())

def generate_audio():
    print("Khởi tạo Vieneu TTS với giọng 'Thiền Tâm Đức'...", flush=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    tts = Vieneu()
    parts = []
    lead = SCRIPT.get("lead_in", 0.5)
    parts.append(np.zeros(int(lead * SR), dtype=np.float32))
    cursor = lead
    timing = []
    
    for i, seg in enumerate(SEGMENTS):
        print(f"Đang sinh đoạn {i+1}: {seg['text'][:40]}...", flush=True)
        a = np.asarray(tts.infer(seg["text"], voice=VOICE), dtype=np.float32)
        dur = len(a) / SR
        timing.append({"id": seg["id"], "start": round(cursor, 3), "end": round(cursor + dur, 3)})
        print(f"   {seg['id']}: {dur:.2f}s", flush=True)
        parts.append(a)
        cursor += dur
        gap = SCRIPT.get("gap", 0.55)
        parts.append(np.zeros(int(gap * SR), dtype=np.float32))
        cursor += gap

    cursor -= gap  # không cộng khoảng lặng sau câu cuối
    parts.pop()
    tail = SCRIPT.get("tail", 2.8)
    parts.append(np.zeros(int(tail * SR), dtype=np.float32))
    total_dur = cursor + tail

    vo = np.concatenate(parts)

    bdata = synth_bell()
    bell_idx = int((cursor + 0.25) * SR)
    blen = min(len(bdata), len(vo) - bell_idx)
    if blen > 0:
        fade = np.linspace(1, 0, blen) ** 0.5
        vo[bell_idx:bell_idx + blen] += bdata[:blen] * fade * 0.70
    else:
        raise SystemExit("❌ Không chèn được chuông kết")

    json.dump({"slug": SLUG, "voice": VOICE, "total": round(total_dur, 3), "segments": timing},
              open(os.path.join(OUT_DIR, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(OUT_DIR, "timing.js"), "w", encoding="utf-8") as f:
        f.write("window.TIMING = " + json.dumps({"total": round(total_dur, 3), "segments": timing}) + ";\n")
    save_wav(vo, AUDIO_WAV)
    print(f"Audio xong: {total_dur:.2f}s tại {AUDIO_WAV}")
    return total_dur

def render_video(total_dur):
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    
    total_frames = int(total_dur * FPS)
    print(f"Bắt đầu render Playwright {total_dur:.2f}s ({total_frames} frames)...", flush=True)
    t0 = time.time()
    
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(f"file://{HTML}")
        pg.wait_for_function("() => !!window.seek")
        pg.wait_for_timeout(400)
        
        for i in range(total_frames):
            t = i / FPS
            pg.evaluate(f"window.seek({t})")
            pg.screenshot(path=os.path.join(FRAMES_DIR, f"f{i:05d}.jpg"), type="jpeg", quality=92)
            if (i + 1) % 150 == 0:
                print(f"  Tiến độ: {i+1}/{total_frames} frames ({(i+1)/total_frames*100:.1f}%) - {time.time()-t0:.1f}s", flush=True)
        b.close()
        
    print(f"Chụp xong. Ghép video...", flush=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAMES_DIR, "f%05d.jpg"),
        "-i", AUDIO_WAV,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_MP4
    ]
    subprocess.run(cmd, check=True)
    print(f"XONG! Video xuất tại: {OUTPUT_MP4}", flush=True)

if __name__ == "__main__":
    dur = generate_audio() if "--skip-tts" not in sys.argv else json.load(open(os.path.join(OUT_DIR, "timing.json")))["total"]
    if not 30 <= dur <= 45:
        print(f"⚠ Thời lượng {dur:.1f}s nằm ngoài 30–45s", flush=True)
    render_video(dur)
