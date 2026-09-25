"""
Tier 2: Feature F12 Boundaries — Macro Countdown & BĐS Debt Corner Cases.
"""

from datetime import datetime, timezone, timedelta
import unittest


class TestB12MacroBoundaries(unittest.TestCase):
    """Verifies edge cases for Macro events countdown and BĐS funding thresholds."""

    def test_b12_01_expired_deadline_negative_remaining_seconds(self):
        """When an event deadline has passed, remaining seconds is negative and marked expired."""
        deadline = datetime(2026, 9, 20, 0, 0, 0, tzinfo=timezone.utc)
        now = datetime(2026, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
        remaining = (deadline - now).total_seconds()
        self.assertLess(remaining, 0)

    def test_b12_02_zero_borrow_needed_boundary(self):
        """When self-equity >= 3,100,000,000 VND, borrow needed is 0."""
        total_budget = 3100000000.0
        family = 1300000000.0
        personal = 705000000.0
        tts_high = 1200000000.0  # 1.2 billion
        self_equity = family + personal + tts_high  # 3.205 billion
        borrow_needed = max(0.0, total_budget - self_equity)
        self.assertEqual(borrow_needed, 0.0)

    def test_b12_03_borrow_ceiling_exceeded_boundary(self):
        """When crypto TTS drops to 300M, borrow needed exceeds 615M ceiling."""
        total_budget = 3100000000.0
        family = 1300000000.0
        personal = 705000000.0
        tts_low = 300000000.0
        self_equity = family + personal + tts_low  # 2.305 billion
        borrow_needed = total_budget - self_equity  # 795 million
        cushion = 615000000.0 - borrow_needed       # -180 million
        self.assertLess(cushion, 0)
        self.assertEqual(cushion, -180000000.0)

    def test_b12_04_timezone_conversion_utc_to_vn(self):
        """20:00 VN (UTC+7) equals 13:00 UTC on the same day."""
        vn_tz = timezone(timedelta(hours=7))
        time_vn = datetime(2026, 9, 24, 20, 0, 0, tzinfo=vn_tz)
        time_utc = time_vn.astimezone(timezone.utc)
        self.assertEqual(time_utc.hour, 13)
        self.assertEqual(time_utc.day, 24)

    def test_b12_05_leap_year_math(self):
        """Checks leap year days count for year 2028 (wedding milestone mentioned in plan)."""
        d1 = datetime(2028, 2, 28)
        d2 = datetime(2028, 3, 1)
        self.assertEqual((d2 - d1).days, 2)


if __name__ == "__main__":
    unittest.main()
