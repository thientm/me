#!/bin/bash
# Cài giám sát viên Mê Tech vào launchd (tài khoản người dùng, không cần sudo).
#   ./install.sh            cài / cài lại
#   ./install.sh --remove   gỡ
# Log: ~/Library/Logs/metech-watchdog.log
set -eu
LABEL=com.metech.watchdog
PL=$HOME/Library/LaunchAgents/$LABEL.plist
SH="$(cd "$(dirname "$0")" && pwd)/watchdog.sh"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
if [[ ${1:-} == --remove ]]; then rm -f "$PL"; echo "đã gỡ $LABEL"; exit 0; fi

# 3 lượt mỗi khung: HH:40 · HH:55 · 10 phút sau giờ đăng. launchd tự chạy bù
# một lần nếu máy ngủ đúng lúc hẹn.
ITEMS=""
for hm in 7:40 7:55 8:10 11:40 11:55 12:10 19:40 19:55 20:10; do
  ITEMS+="<dict><key>Hour</key><integer>${hm%:*}</integer><key>Minute</key><integer>${hm#*:}</integer></dict>"
done
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PL" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$SH</string></array>
  <key>StartCalendarInterval</key><array>$ITEMS</array>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/metech-watchdog.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/metech-watchdog.log</string>
</dict></plist>
EOF
plutil -lint "$PL"
launchctl bootstrap "gui/$(id -u)" "$PL"
echo "đã cài $LABEL → $SH"
launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|path" | head -3
