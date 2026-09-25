"""
Tier 4: Scenario 6 — Behavioral Hesitation Tax & Land Fee Escalation.
Authoritative source: explorer_trend_1/report.md §Tính Năng 2; crypto-plan.md §1 & §7.4.
"""

import unittest

try:
    from crypto_engine.quant.hesitation_tax import calculate_hesitation_tax
    HAS_SCENARIO_6 = True
except ImportError:
    HAS_SCENARIO_6 = False


class TestScenarioLandFeeEscalation(unittest.TestCase):
    """Simulates multi-day delay escalation and financial penalty compounding."""

    def test_7_day_delay_financial_penalty_accumulation(self):
        """After 7 days (168 hours) of delay on 3.1 billion VND land fee:
        - Late penalty = 3.1B * 0.03%/day * 7 days = 6,510,000 VND.
        - Hourly burn rate = 38,750 VND/hour.
        - Status level escalates to DEFCON_1_PARALYSIS when missed count >= 13.
        """
        if not HAS_SCENARIO_6:
            self.skipTest("crypto_engine.quant.hesitation_tax not implemented yet (Milestone M2)")

        result = calculate_hesitation_tax(
            land_fee_vnd=3100000000.0,
            hours_delayed=168.0,
            unexecuted_count=14
        )
        self.assertAlmostEqual(result["tax_late_penalty_vnd"], 6510000.0, delta=100.0)
        self.assertAlmostEqual(result["burn_rate_vnd_per_hour"], 38750.0, delta=1.0)
        self.assertEqual(result["status_level"], "DEFCON_1_PARALYSIS")
        self.assertGreaterEqual(result["total_hesitation_tax_vnd"], 6510000.0)


if __name__ == "__main__":
    unittest.main()
