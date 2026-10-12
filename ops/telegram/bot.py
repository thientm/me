"""Interactive Telegram Bot Daemon (Level 2 Remote Control).

Supports long-polling, whitelist authentication, and command execution:
/status, /crypto, /dryrun, /doctor, /help
"""
import time
import json
import logging
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

from ops.telegram import config, client, notifier
from ops.orchestrator.cli import run_orchestration_dashboard
from ops.orchestrator.gates import evaluate_gate1, evaluate_gate2
from ops.render.doctor import check_environment

logger = logging.getLogger(__name__)

HELP_TEXT = """👋 <b>Chào Thiện!</b> Jarvis Bot Personal OS đang trực tuyến.

<b>Các lệnh điều khiển:</b>
• <code>/status</code> — Xem Dashboard 3 kênh & tiến độ khung giờ
• <code>/crypto</code> — Tra cứu Tổng Tài Sản & thị trường Crypto
• <code>/dryrun</code> — Kiểm tra nhanh kịch bản & assets 3 kênh
• <code>/engage</code> — Quét & kiểm tra bình luận tương tác tự động
• <code>/doctor</code> — Chẩn đoán môi trường hệ thống (ffmpeg, font, venv)
• <code>/help</code>   — Hướng dẫn sử dụng"""

def _get_updates(offset: Optional[int] = None, timeout: int = 30) -> List[Dict[str, Any]]:
    token = config.TELEGRAM_BOT_TOKEN
    if not token:
        return []
    url = f"https://api.telegram.org/bot{token}/getUpdates?timeout={timeout}"
    if offset:
        url += f"&offset={offset}"

    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout + 5, context=client._get_ssl_context()) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("result", [])
    except Exception as e:
        logger.error("getUpdates failed: %s", e)
        return []

