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

# 30.09.2026: mở nền + thu nhỏ, không cướp chuột — xem me-tech/ops/open_chrome.py
exec python3 "$(cd "$(dirname "$0")" && git rev-parse --show-toplevel)/me-tech/ops/open_chrome.py" 9555
