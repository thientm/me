"""
Module: crypto_engine.quant.hesitation_tax
Behavioral Hesitation Tax Ticker (BHT-Ticker) and 10-Minute Commitment Device.
Quant Innovation 2 for Crypto Dashboard.
Zero external dependencies (Python 3 Standard Library only).
"""

from __future__ import annotations
from typing import Dict, Any, Optional

DEFAULT_LAND_FEE_VND: float = 3_100_000_000.0
STATUTORY_DAILY_TAX_RATE: float = 0.0003  # 0.03% / day
LAND_2027_HAZARD_MAX_VND: float = 370_000_000.0  # 370M VND land fee increase risk in 2027
DAILY_HAZARD_ACCRUAL_VND: float = 5_550_000.0   # 5.55M VND / day escalation rate
LATE_OCT_2026_DEADLINE_HOURS: float = 888.0      # 37 days * 24h = 888h from 2026-09-24 to 2026-10-31
COMMITMENT_DEVICE_SECONDS: int = 600            # 10 minutes


def calculate_hesitation_tax(
    land_fee_vnd: float = DEFAULT_LAND_FEE_VND,
    hours_delayed: float = 0.0,
    unexecuted_count: int = 0,
    market_slippage_loss_vnd: float = 0.0,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Computes statutory and behavioral hesitation tax penalties.
    
    Formula:
    - Daily tax penalty = land_fee_vnd * 0.0003 (930,000 VND/day on 3.1B VND)
    - Hourly burn rate = Daily tax penalty / 24 = 38,750 VND/hour
    - Tax late penalty = hours_delayed * Hourly burn rate
    - Land 2027 hazard exposure = up to 370,000,000 VND if delay threatens deadline
    - Status level = DEFCON_1_PARALYSIS if unexecuted_count >= 13, else WARNING or NORMAL
    - Total hesitation tax = tax_late_penalty_vnd + land_2027_hazard_exposure_vnd + market_slippage_loss_vnd
    """
    safe_hours = max(0.0, float(hours_delayed))
    safe_fee = max(0.0, float(land_fee_vnd))
    safe_unexecuted = max(0, int(unexecuted_count))
    safe_slippage = max(0.0, float(market_slippage_loss_vnd))

    # Constant hourly burn rate
    daily_tax_penalty = safe_fee * STATUTORY_DAILY_TAX_RATE
    burn_rate_vnd_per_hour = daily_tax_penalty / 24.0
    burn_rate_vnd_per_second = burn_rate_vnd_per_hour / 3600.0

    # Accumulated late tax penalty
    tax_late_penalty_vnd = safe_hours * burn_rate_vnd_per_hour

    # 2027 land price escalation hazard exposure
    if safe_hours <= 0.0:
        land_2027_hazard_exposure_vnd = 0.0
    elif safe_hours >= LATE_OCT_2026_DEADLINE_HOURS or safe_hours >= 1000.0:
        land_2027_hazard_exposure_vnd = LAND_2027_HAZARD_MAX_VND
    else:
        # Accrues progressively based on days delayed
        days_delayed = safe_hours / 24.0
        accrued = days_delayed * DAILY_HAZARD_ACCRUAL_VND
        land_2027_hazard_exposure_vnd = min(LAND_2027_HAZARD_MAX_VND, accrued)

    # Total hesitation tax
    total_hesitation_tax_vnd = (
        tax_late_penalty_vnd
        + land_2027_hazard_exposure_vnd
        + safe_slippage
    )

    # Status level determination
    if safe_unexecuted >= 13:
        status_level = "DEFCON_1_PARALYSIS"
    elif safe_unexecuted >= 3 or safe_hours >= 24.0:
        status_level = "WARNING"
    else:
        status_level = "NORMAL"

    return {
        "land_fee_vnd": safe_fee,
        "hours_delayed": safe_hours,
        "unexecuted_count": safe_unexecuted,
        "strike_count": safe_unexecuted,
        "burn_rate_vnd_per_hour": round(burn_rate_vnd_per_hour, 2),
        "burn_rate_vnd_per_second": round(burn_rate_vnd_per_second, 4),
        "tax_late_penalty_vnd": round(tax_late_penalty_vnd, 2),
        "land_2027_hazard_exposure_vnd": round(land_2027_hazard_exposure_vnd, 2),
        "market_slippage_loss_vnd": round(safe_slippage, 2),
        "total_hesitation_tax_vnd": round(total_hesitation_tax_vnd, 2),
        "status_level": status_level,
    }


def get_commitment_device_status(
    elapsed_seconds: int = 0,
    total_duration_seconds: int = COMMITMENT_DEVICE_SECONDS
) -> Dict[str, Any]:
    """
    Evaluates 10-minute commitment device countdown status.
    
    Returns:
    - total_duration_seconds: 600
    - remaining_seconds: max(0, 600 - elapsed_seconds)
    - is_expired: elapsed_seconds > 600
    - progress_pct: 0.0 to 1.0
    - status: "ACTIVE" | "EXPIRED"
    """
    safe_elapsed = max(0, int(elapsed_seconds))
    safe_total = max(1, int(total_duration_seconds))
    remaining = max(0, safe_total - safe_elapsed)
    is_expired = safe_elapsed > safe_total
    progress_pct = min(1.0, safe_elapsed / float(safe_total))

    return {
        "total_duration_seconds": safe_total,
        "elapsed_seconds": safe_elapsed,
        "remaining_seconds": remaining,
        "is_expired": is_expired,
        "progress_pct": round(progress_pct, 4),
        "status": "EXPIRED" if is_expired else "ACTIVE",
    }
