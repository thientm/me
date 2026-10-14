#!/usr/bin/env bash
# Quản lý Jarvis Telegram Bot daemon
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PID_FILE="$DIR/ops/telegram/.bot.pid"
LOG_FILE="$DIR/ops/telegram/bot.log"

case "$1" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "🤖 Jarvis Bot is already running (PID: $(cat "$PID_FILE"))."
      exit 0
    fi
    echo "🚀 Starting Jarvis Telegram Bot daemon..."
    cd "$DIR"
    nohup python3 -u -m ops.telegram.bot > "$LOG_FILE" 2>&1 &
    PID=$!
    disown $PID
    echo $PID > "$PID_FILE"
    echo "✓ Bot started with PID $PID (logs: $LOG_FILE)"
    ;;

  stop)
    if [ -f "$PID_FILE" ]; then
      PID=$(cat "$PID_FILE")
      if kill -0 "$PID" 2>/dev/null; then
        echo "🛑 Stopping Jarvis Bot (PID: $PID)..."
        kill "$PID"
        rm -f "$PID_FILE"
        echo "✓ Bot stopped."
      else
        echo "⚠️ Bot PID file exists but process is not running. Removing stale PID file."
        rm -f "$PID_FILE"
      fi
    else
      echo "Bot is not running."
    fi
    ;;

  status)
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "🟢 Jarvis Bot is RUNNING (PID: $(cat "$PID_FILE"))."
    else
      echo "⚪ Jarvis Bot is STOPPED."
    fi
    ;;

  restart)
    $0 stop
    sleep 1
    $0 start
    ;;

  *)
    echo "Dùng: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac
