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

echo "── 2/5 · Chứng chỉ"
# Phần lớn máy không cần gì cả. Chỉ máy sau proxy MITM (vd mạng công ty) mới cần,
# vì uv và Python dùng CA store riêng, không thấy root CA mà tổ chức cài vào keychain.
# Cách nhận biết: thử một kết nối TLS bằng CA mặc định. Fail thì mới vá.
if python3 - <<'PROBE' 2>/dev/null
import urllib.request
urllib.request.urlopen("https://pypi.org/simple/", timeout=8).read(1)
PROBE
then
  echo "   TLS bình thường — không cần vá"
  rm -f ca-bundle.pem
else
  echo "   TLS bị chặn giữa đường (proxy MITM) — dựng ca-bundle.pem từ keychain"
  if [ "$(uname)" = "Darwin" ]; then
    security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain >  ca-bundle.pem 2>/dev/null || true
    security find-certificate -a -p /Library/Keychains/System.keychain                        >> ca-bundle.pem 2>/dev/null || true
    echo "   ca-bundle.pem: $(grep -c 'BEGIN CERTIFICATE' ca-bundle.pem) chứng chỉ"
  else
    echo "   ⚠ không phải macOS — tự trỏ SSL_CERT_FILE tới CA bundle của tổ chức bạn"
  fi
fi
if [ -f ca-bundle.pem ]; then
  export SSL_CERT_FILE="$PWD/ca-bundle.pem"
  export REQUESTS_CA_BUNDLE="$PWD/ca-bundle.pem"
  export NODE_EXTRA_CA_CERTS="$PWD/ca-bundle.pem"
  export UV_SYSTEM_CERTS=1
fi

echo "── 3/5 · Môi trường Python"
uv sync --system-certs
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
