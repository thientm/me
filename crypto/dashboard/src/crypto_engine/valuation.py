"""
Module: crypto_engine.valuation
Realtime and cached valuation engine using Binance Spot and P2P rate endpoints.
Zero external dependencies (100% Python Standard Library urllib.request).
Features automatic SSL fallback (ssl._create_unverified_context) and local caching.
"""

from __future__ import annotations
import json
import ssl
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union, List

from .config import (
    CACHE_RATES_FILE,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
    FALLBACK_WITHDRAWN_VND,
    FALLBACK_BTC_PRICE,
    FALLBACK_SOL_PRICE,
    FALLBACK_P2P_RATE,
    BINANCE_SPOT_URL,
    BINANCE_P2P_URL,
)


@dataclass
class ValuationSnapshot:
    btc_qty: float
    sol_qty: float
    stables_usd: float
    btc_price: float
    sol_price: float
    p2p_rate: float
    crypto_vnd: float
    withdrawn_vnd: float
    tts_vnd: float
    timestamp: str
    data_source: str  # "realtime" | "cache" | "fallback"


def _make_resilient_request(req: urllib.request.Request, timeout: float = 5.0) -> bytes:
    """Execute HTTP request with SSL fallback to unverified context for macOS Python compatibility."""
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            return resp.read()
    except (ssl.SSLCertVerificationError, urllib.error.URLError, Exception) as e:
        # If SSL certificate error or handshake failure, retry with unverified context
        err_msg = str(e)
        if isinstance(e, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in err_msg or "SSL" in err_msg:
            ctx_unverified = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=ctx_unverified, timeout=timeout) as resp:
                return resp.read()
        raise e


def fetch_binance_spot(symbols: Optional[List[str]] = None, timeout: float = 5.0) -> Dict[str, float]:
    """Fetch live Binance spot prices for specified symbols (default BTCUSDT and SOLUSDT)."""
    if symbols is None:
        symbols = ["BTCUSDT", "SOLUSDT"]
    symbols_json = json.dumps(symbols)
    url = f"https://api.binance.com/api/v3/ticker/price?symbols={urllib.request.quote(symbols_json)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )
    content = _make_resilient_request(req, timeout=timeout)
    data = json.loads(content.decode("utf-8"))
    return {item["symbol"]: float(item["price"]) for item in data}


def fetch_binance_p2p(
    asset: str = "USDT",
    fiat: str = "VND",
    trans_amount: str = "50000000",
    timeout: float = 5.0
) -> float:
    """Fetch best Binance P2P SELL price (USDT -> VND) for merchants."""
    payload = {
        "page": 1,
        "rows": 5,
        "payTypes": [],
        "asset": asset,
        "tradeType": "SELL",
        "fiat": fiat,
        "transAmount": str(trans_amount)
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BINANCE_P2P_URL,
        data=data_bytes,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )
    content = _make_resilient_request(req, timeout=timeout)
    res_json = json.loads(content.decode("utf-8"))
    ads = res_json.get("data", [])
    if not ads:
        raise ValueError("Binance P2P returned empty ads array")
    best_rate = float(ads[0]["adv"]["price"])
    return best_rate


def load_cached_rates(cache_path: Optional[Union[Path, str]] = None) -> Tuple[Dict[str, float], str]:
    """
    Load rates from local cache file.
    Returns: (rates_dict, source) where rates_dict has BTCUSDT, SOLUSDT, USDT_VND_P2P keys.
    """
    target_path = Path(cache_path) if cache_path else CACHE_RATES_FILE
    if target_path.exists():
        try:
            content = target_path.read_text(encoding="utf-8")
            data = json.loads(content)
            # Check if rates are nested under "rates"
            if "rates" in data and isinstance(data["rates"], dict):
                r = data["rates"]
                btc_p = float(r.get("BTCUSDT", r.get("btc_price", FALLBACK_BTC_PRICE)))
                sol_p = float(r.get("SOLUSDT", r.get("sol_price", FALLBACK_SOL_PRICE)))
                p2p_r = float(r.get("USDT_VND_P2P", r.get("p2p_rate", FALLBACK_P2P_RATE)))
            else:
                btc_p = float(data.get("BTCUSDT", data.get("btc_price", FALLBACK_BTC_PRICE)))
                sol_p = float(data.get("SOLUSDT", data.get("sol_price", FALLBACK_SOL_PRICE)))
                p2p_r = float(data.get("USDT_VND_P2P", data.get("p2p_rate", FALLBACK_P2P_RATE)))
            return {
                "BTCUSDT": btc_p,
                "SOLUSDT": sol_p,
                "USDT_VND_P2P": p2p_r,
                "btc_price": btc_p,
                "sol_price": sol_p,
                "p2p_rate": p2p_r
            }, "cache"
        except Exception:
            pass

    return {
        "BTCUSDT": FALLBACK_BTC_PRICE,
        "SOLUSDT": FALLBACK_SOL_PRICE,
        "USDT_VND_P2P": FALLBACK_P2P_RATE,
        "btc_price": FALLBACK_BTC_PRICE,
        "sol_price": FALLBACK_SOL_PRICE,
        "p2p_rate": FALLBACK_P2P_RATE
    }, "fallback"


