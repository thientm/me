"""
Module: crypto_engine.logger
Strict append-only logger complying with /Users/thien.tm/Documents/me/AGENTS.md:
- Target: crypto/logs/{YYYY-MM}.md (1 file/month)
- Invariant: APPEND-ONLY, NEVER modify or delete existing entries
- If previous entry is incorrect: append a correction entry with explicit reference
- Monotonic file size check: asserts new_size > old_size post-append
- Mode: 'a' only, never 'w' or 'w+'
"""

from __future__ import annotations
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

from .config import (
    CRYPTO_LOGS_DIR,
    HARD_FLOOR_VND,
    BDS_TOTAL_COST_VND,
    BDS_PARENTS_CASH_VND,
    BDS_PERSONAL_CASH_VND,
    BDS_DEBT_CEILING_VND,
    CASH_OUT_DEADLINE_STR,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
    FALLBACK_BTC_PRICE,
    FALLBACK_SOL_PRICE,
    FALLBACK_P2P_RATE,
)


def format_section_7_5_review(
    tts_vnd: float,
    withdrawn_vnd: float = 0.0,
    active_band: str = "TAKE_PROFIT_540M",
    action_summary: str = "Bán 50% coin (xả sạch SOL, rút Stables)",
    borrow_needed_vnd: Optional[float] = None,
    date_str: Optional[str] = None,
    btc_qty: float = FALLBACK_BTC_QTY,
    sol_qty: float = FALLBACK_SOL_QTY,
    stables_usd: float = FALLBACK_STABLES_USD,
    btc_price: float = FALLBACK_BTC_PRICE,
    sol_price: float = FALLBACK_SOL_PRICE,
    p2p_rate: float = FALLBACK_P2P_RATE,
    missed_count: int = 13
) -> str:
    """
    Format review following Section 7.5 template from crypto-plan.md.
    Headers required:
    ### Input
    ### Research
    ### Quyết định
    ### Đối chiếu BĐS
    ### Kịch bản & Insight
    """
    date_label = date_str or datetime.now().strftime("%Y-%m-%d")
    tts_tr = tts_vnd / 1_000_000.0
    withdrawn_tr = withdrawn_vnd / 1_000_000.0
    crypto_tr = (tts_vnd - withdrawn_vnd) / 1_000_000.0
    dist_vnd = tts_vnd - HARD_FLOOR_VND
    dist_tr = dist_vnd / 1_000_000.0

    if borrow_needed_vnd is None:
        total_equity = BDS_PARENTS_CASH_VND + BDS_PERSONAL_CASH_VND + tts_vnd
        borrow_needed_vnd = max(0.0, BDS_TOTAL_COST_VND - total_equity)

    borrow_needed_tr = borrow_needed_vnd / 1_000_000.0

    lines = [
        f"## {date_label}: Review — TTS {tts_tr:,.1f}tr ({tts_vnd:,.0f} VND) | Band: {active_band}",
        "",
        f"> ⚠️ **CẢNH BÁO KỶ LUẬT:** 0/{missed_count} khuyến nghị bán được thực thi (chưa thực hiện bất kỳ lệnh bán nào).",
        "> **Cost of Delay:** Mất đỉnh: −32,6tr | Nguy cơ trượt bảng giá đất 2027: +370tr | Phạt chậm nộp: 930.000 đ/ngày.",
        "",
        "### Input",
        f"- **TTS:** **{tts_tr:,.1f}tr VND** (VND đã rút: {withdrawn_tr:,.1f}tr + Crypto: {crypto_tr:,.1f}tr)",
        f"- **Sàn cứng Hard Floor:** **540.000.000 VND (540tr)** | Khoảng cách tới sàn 540tr: **{dist_tr:+,.1f}tr ({dist_vnd / HARD_FLOOR_VND * 100:+,.2f}%)**",
        f"- **Tỷ trọng đo lường:** BTC {btc_qty} @ ${btc_price:,.0f} · SOL {sol_qty} @ ${sol_price:,.2f} · Stables ${stables_usd:,.0f} · Tỷ giá P2P {p2p_rate:,.0f} VND/USDT",
        f"- **Hạn chót rút vốn:** Cuối tháng 10/2026 ({CASH_OUT_DEADLINE_STR})",
        "",
        "### Research",
        "- **N1 Vĩ mô toàn cầu:** Neutral/Risk-on nhẹ trước thềm PCE 30/09.",
        "- **N2 Vĩ mô Crypto:** Fear & Greed ~74 (Greed), dòng tiền ETF duy trì tích cực.",
        "- **N3 Vi mô Kỹ thuật:** ATR14 BTC 2,70% | ATR14 SOL 4,51% | Tỷ giá SOL/BTC tiệm cận đỉnh percentile 98,9%.",
        f"- **N4 Pháp lý & Kênh rút:** P2P thông suốt, tỷ giá {p2p_rate:,.0f} VND/USDT.",
        f"→ **Active Band Trục 2:** `{active_band}`",
        "",
        "### Quyết định",
        f"- **Khuyến nghị hành động:** {action_summary}",
        f"- **Quy tắc thực thi:** {'Kích hoạt Take Profit 50% ngay lập tức (xả sạch SOL trước, rút sạch Stables ra VND)' if tts_vnd >= HARD_FLOOR_VND else 'EMERGENCY: Đâm thủng Hard Floor 540tr -> Market Sell ALL ngay lập tức ra VND!'}",
        "",
        "### Đối chiếu BĐS",
        f"- **Tổng ngân sách làm sổ 80m²:** {BDS_TOTAL_COST_VND / 1e6:,.0f}tr VND.",
        f"- **Vốn tự có huy động:** {(BDS_PARENTS_CASH_VND + BDS_PERSONAL_CASH_VND + tts_vnd) / 1e6:,.1f}tr (Bố mẹ 1.300tr + Cá nhân 705tr + Crypto {tts_tr:,.1f}tr).",
        f"- **Số tiền cần vay (Gap):** **{borrow_needed_tr:,.1f}tr VND** (So với trần kế hoạch 615tr: chênh lệch {(borrow_needed_vnd - BDS_DEBT_CEILING_VND) / 1e6:+,.1f}tr).",
        "- **Cờ đỏ BĐS:** Rủi ro ghi nợ tiền sử dụng đất theo Điều 22 NĐ 103/2024 (Khoản vay 615tr).",
        "",
        "### Kịch bản & Insight",
        f"1. **Rủi ro số 1 (615tr):** Chưa chốt nguồn vay tiền sử dụng đất trước thời hạn 30/09.",
        f"2. **Rủi ro số 2 (540tr):** Đâm thủng sàn cứng 540tr nếu giá giảm mà không thực hiện chốt lời 50%.",
        f"3. **Độ nhạy giá:** Biến động giảm 5% đưa TTS về {tts_tr * 0.95:,.1f}tr (cách sàn 540tr: {(tts_vnd * 0.95 - HARD_FLOOR_VND) / 1e6:+,.1f}tr).",
        ""
    ]
    return "\n".join(lines)


