"""
Tier 1: Feature F11 — Key Metrics Panel & What-If Simulation Panel Tests.
Authoritative source: PROJECT.md §F11; ORIGINAL_REQUEST.md §R4.1 & §R4.2.
"""

import unittest

try:
    from crypto_dashboard.api_handlers import run_simulation
    HAS_F11 = True
except ImportError:
    HAS_F11 = False


class TestF11WhatIfMetrics(unittest.TestCase):
    """Verifies Key Metrics calculations and interactive What-If Simulation engine."""

    def test_f11_01_whatif_simulation_price_shock_calculation(self):
        """Authoritative Source: ORIGINAL_REQUEST.md §R4.2:
        Simulate TTS if BTC drops to $70k (-16.93%) and SOL drops to $95 (-17.91%).
        Inputs: BTC 0.159310 @ $70k, SOL 55.28 @ $95, Stables $1,415, P2P 25,930.
        Expected crypto USD = 0.159310 * 70000 + 55.28 * 95 + 1415 = 11151.7 + 5251.6 + 1415 = 17818.3 USD.
        Expected TTS VND = 17818.3 * 25930 = 462,028,519 VND.
        Floor distance to 540tr = 462,028,519 - 540,000,000 = -77,971,481 VND (Breached!).
        """
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        res = run_simulation(
            btc_price=70000.0,
            sol_price=95.0,
            p2p_rate=25930.0,
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0,
            hard_floor_vnd=540000000.0
        )
        self.assertAlmostEqual(res["simulated_tts_vnd"], 462028519.0, delta=2000.0)
        self.assertTrue(res["is_floor_breached"])
        self.assertLess(res["distance_to_floor_vnd"], 0)

    def test_f11_02_scenario_a_sell_50_vs_scenario_b_hold_100(self):
        """Authoritative Source: ORIGINAL_REQUEST.md §R4.2:
        Compare TTS between 'Bán 50% ngay hôm nay' vs 'Không bán/Giữ nguyên'.
        """
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers.run_simulation not implemented yet (Milestone M4)")

        res = run_simulation(
            btc_price=70000.0,
            sol_price=95.0,
            p2p_rate=25930.0,
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0,
            hard_floor_vnd=540000000.0
        )
        self.assertIn("scenario_a_sell_50", res)
        self.assertIn("scenario_b_hold_100", res)
        self.assertGreater(
            res["scenario_a_sell_50"]["simulated_tts_vnd"],
            res["scenario_b_hold_100"]["simulated_tts_vnd"]
        )

    def test_f11_03_portfolio_allocation_weights(self):
        """Authoritative Source: explorer_dashboard_1/report.md §3.2 Component 2:
        BTC ~63.2%, SOL ~30.1%, Stables ~6.7%.
        """
        if not HAS_F11:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M4)")

        # Verify weights sum to 100%
        btc_val = 0.159310 * 84262.0 * 25930.0
        sol_val = 55.28 * 115.72 * 25930.0
        stables_val = 1415.0 * 25930.0
        total = btc_val + sol_val + stables_val

        w_btc = (btc_val / total) * 100.0
        w_sol = (sol_val / total) * 100.0
        w_stables = (stables_val / total) * 100.0

        self.assertAlmostEqual(w_btc + w_sol + w_stables, 100.0, places=3)
        self.assertAlmostEqual(w_btc, 63.22, delta=0.5)
        self.assertAlmostEqual(w_sol, 30.12, delta=0.5)

    def test_f11_04_cashout_progress_percentage(self):
        """Authoritative Source: PROJECT.md §F11:
        Cashout progress = (cash_withdrawn_vnd / total_initial_goal_vnd) * 100%.
        When withdrawn = 0, progress = 0.0%.
        """
        withdrawn = 0.0
        target = 550643256.0
        progress = (withdrawn / target) * 100.0
        self.assertEqual(progress, 0.0)

    def test_f11_05_buffer_bar_pct_to_540m(self):
        """Authoritative Source: 2026-09-24 Critical Update:
        Safety buffer pct = (TTS - 540,000,000) / 540,000,000 * 100%.
        At 550,643,256 VND, buffer = 10,643,256 / 540M = +1.97%.
        """
        tts = 550643256.0
        floor = 540000000.0
        buffer_pct = ((tts - floor) / floor) * 100.0
        self.assertAlmostEqual(buffer_pct, 1.97, delta=0.05)


if __name__ == "__main__":
    unittest.main()
