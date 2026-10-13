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
    floor_vnd: float = 500_000_000,
    action_note: str = "",
    dry_run: bool = False,
    chat_id: Optional[str] = None,
    crypto_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Format and send Crypto Portfolio & Risk Review card (strictly Crypto only)."""
    now_str = datetime.now().strftime("%d/%m %H:%M")
    diff_floor = tts_vnd - floor_vnd
    diff_abs = abs(diff_floor)
    diff_pct = (diff_floor / floor_vnd * 100.0) if floor_vnd > 0 else 0.0
    
    if diff_floor >= 0:
        header_icon = "🟢"
        title = "CRYPTO PORTFOLIO & RISK REVIEW"
        floor_badge = f"+{_format_vnd(diff_floor)} đ ({diff_pct:+.1f}%)"
    else:
        header_icon = "🔴"
        title = "CRYPTO FLOOR BREACH & RISK REVIEW"
        floor_badge = f"⚠️ Thủng {_format_vnd(diff_abs)} đ ({diff_pct:+.1f}%)"

    lines = [
        f"{header_icon} <b>{title}</b>  <i>({now_str})</i>\n",
        "<b>1. ĐỊNH GIÁ & THỊ TRƯỜNG:</b>",
        f"• <b>TTS:</b> <code>{_format_vnd(tts_vnd)} đ</code>  <i>(Sàn: {_format_vnd(floor_vnd)} đ · {floor_badge})</i>",
        f"• <b>Market:</b> BTC <code>${btc_price:,.0f}</code> · SOL <code>${sol_price:,.2f}</code> · P2P <code>{_format_vnd(p2p_rate)}</code>",
    ]

    snapshot = crypto_data.get("snapshot") if crypto_data else None
    matrix = crypto_data.get("matrix") if crypto_data else None

    if snapshot:
        btc_vnd_tr = (snapshot.btc_qty * snapshot.btc_price * snapshot.p2p_rate) / 1e6
        sol_vnd_tr = (snapshot.sol_qty * snapshot.sol_price * snapshot.p2p_rate) / 1e6
        stables_vnd_tr = (snapshot.stables_usd * snapshot.p2p_rate) / 1e6
        tts_tr = snapshot.tts_vnd / 1e6 if snapshot.tts_vnd > 0 else 1.0
        lines.append("• <b>Cơ cấu coin:</b>")
        lines.append(f"  - BTC: {snapshot.btc_qty:.5f} (~{btc_vnd_tr:,.1f}tr đ · {btc_vnd_tr/tts_tr*100:.1f}%)")
        lines.append(f"  - SOL: {snapshot.sol_qty:.2f} (~{sol_vnd_tr:,.1f}tr đ · {sol_vnd_tr/tts_tr*100:.1f}%)")
        lines.append(f"  - USDT: ${snapshot.stables_usd:,.2f} (~{stables_vnd_tr:,.1f}tr đ)")

    if matrix:
        lines.append(f"• <b>Hạn chót bảo toàn vốn:</b> {matrix.deadline_date} (Còn {matrix.days_to_deadline} ngày)\n")
        lines.append("<b>2. MA TRẬN QUYẾT ĐỊNH & KHUYẾN NGHỊ:</b>")
        lines.append(f"• <b>Active Band:</b> <code>{matrix.active_band}</code>")
        if action_note:
            lines.append(f"• <b>Hành động:</b> {html.escape(action_note)}\n")
        
        if matrix.orders_sheet:
            lines.append("<b>3. BẢNG LỆNH 10 PHÚT (THAO TÁC TRÊN SÀN):</b>")
            for o in matrix.orders_sheet:
                est_tr = o['est_vnd'] / 1e6
                qty_str = f"{o['qty']:,}" if isinstance(o['qty'], (int, float)) else str(o['qty'])
                lines.append(f"• <b>[{o['action']} {o['symbol']}]:</b> {qty_str} {o['symbol']} → ~{est_tr:,.1f}tr VND ({html.escape(o['deadline'])})")
    else:
        if action_note:
            lines.append(f"\n⚡ <b>Action:</b> {html.escape(action_note)}")
        lines.append("\n⏳ <i>Hạn chót bảo toàn vốn: 31/10/2026</i>")

    card = "\n".join(lines)
    return client.send_message(card, parse_mode="HTML", dry_run=dry_run, chat_id=chat_id)

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

def notify_master_review(
    review_all_data: Dict[str, Any],
    dry_run: bool = False,
    chat_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Format and send Personal OS Master Review card (ALL: Finance, Crypto, BĐS, Video)."""
    snapshot = review_all_data["snapshot"]
    matrix = review_all_data["matrix"]
    bds_gap = review_all_data["bds_gap"]
    pipeline = review_all_data.get("pipeline")

    now_str = datetime.now().strftime("%d/%m %H:%M")
    diff = matrix.distance_to_floor_vnd
    diff_abs = abs(diff)
    floor_target = getattr(matrix, "hard_floor_vnd", 500_000_000)
    diff_pct = (diff / floor_target * 100) if floor_target > 0 else 0
    diff_badge = f"+{_format_vnd(diff_abs)} đ ({diff_pct:+.1f}%)" if diff >= 0 else f"⚠️ Thủng {_format_vnd(diff_abs)} đ ({diff_pct:+.1f}%)"

    tts_formatted = _format_vnd(snapshot.tts_vnd)
    self_equity_tr = bds_gap["self_equity_vnd"] / 1e6
    borrow_needed_tr = bds_gap["borrow_needed_vnd"] / 1e6
    cushion_tr = bds_gap["cushion_vnd"] / 1e6
    bds_total_tr = bds_gap["total_budget_vnd"] / 1e6
    parents_tr = bds_gap["parents_support_vnd"] / 1e6
    personal_tr = bds_gap["personal_cash_vnd"] / 1e6
    crypto_tr = bds_gap["crypto_val_vnd"] / 1e6

    lines = [
        f"🧭 <b>PERSONAL OS MASTER REVIEW (ALL)</b>  <i>({now_str})</i>\n",
        "<b>1. TỔNG TÀI CHÍNH & VỐN TỰ CÓ:</b>",
        f"• <b>Tổng tự có huy động:</b> <code>{self_equity_tr:,.1f}tr đ</code>",
        f"  - Tiền gửi tiết kiệm hỗ trợ (Bố mẹ): {parents_tr:,.0f}tr đ",
        f"  - Tiền mặt cá nhân bank: {personal_tr:,.0f}tr đ",
        f"  - Danh mục Crypto (TTS live): {crypto_tr:,.1f}tr đ\n",
        "<b>2. QUẢN TRỊ DANH MỤC CRYPTO:</b>",
        f"• <b>TTS:</b> <code>{tts_formatted} đ</code>  <i>(Sàn: 500tr · {diff_badge})</i>",
        f"• <b>Band:</b> <code>{matrix.active_band}</code> — {html.escape(review_all_data['crypto'].get('recommendation', ''))}",
        f"• <b>Hạn chót:</b> {matrix.deadline_date} (Còn {matrix.days_to_deadline} ngày)\n",
        "<b>3. NGHĨA VỤ BĐS PHÙ ĐỔNG 80m² (3.1 TỶ):</b>",
        f"• <b>Tỷ lệ vốn tự có:</b> {self_equity_tr/bds_total_tr*100:.1f}% ({self_equity_tr:,.1f}tr / {bds_total_tr:,.0f}tr)",
        f"• <b>Vay ngân hàng dự kiến:</b> <b>{borrow_needed_tr:,.1f}tr đ</b>",
        f"• <b>Trần nợ kế hoạch:</b> {bds_gap['borrow_ceiling_vnd']/1e6:,.0f}tr đ (Đệm an toàn: {cushion_tr:+,.1f}tr đ 🟢)\n",
    ]

    if pipeline and "channels" in pipeline:
        lines.append(f"<b>4. PIPELINE VIDEO 3 KÊNH (KHUNG {pipeline.get('slot', 8):02d}:00):</b>")
        for ch, d in pipeline["channels"].items():
            s = d["slot_status"]
            if s["status"] == "done":
                p_icon = "🟢"
                desc = f"Đã đủ 3 nền tảng ({', '.join(s['posted'])})"
            elif s["status"] == "partial":
                p_icon = "🟡"
                desc = f"Thiếu: {', '.join(s['missing'])}"
            else:
                p_icon = "⚪"
                desc = "Chưa có bài"
            lines.append(f"• {p_icon} <b>{ch.upper()}:</b> {desc}")
        lines.append("")

    lines.extend([
        "<b>5. HÀNH ĐỘNG TRỌNG TÂM:</b>",
        "⚡ <b>Crypto:</b> Tuân thủ kỷ luật thoát vốn bảo vệ sàn cứng 500tr trước 25/10.",
        "⚡ <b>Video:</b> Giám sát và duyệt bài các khung giờ 08:00, 12:00, 20:00.",
    ])

    card = "\n".join(lines)
    return client.send_message(card, parse_mode="HTML", dry_run=dry_run, chat_id=chat_id)

# Alias for backwards compatibility
notify_crypto_deep_review = notify_master_review

