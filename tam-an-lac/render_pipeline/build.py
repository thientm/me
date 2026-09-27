import os
import shutil
import subprocess
import time
import json
import wave
import numpy as np
from vieneu import Vieneu
from playwright.sync_api import sync_playwright

ROOT = "/Users/thientm/Documents/GitHub/me/tam-an-lac"
OUT_DIR = os.path.join(ROOT, "content", "001_khau_nghiep")
HTML = os.path.join(ROOT, "templates", "scene.html")
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
BELL = "/Users/thientm/Documents/GitHub/me/core-video-engine/bell.wav" # just in case, I will also fall back to thien-tran if it doesn't exist
AUDIO_WAV = os.path.join(OUT_DIR, "voice.wav")
OUTPUT_MP4 = os.path.join(OUT_DIR, "video.mp4")

SR = 48000
FPS = 30
W, H = 1080, 1920

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

def generate_audio():
    print("Khởi tạo Vieneu TTS với giọng 'Thiền Tâm Đức'...", flush=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    tts = Vieneu()
    parts = []
    parts.append(np.zeros(int(0.5 * SR), dtype=np.float32))
    cursor = 0.5
    
    for i, seg in enumerate(SEGMENTS):
        print(f"Đang sinh đoạn {i+1}: {seg['text'][:40]}...", flush=True)
        a = tts.infer(seg["text"], voice="Thiền Tâm Đức")
        dur = len(a) / SR
        parts.append(a)
        cursor += dur
        gap = 0.55
        parts.append(np.zeros(int(gap * SR), dtype=np.float32))
        cursor += gap

    tail = 2.8
    parts.append(np.zeros(int(tail * SR), dtype=np.float32))
    total_dur = cursor + tail

    vo = np.concatenate(parts)

    bell_path = "/Users/thientm/Documents/GitHub/me/thien-tran/render/vo/temple_bell.wav"
    if not os.path.exists(bell_path):
        bell_path = "/Users/thientm/Documents/GitHub/me/core-video-engine/assets/temple_bell.wav"
        
    if os.path.exists(bell_path):
        with wave.open(bell_path, 'rb') as bw:
            bdata = np.frombuffer(bw.readframes(bw.getnframes()), dtype=np.int16).astype(np.float32) / 32767.0
        bell_idx = int((cursor - 0.2) * SR)
        blen = min(len(bdata), len(vo) - bell_idx)
        if blen > 0:
            vo[bell_idx:bell_idx + blen] += bdata[:blen] * 0.70

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
    dur = generate_audio()
    render_video(dur)
