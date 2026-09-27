import os
import shutil
import subprocess
import time
from playwright.sync_api import sync_playwright

HERE = "/Users/thientm/.gemini/antigravity-cli/brain/691b2684-b079-4b16-b768-fec2e4b93619/scratch"
HTML = os.path.join(HERE, "viral_scene.html")
FRAMES_DIR = os.path.join(HERE, "frames_viral")
AUDIO = "/Users/thientm/Documents/GitHub/me/thien-tran/render/vo/viral_buddha.vo.wav"
OUTPUT = "/Users/thientm/Documents/GitHub/me/thien-tran/render/viral_buddha_full.mp4"

FPS = 30
TOTAL = 31.0
W, H = 1080, 1920

def main():
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    
    total_frames = int(TOTAL * FPS)
    print(f"Bắt đầu render full video {TOTAL}s ({total_frames} frames)...", flush=True)
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
        
    print(f"Chụp xong 100% trong {time.time()-t0:.1f}s. Đang ghép video và master audio bằng FFmpeg...", flush=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAMES_DIR, "f%05d.jpg"),
        "-i", AUDIO,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT
    ]
    subprocess.run(cmd, check=True)
    print(f"Hoàn thành xuất sắc full video! File: {OUTPUT}", flush=True)

if __name__ == "__main__":
    main()
