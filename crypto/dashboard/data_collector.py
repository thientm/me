"""Realtime Crypto Data Collector and Metrics Aggregator.

Bridges the crypto_engine domain logic with external consumers (Telegram bot, CLI, etc.).
"""
from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Ensure crypto_engine & crypto_dashboard are accessible in sys.path
_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from crypto_engine.parser import parse_crypto_plan
from crypto_engine.valuation import calculate_tts, ValuationSnapshot
from crypto_engine.matrix import evaluate_binary_matrix, MatrixEvaluation
from crypto_engine.logger import append_review_log
from crypto_engine.proposal import generate_markdown_review
from crypto_engine.config import (
    HARD_FLOOR_VND,
    CRYPTO_LOGS_DIR,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
)

def fetch_realtime_metrics(
    force_offline: bool = False,
    cache_path: Optional[Union[Path, str]] = None,
) -> Dict[str, Any]:
    """Fetch live holdings, spot/P2P rates, calculate TTS and evaluate binary decision matrix."""
    holdings = parse_crypto_plan()
    btc_qty = holdings.get("btc_qty", FALLBACK_BTC_QTY)
    sol_qty = holdings.get("sol_qty", FALLBACK_SOL_QTY)
    stables_usd = holdings.get("stables_usd", FALLBACK_STABLES_USD)
    withdrawn_vnd = holdings.get("withdrawn_vnd", 0.0)
    floor_vnd = float(holdings.get("hard_floor_vnd", HARD_FLOOR_VND))

    snapshot: ValuationSnapshot = calculate_tts(
        btc_qty=btc_qty,
        sol_qty=sol_qty,
        stables_usd=stables_usd,
        withdrawn_vnd=withdrawn_vnd,
        force_offline=force_offline,
        cache_path=cache_path,
    )

    matrix: MatrixEvaluation = evaluate_binary_matrix(
        tts_vnd=snapshot.tts_vnd,
        btc_qty=snapshot.btc_qty,
        sol_qty=snapshot.sol_qty,
        stables_usd=snapshot.stables_usd,
        btc_price=snapshot.btc_price,
        sol_price=snapshot.sol_price,
        p2p_rate=snapshot.p2p_rate,
        withdrawn_vnd=snapshot.withdrawn_vnd,
        snapshot=snapshot,
    )

    if matrix.active_band == "HARD_FLOOR_BREACH":
        diff_abs = abs(matrix.distance_to_floor_vnd)
        diff_str = f"{int(diff_abs):,}".replace(",", ".")
        recommendation = f"⚠️ THỦNG SÀN ({diff_str} đ)! Market Sell toàn bộ SOL & BTC ngay để khóa tiền mặt làm sổ đỏ."
    elif matrix.active_band == "TAKE_PROFIT_540M":
        recommendation = "Khóa chốt lời 50% (xả 100% SOL, bán 1 phần BTC) để bảo toàn sàn 540tr."
    elif matrix.active_band == "OVERRIDE_EMERGENCY":
        recommendation = f"🚨 Override khẩn cấp: {', '.join(matrix.overrides_triggered)}. Bán toàn bộ ngay!"
    else:
        recommendation = "Danh mục ổn định so với sàn cứng 540tr."

    if snapshot.data_source != "realtime":
        recommendation += f" [Nguồn: {snapshot.data_source}]"

    return {
        "total_tts_vnd": snapshot.tts_vnd,
        "btc_price": snapshot.btc_price,
        "sol_price": snapshot.sol_price,
        "p2p_rate": snapshot.p2p_rate,
        "floor_vnd": floor_vnd,
        "recommendation": recommendation,
        "active_band": matrix.active_band,
        "data_source": snapshot.data_source,
        "timestamp": snapshot.timestamp,
        "holdings": holdings,
        "snapshot": snapshot,
        "matrix": matrix,
    }

