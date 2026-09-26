#!/usr/bin/env bash
# Mở Google Chrome với profile riêng cho kênh Thiện Trần
# Lưu toàn bộ phiên đăng nhập (YouTube Studio, TikTok Creator, Facebook Reels)
# Profile nằm ngay tại thien-tran/.browser (đã được .gitignore bảo vệ tuyệt đối)

DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="$DIR/.browser"
PORT=9444

mkdir -p "$PROFILE"

echo "🚀 Đang mở Chrome cho kênh Thiện Trần..."
echo "📂 Profile: $PROFILE"
echo "🔌 Debug Port: $PORT"

exec "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --user-data-dir="$PROFILE" \
  --remote-debugging-port=$PORT \
  --no-first-run \
  --no-default-browser-check \
  "https://studio.youtube.com" \
  "https://www.tiktok.com/tiktokstudio/upload" \
  "https://business.facebook.com"
