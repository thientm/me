"""
Module: crypto_engine.parser
Extracts portfolio holdings, initial capital, withdrawn VND, and execution history
from crypto-plan.md and logs/*.md.
Zero external dependencies (100% Python Standard Library).
"""

from __future__ import annotations
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

from .config import (
    CRYPTO_PLAN_PATH,
    CRYPTO_LOGS_DIR,
    HARD_FLOOR_VND,
    INITIAL_CAPITAL_VND,
    CASH_OUT_DEADLINE_STR,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
    FALLBACK_WITHDRAWN_VND,
)


@dataclass
class PortfolioHoldings:
    btc_qty: float
    sol_qty: float
    stables_usd: float
    withdrawn_vnd: float
    base_capital_vnd: float
    hard_floor_vnd: float
    deadline_date: str
    source_file: str
    is_fallback: bool = False


@dataclass
class LogReviewEntry:
    date_str: str
    header: str
    withdrawn_vnd: float
    file_name: str
    raw_content: str


def normalize_crypto_qty(val_str: str) -> float:
    """Normalize crypto quantity string handling Vietnamese decimal comma (0,15931 -> 0.15931)."""
    cleaned = val_str.replace("*", "").replace("~", "").strip()
    if "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")
    return float(cleaned)


def normalize_stables_usd(val_str: str) -> float:
    """Normalize Stables USD amount (handling ~$1.415, 1415.0, $1,415 -> 1415.0)."""
    cleaned = val_str.replace("$", "").replace("~", "").replace("*", "").strip()
    # Check for thousands separator format like 1.415 where decimal part has exactly 3 digits and integer part < 100
    if "." in cleaned and "," not in cleaned:
        parts = cleaned.split(".")
        if len(parts) == 2 and len(parts[1]) == 3 and parts[0].isdigit() and int(parts[0]) < 100:
            return float(parts[0] + parts[1])
    cleaned = cleaned.replace(",", "")
    return float(cleaned)


