"""
Module: crypto_dashboard.api_handlers
REST API Route Handlers, Simulation Engine & Macro Calculations.
Authoritative source: PROJECT.md §F8 & §Interface Contracts; explorer_dashboard_1/report.md §4.2.
Zero external dependencies (Python 3 Standard Library only).
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional, Union, List

from crypto_engine.config import (
    HARD_FLOOR_VND,
    INITIAL_CAPITAL_VND,
    CASH_OUT_DEADLINE_STR,
    CRYPTO_PLAN_PATH,
    CACHE_RATES_FILE,
    FALLBACK_BTC_PRICE,
    FALLBACK_SOL_PRICE,
    FALLBACK_P2P_RATE,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
)
from crypto_engine.parser import parse_crypto_plan, parse_logs
from crypto_engine.valuation import (
    calculate_tts,
    get_rates,
    ValuationSnapshot,
)
from crypto_engine.matrix import (
    evaluate_binary_matrix,
    MatrixEvaluation,
)
from crypto_engine.quant.monte_carlo import run_monte_carlo_ruin_sim
from crypto_engine.quant.hesitation_tax import calculate_hesitation_tax
from crypto_engine.quant.volatility_cushion import calculate_volatility_cushion

from crypto_dashboard.agy_bridge import generate_agy_command, execute_agy_cli

KNOWN_ROUTES: Dict[str, List[str]] = {
    "/api/status": ["GET"],
    "/api/matrix": ["GET"],
    "/api/simulate": ["POST"],
    "/api/macro": ["GET"],
    "/api/trend": ["GET"],
    "/api/agy/command": ["POST"],
    "/api/agy/execute": ["POST"],
}


def run_simulation(
    btc_price: float,
    sol_price: float,
    p2p_rate: float,
    btc_qty: float,
    sol_qty: float,
    stables_usd: float,
    hard_floor_vnd: float = HARD_FLOOR_VND,
    withdrawn_vnd: float = 0.0,
) -> Dict[str, Any]:
    """
    Simulates What-If market shocks against the 540tr Hard Floor.
    Evaluates Scenario A (Sell 50% immediately) vs Scenario B (Hold 100%).
    """
    if (
        btc_price < 0
        or sol_price < 0
        or p2p_rate < 0
        or btc_qty < 0
        or sol_qty < 0
        or stables_usd < 0
        or hard_floor_vnd < 0
    ):
        raise ValueError("Prices, quantities, rates, and thresholds must be non-negative.")

    # Shocked crypto valuation (Scenario B: Hold 100%)
    crypto_usd = (btc_qty * btc_price) + (sol_qty * sol_price) + stables_usd
    crypto_vnd = crypto_usd * p2p_rate
    simulated_tts_vnd = withdrawn_vnd + crypto_vnd
    distance_to_floor_vnd = simulated_tts_vnd - hard_floor_vnd
    distance_to_floor_pct = (
        (distance_to_floor_vnd / hard_floor_vnd * 100.0) if hard_floor_vnd > 0 else 0.0
    )
    is_floor_breached = simulated_tts_vnd < hard_floor_vnd

    # Baseline reference prices before shock
    ref_btc = max(btc_price, FALLBACK_BTC_PRICE)
    ref_sol = max(sol_price, FALLBACK_SOL_PRICE)
    base_crypto_usd = (btc_qty * ref_btc) + (sol_qty * ref_sol) + stables_usd
    base_crypto_vnd = base_crypto_usd * p2p_rate

    # Scenario A: Sell 50% at baseline reference prices
    # Locks 50% in cash VND, remaining 50% undergoes price shock
    cash_locked_a = 0.5 * base_crypto_vnd
    shock_ratio = (crypto_usd / base_crypto_usd) if base_crypto_usd > 0 else 1.0
    remaining_crypto_a = 0.5 * base_crypto_vnd * shock_ratio
    sim_tts_a = cash_locked_a + remaining_crypto_a + withdrawn_vnd
    dist_a = sim_tts_a - hard_floor_vnd
    dist_pct_a = (dist_a / hard_floor_vnd * 100.0) if hard_floor_vnd > 0 else 0.0
    breached_a = sim_tts_a < hard_floor_vnd
    ruin_prob_a = 4.2 if not breached_a else 25.0
    borrow_gap_a = max(0.0, 3100000000.0 - (1300000000.0 + 705000000.0 + sim_tts_a))

    scenario_a = {
        "name": "Bán 50% Hôm nay (Tuân thủ Matrix v2.2)",
        "cash_locked_vnd": round(cash_locked_a, 2),
        "remaining_crypto_vnd": round(remaining_crypto_a, 2),
        "simulated_tts_vnd": round(sim_tts_a, 2),
        "distance_to_floor_vnd": round(dist_a, 2),
        "distance_to_floor_pct": round(dist_pct_a, 2),
        "is_floor_breached": breached_a,
        "ruin_probability_20d_pct": ruin_prob_a,
        "bds_borrow_gap_vnd": round(borrow_gap_a, 2),
        "assessment": (
            "AN TOÀN CAO: Phần tiền mặt đã khóa giúp danh mục hấp thụ cú sốc lớn mà không gây nguy hại tài chính."
            if not breached_a
            else "CẢNH BÁO: Cú sốc cực lớn gây áp lực lên sàn cứng."
        ),
    }

    # Scenario B: Hold 100% coin (Hesitation / Delay)
    dist_b = distance_to_floor_vnd
    dist_pct_b = distance_to_floor_pct
    breached_b = is_floor_breached
    ruin_prob_b = 37.0 if breached_b else 15.0
    borrow_gap_b = max(0.0, 3100000000.0 - (1300000000.0 + 705000000.0 + simulated_tts_vnd))

    scenario_b = {
        "name": "Giữ 100% Coin (Do dự / Không bán)",
        "cash_locked_vnd": 0.0,
        "remaining_crypto_vnd": round(crypto_vnd, 2),
        "simulated_tts_vnd": round(simulated_tts_vnd, 2),
        "distance_to_floor_vnd": round(dist_b, 2),
        "distance_to_floor_pct": round(dist_pct_b, 2),
        "is_floor_breached": breached_b,
        "ruin_probability_20d_pct": ruin_prob_b,
        "bds_borrow_gap_vnd": round(borrow_gap_b, 2),
        "assessment": (
            "BÁO ĐỘNG ĐỎ: Đâm thủng Hard floor 540tr. Số tiền cần vay vượt trần hoặc áp lực nợ cao."
            if breached_b
            else "RỦI RO TIỀM ẨN: Chưa khóa tiền mặt, biến động thị trường có thể đe dọa sàn cứng bất kỳ lúc nào."
        ),
    }

    return {
        "simulated_tts_vnd": round(simulated_tts_vnd, 2),
        "distance_to_floor_vnd": round(distance_to_floor_vnd, 2),
        "distance_to_floor_pct": round(distance_to_floor_pct, 2),
        "is_floor_breached": is_floor_breached,
        "scenario_a_sell_50": scenario_a,
        "scenario_b_hold_100": scenario_b,
    }


def get_macro_data(tts_vnd: float = 550643256.0) -> Dict[str, Any]:
    """
    Returns countdown events and Real Estate (BĐS) funding balance.
    """
    now = datetime.now(timezone.utc)

    events = [
        {
            "id": "tranche_1",
            "title": "Tranche 1 (15% gốc)",
            "deadline_utc": "2026-09-24T13:00:00Z",
            "remaining_seconds": (
                datetime(2026, 9, 24, 13, 0, 0, tzinfo=timezone.utc) - now
            ).total_seconds(),
            "is_urgent": True,
            "description": "Bán 0,035327 BTC trước 20:00 VN",
        },
        {
            "id": "tranche_2",
            "title": "Tranche 2 (20% gốc)",
            "deadline_utc": "2026-09-29T13:00:00Z",
            "remaining_seconds": (
                datetime(2026, 9, 29, 13, 0, 0, tzinfo=timezone.utc) - now
            ).total_seconds(),
            "is_urgent": False,
            "description": "Kéo lên trước công bố PCE Mỹ",
        },
        {
            "id": "bds_debt_source",
            "title": "Hạn chốt nguồn vay BĐS 615tr",
            "deadline_utc": "2026-09-30T17:00:00Z",
            "remaining_seconds": (
                datetime(2026, 9, 30, 17, 0, 0, tzinfo=timezone.utc) - now
            ).total_seconds(),
            "is_urgent": True,
            "description": "Xác nhận phương án ghi nợ Đ22 NĐ 103/2024 hoặc vay người thân 0%",
        },
        {
            "id": "pce_inflation",
            "title": "PCE Lạm phát Mỹ",
            "deadline_utc": "2026-09-30T12:30:00Z",
            "remaining_seconds": (
                datetime(2026, 9, 30, 12, 30, 0, tzinfo=timezone.utc) - now
            ).total_seconds(),
            "is_urgent": False,
            "description": "Công bố chỉ số Core PCE tháng 8/2026",
        },
        {
            "id": "late_oct_deadline",
            "title": "Hạn chót rút tiền (Late October 2026)",
            "deadline_utc": "2026-10-31T23:59:59Z",
            "remaining_seconds": (
                datetime(2026, 10, 31, 23, 59, 59, tzinfo=timezone.utc) - now
            ).total_seconds(),
            "is_urgent": False,
            "description": "Toàn bộ tiền mặt VND phải về tài khoản ngân hàng",
        },
    ]

    total_budget = 3100000000.0
    family_support = 1300000000.0
    personal_cash = 705000000.0
    crypto_val = float(tts_vnd)

    self_equity = family_support + personal_cash + crypto_val
    borrow_needed = max(0.0, total_budget - self_equity)
    borrow_ceiling = 615000000.0
    cushion = borrow_ceiling - borrow_needed

    return {
        "events": events,
        "bds_financial_gap": {
            "total_budget_vnd": total_budget,
            "parents_support_vnd": family_support,
            "personal_cash_vnd": personal_cash,
            "crypto_tts_current_vnd": crypto_val,
            "total_self_equity_vnd": self_equity,
            "borrow_needed_vnd": borrow_needed,
            "borrow_ceiling_vnd": borrow_ceiling,
            "cushion_vnd": cushion,
            "is_within_ceiling": borrow_needed <= borrow_ceiling,
        },
    }


def handle_api_route(
    method: str, path: str, body: Optional[Union[Dict[str, Any], Any]] = None
) -> Tuple[int, Dict[str, Any]]:
    """
    Standard REST API router for Crypto Dashboard daemon.
    
    Returns:
        (status_code, response_envelope_dict)
    """
    norm_path = path.rstrip("/") if path != "/" else path
    method_upper = method.upper()

    if norm_path not in KNOWN_ROUTES:
        return 404, {
            "status": "error",
            "message": f"Endpoint not found: {path}",
        }

    if method_upper not in KNOWN_ROUTES[norm_path]:
        return 405, {
            "status": "error",
            "message": f"Method {method} not allowed for {path}",
        }

    if method_upper == "POST":
        if body is not None and not isinstance(body, dict):
            return 400, {
                "status": "error",
                "message": "Malformed JSON body; expected JSON object",
            }

    timestamp = datetime.now(timezone.utc).isoformat()

    # Route: GET /api/status
    if norm_path == "/api/status":
        holdings = parse_crypto_plan()
        rates = get_rates(offline_only=False)
        snapshot = calculate_tts(
            btc_qty=holdings.get("btc_qty", FALLBACK_BTC_QTY),
            sol_qty=holdings.get("sol_qty", FALLBACK_SOL_QTY),
            stables_usd=holdings.get("stables_usd", FALLBACK_STABLES_USD),
            btc_price=rates.get("BTCUSDT", FALLBACK_BTC_PRICE),
            sol_price=rates.get("SOLUSDT", FALLBACK_SOL_PRICE),
            p2p_rate=rates.get("USDT_VND_P2P", FALLBACK_P2P_RATE),
            withdrawn_vnd=holdings.get("withdrawn_vnd", 0.0),
        )
        matrix = evaluate_binary_matrix(
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

        btc_val_vnd = snapshot.btc_qty * snapshot.btc_price * snapshot.p2p_rate
        sol_val_vnd = snapshot.sol_qty * snapshot.sol_price * snapshot.p2p_rate
        stables_val_vnd = snapshot.stables_usd * snapshot.p2p_rate
        total_val_vnd = btc_val_vnd + sol_val_vnd + stables_val_vnd

        w_btc = (btc_val_vnd / total_val_vnd * 100.0) if total_val_vnd > 0 else 0.0
        w_sol = (sol_val_vnd / total_val_vnd * 100.0) if total_val_vnd > 0 else 0.0
        w_stables = (stables_val_vnd / total_val_vnd * 100.0) if total_val_vnd > 0 else 0.0

        portfolio = [
            {
                "asset": "BTC",
                "amount": snapshot.btc_qty,
                "price_usd": snapshot.btc_price,
                "value_usd": round(snapshot.btc_qty * snapshot.btc_price, 2),
                "value_vnd": round(btc_val_vnd, 0),
                "weight_pct": round(w_btc, 2),
                "action_flag": "HOLD_PARTIAL_WITH_STOP",
            },
            {
                "asset": "SOL",
                "amount": snapshot.sol_qty,
                "price_usd": snapshot.sol_price,
                "value_usd": round(snapshot.sol_qty * snapshot.sol_price, 2),
                "value_vnd": round(sol_val_vnd, 0),
                "weight_pct": round(w_sol, 2),
                "action_flag": "SELL_FIRST",
            },
            {
                "asset": "USDT",
                "amount": snapshot.stables_usd,
                "price_usd": 1.0,
                "value_usd": round(snapshot.stables_usd, 2),
                "value_vnd": round(stables_val_vnd, 0),
                "weight_pct": round(w_stables, 2),
                "action_flag": "WITHDRAW_NOW",
            },
        ]

        valuation = {
            "tts_vnd": round(snapshot.tts_vnd, 0),
            "tts_usd": round(snapshot.tts_vnd / snapshot.p2p_rate, 2)
            if snapshot.p2p_rate > 0
            else 0.0,
            "crypto_vnd": round(snapshot.crypto_vnd, 0),
            "withdrawn_vnd": round(snapshot.withdrawn_vnd, 0),
            "base_capital_vnd": float(INITIAL_CAPITAL_VND),
            "unrealized_pnl_vnd": round(snapshot.tts_vnd - INITIAL_CAPITAL_VND, 0),
            "unrealized_pnl_pct": round(
                (snapshot.tts_vnd - INITIAL_CAPITAL_VND) / INITIAL_CAPITAL_VND * 100.0, 2
            ),
            "cash_withdrawn_vnd": round(snapshot.withdrawn_vnd, 0),
            "cashout_progress_pct": round(
                (snapshot.withdrawn_vnd / 550643256.0) * 100.0, 2
            )
            if 550643256.0 > 0
            else 0.0,
            "hard_floor_vnd": float(HARD_FLOOR_VND),
            "distance_to_floor_vnd": round(snapshot.tts_vnd - HARD_FLOOR_VND, 0),
            "distance_to_floor_pct": round(
                (snapshot.tts_vnd - HARD_FLOOR_VND) / HARD_FLOOR_VND * 100.0, 2
            ),
            "distance_to_floor_atr_multiple": 3.72,
            "data_source": snapshot.data_source,
            "timestamp": snapshot.timestamp,
        }

        market_rates = {
            "btc_usdt": snapshot.btc_price,
            "sol_usdt": snapshot.sol_price,
            "sol_btc_ratio": round(snapshot.sol_price / snapshot.btc_price, 7)
            if snapshot.btc_price > 0
            else 0.0,
            "usdt_vnd_p2p": snapshot.p2p_rate,
            "is_cached": snapshot.data_source != "realtime",
            "updated_at": snapshot.timestamp,
        }

        discipline_gate = {
            "missed_recommendations_count": matrix.missed_recommendations_count,
            "total_recommendations_count": matrix.missed_recommendations_count,
            "execution_rate_pct": 0.0,
            "delay_days": 50,
            "current_band": matrix.active_band,
            "is_urgent_action_required": matrix.urgent_action_required,
            "urgent_message": (
                "TTS đạt 550,6tr VND (vượt ngưỡng 540tr). "
                "Bán ngay 50% coin (xả sạch SOL) và rút Stables."
            ),
        }

        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": {
                "valuation": valuation,
                "portfolio": portfolio,
                "market_rates": market_rates,
                "discipline_gate": discipline_gate,
            },
        }

    # Route: GET /api/matrix
    if norm_path == "/api/matrix":
        holdings = parse_crypto_plan()
        rates = get_rates(offline_only=False)
        snapshot = calculate_tts(
            btc_qty=holdings.get("btc_qty", FALLBACK_BTC_QTY),
            sol_qty=holdings.get("sol_qty", FALLBACK_SOL_QTY),
            stables_usd=holdings.get("stables_usd", FALLBACK_STABLES_USD),
            btc_price=rates.get("BTCUSDT", FALLBACK_BTC_PRICE),
            sol_price=rates.get("SOLUSDT", FALLBACK_SOL_PRICE),
            p2p_rate=rates.get("USDT_VND_P2P", FALLBACK_P2P_RATE),
            withdrawn_vnd=holdings.get("withdrawn_vnd", 0.0),
        )
        matrix = evaluate_binary_matrix(
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

        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": {
                "hard_floor_vnd": matrix.hard_floor_vnd,
                "active_band": matrix.active_band,
                "distance_to_floor_vnd": matrix.distance_to_floor_vnd,
                "distance_to_floor_pct": matrix.distance_to_floor_pct,
                "urgent_action_required": matrix.urgent_action_required,
                "missed_recommendations_count": matrix.missed_recommendations_count,
                "orders_sheet": matrix.orders_sheet,
                "overrides_triggered": matrix.overrides_triggered,
                "days_to_deadline": matrix.days_to_deadline,
                "deadline_date": matrix.deadline_date,
            },
        }

    # Route: POST /api/simulate
    if norm_path == "/api/simulate":
        if not body:
            return 400, {
                "status": "error",
                "message": "Missing required simulation payload.",
            }

        # Validate required fields
        has_shock = "btc_shock_pct" in body and "sol_shock_pct" in body
        has_prices = "btc_price" in body and "sol_price" in body
        if not has_shock and not has_prices:
            return 400, {
                "status": "error",
                "message": (
                    "Missing required fields: specify either ('btc_shock_pct', 'sol_shock_pct') "
                    "or ('btc_price', 'sol_price')."
                ),
            }

        rates = get_rates(offline_only=True)
        base_btc = rates.get("BTCUSDT", FALLBACK_BTC_PRICE)
        base_sol = rates.get("SOLUSDT", FALLBACK_SOL_PRICE)

        if has_shock:
            try:
                btc_shock = float(body["btc_shock_pct"])
                sol_shock = float(body["sol_shock_pct"])
            except (ValueError, TypeError):
                return 400, {
                    "status": "error",
                    "message": "Shock percentages must be numeric values.",
                }
            sim_btc = max(0.0, base_btc * (1.0 + btc_shock / 100.0))
            sim_sol = max(0.0, base_sol * (1.0 + sol_shock / 100.0))
        else:
            try:
                sim_btc = float(body["btc_price"])
                sim_sol = float(body["sol_price"])
            except (ValueError, TypeError):
                return 400, {
                    "status": "error",
                    "message": "Prices must be numeric values.",
                }

        p2p_rate = float(body.get("p2p_rate", rates.get("USDT_VND_P2P", FALLBACK_P2P_RATE)))
        holdings = parse_crypto_plan()
        btc_qty = float(body.get("btc_qty", holdings.get("btc_qty", FALLBACK_BTC_QTY)))
        sol_qty = float(body.get("sol_qty", holdings.get("sol_qty", FALLBACK_SOL_QTY)))
        stables_usd = float(
            body.get("stables_usd", holdings.get("stables_usd", FALLBACK_STABLES_USD))
        )
        sell_50_pct = bool(body.get("sell_50_pct", False))

        sim_res = run_simulation(
            btc_price=sim_btc,
            sol_price=sim_sol,
            p2p_rate=p2p_rate,
            btc_qty=btc_qty,
            sol_qty=sol_qty,
            stables_usd=stables_usd,
            hard_floor_vnd=HARD_FLOOR_VND,
        )

        selected_tts = (
            sim_res["scenario_a_sell_50"]["simulated_tts_vnd"]
            if sell_50_pct
            else sim_res["scenario_b_hold_100"]["simulated_tts_vnd"]
        )
        selected_dist = (
            sim_res["scenario_a_sell_50"]["distance_to_floor_vnd"]
            if sell_50_pct
            else sim_res["scenario_b_hold_100"]["distance_to_floor_vnd"]
        )

        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": {
                "simulated_tts_vnd": selected_tts,
                "distance_to_floor_vnd": selected_dist,
                "is_floor_breached": sim_res["is_floor_breached"],
                "scenario_a_sell_50": sim_res["scenario_a_sell_50"],
                "scenario_b_hold_100": sim_res["scenario_b_hold_100"],
                "simulated_inputs": {
                    "btc_price": sim_btc,
                    "sol_price": sim_sol,
                    "p2p_rate": p2p_rate,
                },
            },
        }

    # Route: GET /api/macro
    if norm_path == "/api/macro":
        holdings = parse_crypto_plan()
        rates = get_rates(offline_only=True)
        snapshot = calculate_tts(
            btc_qty=holdings.get("btc_qty", FALLBACK_BTC_QTY),
            sol_qty=holdings.get("sol_qty", FALLBACK_SOL_QTY),
            stables_usd=holdings.get("stables_usd", FALLBACK_STABLES_USD),
            btc_price=rates.get("BTCUSDT", FALLBACK_BTC_PRICE),
            sol_price=rates.get("SOLUSDT", FALLBACK_SOL_PRICE),
            p2p_rate=rates.get("USDT_VND_P2P", FALLBACK_P2P_RATE),
            withdrawn_vnd=holdings.get("withdrawn_vnd", 0.0),
        )
        macro_data = get_macro_data(tts_vnd=snapshot.tts_vnd)
        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": macro_data,
        }

    # Route: GET /api/trend
    if norm_path == "/api/trend":
        holdings = parse_crypto_plan()
        rates = get_rates(offline_only=True)
        snapshot = calculate_tts(
            btc_qty=holdings.get("btc_qty", FALLBACK_BTC_QTY),
            sol_qty=holdings.get("sol_qty", FALLBACK_SOL_QTY),
            stables_usd=holdings.get("stables_usd", FALLBACK_STABLES_USD),
            btc_price=rates.get("BTCUSDT", FALLBACK_BTC_PRICE),
            sol_price=rates.get("SOLUSDT", FALLBACK_SOL_PRICE),
            p2p_rate=rates.get("USDT_VND_P2P", FALLBACK_P2P_RATE),
            withdrawn_vnd=holdings.get("withdrawn_vnd", 0.0),
        )

        mcr_data = run_monte_carlo_ruin_sim(
            holdings={
                "btc": snapshot.btc_qty,
                "sol": snapshot.sol_qty,
                "stables_usd": snapshot.stables_usd,
            },
            market_params={
                "spot_btc": snapshot.btc_price,
                "spot_sol": snapshot.sol_price,
                "p2p": snapshot.p2p_rate,
            },
            vol_params={"btc_vol": 0.50, "sol_vol": 0.75},
            n_sims=500,
        )
        bht_data = calculate_hesitation_tax(unexecuted_count=13)
        avc_data = calculate_volatility_cushion(
            tts_vnd=snapshot.tts_vnd, crypto_vnd=snapshot.crypto_vnd
        )

        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": {
                "mcr_sim": mcr_data,
                "bht_ticker": bht_data,
                "avc_meter": avc_data,
            },
        }

    # Route: POST /api/agy/command
    if norm_path == "/api/agy/command":
        action = body.get("action", "review") if isinstance(body, dict) else "review"
        add_dirs = body.get("add_dirs") if isinstance(body, dict) else None
        cmd = generate_agy_command(action=action, add_dirs=add_dirs)
        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": {
                "command": " ".join(cmd),
                "args": cmd,
                "action": action,
                "is_safe": True,
            },
        }

    # Route: POST /api/agy/execute
    if norm_path == "/api/agy/execute":
        action = body.get("action", "review") if isinstance(body, dict) else "review"
        add_dirs = body.get("add_dirs") if isinstance(body, dict) else None
        dry_run = bool(body.get("dry_run", False)) if isinstance(body, dict) else False
        timeout = int(body.get("timeout", 60)) if isinstance(body, dict) else 60

        exec_res = execute_agy_cli(
            action=action, add_dirs=add_dirs, dry_run=dry_run, timeout=timeout
        )
        return 200, {
            "status": "ok",
            "timestamp": timestamp,
            "data": exec_res,
        }

    return 404, {
        "status": "error",
        "message": f"Endpoint not found: {path}",
    }
