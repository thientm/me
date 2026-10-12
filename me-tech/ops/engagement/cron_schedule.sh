#!/usr/bin/env bash
set -euo pipefail

# Di chuyển về thư mục gốc của repository
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_DIR"

LOG_FILE="$REPO_DIR/me-tech/ops/engagement/logs/engagement_bot.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Khởi động Auto Engagement Bot ===" >> "$LOG_FILE"

# Sử dụng uv python
UV_BIN="$HOME/.local/bin/uv"
if [ ! -f "$UV_BIN" ]; then
    UV_BIN="$(which uv || true)"
fi

if [ -z "$UV_BIN" ]; then
    echo "[LỖI] Không tìm thấy uv trong hệ thống!" >> "$LOG_FILE"
    exit 1
fi

# Chạy runner
export PYTHONPATH="me-tech/ops/engagement"
"$UV_BIN" run --with playwright python me-tech/ops/engagement/runner.py "$@" >> "$LOG_FILE" 2>&1 || {
    echo "[CẢNH BÁO] Quá trình engagement gặp lỗi hoặc hoãn do lock." >> "$LOG_FILE"
}

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Kết thúc phiên Engagement ===" >> "$LOG_FILE"