def run_full_crypto_review(
    save_log: bool = True,
    force_offline: bool = False,
    cache_path: Optional[Union[Path, str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Execute full Section 7.5 crypto review pipeline:
    1. Fetch live metrics (holdings, spot/P2P rates, TTS)
    2. Evaluate Binary Decision Matrix and 10-minute order sheet
    3. Calculate Real Estate (Phù Đổng 3.1 tỷ) financial gap and cushion
    4. Generate Section 7.5 Markdown review
    5. Append review to monthly log (crypto/logs/{YYYY-MM}.md)
    """
    metrics = fetch_realtime_metrics(force_offline=force_offline, cache_path=cache_path)
    snapshot: ValuationSnapshot = metrics["snapshot"]
    matrix: MatrixEvaluation = metrics["matrix"]

    # Real Estate gap analysis
    bds_total = 3_100_000_000.0
    parents_support = 1_300_000_000.0
    personal_cash = 830_000_000.0
    crypto_val = snapshot.tts_vnd
    self_equity = parents_support + personal_cash + crypto_val
    borrow_needed = max(0.0, bds_total - self_equity)
    borrow_ceiling = 615_000_000.0
    cushion = borrow_ceiling - borrow_needed

    bds_gap = {
        "total_budget_vnd": bds_total,
        "parents_support_vnd": parents_support,
        "personal_cash_vnd": personal_cash,
        "crypto_val_vnd": crypto_val,
        "self_equity_vnd": self_equity,
        "borrow_needed_vnd": borrow_needed,
        "borrow_ceiling_vnd": borrow_ceiling,
        "cushion_vnd": cushion,
    }

    # Markdown review generation
    now_dt = datetime.now()
    date_label = now_dt.strftime("%Y-%m-%d (%H:%M ICT)")
    review_md = generate_markdown_review(
        snapshot=snapshot,
        eval_matrix=matrix,
        review_date_str=date_label,
    )

    log_path_str = None
    log_saved = False
    if save_log and not dry_run:
        month_str = now_dt.strftime("%Y-%m")
        target_log_file = Path(CRYPTO_LOGS_DIR) / f"{month_str}.md"
        append_review_log(log_path=target_log_file, review_content=review_md)
        log_path_str = str(target_log_file)
        log_saved = True

    return {
        "metrics": metrics,
        "snapshot": snapshot,
        "matrix": matrix,
        "bds_gap": bds_gap,
        "review_md": review_md,
        "log_saved": log_saved,
        "log_path": log_path_str,
    }

def run_master_review_all(
    force_offline: bool = False,
    cache_path: Optional[Union[Path, str]] = None,
) -> Dict[str, Any]:
    """Execute cross-domain Personal OS Master Review (ALL):
    1. Financial & Self-Equity (Parents savings, personal bank cash, crypto TTS)
    2. Crypto Portfolio Status & 540M Hard Floor
    3. Real Estate Phù Đổng (3.1B VND, bank loan gap, 615M ceiling)
    4. 3-Channel Video Pipeline status (Mê Tech, Thiện Trần, Tâm An Lạc)
    """
    metrics = fetch_realtime_metrics(force_offline=force_offline, cache_path=cache_path)
    snapshot: ValuationSnapshot = metrics["snapshot"]
    matrix: MatrixEvaluation = metrics["matrix"]

    # Real Estate & Master Finance gap
    bds_total = 3_100_000_000.0
    parents_support = 1_300_000_000.0
    personal_cash = 830_000_000.0
    crypto_val = snapshot.tts_vnd
    self_equity = parents_support + personal_cash + crypto_val
    borrow_needed = max(0.0, bds_total - self_equity)
    borrow_ceiling = 615_000_000.0
    cushion = borrow_ceiling - borrow_needed

    bds_gap = {
        "total_budget_vnd": bds_total,
        "parents_support_vnd": parents_support,
        "personal_cash_vnd": personal_cash,
        "crypto_val_vnd": crypto_val,
        "self_equity_vnd": self_equity,
        "borrow_needed_vnd": borrow_needed,
        "borrow_ceiling_vnd": borrow_ceiling,
        "cushion_vnd": cushion,
    }

    try:
        from ops.orchestrator.cli import run_orchestration_dashboard
        pipeline_dash = run_orchestration_dashboard()
    except Exception:
        pipeline_dash = None

    return {
        "crypto": metrics,
        "snapshot": snapshot,
        "matrix": matrix,
        "bds_gap": bds_gap,
        "pipeline": pipeline_dash,
    }
