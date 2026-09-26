#!/usr/bin/env python3
"""
Antigravity Custom Skill Helper Script: crypto-manager
Location: skills/crypto-manager/scripts/run_review.py

Automated review, valuation, binary decision matrix evaluation (540tr floor),
and Section 7.5 log generator. Zero external dependencies (Python 3 stdlib only).
"""

from __future__ import annotations
import os
import sys
import json
import re
import ssl
import urllib.request
import urllib.error
import argparse
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict

# Add src to sys.path if running within project
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parents[3]  # .agents/skills/crypto-manager/scripts -> repo root
SRC_CANDIDATES = [
    WORKSPACE_ROOT / "crypto" / "dashboard" / "src",
    WORKSPACE_ROOT / "src",
    SCRIPT_DIR.parent.parent.parent / "src",
    Path("/Users/thien.tm/teamwork_projects/crypto_dashboard/src"),
]
for p in SRC_CANDIDATES:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from crypto_engine.config import (
        CRYPTO_PLAN_PATH,
        CRYPTO_LOGS_DIR,
        CACHE_RATES_FILE,
        HARD_FLOOR_VND,
        CASH_OUT_DEADLINE_STR,
        FALLBACK_BTC_QTY,
        FALLBACK_SOL_QTY,
        FALLBACK_STABLES_USD,
        BDS_TOTAL_COST_VND,
        BDS_PARENTS_CASH_VND,
        BDS_PERSONAL_CASH_VND,
        BDS_DEBT_CEILING_VND,
    )
    from crypto_engine.parser import parse_crypto_plan, parse_logs
    from crypto_engine.valuation import calculate_tts, get_rates
    from crypto_engine.matrix import evaluate_binary_matrix
    from crypto_engine.proposal import generate_markdown_review, generate_structured_proposal
    from crypto_engine.logger import append_review_log
    ENGINE_LOADED = True
except ImportError:
    ENGINE_LOADED = False
    _CANDIDATE_REPOS = [
        Path("/Users/thientm/Documents/GitHub/me"),
        WORKSPACE_ROOT,
        Path("/Users/thien.tm/Documents/me"),
    ]
    _repo = next((p for p in _CANDIDATE_REPOS if (p / "crypto" / "crypto-plan.md").exists()), Path("/Users/thien.tm/Documents/me"))
    CRYPTO_PLAN_PATH = _repo / "crypto" / "crypto-plan.md"
    CRYPTO_LOGS_DIR = _repo / "crypto" / "logs"
    CACHE_RATES_FILE = Path("/Users/thien.tm/teamwork_projects/crypto_dashboard/data/cache_rates.json")
    HARD_FLOOR_VND = 540_000_000.0
    CASH_OUT_DEADLINE_STR = "2026-10-31"
    FALLBACK_BTC_QTY = 0.15931
    FALLBACK_SOL_QTY = 55.28
    FALLBACK_STABLES_USD = 1415.00
    BDS_TOTAL_COST_VND = 3_100_000_000.0
    BDS_PARENTS_CASH_VND = 1_300_000_000.0
    BDS_PERSONAL_CASH_VND = 705_000_000.0
    BDS_DEBT_CEILING_VND = 615_000_000.0


@dataclass
class StandaloneRates:
    btc_price: float
    sol_price: float
    p2p_rate: float
    source: str


