"""
Module: crypto_engine.matrix
Binary Decision Matrix Engine enforcing the 2026-09-24 updated domain constraints:
1. Hard Floor: 540,000,000 VND (540tr).
2. Binary Decision Rule:
   - If TTS >= 540tr VND -> TAKE_PROFIT_540M (Take Profit 50% immediately; SOL first, Stables withdrawn).
   - If TTS < 540tr VND  -> HARD_FLOOR_BREACH (EMERGENCY Market Sell ALL ra VND ngay lập tức!).
   - Middle bands removed.
3. Liquidation priority: Stables -> SOL -> BTC.
4. Cash-out deadline: Late October 2026 (2026-10-31).
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import List, Dict, Optional, Any, Union

from .config import (
    HARD_FLOOR_VND,
    CASH_OUT_DEADLINE_STR,
    OVERRIDE_DAYS_THRESHOLD,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
    FALLBACK_BTC_PRICE,
    FALLBACK_SOL_PRICE,
    FALLBACK_P2P_RATE,
)
from .valuation import ValuationSnapshot


@dataclass
class MatrixEvaluation:
    hard_floor_vnd: float            # 540,000,000.0
    active_band: str                 # "TAKE_PROFIT_540M" | "HARD_FLOOR_BREACH" | "OVERRIDE_EMERGENCY"
    distance_to_floor_vnd: float     # tts_vnd - 540,000,000
    distance_to_floor_pct: float     # (distance_to_floor_vnd / 540,000,000) * 100
    urgent_action_required: bool
    missed_recommendations_count: int
    orders_sheet: List[Dict[str, Any]]
    overrides_triggered: List[str]
    days_to_deadline: int = 0
    deadline_date: str = CASH_OUT_DEADLINE_STR


def get_days_to_deadline(current_date_str: Optional[str] = None) -> int:
    """Calculate remaining calendar days to late October 2026 deadline (2026-10-31)."""
    if current_date_str:
        try:
            curr = datetime.fromisoformat(current_date_str).date()
        except ValueError:
            curr = datetime.strptime(current_date_str[:10], "%Y-%m-%d").date()
    else:
        curr = date.today()
    deadline = datetime.strptime(CASH_OUT_DEADLINE_STR, "%Y-%m-%d").date()
    return (deadline - curr).days


def check_overrides(
    tts_vnd: float,
    override_p2p_blocked: bool = False,
    override_account_restricted: bool = False,
    current_date_str: Optional[str] = None
) -> List[str]:
    """Check non-price emergency override triggers."""
    triggered = []
    if override_p2p_blocked:
        triggered.append("OVERRIDE_LEGAL_P2P_BLOCKED")
    if override_account_restricted:
        triggered.append("OVERRIDE_BINANCE_RESTRICTION")
    days_left = get_days_to_deadline(current_date_str)
    if days_left <= OVERRIDE_DAYS_THRESHOLD:
        triggered.append(f"OVERRIDE_DEADLINE_APPROACHING_{days_left}_DAYS")
    if tts_vnd < HARD_FLOOR_VND:
        triggered.append("OVERRIDE_HARD_FLOOR_BREACHED")
    return triggered


def calculate_take_profit_orders(
    btc_qty: float,
    sol_qty: float,
    stables_usd: float,
    btc_price: float,
    sol_price: float,
    p2p_rate: float,
    withdrawn_vnd: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Calculates 10-minute order sheet for Take Profit 50%:
    Priority Order: Stables -> SOL -> BTC.
    1. Withdraw 100% Stables
    2. Sell 100% SOL
    3. Sell remaining BTC shortfall to reach 50% coin liquidation
    4. Withdraw newly sold USDT to VND
    5. Place Stop-Market on remaining BTC
    """
    orders: List[Dict[str, Any]] = []
    step = 1

    # 1. Withdraw Stables
    if stables_usd > 0.0:
        est_vnd = stables_usd * p2p_rate
        orders.append({
            "step": step,
            "action": "WITHDRAW",
            "symbol": "USDT",
            "symbol_pair": "USDT/VND",
            "order_type": "P2P_SELL",
            "qty": round(stables_usd, 2),
            "price": p2p_rate,
            "price_target": p2p_rate,
            "est_vnd": est_vnd,
            "estimated_vnd": est_vnd,
            "deadline": "Trong 10 phút",
            "reason": "Rút sạch Stables ra VND để loại bỏ Platform Risk",
            "note": "Rút sạch Stables ra VND để loại bỏ Platform Risk"
        })
        step += 1

    # 2. Total coin valuation and 50% coin liquidation target
    coin_usd = (btc_qty * btc_price) + (sol_qty * sol_price)
    coin_vnd = coin_usd * p2p_rate
    target_50_coin_vnd = 0.50 * coin_vnd

    # 3. Sell 100% SOL first (ATR 4.51%, peak SOL/BTC)
    sol_sold_vnd = 0.0
    if sol_qty > 0.0:
        sol_sold_vnd = sol_qty * sol_price * p2p_rate
        orders.append({
            "step": step,
            "action": "SELL",
            "symbol": "SOL",
            "symbol_pair": "SOLUSDT",
            "order_type": "MARKET",
            "qty": round(sol_qty, 4),
            "price": sol_price,
            "price_target": sol_price,
            "est_vnd": sol_sold_vnd,
            "estimated_vnd": sol_sold_vnd,
            "deadline": "Trong 10 phút",
            "reason": "Xả 100% SOL trước (ATR 4.51%, đỉnh SOL/BTC percentile 98.9%)",
            "note": "Xả 100% SOL trước (ATR 4.51%, đỉnh SOL/BTC percentile 98.9%)"
        })
        step += 1

    # 4. Sell remaining shortfall from BTC
    shortfall_vnd = max(0.0, target_50_coin_vnd - sol_sold_vnd)
    btc_to_sell = 0.0
    btc_sold_vnd = 0.0
    btc_price_vnd = btc_price * p2p_rate
    if shortfall_vnd > 0.0 and btc_qty > 0.0 and btc_price_vnd > 0.0:
        btc_to_sell = min(btc_qty, shortfall_vnd / btc_price_vnd)
        btc_sold_vnd = btc_to_sell * btc_price_vnd
        orders.append({
            "step": step,
            "action": "SELL",
            "symbol": "BTC",
            "symbol_pair": "BTCUSDT",
            "order_type": "MARKET",
            "qty": round(btc_to_sell, 5),
            "price": btc_price,
            "price_target": btc_price,
            "est_vnd": btc_sold_vnd,
            "estimated_vnd": btc_sold_vnd,
            "deadline": "Trong 10 phút",
            "reason": "Bán thêm BTC để đạt đúng mục tiêu chốt 50% giá trị coin",
            "note": "Bán thêm BTC để đạt đúng mục tiêu chốt 50% giá trị coin"
        })
        step += 1

    # 5. Withdraw newly sold USDT to VND
    new_usdt = (sol_qty * sol_price) + (btc_to_sell * btc_price)
    if new_usdt > 0.0:
        orders.append({
            "step": step,
            "action": "WITHDRAW",
            "symbol": "USDT",
            "symbol_pair": "USDT/VND",
            "order_type": "P2P_SELL",
            "qty": round(new_usdt, 2),
            "price": p2p_rate,
            "price_target": p2p_rate,
            "est_vnd": new_usdt * p2p_rate,
            "estimated_vnd": new_usdt * p2p_rate,
            "deadline": "Trong 10 phút",
            "reason": "Rút toàn bộ tiền bán coin ra tài khoản ngân hàng VND",
            "note": "Rút toàn bộ tiền bán coin ra tài khoản ngân hàng VND"
        })
        step += 1

    # 6. Stop-Market on remaining BTC to lock in 540tr floor
    remaining_btc = max(0.0, btc_qty - btc_to_sell)
    if remaining_btc > 0.0 and btc_price > 0.0:
        total_safe_cash = (
            withdrawn_vnd +
            (stables_usd * p2p_rate) +
            sol_sold_vnd +
            btc_sold_vnd
        )
        if total_safe_cash >= HARD_FLOOR_VND:
            stop_price = round(btc_price * 0.88, 1)
            reason = "Stop trailing 12% bảo vệ lợi nhuận (Sàn 540tr đã an toàn 100% bằng tiền mặt)"
        else:
            required_floor_deficit = HARD_FLOOR_VND - total_safe_cash
            stop_price = round(required_floor_deficit / (remaining_btc * p2p_rate), 1)
            reason = "Stop-Market GTC bảo vệ sàn cứng 540.000.000 VND cho phần BTC còn lại"

        orders.append({
            "step": step,
            "action": "STOP_MARKET",
            "symbol": "BTC",
            "symbol_pair": "BTCUSDT",
            "order_type": "STOP_MARKET",
            "qty": round(remaining_btc, 5),
            "price": stop_price,
            "price_target": stop_price,
            "est_vnd": remaining_btc * stop_price * p2p_rate,
            "estimated_vnd": remaining_btc * stop_price * p2p_rate,
            "deadline": "GTC (Ratchet thứ Năm hàng tuần)",
            "reason": reason,
            "note": reason
        })

    return orders