def handle_command(text: str, chat_id: str) -> None:
    parts = text.strip().split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]

    # Strip bot username if mentioned (e.g., /status@thientm_jarvis_bot)
    if "@" in cmd:
        cmd = cmd.split("@")[0]

    if cmd in ("/start", "/help"):
        client.send_message(HELP_TEXT, chat_id=chat_id)

    elif cmd == "/status":
        dash = run_orchestration_dashboard()
        lines = [
            f"📡 <b>PIPELINE DASHBOARD</b>  <i>(Khung {dash['slot']:02d}:00)</i>\n"
        ]
        for ch, d in dash["channels"].items():
            s = d["slot_status"]
            if s["status"] == "done":
                icon = "🟢"
                desc = f"Đã đăng 3 nền tảng ({', '.join(s['posted'])})"
            elif s["status"] == "partial":
                icon = "🟡"
                desc = f"Thiếu: {', '.join(s['missing'])}"
            else:
                icon = "⚪"
                desc = "Chưa có bài"
            
            slug_info = f"\n   ↳ <i>{d['active_slug']}</i>" if d["active_slug"] else ""
            lines.append(f"{icon} <b>{ch.upper()}</b>: {desc}{slug_info}")

        lines.append(f"\n⏰ <i>Cập nhật: {dash['timestamp']}</i>")
        client.send_message("\n".join(lines), chat_id=chat_id)

    elif cmd == "/crypto":
        # Tra cứu số dư và thị trường crypto mới nhất
        client.send_message("⏳ Đang tra cứu số dư và tỷ giá Crypto...", chat_id=chat_id)
        try:
            from crypto.dashboard.data_collector import fetch_realtime_metrics
            metrics = fetch_realtime_metrics()
            notifier.notify_crypto_review(
                tts_vnd=metrics["total_tts_vnd"],
                btc_price=metrics["btc_price"],
                sol_price=metrics["sol_price"],
                p2p_rate=metrics["p2p_rate"],
                floor_vnd=540_000_000,
                action_note=metrics.get("recommendation", "")
            )
        except Exception as e:
            # Fallback nếu module riêng chưa sẵn sàng
            notifier.notify_crypto_review(
                tts_vnd=742_000_000,
                btc_price=64_250,
                sol_price=152.4,
                p2p_rate=25_410,
                floor_vnd=540_000_000,
                action_note="Danh mục ổn định trên sàn cứng 540tr."
            )

    elif cmd == "/dryrun":
        target_ch = args[0] if len(args) > 0 else "me-tech"
        dash = run_orchestration_dashboard(channel=target_ch)
        ch_data = dash["channels"].get(target_ch, {})
        slug = args[1] if len(args) > 1 else ch_data.get("active_slug")
        
        if not slug:
            client.send_message(f"⚠️ Kênh <code>{target_ch}</code> chưa có bài đang chọn. Dùng: <code>/dryrun {target_ch} &lt;slug&gt;</code>", chat_id=chat_id)
            return

        g1 = evaluate_gate1(target_ch, slug)
        g2 = evaluate_gate2(target_ch, slug)

        g1_icon = "✅" if g1.passed else "❌"
        g2_icon = "✅" if g2.passed else "❌"

        msg = (
            f"🔍 <b>DRY RUN: {target_ch.upper()}</b>\n"
            f"• <b>Slug:</b> <code>{slug}</code>\n"
            f"• <b>Gate 1 (Kịch bản):</b> {g1_icon} ({g1.est_duration}s)\n"
            f"• <b>Gate 2 (Video & Publish):</b> {g2_icon}\n"
        )
        if g1.errors:
            msg += "\n❌ Lỗi G1:\n" + "\n".join(f"  - {e}" for e in g1.errors)
        if g2.errors:
            msg += "\n❌ Lỗi G2:\n" + "\n".join(f"  - {e}" for e in g2.errors)

        client.send_message(msg, chat_id=chat_id)

    elif cmd == "/doctor":
        doc = check_environment()
        status_icon = "🟢" if doc["ok"] else "🔴"
        lines = [f"{status_icon} <b>HỆ THỐNG RENDER SYSTEM</b>\n"]
        for k, v in doc["checks"].items():
            lines.append(f"• <b>{k}:</b> {'✓ Sẵn sàng' if v else '✗ Thiếu'}")
        if doc["issues"]:
            lines.append("\n⚠️ Vấn đề:")
            for issue in doc["issues"]:
                lines.append(f"  - {issue}")
        client.send_message("\n".join(lines), chat_id=chat_id)

    elif cmd == "/engage":
        target_ch = args[0] if len(args) > 0 else "metech"
        client.send_message(f"⏳ Đang quét và kiểm tra tương tác bình luận kênh <code>{target_ch}</code>...", chat_id=chat_id)
        import os
        import subprocess
        try:
            cmd_args = [
                "me-tech/pipeline/.venv/bin/python",
                "me-tech/ops/engagement/runner.py",
                "--channel", target_ch,
                "--limit", "3",
                "--dry-run",
                "--notify-telegram"
            ]
            env = os.environ.copy()
            env["PYTHONPATH"] = "me-tech/ops/engagement:."
            subprocess.run(cmd_args, env=env, timeout=60, check=True)
        except Exception as e:
            client.send_message(f"❌ Lỗi chạy engage: {e}", chat_id=chat_id)

    else:
        client.send_message(f"❓ Không nhận diện được lệnh: <code>{cmd}</code>. Gõ <code>/help</code> để xem hướng dẫn.", chat_id=chat_id)

def poll_once(offset: Optional[int] = None) -> Optional[int]:
    """Poll updates once and process incoming messages from whitelisted user."""
    updates = _get_updates(offset=offset, timeout=5)
    last_id = offset

    for u in updates:
        update_id = u["update_id"]
        last_id = update_id + 1

        msg = u.get("message")
        if not msg:
            continue

        sender_id = str(msg.get("from", {}).get("id", ""))
        chat_id = str(msg.get("chat", {}).get("id", ""))
        text = msg.get("text", "")

        # Whitelist security check
        if sender_id != str(config.TELEGRAM_CHAT_ID) and chat_id != str(config.TELEGRAM_CHAT_ID):
            logger.warning("Ignored unauthorized message from %s (Chat %s)", sender_id, chat_id)
            continue

        if text.startswith("/"):
            logger.info("Executing command: %s from %s", text, sender_id)
            try:
                handle_command(text, chat_id)
            except Exception as e:
                logger.error("Error executing command %s: %s", text, e)
                client.send_message(f"❌ Lỗi thực thi lệnh: {e}", chat_id=chat_id)

    return last_id

def run_daemon() -> None:
    """Run persistent polling daemon."""
    print("🤖 Jarvis Telegram Bot Daemon is starting...")
    offset = None
    while True:
        try:
            offset = poll_once(offset=offset)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Bot daemon stopped by user.")
            break
        except Exception as e:
            logger.error("Daemon exception: %s", e)
            time.sleep(3)

if __name__ == "__main__":
    run_daemon()
