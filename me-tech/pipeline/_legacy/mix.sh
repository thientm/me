#!/usr/bin/env bash
# Ghép voiceover + nhạc nền vào video đã dựng.
# Dùng: ./mix.sh <slug> <vo.wav|vo.mp3> [bed.wav] [delay_ms]
#
# Nhạc tự động né giọng đọc (sidechain ducking): khi có tiếng nói, nhạc tụt xuống.
set -euo pipefail
SLUG="${1:?can slug}"; VO="${2:?can file voiceover}"; BED="${3:-bed.wav}"; DELAY="${4:-1300}"
SRC="${SLUG}_mute.mp4"; [ -f "$SRC" ] || SRC="${SLUG}_silent.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC" | cut -d. -f1)

# Đẩy giọng trễ DELAY ms cho khớp hình, rồi đệm im lặng cho đủ độ dài video
ffmpeg -y -loglevel error -i "$VO" -af "adelay=${DELAY}|${DELAY},apad=whole_dur=${DUR}" -ar 48000 /tmp/_vo_pad.wav

VOCHAIN="aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,highpass=f=85,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=6:release=180"

# Bản có nhạc — Facebook Reels + YouTube Shorts
ffmpeg -y -i "$SRC" -i /tmp/_vo_pad.wav -i "$BED" -filter_complex "\
[1:a]${VOCHAIN},loudnorm=I=-15:TP=-1.5:LRA=9,asplit=2[vo1][vo2];\
[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,atrim=0:${DUR},volume=-19dB[bedq];\
[bedq][vo2]sidechaincompress=threshold=0.05:ratio=9:attack=8:release=380:makeup=1[bedduck];\
[vo1][bedduck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,\
alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 224k -ar 48000 -movflags +faststart "${SLUG}_vo_music.mp4"

# Bản chỉ giọng — TikTok, add sound native đè lên
ffmpeg -y -loglevel error -i "$SRC" -i /tmp/_vo_pad.wav -filter_complex \
"[1:a]${VOCHAIN},loudnorm=I=-14:TP=-1.5:LRA=9[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 224k -ar 48000 -movflags +faststart "${SLUG}_vo_only.mp4"

rm -f /tmp/_vo_pad.wav
ls -lh "${SLUG}"_vo_*.mp4
