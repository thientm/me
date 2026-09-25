#!/usr/bin/env python3
"""
Adversarial Stress Harness for crypto_engine.quant.monte_carlo.
Executes empirical challenges against extreme parameters, boundary conditions,
and benchmarks execution performance.
"""

import sys
import os
import time
import math
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from crypto_engine.quant.monte_carlo import (
    run_monte_carlo_ruin_sim,
    DEFAULT_HARD_FLOOR_VND,
    DEFAULT_HORIZON_DAYS,
)

BASE_HOLDINGS = {
    "btc": 0.159310,
    "sol": 55.28,
    "stables_usd": 1415.0,
    "cash_vnd": 0.0,
}

BASE_MARKET = {
    "spot_btc": 84262.0,
    "sol_usdt": 115.72,
    "p2p": 25930.0,
}


def benchmark_suite():
    results = {}

    print("=" * 80)
    print("MCR-SIM ADVERSARIAL EMPIRICAL STRESS TEST HARNESS")
    print("Target: src/crypto_engine/quant/monte_carlo.py")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Challenge 1: Extreme Volatility Stress
    # -------------------------------------------------------------------------
    print("\n[CHALLENGE 1] Extreme Volatility Stress (sigma = 0.50, 1.0, 5.0, 0.0, -0.10)")
    sigmas = [0.0, 0.027, 0.15, 0.50, 1.00, 5.00, -0.10]
    vol_results = []
    for sig in sigmas:
        vol = {"sigma_btc": sig, "sigma_sol": sig, "rho": 0.78}
        try:
            t0 = time.perf_counter()
            res = run_monte_carlo_ruin_sim(
                holdings=BASE_HOLDINGS,
                market_params=BASE_MARKET,
                vol_params=vol,
                n_sims=1000,
                horizon_days=37,
                hard_floor=DEFAULT_HARD_FLOOR_VND,
            )
            elapsed = (time.perf_counter() - t0) * 1000
            status = "PASS"
            vol_results.append({
                "sigma": sig,
                "prob_ruin": res["prob_ruin"],
                "var_95": res["var_95_vnd"],
                "median": res["median_tts_vnd"],
                "latency_ms": round(elapsed, 2),
                "status": status,
            })
            print(f"  sigma={sig:5.2f} -> prob_ruin={res['prob_ruin']:6.3f} | VaR95={res['var_95_vnd']:14,.0f} VND | Latency: {elapsed:5.2f}ms [{status}]")
        except Exception as e:
            print(f"  sigma={sig:5.2f} -> EXCEPTION: {e} [FAIL]")
            vol_results.append({"sigma": sig, "error": str(e), "status": "FAIL"})

    results["extreme_volatility"] = vol_results

    # -------------------------------------------------------------------------
    # Challenge 2: Extreme Correlation Stress
    # -------------------------------------------------------------------------
    print("\n[CHALLENGE 2] Extreme Correlation Stress (rho = -1.0, -0.99, 0.0, 0.78, 1.0, 1.5, -2.0)")
    rhos = [-2.0, -1.0, -0.99, -0.5, 0.0, 0.5, 0.78, 1.0, 1.5]
    rho_results = []
    for r in rhos:
        vol = {"sigma_btc": 0.0270, "sigma_sol": 0.0451, "rho": r}
        try:
            t0 = time.perf_counter()
            res = run_monte_carlo_ruin_sim(
                holdings=BASE_HOLDINGS,
                market_params=BASE_MARKET,
                vol_params=vol,
                n_sims=1000,
                horizon_days=37,
                hard_floor=DEFAULT_HARD_FLOOR_VND,
            )
            elapsed = (time.perf_counter() - t0) * 1000
            status = "PASS"
            rho_results.append({
                "rho": r,
                "prob_ruin": res["prob_ruin"],
                "var_95": res["var_95_vnd"],
                "latency_ms": round(elapsed, 2),
                "status": status,
            })
            print(f"  rho={r:5.2f} -> prob_ruin={res['prob_ruin']:6.3f} | VaR95={res['var_95_vnd']:14,.0f} VND | Latency: {elapsed:5.2f}ms [{status}]")
        except Exception as e:
            print(f"  rho={r:5.2f} -> EXCEPTION: {e} [FAIL]")
            rho_results.append({"rho": r, "error": str(e), "status": "FAIL"})

    results["extreme_correlation"] = rho_results

    # -------------------------------------------------------------------------
    # Challenge 3: Horizon Boundary Stress
    # -------------------------------------------------------------------------
    print("\n[CHALLENGE 3] Horizon Boundary Stress (horizon = 0, 1, 7, 37, 180, 365, -5)")
    horizons = [-5, 0, 1, 7, 37, 180, 365]
    horizon_results = []
    for h in horizons:
        vol = {"sigma_btc": 0.0270, "sigma_sol": 0.0451, "rho": 0.78}
        try:
            t0 = time.perf_counter()
            res = run_monte_carlo_ruin_sim(
                holdings=BASE_HOLDINGS,
                market_params=BASE_MARKET,
                vol_params=vol,
                n_sims=1000,
                horizon_days=h,
                hard_floor=DEFAULT_HARD_FLOOR_VND,
            )
            elapsed = (time.perf_counter() - t0) * 1000
            status = "PASS"
            horizon_results.append({
                "input_horizon": h,
                "actual_horizon": res["horizon_days"],
                "prob_ruin": res["prob_ruin"],
                "latency_ms": round(elapsed, 2),
                "status": status,
            })
            print(f"  horizon={h:4d} (eff: {res['horizon_days']:3d}) -> prob_ruin={res['prob_ruin']:6.3f} | Latency: {elapsed:6.2f}ms [{status}]")
        except Exception as e:
            print(f"  horizon={h:4d} -> EXCEPTION: {e} [FAIL]")
            horizon_results.append({"input_horizon": h, "error": str(e), "status": "FAIL"})

    results["horizon_boundaries"] = horizon_results

    # -------------------------------------------------------------------------
    # Challenge 4: Portfolio Balance & Composition Corner Cases
    # -------------------------------------------------------------------------
    print("\n[CHALLENGE 4] Portfolio Composition & Balance Corner Cases")
    portfolios = {
        "Empty Wallet (0 all)": {"btc": 0.0, "sol": 0.0, "stables_usd": 0.0, "cash_vnd": 0.0},
        "Negative Cash Balance (-100M)": {"btc": 0.159310, "sol": 55.28, "stables_usd": 1415.0, "cash_vnd": -100_000_000.0},
        "Whale Portfolio (>100B VND)": {"btc": 100.0, "sol": 1000.0, "stables_usd": 5_000_000.0, "cash_vnd": 10_000_000_000.0},
        "Pure Cash (100% Stables)": {"btc": 0.0, "sol": 0.0, "stables_usd": 30000.0, "cash_vnd": 0.0},
        "Pure BTC (0 SOL, 0 USDT)": {"btc": 0.30, "sol": 0.0, "stables_usd": 0.0, "cash_vnd": 0.0},
    }
    port_results = []
    vol = {"sigma_btc": 0.0270, "sigma_sol": 0.0451, "rho": 0.78}
    for name, p in portfolios.items():
        try:
            res = run_monte_carlo_ruin_sim(
                holdings=p,
                market_params=BASE_MARKET,
                vol_params=vol,
                n_sims=1000,
                horizon_days=37,
                hard_floor=DEFAULT_HARD_FLOOR_VND,
            )
            status = "PASS"
            port_results.append({
                "name": name,
                "initial_tts": res["initial_tts_vnd"],
                "prob_ruin": res["prob_ruin"],
                "safety_status": res["safety_status"],
                "status": status,
            })
            print(f"  {name:32s} -> initTTS={res['initial_tts_vnd']:14,.0f} | ruin={res['prob_ruin']:5.2f} | status={res['safety_status']} [{status}]")
        except Exception as e:
            print(f"  {name:32s} -> EXCEPTION: {e} [FAIL]")
            port_results.append({"name": name, "error": str(e), "status": "FAIL"})

    results["portfolio_boundaries"] = port_results

    # -------------------------------------------------------------------------
    # Challenge 5: Pure Python Performance Benchmarks (5,000 paths < 500ms)
    # -------------------------------------------------------------------------
    print("\n[CHALLENGE 5] Pure Python Performance Benchmarks vs SLA")
    path_counts = [500, 1000, 2000, 5000, 10000]
    perf_results = []
    for n in path_counts:
        timings = []
        for _ in range(3):  # 3 iterations
            t0 = time.perf_counter()
            res = run_monte_carlo_ruin_sim(
                holdings=BASE_HOLDINGS,
                market_params=BASE_MARKET,
                vol_params=vol,
                n_sims=n,
                horizon_days=37,
                hard_floor=DEFAULT_HARD_FLOOR_VND,
            )
            timings.append((time.perf_counter() - t0) * 1000)
        avg_ms = sum(timings) / len(timings)
        min_ms = min(timings)
        sla_pass = avg_ms < 500.0 if n == 5000 else True
        perf_results.append({
            "n_paths": n,
            "avg_ms": round(avg_ms, 2),
            "min_ms": round(min_ms, 2),
            "sla_500ms": sla_pass,
        })
        sla_tag = "PASS (<500ms)" if sla_pass else "FAIL"
        print(f"  {n:6d} paths x 37 days -> Avg: {avg_ms:6.2f}ms (Min: {min_ms:6.2f}ms) | SLA: {sla_tag}")

    results["performance"] = perf_results

    # -------------------------------------------------------------------------
    # Challenge 6: Quant Behavioral & Algorithmic Probes (Findings)
    # -------------------------------------------------------------------------
    print("\n[CHALLENGE 6] Empirical Quant Logic Probes")

    # Probe 6.1: Glidepath overselling inventory clamp
    small_holdings = {"btc": 0.1, "sol": 0.0, "stables_usd": 0.0, "cash_vnd": 0.0}
    oversell_sched = {1: (10.0, 0.0, 0.0)}  # Sells 10 BTC when only owning 0.1 BTC
    res_oversell = run_monte_carlo_ruin_sim(
        holdings=small_holdings,
        market_params={"spot_btc": 80000.0, "sol_usdt": 100.0, "p2p": 25000.0},
        vol_params={"sigma_btc": 0.0, "sigma_sol": 0.0, "rho": 0.0},
        n_sims=50,
        horizon_days=5,
        glidepath_sched=oversell_sched,
    )
    phantom_created = res_oversell["median_tts_vnd"] > (0.1 * 80000.0 * 25000.0 * 1.1)
    probe_6_1 = {
        "description": "Glidepath tranche inventory bounding",
        "initial_tts": res_oversell["initial_tts_vnd"],
        "post_oversell_median_tts": res_oversell["median_tts_vnd"],
        "vulnerability_detected": phantom_created,
        "detail": "Selling 10 BTC on 0.1 BTC portfolio created 20B VND phantom cash without clamping to available quantity.",
    }
    print(f"  Probe 6.1 (Glidepath Oversell): Initial TTS = {res_oversell['initial_tts_vnd']:,.0f} VND -> Terminal TTS = {res_oversell['median_tts_vnd']:,.0f} VND")
    print(f"    Vulnerability Detected: {phantom_created} (Inventory not bounded before adding cash)")

    # Probe 6.2: SELL_50 pure BTC liquidation bypass
    btc_only = {"btc": 0.5, "sol": 0.0, "stables_usd": 0.0, "cash_vnd": 0.0}
    res_sell50_btc = run_monte_carlo_ruin_sim(
        holdings=btc_only,
        market_params={"spot_btc": 80000.0, "sol_usdt": 100.0, "p2p": 25000.0},
        vol_params={"sigma_btc": 0.027, "sigma_sol": 0.045, "rho": 0.78},
        strategy="SELL_50",
        n_sims=50,
        horizon_days=5,
    )
    # If BTC is not halved, initial_tts is 0.5 * 80000 * 25000 = 1,000,000,000 VND
    btc_not_halved = res_sell50_btc["initial_tts_vnd"] == 1_000_000_000.0
    probe_6_2 = {
        "description": "SELL_50 pure BTC liquidation bypass",
        "initial_tts": res_sell50_btc["initial_tts_vnd"],
        "effective_floor": res_sell50_btc["effective_floor_vnd"],
        "vulnerability_detected": btc_not_halved,
        "detail": "Condition 'cash_vnd == 0.0 and (q_sol > 0.0 or q_stables > 0.0)' skips BTC liquidation if SOL and Stables are 0, while still cutting floor to 270M.",
    }
    print(f"  Probe 6.2 (SELL_50 Pure BTC): Initial TTS = {res_sell50_btc['initial_tts_vnd']:,.0f} VND | Effective Floor = {res_sell50_btc['effective_floor_vnd']:,.0f} VND")
    print(f"    Vulnerability Detected: {btc_not_halved} (100% BTC portfolio skips 50% liquidation)")

    # Probe 6.3: SELL_50 Floor Halving Double-Counting
    res_crash_sell50 = run_monte_carlo_ruin_sim(
        holdings=BASE_HOLDINGS,
        market_params=BASE_MARKET,
        vol_params={"sigma_btc": 1.0, "sigma_sol": 1.0, "rho": 0.78},
        strategy="SELL_50",
        n_sims=500,
        horizon_days=37,
    )
    probe_6_3 = {
        "description": "SELL_50 floor halving double-counting under market crash",
        "prob_ruin_under_100pct_vol": res_crash_sell50["prob_ruin"],
        "effective_floor": res_crash_sell50["effective_floor_vnd"],
        "detail": "With 284.7M cash retained in TTS and floor halved to 270M, TTS can never drop below 284.7M, reporting 0.0% ruin even under catastrophic crypto collapse.",
    }
    print(f"  Probe 6.3 (SELL_50 Floor Distortion): Ruin under 100% vol crash = {res_crash_sell50['prob_ruin']:.4f} (Effective Floor: {res_crash_sell50['effective_floor_vnd']:,.0f} VND)")

    results["probes"] = [probe_6_1, probe_6_2, probe_6_3]

    print("\n" + "=" * 80)
    print("STRESS TEST EXECUTION COMPLETED")
    print("=" * 80)
    return results


if __name__ == "__main__":
    benchmark_suite()
