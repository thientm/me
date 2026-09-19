#!/usr/bin/env python3
"""Dựng một video Mê Tech từ file nội dung.

    ./run.sh content/lawzero.json

Chuỗi việc:
    tts.py    lời đọc  -> <slug>.vo.wav + <slug>.timing.json   (nguồn sự thật về thời gian)
    words.py  mốc TỪNG CHỮ -> .work/data.js
    deck.py   nội dung -> .work/deck.js (gom câu thành trạm, chọn chế độ hình)
    music.py  nhạc nền -> .work/bed.wav
    chime.py  chuông kết -> .work/chime.wav
    scene.html + Playwright -> .work/frames/
    ffmpeg    -> render/<slug>.mp4
"""
import argparse, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, ".work")
VO_DIR = os.path.join(HERE, "..", "render", "vo")
OUT_DIR = os.path.join(HERE, "..", "render")
PY = sys.executable
FPS, W, H = 30, 1080, 1920

BED_DB = "-9"          # mức nhạc nền (-12 kín, -9 vừa, -5 rõ)
DUCK_RATIO = "3"
TARGET = (32.0, 38.0)  # độ dài chốt cho một file đăng cả 3 nền tảng


def run(cmd, **kw):
    print("»", " ".join(str(c) for c in cmd[:3]), "...", flush=True)
    subprocess.run(cmd, check=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--skip-tts", action="store_true", help="dùng lại giọng đã render, chỉ dựng lại hình")
    ap.add_argument("--no-verify", action="store_true", help="bỏ cổng Whisper cho nhanh")
    ap.add_argument("--vo-only", action="store_true", help="xuất thêm bản KHÔNG nhạc nền")
    ap.add_argument("--preview", action="store_true", help="xuất thêm bản 540x960 nhẹ để gửi duyệt")
    ap.add_argument("--tts-only", action="store_true",
                    help="chỉ chạy giọng rồi dừng — sửa chữ cho khớp độ dài thì dùng cái này, nhanh gấp 3")
    ap.add_argument("--force", action="store_true",
                    help="dựng kể cả khi độ dài ngoài khoảng chốt")
    a = ap.parse_args()

    cpath = os.path.abspath(a.content)

    # Soát cấu trúc TRƯỚC khi chạy TTS: lỗi chính tả trong file nội dung
    # hỏng trong 1 giây thay vì sau 100 giây dựng.
    import validate
    if not validate.check(cpath):
        raise SystemExit("❌ file nội dung có lỗi — sửa rồi chạy lại")

    slug = json.load(open(cpath, encoding="utf-8"))["slug"]
    os.makedirs(WORK, exist_ok=True); os.makedirs(VO_DIR, exist_ok=True); os.makedirs(OUT_DIR, exist_ok=True)

    vo = os.path.join(VO_DIR, f"{slug}.vo.wav")
    tim = os.path.join(VO_DIR, f"{slug}.timing.json")

    if not a.skip_tts:
        cmd = [PY, os.path.join(HERE, "tts.py"), cpath, VO_DIR]
        if a.no_verify: cmd.append("--no-verify")
        run(cmd)

    total = json.load(open(tim, encoding="utf-8"))["total"]
    print(f"== tổng {total:.2f}s", end="")
    if TARGET[0] <= total <= TARGET[1]:
        print(f"  ✅ trong khoảng chốt {TARGET[0]:.0f}–{TARGET[1]:.0f}s")
    else:
        print(f"  ⚠ NGOÀI khoảng chốt {TARGET[0]:.0f}–{TARGET[1]:.0f}s")
        if not a.force:
            # Dừng ngay. Dựng tiếp là ném đi 100 giây cho một file sẽ phải bỏ.
            raise SystemExit(
                f"❌ dừng. Sửa chữ trong {os.path.basename(cpath)} rồi chạy lại với --tts-only "
                f"(nhanh gấp 3) cho tới khi vào khoảng, sau đó dựng đầy đủ.\n"
                f"   Muốn dựng bằng mọi giá: thêm --force")

    if a.tts_only:
        print("── dừng ở đây (--tts-only)")
        return

    run([PY, os.path.join(HERE, "words.py"), tim, vo, os.path.join(WORK, "data.js")])
    run([PY, os.path.join(HERE, "deck.py"), cpath, os.path.join(WORK, "deck.js")])
    run([PY, os.path.join(HERE, "music.py"), str(total + 0.6)])
    run([PY, os.path.join(HERE, "chime.py"), os.path.join(WORK, "chime.wav")])
    shutil.copy(os.path.join(HERE, "scene.html"), os.path.join(WORK, "scene.html"))

    shoot(total)
    encode(slug, total, a)


def shoot(total):
    fr = os.path.join(WORK, "frames")
    shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    n = int(total * FPS)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + os.path.join(WORK, "scene.html"))
        try:
            pg.wait_for_function("() => !!window.seek")
        except Exception:
            raise SystemExit("scene.html không chạy được:\n  " + "\n  ".join(errs) or "không rõ lỗi")
        pg.wait_for_timeout(700)
        for i in range(n):
            pg.evaluate("t => window.seek(t)", i / FPS)
            pg.screenshot(path=os.path.join(fr, f"f{i:05d}.jpg"), type="jpeg", quality=90)
        b.close()
    print(f"   {n} khung")
    import safezone
    safezone.check(fr)


