"""Sinh ảnh AI cho một bài Tâm An Lạc bằng Antigravity CLI (`agy`) — luật 30.09.2026.

    python render_pipeline/gen_images.py <slug> "<mô tả cảnh 1>" "<mô tả cảnh 2>" "<mô tả cảnh 3>"

→ content/<slug>/img_1.jpg, img_2.jpg, … (1080x1920), ghi vào logs/images.json.
scene.html của bài dùng `url('img_1.jpg')`… thay cho ảnh mẫu templates/buddha_*.jpg.

Vì sao có script này: `agy -p` ghi xong ảnh (~1 phút) nhưng KHÔNG tự thoát, treo tới
--print-timeout. Nên chờ file xuất hiện và đứng yên rồi tự dừng agy.
Mỗi ảnh sinh mới theo nội dung bài — không dùng lại ảnh cũ (logs/images.json).
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "logs", "images.json")
STYLE = ("Photorealistic vertical 9:16 image, serene and natural, soft natural light "
         "(god rays, mist or golden hour), calm Buddhist mood, Vietnamese setting where fitting. "
         "No text, no letters, no watermark, no logos. Leave the lower-middle third visually calm "
         "(it will carry subtitles).")
MODEL = os.environ.get("AGY_MODEL", "gemini-3.8-flash-medium")


def gen_one(out_png, scene, wait=240):
    d = os.path.dirname(out_png)
    prompt = (f"Use your image generation tool to create ONE image. {STYLE} Scene: {scene} "
              f"Save it as a PNG file at exactly this path: {out_png} . Do nothing else.")
    log = out_png + ".agy.jsonl"
    p = subprocess.Popen(["agy", "-p", prompt, "--add-dir", d, "--model", MODEL,
                          "--print-timeout", f"{wait}s", "--dangerously-skip-permissions",
                          "--output-format", "stream-json"],
                         cwd=d, stdout=open(log, "w"), stderr=subprocess.STDOUT)
    t0, last = time.time(), -1
    while time.time() - t0 < wait:
        time.sleep(3)
        err = quota_error(log)
        if err:
            p.terminate()
            sys.exit(f"[X] HẾT QUOTA sinh ảnh agy: {err}")
        if os.path.exists(out_png):
            sz = os.path.getsize(out_png)
            if sz > 50_000 and sz == last:      # đã ghi xong (kích thước đứng yên)
                break
            last = sz
        if p.poll() is not None and not os.path.exists(out_png):
            break
    if p.poll() is None:
        p.terminate()
        try:
            p.wait(10)
        except subprocess.TimeoutExpired:
            p.kill()
    if not os.path.exists(out_png):
        sys.exit(f"[X] agy không tạo được ảnh: {scene[:60]}")
    return out_png


def quota_error(log):
    """30.09.2026: tài khoản agy chỉ ~1 ảnh / 5 giờ (gemini-3.1-flash-image) → 429 RESOURCE_EXHAUSTED."""
    try:
        for line in open(log, encoding="utf-8"):
            if '"generate_image"' in line and '"ERROR"' in line:
                e = json.loads(line)["step_update"]["tool_info"]["error"]["message"]
                if "429" in e or "RESOURCE_EXHAUSTED" in e:
                    import re
                    m = re.search(r"quota will reset after ([\w.]+)", e)
                    return "reset sau " + (m.group(1) if m else "?")
                return e[:200]
    except Exception:
        pass
    return None


def to_vertical(png, jpg, W=1080, H=1920):
    im = Image.open(png).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im.crop((l, t, l + W, t + H)).save(jpg, quality=92)


def main():
    slug, scenes = sys.argv[1], sys.argv[2:]
    if not scenes:
        sys.exit(__doc__)
    out = os.path.join(ROOT, "content", slug)
    os.makedirs(out, exist_ok=True)
    try:
        led = json.load(open(LEDGER, encoding="utf-8"))
    except Exception:
        led = []
    for i, scene in enumerate(scenes, 1):
        png = os.path.join(out, f"img_{i}.png")
        jpg = os.path.join(out, f"img_{i}.jpg")
        if os.path.exists(png):
            os.remove(png)
        t = time.time()
        gen_one(png, scene)
        to_vertical(png, jpg)
        print(f"[OK] img_{i}.jpg ({time.time() - t:.0f}s) — {scene[:70]}")
        led.append({"slug": slug, "file": f"content/{slug}/img_{i}.jpg", "scene": scene,
                    "model": MODEL, "luc": dt.datetime.now().strftime("%d.%m.%Y %H:%M")})
    json.dump(led, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
