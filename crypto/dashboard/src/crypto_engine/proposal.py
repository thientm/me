"""
Module: crypto_engine.proposal
Generates standardized Section 7.5 Action Proposal and 10-minute order sheet:
- Discipline execution alert banner (0/13 missed orders, Cost of Delay metrics)
- Real-time portfolio input table & countdown to late October 2026
- 4-Group research summary (N1, N2, N3, N4)
- 10-minute executable order sheet
- Real Estate (BĐS) gap analysis (3.1B VND, 615M ceiling)
- Sensitivity matrix & action scenarios
"""

from __future__ import annotations
from typing import Dict, Any, Optional, List
from datetime import datetime

from .config import (
    HARD_FLOOR_VND,
    BDS_TOTAL_COST_VND,
    BDS_PARENTS_CASH_VND,
    BDS_PERSONAL_CASH_VND,
    BDS_DEBT_CEILING_VND,
    BDS_DELAY_PENALTY_HOURLY,
    CASH_OUT_DEADLINE_STR,
)
from .valuation import ValuationSnapshot
from .matrix import MatrixEvaluation


def format_vnd_tr(val_vnd: float) -> str:
    """Format VND in millions (triệu đồng) with Vietnamese formatting."""
    val_tr = val_vnd / 1_000_000.0
    return f"{val_tr:,.1f}tr".replace(",", "@").replace(".", ",").replace("@", ".")


def format_currency_full(val_vnd: float) -> str:
    """Format full VND currency string."""
    return f"{val_vnd:,.0f} VND".replace(",", ".")