def save_cached_rates(
    btc_price: float,
    sol_price: float,
    p2p_rate: float,
    cache_path: Optional[Union[Path, str]] = None
) -> None:
    """Save latest fetched rates to local cache file atomically."""
    target_path = Path(cache_path) if cache_path else CACHE_RATES_FILE
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "btc_price": btc_price,
            "sol_price": sol_price,
            "p2p_rate": p2p_rate,
            "rates": {
                "BTCUSDT": btc_price,
                "SOLUSDT": sol_price,
                "USDT_VND_P2P": p2p_rate
            },
            "metadata": {
                "source": "realtime",
                "status": "valid"
            }
        }
        target_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except Exception:
        pass


def get_rates(
    cache_path: Optional[Union[Path, str]] = None,
    offline_only: bool = False,
    timeout: float = 5.0
) -> Dict[str, float]:
    """
    Get market rates dictionary:
    Keys guaranteed: BTCUSDT, SOLUSDT, USDT_VND_P2P, btc_price, sol_price, p2p_rate.
    """
    if offline_only:
        rates, _ = load_cached_rates(cache_path)
        return rates

    try:
        spot = fetch_binance_spot(timeout=timeout)
        p2p = fetch_binance_p2p(timeout=timeout)
        btc_p = spot["BTCUSDT"]
        sol_p = spot["SOLUSDT"]
        save_cached_rates(btc_p, sol_p, p2p, cache_path)
        return {
            "BTCUSDT": btc_p,
            "SOLUSDT": sol_p,
            "USDT_VND_P2P": p2p,
            "btc_price": btc_p,
            "sol_price": sol_p,
            "p2p_rate": p2p
        }
    except Exception:
        rates, _ = load_cached_rates(cache_path)
        return rates


def calculate_tts(
    btc_qty: float = FALLBACK_BTC_QTY,
    sol_qty: float = FALLBACK_SOL_QTY,
    stables_usd: float = FALLBACK_STABLES_USD,
    btc_price: Optional[float] = None,
    sol_price: Optional[float] = None,
    p2p_rate: Optional[float] = None,
    withdrawn_vnd: float = 0.0,
    data_source: Optional[str] = None,
    cache_path: Optional[Union[Path, str]] = None,
    force_offline: bool = False
) -> ValuationSnapshot:
    """
    Computes total portfolio valuation (TTS) and returns ValuationSnapshot.
    Formula: TTS = withdrawn_vnd + (btc*btc_price + sol*sol_price + stables_usd) * p2p_rate.
    """
    source = data_source or "realtime"
    if btc_price is None or sol_price is None or p2p_rate is None:
        rates_dict = get_rates(cache_path=cache_path, offline_only=force_offline)
        btc_price = rates_dict["btc_price"] if btc_price is None else btc_price
        sol_price = rates_dict["sol_price"] if sol_price is None else sol_price
        p2p_rate = rates_dict["p2p_rate"] if p2p_rate is None else p2p_rate
        if force_offline:
            source = "cache"

    crypto_usd = (btc_qty * btc_price) + (sol_qty * sol_price) + stables_usd
    crypto_vnd = crypto_usd * p2p_rate
    tts_vnd = withdrawn_vnd + crypto_vnd

    return ValuationSnapshot(
        btc_qty=btc_qty,
        sol_qty=sol_qty,
        stables_usd=stables_usd,
        btc_price=round(btc_price, 2),
        sol_price=round(sol_price, 2),
        p2p_rate=round(p2p_rate, 2),
        crypto_vnd=round(crypto_vnd, 2),
        withdrawn_vnd=round(withdrawn_vnd, 2),
        tts_vnd=round(tts_vnd, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
        data_source=source
    )


# Alias for calculate_tts for API compatibility
calculate_valuation = calculate_tts
