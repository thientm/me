"""
Configuration and constants for the Crypto Portfolio Management Engine.
Enforces domain constraints updated on 2026-09-24:
- Hard Floor: 540,000,000 VND (540tr)
- Binary Decision Matrix (>=540tr: Take profit 50%; <540tr: Emergency Market Sell ALL)
- Cash-out Deadline: Late October 2026 (2026-10-31)
"""

from pathlib import Path

# Paths to personal personal-os repository
_CANDIDATE_REPOS = [
    Path("/Users/thientm/Documents/GitHub/me"),
    Path(__file__).resolve().parents[4],
    Path("/Users/thien.tm/Documents/me"),
]
PERSONAL_REPO_DIR = next((p for p in _CANDIDATE_REPOS if (p / "crypto" / "crypto-plan.md").exists()), Path("/Users/thien.tm/Documents/me"))
CRYPTO_PLAN_PATH = PERSONAL_REPO_DIR / "crypto" / "crypto-plan.md"
CRYPTO_LOGS_DIR = PERSONAL_REPO_DIR / "crypto" / "logs"
REAL_ESTATE_PLAN_PATH = PERSONAL_REPO_DIR / "real-estate" / "real-estate-plan.md"

# Project paths
_CANDIDATE_PROJECT_ROOTS = [
    Path(__file__).resolve().parents[2],
    Path("/Users/thien.tm/teamwork_projects/crypto_dashboard"),
]
PROJECT_ROOT = next((p for p in _CANDIDATE_PROJECT_ROOTS if p.exists()), Path("/Users/thien.tm/teamwork_projects/crypto_dashboard"))
DATA_DIR = PROJECT_ROOT / "data"
CACHE_RATES_FILE = DATA_DIR / "cache_rates.json"

# Financial thresholds & parameters (2026-09-24 Critical Update)
HARD_FLOOR_VND: float = 540_000_000.0
INITIAL_CAPITAL_VND: float = 650_000_000.0
CASH_OUT_DEADLINE_STR: str = "2026-10-31"  # Late October 2026
OVERRIDE_DAYS_THRESHOLD: int = 14          # <14 days to deadline triggers emergency liquidation

# Authoritative measured holdings fallback
FALLBACK_BTC_QTY: float = 0.15931
FALLBACK_SOL_QTY: float = 55.28
FALLBACK_STABLES_USD: float = 1415.0
FALLBACK_WITHDRAWN_VND: float = 0.0

# Baseline market rates fallback
FALLBACK_BTC_PRICE: float = 84262.0
FALLBACK_SOL_PRICE: float = 115.72
FALLBACK_P2P_RATE: float = 25930.0

# Real Estate (BĐS Phù Đổng 80m2) parameters
BDS_TOTAL_COST_VND: float = 3_100_000_000.0
BDS_PARENTS_CASH_VND: float = 1_300_000_000.0
BDS_PERSONAL_CASH_VND: float = 705_000_000.0
BDS_DEBT_CEILING_VND: float = 615_000_000.0
BDS_PLANNED_LOAN_VND: float = BDS_DEBT_CEILING_VND
BDS_DELAY_PENALTY_HOURLY: float = 38_750.0  # 930k VND/day
BDS_DEBT_DECISION_DATE: str = "2026-09-30"

# Binance API Endpoints
BINANCE_SPOT_URL = "https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22SOLUSDT%22%5D"
BINANCE_P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
