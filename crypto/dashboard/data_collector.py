"""Realtime Crypto Data Collector and Metrics Aggregator.

Bridges the crypto_engine domain logic with external consumers (Telegram bot, CLI, etc.).
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Ensure crypto_engine & crypto_dashboard are accessible in sys.path
_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from crypto_engine.parser import parse_crypto_plan
from crypto_engine.valuation import calculate_tts, ValuationSnapshot
from crypto_engine.matrix import evaluate_binary_matrix, MatrixEvaluation
from crypto_engine.config import (
    HARD_FLOOR_VND,
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
