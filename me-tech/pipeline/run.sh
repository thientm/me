#!/usr/bin/env bash
# Bọc build.py kèm biến môi trường chứng chỉ — dùng cái này thay vì gọi python trực tiếp.
#   ./run.sh content/<slug>.json [--skip-tts] [--vo-only] [--no-verify]
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || { echo "❌ chưa có .venv — chạy ./bootstrap.sh trước"; exit 1; }
export SSL_CERT_FILE="$PWD/ca-bundle.pem"
export REQUESTS_CA_BUNDLE="$PWD/ca-bundle.pem"
exec ./.venv/bin/python build.py "$@"
