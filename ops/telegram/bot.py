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
• <code>/crypto</code> — Quản trị rủi ro & danh mục Crypto (Sàn 500tr, Cơ cấu coin, Bảng lệnh 10p)
• <code>/review</code> — Master Review ALL toàn bộ hệ thống (Tài chính, BĐS 3.1 tỷ, Crypto, Video 3 kênh)
• <code>/status</code> — Xem Dashboard 3 kênh video & tiến độ khung giờ
• <code>/dryrun</code> — Kiểm tra nhanh kịch bản & assets 3 kênh video
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
    except urllib.error.HTTPError as e:
        if e.code == 409:
            logger.warning("getUpdates 409 Conflict: another instance is running. Backing off 25s...")
            time.sleep(25)
        else:
            logger.error("getUpdates HTTP error %s: %s", e.code, e)
            time.sleep(5)
        return []
    except Exception as e:
        logger.error("getUpdates failed: %s", e)
        time.sleep(3)
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
        # Tra cứu số dư và quản trị rủi ro danh mục crypto (thuần túy Crypto)
        client.send_message("⏳ Đang tra cứu danh mục Crypto & tính toán quản trị rủi ro...", chat_id=chat_id)
        try:
            from crypto.dashboard.data_collector import fetch_realtime_metrics
            metrics = fetch_realtime_metrics()
            notifier.notify_crypto_review(
                tts_vnd=metrics["total_tts_vnd"],
                btc_price=metrics["btc_price"],
                sol_price=metrics["sol_price"],
                p2p_rate=metrics["p2p_rate"],
                floor_vnd=metrics.get("floor_vnd", 500_000_000),
                action_note=metrics.get("recommendation", ""),
                chat_id=chat_id,
                crypto_data=metrics,
            )
        except Exception as e:
            logger.error("Lỗi tra cứu crypto: %s", e, exc_info=True)
            client.send_message(f"❌ Không thể tra cứu dữ liệu Crypto: {e}", chat_id=chat_id)

    elif cmd in ("/review", "/all"):
        # Master Review ALL: Toàn bộ Personal OS (Tài chính, BĐS 3.1 tỷ, Crypto, Video 3 kênh)
        client.send_message("⏳ Đang chạy Personal OS Master Review (ALL: Tài chính, BĐS, Crypto, Video)...", chat_id=chat_id)
        try:
            from crypto.dashboard.data_collector import run_master_review_all
            review_all = run_master_review_all()
            notifier.notify_master_review(
                review_all_data=review_all,
                chat_id=chat_id,
            )
        except Exception as e:
            logger.error("Lỗi chạy Master Review ALL: %s", e, exc_info=True)
            client.send_message(f"❌ Không thể chạy Master Review: {e}", chat_id=chat_id)

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

BOT_COMMANDS = [
    {"command": "crypto", "description": "💰 Quản trị Crypto & tỷ giá live (Sàn 500tr)"},
    {"command": "review", "description": "📑 Master Review ALL (Tài chính, BĐS, Crypto, Video)"},
    {"command": "status", "description": "📊 Dashboard 3 kênh video & tiến độ khung giờ"},
    {"command": "engage", "description": "💬 Quét & tương tác bình luận tự động"},
    {"command": "dryrun", "description": "🔍 Kiểm tra Gate 1 & Gate 2 kịch bản video"},
    {"command": "doctor", "description": "🩺 Kiểm tra sức khỏe môi trường (ffmpeg, chrome)"},
    {"command": "help", "description": "❓ Hướng dẫn sử dụng bot & danh sách lệnh"}
]

def register_bot_commands() -> bool:
    """Register commands with Telegram Bot API so they appear in autocomplete menu."""
    token = config.TELEGRAM_BOT_TOKEN
    if not token:
        return False
    url = f"https://api.telegram.org/bot{token}/setMyCommands"
    payload = json.dumps({"commands": BOT_COMMANDS}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10, context=client._get_ssl_context()) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("ok", False)
    except Exception as e:
        logger.warning("Could not register bot commands: %s", e)
        return False

def run_daemon() -> None:
    """Run persistent polling daemon."""
    print("🤖 Jarvis Telegram Bot Daemon is starting...")
    if register_bot_commands():
        print("✅ Đã đồng bộ danh sách lệnh lên menu Telegram.")
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
