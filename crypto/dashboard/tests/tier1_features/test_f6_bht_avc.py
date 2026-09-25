"""
Tier 1: Feature F6 — Quant Innovation 2: BHT-Ticker & AVC-Meter Tests.
Authoritative source: PROJECT.md §F6; explorer_trend_1/report.md §Tính Năng 2 & §Tính Năng 3.
"""

import unittest

try:
    from crypto_engine.quant.hesitation_tax import calculate_hesitation_tax, get_commitment_device_status
    from crypto_engine.quant.volatility_cushion import calculate_volatility_cushion
    HAS_F6 = True
except ImportError:
    HAS_F6 = False


class TestF6BHTandAVC(unittest.TestCase):
    """Verifies Behavioral Hesitation Tax (BHT) and Dynamic ATR Volatility Cushion (AVC)."""

    def test_f6_01_bht_hourly_burn_rate_oracle(self):
        """Authoritative Source: explorer_trend_1/report.md §2.2:
        3.1 billion VND * 0.03%/day = 930,000 VND/day = 38,750 VND/hour = 645.83 VND/minute.
        """
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.hesitation_tax not implemented yet (Milestone M2)")

        tax_data = calculate_hesitation_tax(
            land_fee_vnd=3100000000.0,
            hours_delayed=1.0,
            unexecuted_count=13
        )
        self.assertAlmostEqual(tax_data["burn_rate_vnd_per_hour"], 38750.0, delta=1.0)
        self.assertAlmostEqual(tax_data["tax_late_penalty_vnd"], 38750.0, delta=1.0)

    def test_f6_02_commitment_device_10_minute_timeout(self):
        """Authoritative Source: explorer_trend_1/report.md §3:
        Commitment device timer lasts 10 minutes (600 seconds) from recommendation trigger.
        """
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.hesitation_tax not implemented yet (Milestone M2)")

        status = get_commitment_device_status(elapsed_seconds=300)
        self.assertEqual(status["total_duration_seconds"], 600)
        self.assertEqual(status["remaining_seconds"], 300)
        self.assertFalse(status["is_expired"])

        expired_status = get_commitment_device_status(elapsed_seconds=601)
        self.assertTrue(expired_status["is_expired"])

    def test_f6_03_avc_volatility_cushion_ratio_formula(self):
        """Authoritative Source: explorer_trend_1/report.md §2.2:
        VCR = Cushion_VND / Daily_ATR_VND where Cushion = TTS - 540,000,000.
        If TTS = 550,643,256, Cushion = 10,643,256 VND.
        If Daily_ATR_VND = 15,380,000 VND -> VCR = 10,643,256 / 15,380,000 = ~0.69 days.
        """
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.volatility_cushion not implemented yet (Milestone M2)")

        cushion_result = calculate_volatility_cushion(
            tts_vnd=550643256.0,
            crypto_vnd=496100000.0,
            portfolio_daily_atr_pct=0.0310,
            hard_floor_vnd=540000000.0
        )
        expected_cushion = 550643256.0 - 540000000.0  # 10,643,256
        expected_daily_atr = 496100000.0 * 0.0310       # 15,379,100
        expected_vcr = expected_cushion / expected_daily_atr

        self.assertAlmostEqual(cushion_result["cushion_vnd"], expected_cushion, delta=1.0)
        self.assertAlmostEqual(cushion_result["vcr_days"], expected_vcr, places=2)

    def test_f6_04_avc_risk_zone_classification(self):
        """Authoritative Source: explorer_trend_1/report.md §2.2:
        VCR < 3.0 -> RED_DANGER; 3.0 <= VCR < 6.0 -> YELLOW_CAUTION; VCR >= 6.0 -> GREEN_SAFE.
        """
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.volatility_cushion not implemented yet (Milestone M2)")

        # Case 1: Cushion thin (< 3.0 days)
        res_danger = calculate_volatility_cushion(
            tts_vnd=550000000.0, crypto_vnd=450000000.0, portfolio_daily_atr_pct=0.03, hard_floor_vnd=540000000.0
        )
        self.assertEqual(res_danger["risk_zone"], "RED_DANGER")

        # Case 2: Cushion safe (>= 6.0 days)
        res_safe = calculate_volatility_cushion(
            tts_vnd=700000000.0, crypto_vnd=200000000.0, portfolio_daily_atr_pct=0.02, hard_floor_vnd=540000000.0
        )
        self.assertEqual(res_safe["risk_zone"], "GREEN_SAFE")

    def test_f6_05_cppi_safe_crypto_capacity(self):
        """Authoritative Source: explorer_trend_1/report.md §2.3:
        CPPI Safe Capacity: Exposure_max = Cushion / (k * Daily_ATR_pct) where k=3.0.
        """
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.volatility_cushion not implemented yet (Milestone M2)")

        cushion_result = calculate_volatility_cushion(
            tts_vnd=550643256.0,
            crypto_vnd=496100000.0,
            portfolio_daily_atr_pct=0.0310,
            hard_floor_vnd=540000000.0
        )
        cushion = 550643256.0 - 540000000.0
        expected_safe_cap = cushion / (3.0 * 0.0310)
        self.assertAlmostEqual(cushion_result["cppi_max_safe_crypto_vnd"], expected_safe_cap, delta=1000.0)


if __name__ == "__main__":
    unittest.main()
