"""
Module: crypto_engine.quant.volatility_cushion
Dynamic ATR-Normalized Volatility Cushion & CPPI De-risking Meter (AVC-Meter).
Quant Innovation 3 for Crypto Dashboard.
Zero external dependencies (Python 3 Standard Library only).
"""

from __future__ import annotations
import math
from typing import Dict, Any, Optional, Union

DEFAULT_HARD_FLOOR_VND: float = 540_000_000.0
DEFAULT_PORTFOLIO_ATR_PCT: float = 0.0310  # 3.10% daily portfolio ATR
DEFAULT_CPPI_MULTIPLIER: float = 3.0       # k = 3.0 (3-sigma cushion buffer)


def calculate_volatility_cushion(
    tts_vnd: Union[float, Dict[str, Any]],
    crypto_vnd: Optional[float] = None,
    portfolio_daily_atr_pct: float = DEFAULT_PORTFOLIO_ATR_PCT,
    hard_floor_vnd: float = DEFAULT_HARD_FLOOR_VND,
    k_factor: float = DEFAULT_CPPI_MULTIPLIER,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Computes Volatility Cushion Ratio (VCR) and CPPI Safe Exposure Capacity.
    
    Formula:
    - Cushion (VND) = TTS - Hard_Floor
    - Daily ATR Noise (VND) = Crypto_VND * Portfolio_Daily_ATR_Pct
    - VCR (Days) = Cushion / Daily_ATR_Noise
    - Risk Zone Classification:
        * VCR < 3.0 or Cushion <= 0 -> RED_DANGER
        * 3.0 <= VCR < 6.0          -> YELLOW_CAUTION
        * VCR >= 6.0                -> GREEN_SAFE
    - CPPI Max Safe Crypto (VND) = Cushion / (k * Portfolio_Daily_ATR_Pct)
    - Excess Risk (VND) = max(0, Crypto_VND - CPPI_Max_Safe_Crypto)
    """
    # Support dict input if passed
    if isinstance(tts_vnd, dict):
        d = tts_vnd
        safe_tts = float(d.get("tts_vnd", d.get("tts", 0.0)))
        safe_crypto = float(d.get("crypto_vnd", d.get("crypto", safe_tts)))
        safe_atr_pct = float(d.get("portfolio_daily_atr_pct", portfolio_daily_atr_pct))
        safe_floor = float(d.get("hard_floor_vnd", hard_floor_vnd))
    else:
        safe_tts = float(tts_vnd)
        safe_crypto = safe_tts if crypto_vnd is None else float(crypto_vnd)
        safe_atr_pct = float(portfolio_daily_atr_pct)
        safe_floor = float(hard_floor_vnd)

    safe_k = max(0.1, float(k_factor))
    cushion_vnd = safe_tts - safe_floor
    daily_noise_vnd = safe_crypto * safe_atr_pct

    # Volatility Cushion Ratio (VCR) in days of normal market noise
    if daily_noise_vnd == 0.0 or safe_crypto == 0.0:
        if cushion_vnd > 0.0:
            vcr_days = 999.0
            risk_zone = "GREEN_SAFE"
        elif cushion_vnd == 0.0:
            vcr_days = 0.0
            risk_zone = "RED_DANGER"
        else:
            vcr_days = -999.0
            risk_zone = "RED_DANGER"
    else:
        vcr_days = cushion_vnd / daily_noise_vnd
        if cushion_vnd <= 0.0 or vcr_days < 3.0:
            risk_zone = "RED_DANGER"
        elif 3.0 <= vcr_days < 6.0:
            risk_zone = "YELLOW_CAUTION"
        else:
            risk_zone = "GREEN_SAFE"

    # CPPI Safe Crypto Capacity
    if safe_atr_pct > 0.0:
        cppi_max_safe_crypto_vnd = cushion_vnd / (safe_k * safe_atr_pct)
    else:
        cppi_max_safe_crypto_vnd = safe_tts

    excess_risk_vnd = max(0.0, safe_crypto - max(0.0, cppi_max_safe_crypto_vnd))
    cushion_pct = (cushion_vnd / safe_tts) if safe_tts > 0.0 else 0.0

    # Post-action projection: If 50% de-risking executed (crypto cut by 50%, remaining BTC ATR ~2.70%)
    projected_crypto = safe_crypto * 0.5
    projected_daily_noise = projected_crypto * 0.0270
    projected_vcr = (cushion_vnd / projected_daily_noise) if projected_daily_noise > 0 else 999.0

    return {
        "tts_vnd": safe_tts,
        "crypto_vnd": safe_crypto,
        "hard_floor_vnd": safe_floor,
        "cushion_vnd": cushion_vnd,
        "cushion_pct": round(cushion_pct, 4),
        "portfolio_daily_atr_pct": safe_atr_pct,
        "daily_noise_vnd": daily_noise_vnd,
        "vcr_days": vcr_days,
        "risk_zone": risk_zone,
        "cppi_max_safe_crypto_vnd": cppi_max_safe_crypto_vnd,
        "excess_risk_vnd": excess_risk_vnd,
        "post_action_vcr_projection": round(projected_vcr, 2),
        "action_required": "URGENT_DE_RISK_50_PCT" if risk_zone == "RED_DANGER" else (
            "TRIM_RISK_TO_SAFE_CAP" if risk_zone == "YELLOW_CAUTION" else "HOLD_OR_GLIDEPATH"
        ),
    }
