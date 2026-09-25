"""
Tier 2: Feature F11 Boundaries — What-If Simulation Engine Corner Cases.
"""

import unittest

try:
    from crypto_dashboard.api_handlers import run_simulation
    HAS_F11 = True
except ImportError:
    HAS_F11 = False


class TestB11SimulationBoundaries(unittest.TestCase):
    """Verifies edge cases and extreme inputs for What-If Simulation."""

    def test_b11_01_total_market_wipeout_simulation(self):
        """When prices crash to 0, simulated TTS equals stables * p2p."""
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        res = run_simulation(
            btc_price=0.0,
            sol_price=0.0,
            p2p_rate=25930.0,
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0,
            hard_floor_vnd=540000000.0
        )
        expected_tts = 1415.0 * 25930.0  # 36,690,950 VND
        self.assertAlmostEqual(res["simulated_tts_vnd"], expected_tts, delta=100.0)
        self.assertTrue(res["is_floor_breached"])

    def test_b11_02_zero_coin_holdings_simulation(self):
        """Simulation with 0 BTC and 0 SOL returns stables-only valuation."""
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        res = run_simulation(
            btc_price=84000.0,
            sol_price=115.0,
            p2p_rate=25000.0,
            btc_qty=0.0,
            sol_qty=0.0,
            stables_usd=1000.0,
            hard_floor_vnd=540000000.0
        )
        self.assertEqual(res["simulated_tts_vnd"], 1000.0 * 25000.0)

    def test_b11_03_negative_price_rejected(self):
        """Negative price inputs should raise ValueError."""
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        with self.assertRaises((ValueError, AssertionError)):
            run_simulation(
                btc_price=-1000.0, sol_price=100.0, p2p_rate=25000.0,
                btc_qty=0.1, sol_qty=1.0, stables_usd=0.0, hard_floor_vnd=540000000.0
            )

    def test_b11_04_high_p2p_rate_simulation(self):
        """High P2P rate (e.g. 35,000 VND) scales accurately."""
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        res = run_simulation(
            btc_price=100000.0, sol_price=200.0, p2p_rate=35000.0,
            btc_qty=0.1, sol_qty=10.0, stables_usd=1000.0, hard_floor_vnd=540000000.0
        )
        crypto_usd = 0.1 * 100000.0 + 10.0 * 200.0 + 1000.0  # 10k + 2k + 1k = 13k
        expected_tts = 13000.0 * 35000.0  # 455M
        self.assertAlmostEqual(res["simulated_tts_vnd"], expected_tts, delta=100.0)

    def test_b11_05_distance_to_floor_exact_difference(self):
        """distance_to_floor_vnd must equal simulated_tts_vnd - 540,000,000."""
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        res = run_simulation(
            btc_price=80000.0, sol_price=100.0, p2p_rate=25000.0,
            btc_qty=0.1, sol_qty=10.0, stables_usd=1000.0, hard_floor_vnd=540000000.0
        )
        expected_diff = res["simulated_tts_vnd"] - 540000000.0
        self.assertAlmostEqual(res["distance_to_floor_vnd"], expected_diff, delta=1.0)


if __name__ == "__main__":
    unittest.main()
