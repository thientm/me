#!/usr/bin/env bash
# Cài đặt một lần trên máy mới. Chạy lại được nhiều lần, không hỏng gì.
#   ./bootstrap.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "── 1/5 · Kiểm tra công cụ"
for c in uv ffmpeg; do
  command -v "$c" >/dev/null || { echo "❌ thiếu $c — cài bằng: brew install $c"; exit 1; }
done
echo "   uv, ffmpeg ✓"

echo "── 2/5 · Chứng chỉ (máy công ty có proxy MITM)"
# uv và Python dùng CA store riêng, không thấy root CA công ty cài trong keychain
if [ ! -f ca-bundle.pem ]; then
  security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain >  ca-bundle.pem 2>/dev/null || true
  security find-certificate -a -p /Library/Keychains/System.keychain                        >> ca-bundle.pem 2>/dev/null || true
fi
N=$(grep -c "BEGIN CERTIFICATE" ca-bundle.pem 2>/dev/null || echo 0)
echo "   ca-bundle.pem: $N chứng chỉ"
export SSL_CERT_FILE="$PWD/ca-bundle.pem"
export REQUESTS_CA_BUNDLE="$PWD/ca-bundle.pem"
export NODE_EXTRA_CA_CERTS="$PWD/ca-bundle.pem"
export UV_NATIVE_TLS=1

echo "── 3/5 · Môi trường Python"
uv sync --native-tls
echo "   .venv ✓"

echo "── 4/5 · Chromium cho Playwright"
./.venv/bin/playwright install chromium

echo "── 5/5 · Font Be Vietnam Pro"
mkdir -p ~/Library/Fonts
for v in Regular Medium SemiBold Bold ExtraBold Black; do
  f="$HOME/Library/Fonts/BeVietnamPro-$v.ttf"
  [ -f "$f" ] || curl -sS -L -o "$f" \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/bevietnampro/BeVietnamPro-$v.ttf"
done
echo "   font ✓"

cat <<'TXT'

✅ Xong. Chạy thử:

   ./run.sh content/gemini-live.json

Lần chạy đầu sẽ tải model (VieNeu ~580MB, Whisper ~460MB) rồi cache lại.
TXT