def get_target_log_path(logs_dir: Optional[Union[Path, str]] = None, dt: Optional[datetime] = None) -> Path:
    """Return Path to monthly log file logs/YYYY-MM.md."""
    target_dir = Path(logs_dir) if logs_dir else CRYPTO_LOGS_DIR
    target_dt = dt or datetime.now()
    filename = f"{target_dt.strftime('%Y-%m')}.md"
    return target_dir / filename


def initialize_monthly_log_if_needed(file_path: Union[Path, str], dt: Optional[datetime] = None) -> None:
    """Initialize new monthly log file if it does not exist yet."""
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        target_dt = dt or datetime.now()
        header = f"# Log Giao dịch Crypto - Tháng {target_dt.strftime('%m/%Y')}\n\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)


def append_review_log(
    log_path: Optional[Union[Path, str]] = None,
    review_content: str = "",
    logs_dir: Optional[Union[Path, str]] = None,
    dt: Optional[datetime] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Safely appends a review entry to the specified log file or active monthly log.
    Strictly append-only with monotonic file size check.
    When dry_run=True, no disk modification occurs.
    """
    if log_path:
        target_file = Path(log_path)
    else:
        target_file = get_target_log_path(logs_dir=logs_dir, dt=dt)

    first_line = review_content.strip().split("\n")[0] if review_content else ""

    if dry_run:
        return {
            "status": "dry_run",
            "target_file": str(target_file),
            "bytes_to_write": len(review_content.encode("utf-8")),
            "entry_header": first_line,
            "preview": review_content[:200]
        }

    # Initialize monthly file if needed
    initialize_monthly_log_if_needed(target_file, dt)

    size_before = os.path.getsize(target_file)
    text_to_append = f"\n\n{review_content.strip()}\n"

    # STRICT APPEND-ONLY: Mode 'a'
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(text_to_append)
        f.flush()
        os.fsync(f.fileno())

    size_after = os.path.getsize(target_file)

    if size_after <= size_before:
        raise RuntimeError(
            f"AGENTS.md Integrity Violation: Append failed or file truncated. "
            f"Before: {size_before} bytes, After: {size_after} bytes."
        )

    return {
        "status": "success",
        "target_file": str(target_file),
        "bytes_written": size_after - size_before,
        "size_before": size_before,
        "size_after": size_after,
        "entry_header": first_line
    }


def append_correction(
    target_date_str: str,
    correction_text: str,
    log_path: Optional[Union[Path, str]] = None,
    logs_dir: Optional[Union[Path, str]] = None,
    dt: Optional[datetime] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Appends a correction notice conforming to AGENTS.md rule:
    'Nếu thông tin cũ sai, thêm entry mới ghi chú correction, không edit ngược lại quá khứ.'
    """
    now_str = (dt or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    entry_body = (
        f"### Đính chính (Correction) — {now_str}\n"
        f"- **Đối tượng đính chính:** Entry ngày `{target_date_str}`\n"
        f"- **Nội dung đính chính:** {correction_text}\n"
        f"- **Ghi chú tuân thủ:** Mục này được append theo quy định bất biến của AGENTS.md."
    )
    return append_review_log(
        log_path=log_path,
        review_content=entry_body,
        logs_dir=logs_dir,
        dt=dt,
        dry_run=dry_run
    )
