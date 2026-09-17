#!/usr/bin/env bash
# Mê Tech — dựng reel 9:16 từ HTML animation
# Dùng: ./build.sh <slug>      (vd: ./build.sh gemini-live)
set -euo pipefail
SLUG="${1:?can slug, vd: ./build.sh gemini-live}"
AUDIO="${2:-bed.wav}"          # truyền mp3 riêng nếu muốn thay nhạc

node scene.js                                   # scene.js  -> video.html
python3 music.py                                # -> bed.wav (bỏ qua nếu dùng nhạc ngoài)
node capture.js full                            # -> frames/*.jpg  (30fps)

ffmpeg -y -framerate 30 -i frames/f%05d.jpg -i "$AUDIO" \
  -filter_complex "[0:v]format=yuv420p,eq=saturation=1.04:contrast=1.03[v];\
[1:a]atrim=0:32,afade=t=out:st=30:d=2,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 21 -maxrate 4500k -bufsize 9M \
  -profile:v high -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 224k -ar 48000 -shortest "${SLUG}_music.mp4"

ffmpeg -y -i "${SLUG}_music.mp4" -an -c:v copy -movflags +faststart "${SLUG}_mute.mp4"
rm -rf frames
ls -lh "${SLUG}"_*.mp4