def calculate_emergency_sell_all_orders(
    btc_qty: float,
    sol_qty: float,
    stables_usd: float,
    btc_price: float,
    sol_price: float,
    p2p_rate: float,
    reason_prefix: str = "EMERGENCY"
) -> List[Dict[str, Any]]:
    """
    Emergency liquidation of 100% portfolio assets:
    1. Withdraw 100% Stables
    2. Market sell 100% SOL
    3. Market sell 100% BTC
    4. Withdraw 100% USDT to VND
    """
    orders: List[Dict[str, Any]] = []
    step = 1

    if stables_usd > 0.0:
        orders.append({
            "step": step,
            "action": "WITHDRAW",
            "symbol": "USDT",
            "symbol_pair": "USDT/VND",
            "order_type": "P2P_SELL",
            "qty": round(stables_usd, 2),
            "price": p2p_rate,
            "price_target": p2p_rate,
            "est_vnd": stables_usd * p2p_rate,
            "estimated_vnd": stables_usd * p2p_rate,
            "deadline": "Ngay lập tức",
            "reason": f"{reason_prefix}: Rút sạch Stables ra VND",
            "note": f"{reason_prefix}: Rút sạch Stables ra VND"
        })
        step += 1

    if sol_qty > 0.0:
        sol_vnd = sol_qty * sol_price * p2p_rate
        orders.append({
            "step": step,
            "action": "SELL",
            "symbol": "SOL",
            "symbol_pair": "SOLUSDT",
            "order_type": "MARKET",
            "qty": round(sol_qty, 4),
            "price": sol_price,
            "price_target": sol_price,
            "est_vnd": sol_vnd,
            "estimated_vnd": sol_vnd,
            "deadline": "Ngay lập tức",
            "reason": f"{reason_prefix}: Market Sell toàn bộ SOL",
            "note": f"{reason_prefix}: Market Sell toàn bộ SOL"
        })
        step += 1

    if btc_qty > 0.0:
        btc_vnd = btc_qty * btc_price * p2p_rate
        orders.append({
            "step": step,
            "action": "SELL",
            "symbol": "BTC",
            "symbol_pair": "BTCUSDT",
            "order_type": "MARKET",
            "qty": round(btc_qty, 5),
            "price": btc_price,
            "price_target": btc_price,
            "est_vnd": btc_vnd,
            "estimated_vnd": btc_vnd,
            "deadline": "Ngay lập tức",
            "reason": f"{reason_prefix}: Market Sell toàn bộ BTC",
            "note": f"{reason_prefix}: Market Sell toàn bộ BTC"
        })
        step += 1

    total_usdt = (sol_qty * sol_price) + (btc_qty * btc_price)
    if total_usdt > 0.0:
        orders.append({
            "step": step,
            "action": "WITHDRAW",
            "symbol": "USDT",
            "symbol_pair": "USDT/VND",
            "order_type": "P2P_SELL",
            "qty": round(total_usdt, 2),
            "price": p2p_rate,
            "price_target": p2p_rate,
            "est_vnd": total_usdt * p2p_rate,
            "estimated_vnd": total_usdt * p2p_rate,
            "deadline": "Ngay lập tức",
            "reason": f"{reason_prefix}: Rút toàn bộ tiền bán coin ra tài khoản ngân hàng VND",
            "note": f"{reason_prefix}: Rút toàn bộ tiền bán coin ra tài khoản ngân hàng VND"
        })

    return orders


