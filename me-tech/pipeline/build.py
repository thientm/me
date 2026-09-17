#!/usr/bin/env python3
"""Dựng một video Mê Tech từ file nội dung.

    python build.py content/gemini-live.json

Thứ tự: giọng đọc trước, timeline suy ra từ giọng, rồi mới dựng hình.
Không có mốc thời gian nào viết tay.

    content/<slug>.json ──► tts.py ──► <slug>.vo.wav + <slug>.timing.json
                                          │
                                          ├─► render.py ──► frames/
                                          └─► music.py  ──► bed.wav
                                                  │
                                                  └─► ffmpeg ──► <slug>_music.mp4
                                                                 <slug>_vo_only.mp4
"""
import json, os, subprocess, sys, shutil, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
WORK   = os.path.join(HERE, ".work")
VO_DIR = os.path.join(HERE, "..", "render", "vo")
OUT_DIR = os.path.join(HERE, "..", "render")
BED_DB = "-9"           # mức nhạc nền (-12 kín, -9 vừa, -5 rõ)
DUCK_RATIO = "3"        # nhạc né giọng: càng cao càng né mạnh (9 = biến mất)
# ngưỡng 0.03 để cả những chữ nói nhỏ ở cuối câu cũng đẩy được nhạc xuống;
# release 450ms để nhạc không trồi lên giữa lúc câu chưa dứt

def run(cmd, **kw):
    print("»", " ".join(str(c) for c in cmd[:4]), "...", flush=True)
    subprocess.run(cmd, check=True, **kw)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--skip-tts", action="store_true", help="dùng lại giọng đã render, chỉ dựng lại hình")
    ap.add_argument("--no-verify", action="store_true", help="bỏ cổng Whisper cho nhanh")
    ap.add_argument("--vo-only", action="store_true",
                    help="xuất thêm bản KHÔNG nhạc nền (chỉ dùng khi muốn đè sound native của TikTok)")
    a = ap.parse_args()
    cpath = os.path.abspath(a.content)
    slug = json.load(open(cpath, encoding="utf-8"))["slug"]
    skip_tts = a.skip_tts

    vo = os.path.join(VO_DIR, f"{slug}.vo.wav")
    tim = os.path.join(VO_DIR, f"{slug}.timing.json")

    if not skip_tts:
        cmd = [PY, os.path.join(HERE, "tts.py"), cpath, VO_DIR]
        if a.no_verify: cmd.append("--no-verify")
        run(cmd)
    man = json.load(open(tim, encoding="utf-8"))
    total = man["total"]
    last_end = man["segments"][-1]["end"]
    print(f"== tổng {total:.2f}s, câu cuối kết thúc {last_end:.2f}s")

    run([PY, os.path.join(HERE, "render.py"), tim, vo])
    run([PY, os.path.join(HERE, "music.py"), str(total + 0.6)])

    fade = f"{max(last_end + 0.45, total - 2.4):.2f}"   # chỉ fade SAU khi câu cuối nói xong
    # giọng TTS vốn đã sạch — không cần khử nhiễu
    voch = ("aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            "highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=6:release=180")
    fc = (f"[0:v]format=yuv420p,eq=saturation=1.04:contrast=1.03[v];"
          f"[1:a]{voch},loudnorm=I=-15:TP=-1.5:LRA=9,asplit=2[vo1][vo2];"
          f"[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
          f"atrim=0:{total},volume={BED_DB}dB[bedq];"
          f"[bedq][vo2]sidechaincompress=threshold=0.03:ratio={DUCK_RATIO}:attack=12:release=450:makeup=1[bedduck];"
          f"[vo1][bedduck]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
          f"apad=whole_dur={total},atrim=0:{total},"          # sidechain+amix hay nuốt mất phần đuôi
          f"afade=t=out:st={fade}:d=1.6,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.97[a]")

    mus = os.path.join(OUT_DIR, f"{slug}.mp4")           # BẢN CHÍNH — dùng cho cả 3 nền tảng
    run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",os.path.join(WORK,"frames","f%05d.jpg"),
         "-i",vo,"-i",os.path.join(WORK,"bed.wav"),"-filter_complex",fc,"-map","[v]","-map","[a]",
         "-c:v","libx264","-preset","slow","-crf","21","-maxrate","4500k","-bufsize","9M",
         "-profile:v","high","-pix_fmt","yuv420p","-movflags","+faststart",
         "-c:a","aac","-b:a","224k","-ar","48000","-t",str(total),mus], cwd=HERE)

    outs = [mus]
    if a.vo_only:
        only = os.path.join(OUT_DIR, f"{slug}.vo-only.mp4")
        run(["ffmpeg","-y","-loglevel","error","-i",mus,"-i",vo,"-filter_complex",
             f"[1:a]{voch},loudnorm=I=-14:TP=-1.5:LRA=9,apad=whole_dur={total},atrim=0:{total}[a]",
             "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","224k","-ar","48000",
             "-movflags","+faststart",only], cwd=HERE)
        outs.append(only)

    shutil.rmtree(os.path.join(WORK,"frames"), ignore_errors=True)
    print("\n" + "\n".join("✅ " + o for o in outs))
    print("   Facebook Reels · YouTube Shorts · TikTok — dùng chung file đầu tiên.")

if __name__ == "__main__":
    main()
