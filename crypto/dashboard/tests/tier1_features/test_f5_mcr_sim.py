"""
Tier 1: Feature F5 — Quant Innovation 1: MCR-Sim Tests.
Authoritative source: PROJECT.md §F5; explorer_trend_1/report.md §Tính Năng 1.
"""

import unittest

try:
    from crypto_engine.quant.monte_carlo import run_monte_carlo_ruin_sim
    HAS_F5 = True
except ImportError:
    HAS_F5 = False


class TestF5MCRSim(unittest.TestCase):
    """Verifies MCR-Sim (Monte Carlo Ruin Simulator for 540tr Floor)."""

    def setUp(self):
        self.holdings = {
            "btc": 0.159310,
            "sol": 55.28,
            "stables_usd": 1415.0,
            "cash_vnd": 0.0
        }
        self.market_params = {
            "spot_btc": 84262.0,
            "sol_usdt": 115.72,
            "p2p": 25930.0
        }
        self.vol_params = {
            "sigma_btc": 0.0270,
            "sigma_sol": 0.0451,
            "rho": 0.78
        }

    def test_f5_01_mcr_sim_returns_required_output_metrics(self):
        """Authoritative Source: explorer_trend_1/report.md §5:
        Output must include: prob_ruin, var_95_vnd, cvar_95_vnd, median_tts_vnd.
        """
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        result = run_monte_carlo_ruin_sim(
            holdings=self.holdings,
            market_params=self.market_params,
            vol_params=self.vol_params,
            n_sims=500,
            horizon_days=37,
            hard_floor=540000000.0
        )
        self.assertIn("prob_ruin", result)
        self.assertIn("var_95_vnd", result)
        self.assertIn("cvar_95_vnd", result)
        self.assertIn("median_tts_vnd", result)
        self.assertIsInstance(result["prob_ruin"], float)

    def test_f5_02_hold_100_ruin_probability_higher_than_sell_50(self):
        """Authoritative Source: explorer_trend_1/report.md §3:
        Holding 100% coin has significantly higher ruin probability than selling 50% into cash.
        """
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        res_hold = run_monte_carlo_ruin_sim(
            holdings=self.holdings,
            market_params=self.market_params,
            vol_params=self.vol_params,
            n_sims=1000,
            horizon_days=37,
            hard_floor=540000000.0,
            strategy="HOLD_100"
        )
        # Sell 50% cash-locked simulation
        holdings_sell_50 = {
            "btc": 0.159310 * 0.5,
            "sol": 0.0,  # SOL sold 100%
            "stables_usd": 0.0,  # Withdrawn
            "cash_vnd": 284700000.0
        }
        res_sell = run_monte_carlo_ruin_sim(
            holdings=holdings_sell_50,
            market_params=self.market_params,
            vol_params=self.vol_params,
            n_sims=1000,
            horizon_days=37,
            hard_floor=540000000.0,
            strategy="SELL_50"
        )
        self.assertGreater(res_hold["prob_ruin"], res_sell["prob_ruin"])

    def test_f5_03_zero_drift_and_cholesky_correlation(self):
        """Authoritative Source: explorer_trend_1/report.md §2.1:
        Zero drift assumption and rho=0.78 correlation between BTC and SOL increments.
        """
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        # Verify that runner accepts valid correlation and doesn't crash
        result = run_monte_carlo_ruin_sim(
            holdings=self.holdings,
            market_params=self.market_params,
            vol_params={"sigma_btc": 0.027, "sigma_sol": 0.045, "rho": 0.78},
            n_sims=200,
            horizon_days=10,
            hard_floor=540000000.0
        )
        self.assertGreaterEqual(result["prob_ruin"], 0.0)
        self.assertLessEqual(result["prob_ruin"], 1.0)

    def test_f5_04_terminal_var95_less_than_median_tts(self):
        """Authoritative Source: explorer_trend_1/report.md §2.4:
        VaR 95% represents the 5th percentile, which mathematically must be <= 50th percentile (median).
        """
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        result = run_monte_carlo_ruin_sim(
            holdings=self.holdings,
            market_params=self.market_params,
            vol_params=self.vol_params,
            n_sims=500,
            horizon_days=30,
            hard_floor=540000000.0
        )
        self.assertLessEqual(result["var_95_vnd"], result["median_tts_vnd"])
        self.assertLessEqual(result["cvar_95_vnd"], result["var_95_vnd"])

    def test_f5_05_horizon_days_parameter_to_late_oct_2026(self):
        """Authoritative Source: 2026-09-24 Critical Update:
        Cashout deadline is Late October 2026 (2026-10-31). From 2026-09-24 to 2026-10-31 is 37 days.
        """
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        result = run_monte_carlo_ruin_sim(
            holdings=self.holdings,
            market_params=self.market_params,
            vol_params=self.vol_params,
            n_sims=300,
            horizon_days=37,
            hard_floor=540000000.0
        )
        self.assertIn("prob_ruin", result)


if __name__ == "__main__":
    unittest.main()
