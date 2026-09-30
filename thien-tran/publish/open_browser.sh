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

# 30.09.2026: mở nền + thu nhỏ, không cướp chuột — xem me-tech/ops/open_chrome.py
exec python3 "$(cd "$(dirname "$0")" && git rev-parse --show-toplevel)/me-tech/ops/open_chrome.py" 9444
