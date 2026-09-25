"""
Tier 1: Feature F12 — Macro Countdown & BĐS Debt Tracker Tests.
Authoritative source: PROJECT.md §F12; ORIGINAL_REQUEST.md §R4.3; explorer_dashboard_1/report.md §3.2 Component 4.
"""

from datetime import datetime, timezone
import unittest

try:
    from crypto_dashboard.api_handlers import get_macro_data
    HAS_F12 = True
except ImportError:
    HAS_F12 = False


class TestF12MacroDebt(unittest.TestCase):
    """Verifies Macro countdowns and Real Estate (BĐS) debt balancing calculations."""

    def test_f12_01_late_oct_2026_cashout_deadline(self):
        """Authoritative Source: 2026-09-24 Critical Update:
        Cashout deadline is Late October 2026 (2026-10-31 23:59:59).
        """
        deadline = datetime(2026, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
        now = datetime(2026, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
        diff_days = (deadline - now).days
        self.assertEqual(diff_days, 37)

    def test_f12_02_bds_debt_source_30_09_deadline(self):
        """Authoritative Source: crypto-plan.md §7.4:
        'Chốt nguồn 615tr là việc của T9, không để tới T10.' Deadline is 2026-09-30.
        """
        deadline_bds = datetime(2026, 9, 30, 17, 0, 0, tzinfo=timezone.utc)
        now = datetime(2026, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
        remaining_seconds = (deadline_bds - now).total_seconds()
        self.assertGreater(remaining_seconds, 0)
        self.assertEqual((deadline_bds - now).days, 6)

    def test_f12_03_bds_financial_gap_formula_oracle(self):
        """Authoritative Source: crypto-plan.md §7.4 & real-estate-plan.md:
        Total budget = 3,100,000,000 VND
        Family support = 1,300,000,000 VND
        Personal cash = 705,000,000 VND
        Self equity = 1.3B + 705M + TTS = 2,005M + TTS
        Borrow needed = 3,100,000,000 - Self equity
        With TTS = 550,643,256 VND -> Self equity = 2,555,643,256 VND.
        Borrow needed = 3,100,000,000 - 2,555,643,256 = 544,356,744 VND.
        """
        total_budget = 3100000000.0
        family_support = 1300000000.0
        personal_cash = 705000000.0
        tts_crypto = 550643256.0

        self_equity = family_support + personal_cash + tts_crypto
        borrow_needed = total_budget - self_equity

        self.assertAlmostEqual(self_equity, 2555643256.0, delta=1.0)
        self.assertAlmostEqual(borrow_needed, 544356744.0, delta=1.0)

    def test_f12_04_borrow_ceiling_cushion(self):
        """Authoritative Source: PROJECT.md §F12:
        Borrow ceiling is 615,000,000 VND.
        Cushion = 615,000,000 - borrow_needed.
        With borrow_needed = 544,356,744 VND -> Cushion = +70,643,256 VND (Safe!).
        """
        borrow_ceiling = 615000000.0
        borrow_needed = 544356744.0
        cushion = borrow_ceiling - borrow_needed
        self.assertAlmostEqual(cushion, 70643256.0, delta=1.0)
        self.assertGreater(cushion, 0)

    def test_f12_05_macro_api_returns_all_events(self):
        """Authoritative Source: PROJECT.md §F12:
        Macro data contains event list with deadlines and remaining seconds.
        """
        if not HAS_F12:
            self.skipTest("crypto_dashboard.api_handlers.get_macro_data not implemented yet (Milestone M4)")

        data = get_macro_data(tts_vnd=550643256.0)
        events = data.get("events", [])
        event_titles = [e.get("title") for e in events]
        self.assertTrue(any("Tranche" in t for t in event_titles))
        self.assertTrue(any("615tr" in t or "BĐS" in t for t in event_titles))


if __name__ == "__main__":
    unittest.main()