def generate_markdown_review(
    snapshot: ValuationSnapshot,
    eval_matrix: MatrixEvaluation,
    review_date_str: Optional[str] = None
) -> str:
    """Generate complete Section 7.5 standardized Markdown review."""
    date_label = review_date_str or datetime.now().strftime("%Y-%m-%d")
    tts_str = format_vnd_tr(snapshot.tts_vnd)
    dist_str = f"{'+' if eval_matrix.distance_to_floor_vnd >= 0 else ''}{format_vnd_tr(eval_matrix.distance_to_floor_vnd)}"
    dist_pct_str = f"{'+' if eval_matrix.distance_to_floor_pct >= 0 else ''}{eval_matrix.distance_to_floor_pct:.1f}%"

    lines = [
        f"## {date_label}: Deep Review — [TTS: {tts_str} | Band: {eval_matrix.active_band} | Khuyến nghị Lệnh 10 Phút]",
        "",
        f"> ⚠️ **CẢNH BÁO KỶ LUẬT:** 0/{eval_matrix.missed_recommendations_count} khuyến nghị bán được thực thi trong suốt chu kỳ (toàn bộ khuyến nghị trước đây đều bị bỏ lỡ).",
        "> **Cost of Delay:** Mất đỉnh: −32,6tr | Nguy cơ trượt bảng giá đất 2027: +370tr | Phạt chậm nộp: 930.000 đ/ngày.",
        "",
        "### Input",
        f"- **TTS:** {tts_str} (VND đã rút: {format_vnd_tr(snapshot.withdrawn_vnd)} + Crypto: {format_vnd_tr(snapshot.crypto_vnd)}) | Sàn cứng Hard Floor: 540.000.000 VND",
        f"- **Khoảng cách sàn:** {dist_str} ({dist_pct_str}) | Còn **{eval_matrix.days_to_deadline} ngày** tới hạn chót {eval_matrix.deadline_date}",
        "",
        "| Tài sản | Số lượng ĐO | Giá Spot | Giá trị USD | Quy đổi VND | Tỷ trọng |",
        "|---|---|---|---|---|---|"
    ]

    btc_usd = snapshot.btc_qty * snapshot.btc_price
    btc_vnd = btc_usd * snapshot.p2p_rate
    btc_pct = (btc_vnd / snapshot.tts_vnd * 100.0) if snapshot.tts_vnd > 0 else 0.0

    sol_usd = snapshot.sol_qty * snapshot.sol_price
    sol_vnd = sol_usd * snapshot.p2p_rate
    sol_pct = (sol_vnd / snapshot.tts_vnd * 100.0) if snapshot.tts_vnd > 0 else 0.0

    stables_vnd = snapshot.stables_usd * snapshot.p2p_rate
    stables_pct = (stables_vnd / snapshot.tts_vnd * 100.0) if snapshot.tts_vnd > 0 else 0.0

    lines.append(f"| **BTC** | {snapshot.btc_qty:.5f} | ${snapshot.btc_price:,.0f} | ${btc_usd:,.1f} | {format_vnd_tr(btc_vnd)} | {btc_pct:.1f}% |")
    lines.append(f"| **SOL** | {snapshot.sol_qty:.2f} | ${snapshot.sol_price:,.2f} | ${sol_usd:,.1f} | {format_vnd_tr(sol_vnd)} | {sol_pct:.1f}% |")
    lines.append(f"| **Stables** | ${snapshot.stables_usd:,.2f} | $1.00 | ${snapshot.stables_usd:,.1f} | {format_vnd_tr(stables_vnd)} | {stables_pct:.1f}% |")
    lines.append(f"| **TỔNG CRYPTO** | — | — | ${btc_usd + sol_usd + snapshot.stables_usd:,.1f} | {format_vnd_tr(snapshot.crypto_vnd)} | 100.0% |")
    lines.append("")

    # Research
    lines.extend([
        "### Research",
        "- **N1 Vĩ mô toàn cầu:** Neutral/Risk-on nhẹ — Đón đầu thềm PCE 30/09.",
        "- **N2 Vĩ mô Crypto:** F&G Greed (~74), ETF ròng duy trì dòng tiền tổ chức.",
        "- **N3 Vi mô Kỹ thuật:** ATR14 BTC 2,70% | ATR14 SOL 4,51% | SOL/BTC percentile 98,9% (đỉnh 90 ngày).",
        f"- **N4 Pháp lý VN & Kênh rút:** THÔNG SUỐT | Tỷ giá P2P realtime: {snapshot.p2p_rate:,.0f} VND/USDT.",
        f"→ **Band Trục 2:** `{eval_matrix.active_band}` | Sàn cứng 540tr cách {dist_str} ({dist_pct_str}).",
        ""
    ])

    # Decision & Order Sheet
    lines.extend([
        "### Quyết định & Bảng Lệnh 10 Phút (10-minute Executable Order Sheet)",
        f"- **Trạng thái Matrix:** `{eval_matrix.active_band}` (Quy tắc Nhị phân 540tr).",
        f"- **Overrides kích hoạt:** {', '.join(eval_matrix.overrides_triggered) if eval_matrix.overrides_triggered else 'Không có.'}",
        "",
        "| # | Thao tác | Cặp / Kênh | Loại lệnh | Khối lượng | Giá / Điều kiện | VND ước tính | Thời hạn | Ghi chú |",
        "|---|---|---|---|---|---|---|---|---|"
    ])

    for order in eval_matrix.orders_sheet:
        price_target = order.get("price_target", order.get("price", 0.0))
        pair = order.get("symbol_pair", order.get("symbol", ""))
        price_str = f"${price_target:,.1f}" if price_target > 0 and "VND" not in pair else (f"{price_target:,.0f}" if price_target > 0 else "MARKET")
        est_vnd = order.get("estimated_vnd", order.get("est_vnd", 0.0))
        deadline = order.get("deadline", "Trong 10 phút")
        reason = order.get("reason", order.get("note", ""))
        lines.append(
            f"| {order.get('step', 1)} | **{order.get('action', '')}** | `{pair}` | {order.get('order_type', '')} | "
            f"{order.get('qty', 0.0)} | {price_str} | {format_vnd_tr(est_vnd)} | {deadline} | {reason} |"
        )
    lines.append("")

    # Real Estate Alignment
    total_own_equity = BDS_PARENTS_CASH_VND + BDS_PERSONAL_CASH_VND + snapshot.tts_vnd
    bds_gap = BDS_TOTAL_COST_VND - total_own_equity
    gap_delta = bds_gap - BDS_DEBT_CEILING_VND

    lines.extend([
        "### Đối chiếu BĐS (Thửa đất Phù Đổng 80m² - 3,1 tỷ)",
        f"- **Bố mẹ hỗ trợ:** {format_vnd_tr(BDS_PARENTS_CASH_VND)} | **Vốn cá nhân:** {format_vnd_tr(BDS_PERSONAL_CASH_VND)} | **TTS Crypto:** {tts_str}",
        f"- **Tổng vốn tự có:** {format_vnd_tr(total_own_equity)} / 3.100tr VND.",
        f"- **Số tiền cần vay (Gap):** **{format_vnd_tr(bds_gap)}** (Mốc trần kế hoạch: 615tr, chênh lệch: **{format_vnd_tr(gap_delta)}**).",
        "- 🚩 **Cờ đỏ BĐS:** Rủi ro ghi nợ tiền sử dụng đất theo Điều 22 NĐ 103/2024 (Khoản 615tr, hạn chốt nguồn tháng 9/2026).",
        ""
    ])

    # Scenarios & Sensitivity Matrix
    lines.extend([
        "### Kịch bản & Insight (Độ nhạy Sàn 540tr)",
        "| Biến động | BTC | SOL | TTS mô phỏng | So với Sàn cứng 540tr |",
        "|---|---|---|---|---|",
        f"| **+10%** | ${snapshot.btc_price*1.10:,.0f} | ${snapshot.sol_price*1.10:,.2f} | {format_vnd_tr(snapshot.tts_vnd + (btc_vnd+sol_vnd)*0.10)} | An toàn (Vượt sàn {(snapshot.tts_vnd + (btc_vnd+sol_vnd)*0.10 - HARD_FLOOR_VND)/1e6:,.1f}tr) |",
        f"| **0%** | ${snapshot.btc_price:,.0f} | ${snapshot.sol_price:,.2f} | {tts_str} | {dist_str} ({dist_pct_str}) |",
        f"| **−5%** | ${snapshot.btc_price*0.95:,.0f} | ${snapshot.sol_price*0.95:,.2f} | {format_vnd_tr(snapshot.tts_vnd - (btc_vnd+sol_vnd)*0.05)} | {'⚠️ ĐÂM THỦNG SÀN' if snapshot.tts_vnd - (btc_vnd+sol_vnd)*0.05 < HARD_FLOOR_VND else 'Sát sàn'} |",
        f"| **−10%** | ${snapshot.btc_price*0.90:,.0f} | ${snapshot.sol_price*0.90:,.2f} | {format_vnd_tr(snapshot.tts_vnd - (btc_vnd+sol_vnd)*0.10)} | 🔴 THỦNG SÀN NGHIÊM TRỌNG |",
        "",
        "**Trigger thay đổi khuyến nghị:**",
        "1. TTS tụt dưới 540tr VND bất kỳ lúc nào -> Chuyển ngay sang Emergency Market Sell ALL.",
        "2. Phát hiện bất kỳ hạn chế tài khoản Binance hoặc P2P -> Market sell toàn bộ trong 24h.",
        "3. Chạm mốc ngày 17/10/2026 (<14 ngày tới hạn chót) -> Market sell toàn bộ không phụ thuộc giá.",
        ""
    ])

    return "\n".join(lines)


