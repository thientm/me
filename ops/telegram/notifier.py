"""Message formatter and notifier for Personal OS domains."""
import html
from datetime import datetime
from typing import Dict, Any, Optional

from ops.telegram import client

def _format_vnd(amount: float) -> str:
    return f"{int(amount):,}".replace(",", ".")

def notify_crypto_review(
    tts_vnd: float,
    btc_price: float,
    sol_price: float,
    p2p_rate: float,
    floor_vnd: float = 540_000_000,
    action_note: str = "",
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send Crypto Daily Review card."""
    now_str = datetime.now().strftime("%d/%m/%Y")
    diff_floor = tts_vnd - floor_vnd
    
    if diff_floor >= 0:
        floor_status = f"✅ An toàn (+{_format_vnd(diff_floor)} VND)"
    else:
        floor_status = f"⚠️ Thủng {_format_vnd(abs(diff_floor))} VND"

    card = (
        f"📊 <b>CRYPTO DAILY REVIEW — {now_str}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Tổng tài sản (TTS):</b> {_format_vnd(tts_vnd)} VND\n"
        f"🛡️ <b>Sàn cứng kỷ luật:</b> {_format_vnd(floor_vnd)} VND ({floor_status})\n"
        f"📈 <b>Tỷ giá & Thị trường:</b>\n"
        f"  • BTC: ${btc_price:,.0f}\n"
        f"  • SOL: ${sol_price:,.2f}\n"
        f"  • P2P USDT: {_format_vnd(p2p_rate)} VND\n"
    )

    if action_note:
        card += (
            f"🚨 <b>Khuyến nghị hành động:</b>\n"
            f"  👉 {html.escape(action_note)}\n"
        )

    card += (
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ <i>Hạn chót bảo toàn vốn: 31/10/2026</i>"
    )

    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)

def notify_pipeline_status(
    slot: str,
    channel: str,
    slug: Optional[str] = None,
    gates: Optional[Dict[str, bool]] = None,
    next_slot: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send Video Pipeline status card."""
    card = (
        f"🎬 <b>VIDEO PIPELINE — KHUNG GIỜ {html.escape(slot)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📺 <b>Kênh:</b> {html.escape(channel)}\n"
    )

    if slug:
        card += f"📌 <b>Chủ đề:</b> <code>{html.escape(slug)}</code>\n"

    if gates:
        card += "🚦 <b>Trạng thái các Gate:</b>\n"
        for gate_name, passed in gates.items():
            icon = "✅ PASS" if passed else "❌ FAILED"
            card += f"  • {html.escape(gate_name)}: {icon}\n"

    card += "━━━━━━━━━━━━━━━━━━━━\n"
    if next_slot:
        card += f"⏰ <i>Slot kế tiếp: {html.escape(next_slot)}</i>"
    else:
        card += "🚀 <i>Personal OS Automation</i>"

    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)

def notify_alert(
    source: str,
    error_msg: str,
    action_needed: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send urgent alert card."""
    card = (
        f"🚨 <b>CẢNH BÁO HỆ THỐNG — {html.escape(source)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"❌ <b>Lỗi phát hiện:</b>\n"
        f"<code>{html.escape(error_msg)}</code>\n"
    )

    if action_needed:
        card += (
            f"🛠️ <b>Hành động cần làm:</b>\n"
            f"👉 {html.escape(action_needed)}\n"
        )

    card += "━━━━━━━━━━━━━━━━━━━━"
    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)

def send_custom_notification(
    title: str,
    message: str,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send generic notification."""
    card = (
        f"🔔 <b>{html.escape(title)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{html.escape(message)}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)
