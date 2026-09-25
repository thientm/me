"""
Module: crypto_engine.quant.monte_carlo
Monte Carlo Liquidity Ruin Probability & First-Passage Exit Simulator (MCR-Sim).
Quant Innovation 1 for Crypto Dashboard.
Zero external dependencies (Python 3 Standard Library only: math, random).
"""

from __future__ import annotations
import math
import random
from typing import Dict, Any, Optional, Tuple, List, Union

DEFAULT_HARD_FLOOR_VND: float = 540_000_000.0
DEFAULT_HORIZON_DAYS: int = 37  # 2026-09-24 to 2026-10-31 Late October cashout deadline
DEFAULT_N_SIMS: int = 1000
DEFAULT_RHO: float = 0.78       # BTC-SOL empirical correlation


def run_monte_carlo_ruin_sim(
    holdings: Dict[str, Any],
    market_params: Dict[str, Any],
    vol_params: Dict[str, Any],
    n_sims: int = DEFAULT_N_SIMS,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
    hard_floor: float = DEFAULT_HARD_FLOOR_VND,
    strategy: str = "HOLD_100",
    glidepath_sched: Optional[Dict[int, Tuple[float, float, float]]] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Simulates stochastic TTS paths using correlated Wiener increments (Cholesky decomposition)
    under a zero-drift geometric brownian motion.
    
    Evaluates First-Passage Ruin Probability against the hard floor (TTS(t) < hard_floor)
    over the horizon up to Late October 2026 (37 days).
    
    Returns:
    - prob_ruin: float (first-passage ruin frequency)
    - var_95_vnd: float (5th percentile terminal TTS)
    - cvar_95_vnd: float (conditional expectation of worst 5% tail)
    - median_tts_vnd: float (50th percentile terminal TTS)
    - percentiles: {"p5", "p50", "p95"}
    - safety_status: "CRITICAL_RUIN_RISK" | "SAFE_SECURED"
    """
    safe_sims = max(10, int(n_sims))
    safe_horizon = max(1, int(horizon_days))
    safe_floor = float(hard_floor)

    # Extract holdings
    q_btc = float(holdings.get("btc", 0.0))
    q_sol = float(holdings.get("sol", 0.0))
    q_stables = float(holdings.get("stables_usd", holdings.get("stables", 0.0)))
    cash_vnd = float(holdings.get("cash_vnd", holdings.get("cash_vnd_withdrawn", holdings.get("withdrawn_vnd", 0.0))))

    # Extract market parameters
    spot_btc = float(market_params.get("spot_btc", market_params.get("btc_usdt", 84262.0)))
    spot_sol = float(market_params.get("sol_usdt", market_params.get("spot_sol", 115.72)))
    p2p = float(market_params.get("p2p", market_params.get("p2p_rate", 25930.0)))

    # Extract volatility parameters
    sigma_btc = max(0.0, float(vol_params.get("sigma_btc", vol_params.get("btc_atr14_pct", 0.0270))))
    sigma_sol = max(0.0, float(vol_params.get("sigma_sol", vol_params.get("sol_atr14_pct", 0.0451))))
    raw_rho = float(vol_params.get("rho", vol_params.get("correlation", DEFAULT_RHO)))
    clamped_rho = min(1.0, max(-1.0, raw_rho))
    sqrt_1_rho2 = math.sqrt(max(0.0, 1.0 - clamped_rho ** 2))

    # Evaluate strategy and floor adjustments
    # Under SELL_50 or de-risking strategies, the target floor is scaled to the remaining exposure
    strat_upper = strategy.upper() if strategy else "HOLD_100"
    if "SELL_50" in strat_upper or "BAND_50" in strat_upper:
        effective_floor = safe_floor * 0.5
        # If unliquidated holdings were passed, simulate immediate 50% de-risking
        if cash_vnd == 0.0 and (q_sol > 0.0 or q_stables > 0.0):
            cash_vnd += (q_sol * spot_sol + q_stables + 0.5 * q_btc * spot_btc) * p2p
            q_sol = 0.0
            q_stables = 0.0
            q_btc = 0.5 * q_btc
    else:
        effective_floor = safe_floor

    # Zero-drift Ito adjustments (-0.5 * sigma^2)
    s_btc_drift = -0.5 * (sigma_btc ** 2)
    s_sol_drift = -0.5 * (sigma_sol ** 2)

    # Initial TTS evaluation
    initial_tts = cash_vnd + (q_btc * spot_btc + q_sol * spot_sol + q_stables) * p2p
    initial_ruined = initial_tts < effective_floor

    ruin_count = 0
    terminal_tts_list: List[float] = []

    # Fast bindings for Python loop
    random_gauss = random.gauss
    math_exp = math.exp

    for _ in range(safe_sims):
        p_b = spot_btc
        p_s = spot_sol
        cur_q_b = q_btc
        cur_q_s = q_sol
        cur_q_u = q_stables
        cur_cash = cash_vnd
        ruined = initial_ruined

        for t in range(1, safe_horizon + 1):
            # Correlated Wiener increments via Cholesky decomposition
            z1 = random_gauss(0.0, 1.0)
            z2 = random_gauss(0.0, 1.0)
            w1 = z1
            w2 = clamped_rho * z1 + sqrt_1_rho2 * z2

            if sigma_btc > 0.0:
                p_b *= math_exp(s_btc_drift + sigma_btc * w1)
            if sigma_sol > 0.0:
                p_s *= math_exp(s_sol_drift + sigma_sol * w2)

            # Apply glidepath tranches if scheduled for day t
            if glidepath_sched and t in glidepath_sched:
                d_b, d_s, d_u = glidepath_sched[t]
                cur_cash += (d_b * p_b + d_s * p_s + d_u) * p2p
                cur_q_b = max(0.0, cur_q_b - d_b)
                cur_q_s = max(0.0, cur_q_s - d_s)
                cur_q_u = max(0.0, cur_q_u - d_u)

            tts_t = cur_cash + (cur_q_b * p_b + cur_q_s * p_s + cur_q_u) * p2p
            if tts_t < effective_floor:
                ruined = True

        if ruined:
            ruin_count += 1
        terminal_tts_list.append(tts_t)

    prob_ruin = float(ruin_count) / float(safe_sims)
    terminal_tts_list.sort()

    # Percentiles: VaR 95% = 5th percentile, CVaR 95% = mean of values <= 5th percentile
    idx_5 = max(0, min(safe_sims - 1, int(safe_sims * 0.05)))
    var_95 = terminal_tts_list[idx_5]
    tail = terminal_tts_list[: max(1, idx_5 + 1)]
    cvar_95 = sum(tail) / float(len(tail))

    idx_50 = max(0, min(safe_sims - 1, int(safe_sims * 0.5)))
    median_tts = terminal_tts_list[idx_50]

    idx_95 = max(0, min(safe_sims - 1, int(safe_sims * 0.95)))
    p95 = terminal_tts_list[idx_95]

    return {
        "prob_ruin": prob_ruin,
        "var_95_vnd": round(var_95, 2),
        "cvar_95_vnd": round(cvar_95, 2),
        "median_tts_vnd": round(median_tts, 2),
        "percentiles": {
            "p5": round(var_95, 2),
            "p50": round(median_tts, 2),
            "p95": round(p95, 2),
        },
        "safety_status": "CRITICAL_RUIN_RISK" if prob_ruin >= 0.10 else "SAFE_SECURED",
        "n_sims": safe_sims,
        "horizon_days": safe_horizon,
        "hard_floor_vnd": safe_floor,
        "effective_floor_vnd": effective_floor,
        "strategy": strategy,
        "initial_tts_vnd": round(initial_tts, 2),
    }