def evaluate_binary_matrix(
    tts_vnd: Optional[float] = None,
    btc_qty: float = FALLBACK_BTC_QTY,
    sol_qty: float = FALLBACK_SOL_QTY,
    stables_usd: float = FALLBACK_STABLES_USD,
    btc_price: float = FALLBACK_BTC_PRICE,
    sol_price: float = FALLBACK_SOL_PRICE,
    p2p_rate: float = FALLBACK_P2P_RATE,
    withdrawn_vnd: float = 0.0,
    override_p2p_blocked: bool = False,
    override_account_restricted: bool = False,
    missed_count: int = 13,
    current_date_str: Optional[str] = None,
    snapshot: Optional[ValuationSnapshot] = None
) -> MatrixEvaluation:
    """
    Evaluates Binary Decision Matrix according to updated constraints:
    - If TTS >= 540tr VND -> TAKE_PROFIT_540M (Take profit 50% immediately)
    - If TTS < 540tr VND -> HARD_FLOOR_BREACH (EMERGENCY Market Sell ALL)
    """
    if snapshot is not None:
        tts_vnd = snapshot.tts_vnd
        btc_qty = snapshot.btc_qty
        sol_qty = snapshot.sol_qty
        stables_usd = snapshot.stables_usd
        btc_price = snapshot.btc_price
        sol_price = snapshot.sol_price
        p2p_rate = snapshot.p2p_rate
        withdrawn_vnd = snapshot.withdrawn_vnd

    if tts_vnd is None:
        crypto_usd = (btc_qty * btc_price) + (sol_qty * sol_price) + stables_usd
        tts_vnd = withdrawn_vnd + (crypto_usd * p2p_rate)

    overrides = check_overrides(
        tts_vnd=tts_vnd,
        override_p2p_blocked=override_p2p_blocked,
        override_account_restricted=override_account_restricted,
        current_date_str=current_date_str
    )

    days_left = get_days_to_deadline(current_date_str)
    distance_vnd = tts_vnd - HARD_FLOOR_VND
    distance_pct = (distance_vnd / HARD_FLOOR_VND) * 100.0

    # Decision Matrix Evaluation
    if any("OVERRIDE" in o and "HARD_FLOOR" not in o for o in overrides):
        active_band = "OVERRIDE_EMERGENCY"
        urgent = True
        orders = calculate_emergency_sell_all_orders(
            btc_qty=btc_qty,
            sol_qty=sol_qty,
            stables_usd=stables_usd,
            btc_price=btc_price,
            sol_price=sol_price,
            p2p_rate=p2p_rate,
            reason_prefix="OVERRIDE EMERGENCY"
        )
    elif tts_vnd >= HARD_FLOOR_VND:
        active_band = "TAKE_PROFIT_540M"
        urgent = True
        orders = calculate_take_profit_orders(
            btc_qty=btc_qty,
            sol_qty=sol_qty,
            stables_usd=stables_usd,
            btc_price=btc_price,
            sol_price=sol_price,
            p2p_rate=p2p_rate,
            withdrawn_vnd=withdrawn_vnd
        )
    else:
        active_band = "HARD_FLOOR_BREACH"
        urgent = True
        orders = calculate_emergency_sell_all_orders(
            btc_qty=btc_qty,
            sol_qty=sol_qty,
            stables_usd=stables_usd,
            btc_price=btc_price,
            sol_price=sol_price,
            p2p_rate=p2p_rate,
            reason_prefix="HARD FLOOR BREACHED (<540tr)"
        )

    return MatrixEvaluation(
        hard_floor_vnd=HARD_FLOOR_VND,
        active_band=active_band,
        distance_to_floor_vnd=distance_vnd,
        distance_to_floor_pct=distance_pct,
        urgent_action_required=urgent,
        missed_recommendations_count=missed_count,
        orders_sheet=orders,
        overrides_triggered=overrides,
        days_to_deadline=days_left,
        deadline_date=CASH_OUT_DEADLINE_STR
    )


# Alias evaluate_matrix
evaluate_matrix = evaluate_binary_matrix