def encode(slug, total, a):
    vo = os.path.join(VO_DIR, f"{slug}.vo.wav")
    tim = json.load(open(os.path.join(VO_DIR, f"{slug}.timing.json"), encoding="utf-8"))
    outro = tim["segments"][-1]["start"]
    ch_ms = int(max(outro - 0.30, 0) * 1000)      # chuông vào trước tên kênh một nhịp
    fade = max(total - 1.05, 1.0)                 # nhạc chỉ tắt sau khi chuông ngân hết

    voch = ("aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            "highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=6:release=180")
    fc = (f"[0:v]format=yuv420p,eq=saturation=1.03[v];"
          f"[1:a]{voch},loudnorm=I=-15:TP=-1.5:LRA=9,asplit=2[vo1][vo2];"
          f"[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
          f"atrim=0:{total},volume={BED_DB}dB[bedq];"
          f"[bedq][vo2]sidechaincompress=threshold=0.03:ratio={DUCK_RATIO}:attack=12:"
          f"release=450:makeup=1[bd];"
          f"[3:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
          f"adelay={ch_ms}|{ch_ms},volume=-8dB[ch];"
          f"[vo1][bd][ch]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
          f"apad=whole_dur={total},atrim=0:{total},"      # sidechain+amix hay nuốt mất đuôi
          f"afade=t=out:st={fade:.2f}:d=1.0,"
          f"loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.97[a]")

    src = ["-framerate", str(FPS), "-i", os.path.join(WORK, "frames", "f%05d.jpg"),
           "-i", vo, "-i", os.path.join(WORK, "bed.wav"), "-i", os.path.join(WORK, "chime.wav")]
    mus = os.path.join(OUT_DIR, f"{slug}.mp4")     # BẢN CHÍNH — cả 3 nền tảng dùng chung
    run(["ffmpeg", "-y", "-loglevel", "error", *src, "-filter_complex", fc,
         "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "slow", "-crf", "21",
         "-maxrate", "4500k", "-bufsize", "9M",
         "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "224k", "-ar", "48000", "-t", str(total), mus], cwd=HERE)

    outs = [mus]
    if a.vo_only:
        only = os.path.join(OUT_DIR, f"{slug}.vo-only.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", mus, "-i", vo, "-filter_complex",
             f"[1:a]{voch},loudnorm=I=-14:TP=-1.5:LRA=9,apad=whole_dur={total},atrim=0:{total}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "224k",
             "-ar", "48000", "-movflags", "+faststart", only], cwd=HERE)
        outs.append(only)
    if a.preview:
        prev = os.path.join(OUT_DIR, f"{slug}.preview.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", mus,
             "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
             "-crf", "24", "-maxrate", "1400k", "-bufsize", "3M", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", prev], cwd=HERE)
        outs.append(prev)

    shutil.rmtree(os.path.join(WORK, "frames"), ignore_errors=True)
    print("\n" + "\n".join("✅ " + o for o in outs))
    print("   Facebook Reels · YouTube Shorts · TikTok — dùng chung file đầu tiên.")


if __name__ == "__main__":
    main()
