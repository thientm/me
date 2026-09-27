#!/usr/bin/env bash
# Mở Google Chrome với profile riêng cho Tâm An Lạc
# Lưu toàn bộ phiên đăng nhập (YouTube Studio, TikTok Creator, Facebook Reels)

DIR="$(cd "$(dirname "$0")" && pwd)"
PROFILE="$DIR/chrome_profile"
PORT=9555

mkdir -p "$PROFILE"

echo "🚀 Đang mở Chrome cho kênh Tâm An Lạc..."
echo "📂 Profile: $PROFILE"
echo "🔌 Debug Port: $PORT"

exec "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --user-data-dir="$PROFILE" \
  --remote-debugging-port=$PORT \
  --no-first-run \
  --no-default-browser-check \
  "https://studio.youtube.com" \
  "https://www.tiktok.com/creator-center/upload?from=upload" \
  "https://business.facebook.com"
