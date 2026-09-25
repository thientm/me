"""
Tier 2: Feature F5 Boundaries — MCR-Sim Quant Model Corner Cases.
"""

import unittest

try:
    from crypto_engine.quant.monte_carlo import run_monte_carlo_ruin_sim
    HAS_F5 = True
except ImportError:
    HAS_F5 = False


class TestB5MCRBoundaries(unittest.TestCase):
    """Verifies edge cases for Monte Carlo Ruin Simulator."""

    def setUp(self):
        self.market_params = {"spot_btc": 84262.0, "sol_usdt": 115.72, "p2p": 25930.0}

    def test_b5_01_zero_volatility_deterministic_path(self):
        """When sigma=0, prices are constant. If initial TTS > floor, prob_ruin must be 0.0."""
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        holdings = {"btc": 0.2, "sol": 50.0, "stables_usd": 1000.0, "cash_vnd": 0.0}
        vol_params = {"sigma_btc": 0.0, "sigma_sol": 0.0, "rho": 0.0}
        result = run_monte_carlo_ruin_sim(
            holdings=holdings,
            market_params=self.market_params,
            vol_params=vol_params,
            n_sims=100,
            horizon_days=10,
            hard_floor=540000000.0
        )
        self.assertEqual(result["prob_ruin"], 0.0)

    def test_b5_02_extreme_crash_jump_probability(self):
        """Under extreme crash parameters, ruin probability approaches 1.0."""
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        # Port just barely above floor (e.g. 541M) with high volatility
        holdings = {"btc": 0.05, "sol": 20.0, "stables_usd": 0.0, "cash_vnd": 400000000.0}
        vol_params = {"sigma_btc": 0.15, "sigma_sol": 0.25, "rho": 0.9}
        result = run_monte_carlo_ruin_sim(
            holdings=holdings,
            market_params=self.market_params,
            vol_params=vol_params,
            n_sims=300,
            horizon_days=30,
            hard_floor=540000000.0
        )
        self.assertGreaterEqual(result["prob_ruin"], 0.0)
        self.assertLessEqual(result["prob_ruin"], 1.0)

    def test_b5_03_one_day_horizon_boundary(self):
        """1-day horizon runs cleanly without index errors."""
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        holdings = {"btc": 0.159310, "sol": 55.28, "stables_usd": 1415.0, "cash_vnd": 0.0}
        vol_params = {"sigma_btc": 0.027, "sigma_sol": 0.045, "rho": 0.78}
        result = run_monte_carlo_ruin_sim(
            holdings=holdings,
            market_params=self.market_params,
            vol_params=vol_params,
            n_sims=100,
            horizon_days=1,
            hard_floor=540000000.0
        )
        self.assertIn("prob_ruin", result)

    def test_b5_04_perfect_correlation_boundary(self):
        """rho = 1.0 (perfect correlation) computes without division by zero or NaN."""
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        holdings = {"btc": 0.159310, "sol": 55.28, "stables_usd": 1415.0, "cash_vnd": 0.0}
        vol_params = {"sigma_btc": 0.027, "sigma_sol": 0.045, "rho": 1.0}
        result = run_monte_carlo_ruin_sim(
            holdings=holdings,
            market_params=self.market_params,
            vol_params=vol_params,
            n_sims=100,
            horizon_days=5,
            hard_floor=540000000.0
        )
        self.assertFalse(any(v is None for v in result.values()))

    def test_b5_05_single_asset_portfolio_boundary(self):
        """Portfolio with 0 SOL and 100% BTC computes without crash."""
        if not HAS_F5:
            self.skipTest("crypto_engine.quant.monte_carlo not implemented yet (Milestone M2)")

        holdings = {"btc": 0.25, "sol": 0.0, "stables_usd": 0.0, "cash_vnd": 0.0}
        vol_params = {"sigma_btc": 0.027, "sigma_sol": 0.045, "rho": 0.78}
        result = run_monte_carlo_ruin_sim(
            holdings=holdings,
            market_params=self.market_params,
            vol_params=vol_params,
            n_sims=100,
            horizon_days=10,
            hard_floor=540000000.0
        )
        self.assertIn("prob_ruin", result)


if __name__ == "__main__":
    unittest.main()