def extract_withdrawn_vnd(text: str) -> float:
    """Extract withdrawn VND amount into bank account from text."""
    patterns = [
        r"Tiến\s+độ\s+luỹ\s+kế\s+rút\s+VND[:\s*]+([0-9.,]+)\s*(?:tr|triệu|đ|VND)?",
        r"Tiến\s+độ\s+rút\s+VND[:\s*]+([0-9.,]+)\s*(?:tr|triệu|đ|VND|/)",
        r"VND\s+đã\s+rút[:\s*]+([0-9.,]+)\s*(?:tr|triệu|đ|VND)",
        r"Tiền\s+mặt\s+đã\s+rút[:\s*]+([0-9.,]+)\s*(?:tr|triệu|đ|VND)",
        r"Đã\s+rút\s+VND[:\s*]+([0-9.,]+)\s*(?:tr|triệu|đ|VND)",
        r"Đã\s+rút[:\s*]+([0-9.,]+)\s*(?:tr|triệu|đ|VND)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val_raw = m.group(1).replace(",", ".")
            try:
                val = float(val_raw)
                return val * 1_000_000.0 if val < 10_000 else val
            except ValueError:
                continue
    return 0.0


def extract_missed_count(text: str) -> int:
    """Extract count of unexecuted recommendations (e.g. 0/13 or 0/14)."""
    patterns = [
        r"0/(\d+)\s+khuyến\s+nghị",
        r"Lệnh\s+thực\s+thi[:\s*]+0/(\d+)",
        r"\(0/(\d+)\s+khuyến\s+nghị\s+thực\s+thi\)",
        r"chưa\s+bán\s+gì.*?0/(\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                pass
    return 13  # Authoritative default baseline


def parse_portfolio_plan(plan_path: Optional[Union[Path, str]] = None) -> PortfolioHoldings:
    """Parse crypto-plan.md and return PortfolioHoldings dataclass."""
    target_path = Path(plan_path) if plan_path else CRYPTO_PLAN_PATH
    if not target_path.exists():
        return PortfolioHoldings(
            btc_qty=FALLBACK_BTC_QTY,
            sol_qty=FALLBACK_SOL_QTY,
            stables_usd=FALLBACK_STABLES_USD,
            withdrawn_vnd=FALLBACK_WITHDRAWN_VND,
            base_capital_vnd=INITIAL_CAPITAL_VND,
            hard_floor_vnd=HARD_FLOOR_VND,
            deadline_date=CASH_OUT_DEADLINE_STR,
            source_file="fallback_default",
            is_fallback=True
        )

    text = target_path.read_text(encoding="utf-8")
    btc_qty: Optional[float] = None
    sol_qty: Optional[float] = None
    stables_usd: Optional[float] = None

    # Tier 1: Markdown Table at Section 2
    for line in text.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            asset = parts[1].replace("*", "").upper()
            sl_val = parts[2]
            if "BTC" in asset and btc_qty is None:
                try:
                    btc_qty = normalize_crypto_qty(sl_val)
                except Exception:
                    pass
            elif "SOL" in asset and sol_qty is None:
                try:
                    sol_qty = normalize_crypto_qty(sl_val)
                except Exception:
                    pass
            elif any(s in asset for s in ["STABLE", "USDT", "USDC"]) and stables_usd is None:
                try:
                    stables_usd = normalize_stables_usd(sl_val)
                except Exception:
                    pass

    # Tier 2: Inline Context Regex
    if btc_qty is None:
        m = re.search(r"BTC[:\s*]+([0-9.,]+)", text)
        if m:
            try:
                btc_qty = normalize_crypto_qty(m.group(1))
            except Exception:
                pass
    if sol_qty is None:
        m = re.search(r"SOL[:\s*]+([0-9.,]+)", text)
        if m:
            try:
                sol_qty = normalize_crypto_qty(m.group(1))
            except Exception:
                pass
    if stables_usd is None:
        m = re.search(r"(?:stables?|USDT)[:\s*]+(?:~\s*)?\$?([0-9.,]+)", text, re.IGNORECASE)
        if m:
            try:
                stables_usd = normalize_stables_usd(m.group(1))
            except Exception:
                pass

    # Tier 3: Initial Capital
    capital = INITIAL_CAPITAL_VND
    cap_match = re.search(r"(?:Tổng\s+vốn\s+gốc|initial)[^:]*:\s*([0-9.,]+)", text, re.IGNORECASE)
    if cap_match:
        try:
            val_clean = cap_match.group(1).replace(",", "").replace(".", "")
            capital = float(val_clean)
        except Exception:
            pass

    btc_final = btc_qty if btc_qty is not None else FALLBACK_BTC_QTY
    sol_final = sol_qty if sol_qty is not None else FALLBACK_SOL_QTY
    stables_final = stables_usd if stables_usd is not None else FALLBACK_STABLES_USD
    withdrawn = extract_withdrawn_vnd(text)

    return PortfolioHoldings(
        btc_qty=btc_final,
        sol_qty=sol_final,
        stables_usd=stables_final,
        withdrawn_vnd=withdrawn,
        base_capital_vnd=capital,
        hard_floor_vnd=HARD_FLOOR_VND,
        deadline_date=CASH_OUT_DEADLINE_STR,
        source_file=str(target_path),
        is_fallback=(btc_qty is None or sol_qty is None or stables_usd is None)
    )


def parse_crypto_plan(plan_path: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
    """Parse crypto-plan.md and return dictionary satisfying test contracts."""
    holdings = parse_portfolio_plan(plan_path)
    return {
        "btc_qty": holdings.btc_qty,
        "sol_qty": holdings.sol_qty,
        "stables_usd": holdings.stables_usd,
        "withdrawn_vnd": holdings.withdrawn_vnd,
        "base_capital_vnd": int(holdings.base_capital_vnd),
        "hard_floor_vnd": holdings.hard_floor_vnd,
        "deadline_date": holdings.deadline_date,
        "source_file": holdings.source_file,
        "is_fallback": holdings.is_fallback
    }


def parse_logs(logs_path_or_dir: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
    """
    Parse logs file or directory to extract cumulative withdrawn VND and missed recommendations count.
    Accepts either a single file path or directory path.
    """
    target = Path(logs_path_or_dir) if logs_path_or_dir else CRYPTO_LOGS_DIR
    if not target.exists():
        return {
            "withdrawn_vnd": 0.0,
            "missed_recommendations_count": 13,
            "latest_review_date": None,
            "entries_count": 0
        }

    total_withdrawn = 0.0
    missed_count = 13
    latest_date = None
    entries_count = 0

    files_to_read: List[Path] = []
    if target.is_file():
        files_to_read.append(target)
    elif target.is_dir():
        files_to_read = sorted(target.glob("*.md"))

    for log_file in files_to_read:
        try:
            content = log_file.read_text(encoding="utf-8")
            sections = re.split(r"\n(?=##\s+)", content)
            for sec in sections:
                sec = sec.strip()
                if not sec.startswith("##"):
                    continue
                entries_count += 1
                w = extract_withdrawn_vnd(sec)
                if w > total_withdrawn:
                    total_withdrawn = w
                mc = extract_missed_count(sec)
                if mc > missed_count:
                    missed_count = mc
                first_line = sec.splitlines()[0]
                dm = re.search(r"(\d{4}-\d{2}-\d{2})", first_line)
                if dm:
                    latest_date = dm.group(1)
        except Exception:
            continue

    return {
        "withdrawn_vnd": total_withdrawn,
        "missed_recommendations_count": missed_count,
        "latest_review_date": latest_date,
        "entries_count": entries_count
    }


def parse_logs_history(logs_dir: Optional[Union[Path, str]] = None) -> List[LogReviewEntry]:
    """Read all review history entries from logs directory."""
    target_dir = Path(logs_dir) if logs_dir else CRYPTO_LOGS_DIR
    if not target_dir.exists():
        return []

    entries: List[LogReviewEntry] = []
    files = [target_dir] if target_dir.is_file() else sorted(target_dir.glob("*.md"))
    for log_file in files:
        try:
            content = log_file.read_text(encoding="utf-8")
            sections = re.split(r"\n(?=##\s+)", content)
            for sec in sections:
                sec = sec.strip()
                if not sec.startswith("##"):
                    continue
                first_line = sec.splitlines()[0]
                date_match = re.search(r"(\d{4}-\d{2}-\d{2})", first_line)
                entry_date = date_match.group(1) if date_match else first_line[2:].strip()
                withdrawn = extract_withdrawn_vnd(sec)
                entries.append(LogReviewEntry(
                    date_str=entry_date,
                    header=first_line,
                    withdrawn_vnd=withdrawn,
                    file_name=log_file.name,
                    raw_content=sec
                ))
        except Exception:
            continue
    return entries
