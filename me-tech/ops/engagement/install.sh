#!/usr/bin/env bash
# Cài đặt hoặc gỡ Auto Engagement Bot vào launchd (tài khoản người dùng, không cần sudo).
#   ./install.sh            cài / cài lại (tự động nhận diện thư mục repo hiện tại)
#   ./install.sh --remove   gỡ
set -euo pipefail

LABEL="com.me.engagement"
PL="$HOME/Library/LaunchAgents/$LABEL.plist"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RUNNER_SH="$SCRIPT_DIR/cron_schedule.sh"
LOG_FILE="$SCRIPT_DIR/logs/engagement_bot.log"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true

if [[ ${1:-} == "--remove" ]]; then
    rm -f "$PL"
    echo "✓ Đã gỡ $LABEL khỏi launchd"
    exit 0
fi

mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$HOME/Library/LaunchAgents"

# 4 khung giờ quét sau giờ đăng: 08:30 · 12:30 · 16:30 · 20:30
INTERVALS=""
for hm in 8:30 12:30 16:30 20:30; do
    INTERVALS+="<dict><key>Hour</key><integer>${hm%:*}</integer><key>Minute</key><integer>${hm#*:}</integer></dict>"
done

cat > "$PL" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>WorkingDirectory</key>
    <string>$REPO_DIR</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$RUNNER_SH</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        $INTERVALS
    </array>
    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>
    <key>StandardErrorPath</key>
    <string>$LOG_FILE</string>
</dict>
</plist>
EOF

plutil -lint "$PL"
launchctl bootstrap "gui/$(id -u)" "$PL"

echo "✓ Đã cài $LABEL thành công trên máy này!"
echo "  - Script chạy: $RUNNER_SH"
echo "  - File log: $LOG_FILE"
launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|path" | head -3 || true