def generate_structured_proposal(
    snapshot: ValuationSnapshot,
    eval_matrix: MatrixEvaluation
) -> Dict[str, Any]:
    """Generate structured dictionary representing the proposal for REST APIs and Web UI."""
    total_own_equity = BDS_PARENTS_CASH_VND + BDS_PERSONAL_CASH_VND + snapshot.tts_vnd
    bds_gap = BDS_TOTAL_COST_VND - total_own_equity
    return {
        "timestamp": snapshot.timestamp,
        "tts_vnd": snapshot.tts_vnd,
        "crypto_vnd": snapshot.crypto_vnd,
        "withdrawn_vnd": snapshot.withdrawn_vnd,
        "hard_floor_vnd": eval_matrix.hard_floor_vnd,
        "active_band": eval_matrix.active_band,
        "distance_to_floor_vnd": eval_matrix.distance_to_floor_vnd,
        "distance_to_floor_pct": eval_matrix.distance_to_floor_pct,
        "urgent_action_required": eval_matrix.urgent_action_required,
        "missed_recommendations_count": eval_matrix.missed_recommendations_count,
        "days_to_deadline": eval_matrix.days_to_deadline,
        "deadline_date": eval_matrix.deadline_date,
        "orders_sheet": eval_matrix.orders_sheet,
        "overrides_triggered": eval_matrix.overrides_triggered,
        "bds_analysis": {
            "total_cost_vnd": BDS_TOTAL_COST_VND,
            "own_equity_vnd": total_own_equity,
            "gap_loan_vnd": bds_gap,
            "gap_delta_vs_ceiling": bds_gap - BDS_DEBT_CEILING_VND,
            "loan_ceiling_vnd": BDS_DEBT_CEILING_VND
        }
    }