def fetch_standalone_rates(
    offline: bool = False,
    cache_file: str = str(CACHE_RATES_FILE),
    btc_override: float = None,
    sol_override: float = None,
    p2p_override: float = None
) -> StandaloneRates:
    """Fetch market rates standalone with resilient SSL fallback and local cache."""
    if btc_override and sol_override and p2p_override:
        return StandaloneRates(btc_override, sol_override, p2p_override, "override")

    if not offline:
        try:
            # First try verified SSL, then fallback to unverified
            for ctx in [ssl.create_default_context(), ssl._create_unverified_context()]:
                try:
                    spot_url = "https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22SOLUSDT%22%5D"
                    req = urllib.request.Request(spot_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                        spot_data = json.loads(resp.read().decode())
                    btc_p = float([x["price"] for x in spot_data if x["symbol"] == "BTCUSDT"][0])
                    sol_p = float([x["price"] for x in spot_data if x["symbol"] == "SOLUSDT"][0])

                    p2p_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
                    p2p_payload = json.dumps({
                        "page": 1, "rows": 5, "payTypes": [], "asset": "USDT",
                        "tradeType": "SELL", "fiat": "VND", "transAmount": "50000000"
                    }).encode("utf-8")
                    p2p_req = urllib.request.Request(
                        p2p_url,
                        data=p2p_payload,
                        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                        method="POST"
                    )
                    with urllib.request.urlopen(p2p_req, timeout=5, context=ctx) as p2p_resp:
                        p2p_data = json.loads(p2p_resp.read().decode())
                    p2p_p = float(p2p_data["data"][0]["adv"]["price"])

                    # Save to cache
                    try:
                        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                        with open(cache_file, "w", encoding="utf-8") as f:
                            json.dump({
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "btc_price": btc_p, "sol_price": sol_p, "p2p_rate": p2p_p,
                                "rates": {"BTCUSDT": btc_p, "SOLUSDT": sol_p, "USDT_VND_P2P": p2p_p}
                            }, f, indent=2)
                    except Exception:
                        pass

                    return StandaloneRates(btc_p, sol_p, p2p_p, "realtime")
                except (ssl.SSLCertVerificationError, urllib.error.URLError, Exception):
                    continue
        except Exception:
            pass

    # Read from cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                c = json.load(f)
            btc_p = c.get("btc_price", c.get("rates", {}).get("BTCUSDT", 84262.0))
            sol_p = c.get("sol_price", c.get("rates", {}).get("SOLUSDT", 115.72))
            p2p_p = c.get("p2p_rate", c.get("rates", {}).get("USDT_VND_P2P", 25930.0))
            return StandaloneRates(float(btc_p), float(sol_p), float(p2p_p), "cache")
        except Exception:
            pass

    return StandaloneRates(84262.0, 115.72, 25930.0, "fallback")


def main():
    parser = argparse.ArgumentParser(description="Antigravity Custom Skill: crypto-manager runner")
    parser.add_argument("--plan", default=str(CRYPTO_PLAN_PATH), help="Path to crypto-plan.md")
    parser.add_argument("--logs-dir", default=str(CRYPTO_LOGS_DIR), help="Path to logs directory")
    parser.add_argument("--cache-file", default=str(CACHE_RATES_FILE), help="Path to rate cache file")
    parser.add_argument("--offline", action="store_true", help="Do not call network, use cache/fallbacks")
    parser.add_argument("--btc-price", type=float, help="Manual override BTC price (USD)")
    parser.add_argument("--sol-price", type=float, help="Manual override SOL price (USD)")
    parser.add_argument("--p2p-rate", type=float, help="Manual override P2P USDT/VND rate")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--append", action="store_true", help="Safely append review to monthly log file")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute writes, simulate output")

    args = parser.parse_args()

    # 1. Parse state
    if ENGINE_LOADED:
        plan_dict = parse_crypto_plan(args.plan)
        logs_dict = parse_logs(args.logs_dir)
        btc_qty = plan_dict.get("btc_qty", FALLBACK_BTC_QTY)
        sol_qty = plan_dict.get("sol_qty", FALLBACK_SOL_QTY)
        stables_usd = plan_dict.get("stables_usd", FALLBACK_STABLES_USD)
        withdrawn_vnd = logs_dict.get("withdrawn_vnd", 0.0)
        missed_count = logs_dict.get("missed_recommendations_count", 13)
    else:
        btc_qty = FALLBACK_BTC_QTY
        sol_qty = FALLBACK_SOL_QTY
        stables_usd = FALLBACK_STABLES_USD
        withdrawn_vnd = 0.0
        missed_count = 13

    # 2. Get rates
    rates = fetch_standalone_rates(
        offline=args.offline,
        cache_file=args.cache_file,
        btc_override=args.btc_price,
        sol_override=args.sol_price,
        p2p_override=args.p2p_rate
    )

    # 3. Valuation & Matrix Evaluation
    if ENGINE_LOADED:
        snapshot = calculate_tts(
            btc_qty=btc_qty,
            sol_qty=sol_qty,
            stables_usd=stables_usd,
            btc_price=rates.btc_price,
            sol_price=rates.sol_price,
            p2p_rate=rates.p2p_rate,
            withdrawn_vnd=withdrawn_vnd,
            data_source=rates.source,
            cache_path=args.cache_file,
            force_offline=args.offline
        )
        mat = evaluate_binary_matrix(
            snapshot=snapshot,
            missed_count=missed_count
        )
        md_output = generate_markdown_review(snapshot, mat)
        structured = generate_structured_proposal(snapshot, mat)
    else:
        crypto_usd = (btc_qty * rates.btc_price) + (sol_qty * rates.sol_price) + stables_usd
        crypto_vnd = crypto_usd * rates.p2p_rate
        tts_vnd = withdrawn_vnd + crypto_vnd
        dist_vnd = tts_vnd - HARD_FLOOR_VND
        dist_pct = (dist_vnd / HARD_FLOOR_VND) * 100.0
        active_band = "TAKE_PROFIT_540M" if tts_vnd >= HARD_FLOOR_VND else "HARD_FLOOR_BREACH"
        md_output = f"## Automated Review — TTS: {tts_vnd/1e6:.1f}tr | Band: {active_band}\nHard Floor: 540tr."
        structured = {
            "tts_vnd": tts_vnd,
            "crypto_vnd": crypto_vnd,
            "withdrawn_vnd": withdrawn_vnd,
            "active_band": active_band,
            "hard_floor_vnd": HARD_FLOOR_VND,
            "distance_to_floor_vnd": dist_vnd,
            "distance_to_floor_pct": dist_pct,
            "urgent_action_required": True,
            "missed_recommendations_count": missed_count,
            "orders_sheet": []
        }

    # 4. Optional Append
    appended_file = None
    if args.append and not args.dry_run:
        if ENGINE_LOADED:
            res = append_review_log(logs_dir=args.logs_dir, review_content=md_output)
            appended_file = res.get("target_file")
        else:
            now = datetime.now()
            month_file = os.path.join(args.logs_dir, f"{now.strftime('%Y-%m')}.md")
            os.makedirs(args.logs_dir, exist_ok=True)
            with open(month_file, "a", encoding="utf-8") as f:
                f.write("\n\n" + md_output.strip() + "\n")
            appended_file = month_file

    # 5. Output
    if args.json:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "SUCCESS",
            "rates": {
                "btc_price": rates.btc_price,
                "sol_price": rates.sol_price,
                "p2p_rate": rates.p2p_rate,
                "source": rates.source
            },
            "portfolio": {
                "btc_qty": btc_qty,
                "sol_qty": sol_qty,
                "stables_usd": stables_usd,
                "withdrawn_vnd": withdrawn_vnd,
                "unexecuted_orders_count": missed_count
            },
            "valuation": {
                "crypto_vnd": structured.get("crypto_vnd", 0.0),
                "withdrawn_vnd": structured.get("withdrawn_vnd", 0.0),
                "tts_vnd": structured.get("tts_vnd", 0.0)
            },
            "matrix": structured.get("orders_sheet", []),
            "evaluation": {
                "active_band": structured.get("active_band", ""),
                "hard_floor_vnd": structured.get("hard_floor_vnd", HARD_FLOOR_VND),
                "distance_to_floor_vnd": structured.get("distance_to_floor_vnd", 0.0),
                "distance_to_floor_pct": structured.get("distance_to_floor_pct", 0.0),
                "urgent_action_required": structured.get("urgent_action_required", False),
                "summary": f"Active Band: {structured.get('active_band', '')}"
            },
            "bds": structured.get("bds_analysis", {
                "loan_gap_vnd": BDS_TOTAL_COST_VND - (BDS_PARENTS_CASH_VND + BDS_PERSONAL_CASH_VND + structured.get("tts_vnd", 0.0)),
                "red_flag": True
            }),
            "log_appended_to": appended_file
        }
        print(json.dumps(payload, indent=2))
    else:
        print(md_output)
        if appended_file:
            print(f"\n[OK] Successfully appended Section 7.5 review to {appended_file}")

    # Exit codes
    band = structured.get("active_band", "")
    if band == "HARD_FLOOR_BREACH":
        sys.exit(2)
    elif band == "TAKE_PROFIT_540M":
        sys.exit(3)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
