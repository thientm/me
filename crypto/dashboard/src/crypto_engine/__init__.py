"""
Package: crypto_engine
Core Portfolio Management Engine for Crypto Dashboard.
Zero external dependencies (Python 3 Standard Library only).
"""

from .config import (
    HARD_FLOOR_VND,
    INITIAL_CAPITAL_VND,
    CASH_OUT_DEADLINE_STR,
    CRYPTO_PLAN_PATH,
    CRYPTO_LOGS_DIR,
    CACHE_RATES_FILE,
)

from .parser import (
    PortfolioHoldings,
    parse_portfolio_plan,
    parse_crypto_plan,
    parse_logs,
    parse_logs_history,
)

from .valuation import (
    ValuationSnapshot,
    calculate_tts,
    calculate_valuation,
    get_rates,
    fetch_binance_spot,
    fetch_binance_p2p,
    load_cached_rates,
    save_cached_rates,
)

from .matrix import (
    MatrixEvaluation,
    evaluate_binary_matrix,
    evaluate_matrix,
    check_overrides,
    calculate_take_profit_orders,
    calculate_emergency_sell_all_orders,
)

from .proposal import (
    generate_markdown_review,
    generate_structured_proposal,
)

from .logger import (
    format_section_7_5_review,
    append_review_log,
    append_correction,
)

__all__ = [
    "HARD_FLOOR_VND",
    "INITIAL_CAPITAL_VND",
    "CASH_OUT_DEADLINE_STR",
    "CRYPTO_PLAN_PATH",
    "CRYPTO_LOGS_DIR",
    "CACHE_RATES_FILE",
    "PortfolioHoldings",
    "parse_portfolio_plan",
    "parse_crypto_plan",
    "parse_logs",
    "parse_logs_history",
    "ValuationSnapshot",
    "calculate_tts",
    "calculate_valuation",
    "get_rates",
    "fetch_binance_spot",
    "fetch_binance_p2p",
    "load_cached_rates",
    "save_cached_rates",
    "MatrixEvaluation",
    "evaluate_binary_matrix",
    "evaluate_matrix",
    "check_overrides",
    "calculate_take_profit_orders",
    "calculate_emergency_sell_all_orders",
    "generate_markdown_review",
    "generate_structured_proposal",
    "format_section_7_5_review",
    "append_review_log",
    "append_correction",
]
