#!/usr/bin/env bash
# Điểm chạy duy nhất. Tự kiểm tra môi trường, tự vá nếu thiếu, rồi mới dựng.
#
#   ./run.sh content/<slug>.json [--skip-tts] [--vo-only] [--no-verify]
#   ./run.sh --doctor        chỉ kiểm tra, không dựng
#
# Lần đầu trên máy mới: tự gọi bootstrap.sh, không cần ai nhớ.
set -uo pipefail
cd "$(dirname "$0")"

STAMP=".work/.health"
KEY="$( { shasum pyproject.toml 2>/dev/null || echo x; } | cut -c1-12 )-v1"
MODEL_CACHE="$HOME/.cache/huggingface"
FONT="$HOME/Library/Fonts/BeVietnamPro-Bold.ttf"
CHROME_DIR="$HOME/Library/Caches/ms-playwright"

fail=0; need=0; notes=()
chk() { # chk "tên" <điều kiện đã eval> <có tự vá được không>
  if [ "$2" = "1" ]; then printf "  ✓ %s\n" "$1"
  else
    if [ "${3:-1}" = "1" ]; then printf "  ⟳ %s — sẽ tự cài\n" "$1"; need=1
    else printf "  ✗ %s\n" "$1"; fail=1; fi
  fi
}

echo "── healthcheck"
chk "ffmpeg"            "$(command -v ffmpeg >/dev/null && echo 1 || echo 0)" 0
chk "uv"                "$(command -v uv      >/dev/null && echo 1 || echo 0)" 0
chk ".venv"             "$([ -x .venv/bin/python ] && echo 1 || echo 0)"
chk "font Be Vietnam"   "$([ -f "$FONT" ] && echo 1 || echo 0)"
chk "chromium"          "$(ls -d "$CHROME_DIR"/chromium* >/dev/null 2>&1 && echo 1 || echo 0)"
chk "phụ thuộc khớp"    "$([ "$(cat "$STAMP" 2>/dev/null)" = "$KEY" ] && echo 1 || echo 0)"

if [ "$fail" = "1" ]; then
  echo "❌ Thiếu công cụ hệ thống. Chạy:  brew install uv ffmpeg"; exit 1
fi

if [ "$need" = "1" ]; then
  echo "── môi trường chưa sẵn sàng, chạy bootstrap (một lần, ~5 phút)"
  ./bootstrap.sh || { echo "❌ bootstrap thất bại"; exit 1; }
  mkdir -p .work && echo "$KEY" > "$STAMP"
  echo "── bootstrap xong"
fi

# chỉ máy sau proxy MITM mới có file này (bootstrap tự quyết)
if [ -f ca-bundle.pem ]; then
  export SSL_CERT_FILE="$PWD/ca-bundle.pem"
  export REQUESTS_CA_BUNDLE="$PWD/ca-bundle.pem"
fi

# kiểm tra import thật — bắt được venv hỏng mà thư mục vẫn còn
if ! ./.venv/bin/python -c "import vieneu, faster_whisper, playwright, numpy, scipy" 2>/dev/null; then
  echo "── .venv thiếu gói, cài lại"
  ./bootstrap.sh || exit 1
  mkdir -p .work && echo "$KEY" > "$STAMP"
fi

if [ ! -d "$MODEL_CACHE" ] || [ "$(du -sm "$MODEL_CACHE" 2>/dev/null | cut -f1)" -lt 800 ]; then
  echo "  ⓘ Model chưa có đủ trong cache — lần chạy này sẽ tải ~1GB (VieNeu + Whisper), chậm hơn bình thường."
fi

[ "${1:-}" = "--doctor" ] && { echo "✅ môi trường sẵn sàng"; exit 0; }
[ $# -eq 0 ] && { echo "Dùng: ./run.sh content/<slug>.json"; exit 1; }

echo "── dựng"
exec ./.venv/bin/python build.py "$@"
