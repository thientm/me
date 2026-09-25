"""
Tier 2: Feature F6 Boundaries — BHT-Ticker & AVC-Meter Corner Cases.
"""

import unittest

try:
    from crypto_engine.quant.hesitation_tax import calculate_hesitation_tax
    from crypto_engine.quant.volatility_cushion import calculate_volatility_cushion
    HAS_F6 = True
except ImportError:
    HAS_F6 = False


class TestB6BHTandAVCBoundaries(unittest.TestCase):
    """Verifies edge cases and division-by-zero safeguards for BHT and AVC models."""

    def test_b6_01_zero_hours_delayed_zero_penalty(self):
        """Zero hours delayed results in 0 VND late tax penalty."""
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.hesitation_tax not implemented yet (Milestone M2)")

        result = calculate_hesitation_tax(land_fee_vnd=3100000000.0, hours_delayed=0.0)
        self.assertEqual(result["tax_late_penalty_vnd"], 0.0)

    def test_b6_02_post_2027_hazard_exposure_triggers_at_deadline(self):
        """When delay exceeds 2026 cutoff, 370M land price hazard exposure is fully included."""
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.hesitation_tax not implemented yet (Milestone M2)")

        result = calculate_hesitation_tax(land_fee_vnd=3100000000.0, hours_delayed=1000.0)
        self.assertGreaterEqual(result["land_2027_hazard_exposure_vnd"], 370000000.0)

    def test_b6_03_zero_cushion_vcr_is_zero(self):
        """When TTS == 540,000,000 VND exactly, cushion is 0 and VCR is 0.0 days."""
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.volatility_cushion not implemented yet (Milestone M2)")

        result = calculate_volatility_cushion(
            tts_vnd=540000000.0, crypto_vnd=400000000.0, portfolio_daily_atr_pct=0.03, hard_floor_vnd=540000000.0
        )
        self.assertEqual(result["cushion_vnd"], 0.0)
        self.assertEqual(result["vcr_days"], 0.0)
        self.assertEqual(result["risk_zone"], "RED_DANGER")

    def test_b6_04_negative_cushion_vcr_negative(self):
        """When TTS < 540M, cushion is negative and status is RED_DANGER."""
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.volatility_cushion not implemented yet (Milestone M2)")

        result = calculate_volatility_cushion(
            tts_vnd=500000000.0, crypto_vnd=400000000.0, portfolio_daily_atr_pct=0.03, hard_floor_vnd=540000000.0
        )
        self.assertEqual(result["cushion_vnd"], -40000000.0)
        self.assertLess(result["vcr_days"], 0.0)
        self.assertEqual(result["risk_zone"], "RED_DANGER")

    def test_b6_05_zero_crypto_division_by_zero_safeguard(self):
        """When crypto_vnd = 0 (100% in cash), daily ATR is 0. Function must handle without ZeroDivisionError."""
        if not HAS_F6:
            self.skipTest("crypto_engine.quant.volatility_cushion not implemented yet (Milestone M2)")

        result = calculate_volatility_cushion(
            tts_vnd=550000000.0, crypto_vnd=0.0, portfolio_daily_atr_pct=0.03, hard_floor_vnd=540000000.0
        )
        self.assertIn("vcr_days", result)
        self.assertEqual(result["risk_zone"], "GREEN_SAFE")


if __name__ == "__main__":
    unittest.main()
