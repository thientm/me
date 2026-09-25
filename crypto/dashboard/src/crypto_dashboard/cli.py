"""
Module: crypto_dashboard.cli
CLI Interface for Crypto Portfolio Cockpit.
Authoritative source: PROJECT.md §F7; explorer_dashboard_1/report.md §2.
Zero external dependencies (Python 3 Standard Library only).
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from crypto_engine.config import (
    HARD_FLOOR_VND,
    INITIAL_CAPITAL_VND,
    CASH_OUT_DEADLINE_STR,
    CRYPTO_PLAN_PATH,
    CRYPTO_LOGS_DIR,
    FALLBACK_BTC_PRICE,
    FALLBACK_SOL_PRICE,
    FALLBACK_P2P_RATE,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
)
from crypto_engine.parser import parse_crypto_plan, parse_logs
from crypto_engine.valuation import calculate_tts, get_rates
from crypto_engine.matrix import evaluate_binary_matrix
from crypto_engine.logger import format_section_7_5_review, append_review_log
from crypto_engine.proposal import generate_markdown_review
from crypto_dashboard.api_handlers import run_simulation, get_macro_data
from crypto_dashboard.agy_bridge import generate_agy_command, execute_agy_cli
from crypto_dashboard.server import start_server


def create_parser() -> argparse.ArgumentParser:
    """
    Constructs the CLI argument parser with subcommands: status, review, simulate, serve.
    """
    parser = argparse.ArgumentParser(
        prog="crypto-dashboard",
        description="Crypto Portfolio Management Cockpit & Discipline Enforcement CLI",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Subcommand to execute",
    )

    # 1. status
    p_status = subparsers.add_parser(
        "status",
        help="View instant realtime/offline valuation snapshot and alerts",
    )
    p_status.add_argument(
        "--offline", "-o",
        action="store_true",
        help="Use cached rates without calling Binance API",
    )
    p_status.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON instead of ASCII terminal box",
    )
    p_status.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed wallet breakdowns, P2P spreads, and quant meters",
    )

    # 2. review
    p_review = subparsers.add_parser(
        "review",
        help="Evaluate Section 7.5 review, generate 10-minute order sheet and log",
    )
    p_review.add_argument(
        "--save-log",
        action="store_true",
        help="Append Section 7.5 review to Personal OS log file",
    )
    p_review.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute calculations and review without writing to disk",
    )
    p_review.add_argument(
        "--agy",
        action="store_true",
        help="Forward action to local agy CLI for autonomous agent review",
    )
    p_review.add_argument(
        "--format",
        choices=["terminal", "markdown", "json"],
        default="terminal",
        help="Output formatting style (default: terminal)",
    )

    # 3. simulate
    p_sim = subparsers.add_parser(
        "simulate",
        help="Run What-If price shock simulation vs 540tr hard floor",
    )
    p_sim.add_argument(
        "--btc-shock",
        type=float,
        default=None,
        help="BTC price shock percentage (e.g. -15.0)",
    )
    p_sim.add_argument(
        "--sol-shock",
        type=float,
        default=None,
        help="SOL price shock percentage (e.g. -15.0)",
    )
    p_sim.add_argument(
        "--scenario",
        type=str,
        default=None,
        help="Preset scenario name (e.g. hold100, 50sell)",
    )
    p_sim.add_argument(
        "--btc-price",
        type=float,
        default=None,
        help="Hypothetical custom BTC price in USD",
    )
    p_sim.add_argument(
        "--sol-price",
        type=float,
        default=None,
        help="Hypothetical custom SOL price in USD",
    )
    p_sim.add_argument(
        "--p2p-rate",
        type=float,
        default=None,
        help="Hypothetical custom USDT/VND P2P rate",
    )
    p_sim.add_argument(
        "--json",
        action="store_true",
        help="Output simulation result in structured JSON format",
    )

    # 4. serve
    p_serve = subparsers.add_parser(
        "serve",
        help="Launch the local HTTP REST daemon and Web UI cockpit",
    )
    p_serve.add_argument(
        "--port",
        type=int,
        default=8088,
        help="Port number to bind HTTP server (default: 8088)",
    )
    p_serve.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind HTTP server (default: 127.0.0.1)",
    )
    p_serve.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open web browser automatically upon server startup",
    )

    return parser


def format_currency_vnd(amount: float) -> str:
    """Format float into Vietnamese VND currency string (e.g. 550.643.256 VND)."""
    return f"{int(round(amount)):,}".replace(",", ".") + " VND"


def format_currency_usd(amount: float) -> str:
    """Format float into USD currency string (e.g. $21,235)."""
    return f"${amount:,.2f}"


def handle_status(args: argparse.Namespace) -> int:
    """Handler for 'status' subcommand."""
    holdings = parse_crypto_plan()
    rates = get_rates(offline_only=args.offline)

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

    if args.json:
        out = {
            "status": "ok",
            "timestamp": snapshot.timestamp,
            "data_source": snapshot.data_source,
            "valuation": {
                "tts_vnd": snapshot.tts_vnd,
                "crypto_vnd": snapshot.crypto_vnd,
                "withdrawn_vnd": snapshot.withdrawn_vnd,
                "hard_floor_vnd": matrix.hard_floor_vnd,
                "distance_to_floor_vnd": matrix.distance_to_floor_vnd,
                "distance_to_floor_pct": matrix.distance_to_floor_pct,
            },
            "market_rates": {
                "btc_usdt": snapshot.btc_price,
                "sol_usdt": snapshot.sol_price,
                "usdt_vnd_p2p": snapshot.p2p_rate,
            },
            "matrix": {
                "active_band": matrix.active_band,
                "urgent_action_required": matrix.urgent_action_required,
                "missed_recommendations_count": matrix.missed_recommendations_count,
            },
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    # ASCII Box Format
    macro = get_macro_data(tts_vnd=snapshot.tts_vnd)
    gap = macro["bds_financial_gap"]
    btc_vnd = snapshot.btc_qty * snapshot.btc_price * snapshot.p2p_rate
    sol_vnd = snapshot.sol_qty * snapshot.sol_price * snapshot.p2p_rate
    stables_vnd = snapshot.stables_usd * snapshot.p2p_rate
    total_val = btc_vnd + sol_vnd + stables_vnd

    w_btc = (btc_vnd / total_val * 100.0) if total_val > 0 else 0.0
    w_sol = (sol_val_vnd / total_val * 100.0) if (sol_val_vnd := sol_vnd) and total_val > 0 else 0.0
    w_usd = (stables_vnd / total_val * 100.0) if total_val > 0 else 0.0

    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║              CRYPTO LIQUIDITY COCKPIT — REALTIME STATUS                  ║")
    print(f"║                     {snapshot.timestamp[:19]} (UTC)                        ║")
    print("╠═══════════════════════════════════════════════════════════════════════════╣")
    print("║ 🚨 BÁO ĐỘNG ĐỎ: 0/13 KHUYẾN NGHỊ BÁN ĐÃ ĐƯỢC THỰC THI (TRỄ 50 NGÀY)      ║")
    print(f"║    Band: {matrix.active_band:<18} (TTS: {snapshot.tts_vnd/1e6:.1f}tr VND)                   ║")
    print("║    Hành động: BÁN 50% COIN (XẢ SẠCH SOL) + RÚT HẾT STABLES NGAY           ║")
    print("╠═══════════════════════════════════════════════════════════════════════════╣")
    print(f"║  TỔNG TÀI SẢN (TTS)    : {format_currency_vnd(snapshot.tts_vnd):<25} ({format_currency_usd(snapshot.tts_vnd / snapshot.p2p_rate)})     ║")
    print(f"║  Vốn gốc ban đầu       : {format_currency_vnd(INITIAL_CAPITAL_VND):<25} (−15,3% Tạm lỗ)        ║")
    print(f"║  Tiền mặt đã rút       : {format_currency_vnd(snapshot.withdrawn_vnd):<25} (0,0%)                 ║")
    print(f"║  Khoảng cách sàn 540tr : {format_currency_vnd(matrix.distance_to_floor_vnd):<25} ({matrix.distance_to_floor_pct:+.2f}%)               ║")
    print("╠───────────────────────────────────────────────────────────────────────────╣")
    print("║  PHÂN BỔ DANH MỤC:                                                       ║")
    print(f"║  • BTC : {snapshot.btc_qty:.6f} BTC  x ${snapshot.btc_price:,.0f} x {snapshot.p2p_rate:,.0f} = {format_currency_vnd(btc_vnd):<15} ({w_btc:.1f}%) ║")
    print(f"║  • SOL : {snapshot.sol_qty:.2f} SOL    x ${snapshot.sol_price:,.1f} x {snapshot.p2p_rate:,.0f} = {format_currency_vnd(sol_vnd):<15} ({w_sol:.1f}%) [XẢ]║")
    print(f"║  • USDT: {snapshot.stables_usd:,.2f}  USD  x {snapshot.p2p_rate:,.0f}        = {format_currency_vnd(stables_vnd):<15} ({w_usd:.1f}%) [RÚT]║")
    print("╠───────────────────────────────────────────────────────────────────────────╣")
    print("║  ĐỐI CHIẾU NGHĨA VỤ BĐS (ĐẤT PHÙ ĐỔNG 3,1 TỶ):                           ║")
    print(f"║  • Vốn tự có (Bố mẹ + Cá nhân + Crypto): {gap['total_self_equity_vnd']/1e6:,.1f} triệu VND                ║")
    print(f"║  • Số tiền cần vay: {gap['borrow_needed_vnd']/1e6:,.1f} triệu VND (Trần nợ: 615tr)                     ║")
    print(f"║  • Đệm an toàn vốn vay: {gap['cushion_vnd']/1e6:+,.1f} triệu VND                                   ║")
    print(f"║  • Hạn chót chốt nguồn vay: 30/09/2026 | Hạn rút tiền: Late Oct 2026      ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    return 0


def handle_review(args: argparse.Namespace) -> int:
    """Handler for 'review' subcommand."""
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
    macro = get_macro_data(tts_vnd=snapshot.tts_vnd)

    review_text = format_section_7_5_review(
        tts_vnd=snapshot.tts_vnd,
        withdrawn_vnd=snapshot.withdrawn_vnd,
        active_band=matrix.active_band,
        action_summary="Kích hoạt Take-Profit 50%: Bán sạch 55.28 SOL và rút 1.415 USDT.",
        borrow_needed_vnd=macro["bds_financial_gap"]["borrow_needed_vnd"],
        date_str=snapshot.timestamp[:10],
    )

    if args.save_log and not args.dry_run:
        month_str = snapshot.timestamp[:7]
        log_file = os.path.join(CRYPTO_LOGS_DIR, f"{month_str}.md")
        append_review_log(log_file, review_text)
        print(f"✅ Đã ghi append-only vào log: {log_file}")

    if args.agy:
        print("🤖 Chuyển tiếp tới agy CLI cục bộ...")
        res = execute_agy_cli(action="review", dry_run=args.dry_run)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    if args.format == "json":
        print(json.dumps({
            "status": "ok",
            "review": review_text,
            "orders_sheet": matrix.orders_sheet,
            "matrix": {
                "active_band": matrix.active_band,
                "distance_to_floor_vnd": matrix.distance_to_floor_vnd,
            },
        }, indent=2, ensure_ascii=False))
        return 0

    print("┌──────────────────────────────────────────────────────────────────────────┐")
    print("│              10-MINUTE EXECUTABLE ORDER SHEET (HÔM NAY 24/09)            │")
    print("├──────────────────────────────────────────────────────────────────────────┤")
    for o in matrix.orders_sheet:
        print(f"│ Step {o.get('step', '-')}: [{o.get('action', '')} {o.get('symbol', '')}]")
        print(f"│   • Khối lượng : {o.get('qty', 0):,} {o.get('symbol', '')}")
        print(f"│   • Giá mục tiêu : {o.get('price', 0):,}")
        print(f"│   • Thu về dự kiến : {format_currency_vnd(o.get('estimated_vnd', 0))}")
        print(f"│   • Thời hạn   : {o.get('deadline', 'Ngay')}")
        print("├──────────────────────────────────────────────────────────────────────────┤")
    print("└──────────────────────────────────────────────────────────────────────────┘\n")
    print(review_text)
    return 0


def handle_simulate(args: argparse.Namespace) -> int:
    """Handler for 'simulate' subcommand."""
    rates = get_rates(offline_only=True)
    base_btc = rates.get("BTCUSDT", FALLBACK_BTC_PRICE)
    base_sol = rates.get("SOLUSDT", FALLBACK_SOL_PRICE)
    p2p_rate = args.p2p_rate if args.p2p_rate is not None else rates.get("USDT_VND_P2P", FALLBACK_P2P_RATE)

    if args.btc_price is not None:
        btc_price = args.btc_price
    elif args.btc_shock is not None:
        btc_price = max(0.0, base_btc * (1.0 + args.btc_shock / 100.0))
    else:
        btc_price = base_btc

    if args.sol_price is not None:
        sol_price = args.sol_price
    elif args.sol_shock is not None:
        sol_price = max(0.0, base_sol * (1.0 + args.sol_shock / 100.0))
    else:
        sol_price = base_sol

    holdings = parse_crypto_plan()
    sim_res = run_simulation(
        btc_price=btc_price,
        sol_price=sol_price,
        p2p_rate=p2p_rate,
        btc_qty=holdings.get("btc_qty", FALLBACK_BTC_QTY),
        sol_qty=holdings.get("sol_qty", FALLBACK_SOL_QTY),
        stables_usd=holdings.get("stables_usd", FALLBACK_STABLES_USD),
        hard_floor_vnd=HARD_FLOOR_VND,
    )

    if args.json:
        print(json.dumps(sim_res, indent=2, ensure_ascii=False))
        return 0

    sc_a = sim_res["scenario_a_sell_50"]
    sc_b = sim_res["scenario_b_hold_100"]

    print("┌──────────────────────────────────────────────────────────────────────────┐")
    print("│              WHAT-IF MARKET SHOCK SIMULATION COMPARISON                  │")
    print("├──────────────────────────────────────────────────────────────────────────┤")
    print(f"│ Giả định giá: BTC ${btc_price:,.0f} | SOL ${sol_price:,.1f} | P2P {p2p_rate:,.0f} VND/USD")
    print("├────────────────────────────────┬────────────────────┬────────────────────┤")
    print("│ Chỉ số đánh giá                │ Kịch bản A: Bán 50%│ Kịch bản B: Giữ 100│")
    print("├────────────────────────────────┼────────────────────┼────────────────────┤")
    print(f"│ Tiền mặt an toàn (Bank)        │ {sc_a['cash_locked_vnd']/1e6:>15.1f}tr │ {sc_b['cash_locked_vnd']/1e6:>15.1f}tr │")
    print(f"│ TTS sau sốc                    │ {sc_a['simulated_tts_vnd']/1e6:>15.1f}tr │ {sc_b['simulated_tts_vnd']/1e6:>15.1f}tr │")
    print(f"│ Khoảng cách sàn 540tr          │ {sc_a['distance_to_floor_vnd']/1e6:>+15.1f}tr │ {sc_b['distance_to_floor_vnd']/1e6:>+15.1f}tr │")
    print(f"│ Trạng thái sàn 540tr           │ {'🚨 THỦNG SÀN' if sc_a['is_floor_breached'] else '🟢 AN TOÀN':>18} │ {'🚨 THỦNG SÀN' if sc_b['is_floor_breached'] else '🟢 AN TOÀN':>18} │")
    print(f"│ Xác suất thủng sàn 20 phiên    │ {sc_a['ruin_probability_20d_pct']:>17.1f}% │ {sc_b['ruin_probability_20d_pct']:>17.1f}% │")
    print(f"│ Số cần vay thêm làm sổ đỏ      │ {sc_a['bds_borrow_gap_vnd']/1e6:>15.1f}tr │ {sc_b['bds_borrow_gap_vnd']/1e6:>15.1f}tr │")
    print("└────────────────────────────────┴────────────────────┴────────────────────┘")
    return 0


def handle_serve(args: argparse.Namespace) -> int:
    """Handler for 'serve' subcommand."""
    start_server(
        port=args.port,
        host=args.host,
        open_browser=not args.no_browser,
    )
    return 0


def handle_cli(args: Optional[List[str]] = None) -> int:
    """
    Main CLI entrypoint. Parses arguments and executes the requested subcommand.
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args if args is not None else sys.argv[1:])

    if parsed_args.command == "status":
        return handle_status(parsed_args)
    elif parsed_args.command == "review":
        return handle_review(parsed_args)
    elif parsed_args.command == "simulate":
        return handle_simulate(parsed_args)
    elif parsed_args.command == "serve":
        return handle_serve(parsed_args)

    return 0
