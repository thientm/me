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
    """Format and send Crypto Review card following mobile-first best practices."""
    now_str = datetime.now().strftime("%d/%m %H:%M")
    diff_floor = tts_vnd - floor_vnd
    
    if diff_floor >= 0:
        header_icon = "🟢"
        title = "CRYPTO PORTFOLIO UPDATE"
        floor_badge = f"+{_format_vnd(diff_floor)} đ"
    else:
        header_icon = "🔴"
        title = "CRYPTO FLOOR BREACH"
        floor_badge = f"⚠️ Thủng {_format_vnd(abs(diff_floor))} đ"

    lines = [
        f"{header_icon} <b>{title}</b>  <i>({now_str})</i>\n",
        f"<b>TTS:</b> <code>{_format_vnd(tts_vnd)} đ</code>  <i>(Sàn: {_format_vnd(floor_vnd)} đ · {floor_badge})</i>",
        f"<b>Market:</b> BTC <code>${btc_price:,.0f}</code> · SOL <code>${sol_price:,.2f}</code> · P2P <code>{_format_vnd(p2p_rate)}</code>\n",
    ]

    if action_note:
        lines.append(f"⚡ <b>Action:</b> {html.escape(action_note)}\n")

    lines.append("⏳ <i>Hạn chót bảo toàn vốn: 31/10/2026</i>")
    card = "\n".join(lines)

    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)

def notify_pipeline_status(
    slot: str,
    channel: str,
    slug: Optional[str] = None,
    gates: Optional[Dict[str, bool]] = None,
    next_slot: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send Video Pipeline status card following mobile-first best practices."""
    all_passed = True
    gate_icons = []
    if gates:
        for name, passed in gates.items():
            if not passed:
                all_passed = False
            icon = "✅" if passed else "❌"
            clean_name = name.split("(")[0].strip()
            gate_icons.append(f"{clean_name} {icon}")

    header_icon = "🟢" if all_passed else "🔴"
    status_text = "COMPLETED" if all_passed else "ATTENTION NEEDED"

    lines = [
        f"{header_icon} <b>{html.escape(channel.upper())} · {html.escape(slot)} {status_text}</b>\n"
    ]

    if slug:
        lines.append(f"<b>Slug:</b> <code>{html.escape(slug)}</code>")

    if gate_icons:
        lines.append(f"<b>Gates:</b> {' · '.join(gate_icons)}")

    if next_slot:
        lines.append(f"\n⏰ <i>Next slot: {html.escape(next_slot)}</i>")

    card = "\n".join(lines)
    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)

def notify_alert(
    source: str,
    error_msg: str,
    action_needed: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send urgent alert card."""
    now_str = datetime.now().strftime("%H:%M:%S")
    lines = [
        f"🚨 <b>ALERT: {html.escape(source.upper())}</b>  <i>({now_str})</i>\n",
        f"<b>Issue:</b> <code>{html.escape(error_msg)}</code>\n",
    ]
    if action_needed:
        lines.append(f"🛠️ <b>Action:</b> {html.escape(action_needed)}")

    card = "\n".join(lines)
    return client.send_message(card, parse_mode="HTML", dry_run=dry_run)

def notify_engagement_report(
    channel: str,
    stats: Dict[str, Any],
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Format and send Auto-Engagement Report card to Telegram."""
    now_str = datetime.now().strftime("%d/%m %H:%M")
    mode_str = " (DRY-RUN)" if dry_run else ""
    lines = [
        f"💬 <b>AUTO-ENGAGEMENT REPORT{mode_str}</b>  <i>({now_str})</i>\n",
        f"<b>Channel:</b> <code>{html.escape(channel.upper())}</code>",
    ]

    total_replies = stats.get("replies", 0)
    total_hearts = stats.get("hearts", 0)
    total_likes = stats.get("likes", 0)
    total_spam = stats.get("spam", 0)

    lines.append(f"<b>Actions:</b> 💬 {total_replies} phản hồi · ❤️ {total_hearts} tim · 👍 {total_likes} thích")
    if total_spam:
        lines.append(f"🛡️ <b>Spam đã chặn:</b> {total_spam}")

    sample_replies = stats.get("sample_replies", [])
    if sample_replies:
        lines.append("\n📝 <b>Mẫu phản hồi đã gửi:</b>")
        for sr in sample_replies[:2]:
            cleaned_sr = html.escape(sr.strip().replace("\n", " "))
            if len(cleaned_sr) > 90:
                cleaned_sr = cleaned_sr[:87] + "..."
            lines.append(f"• <i>\"{cleaned_sr}\"</i>")

    card = "\n".join(lines)
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

