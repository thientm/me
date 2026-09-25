"""
Tier 4: Scenario 4 — 30-Day Simulated Glidepath Progression.
Authoritative source: crypto-plan.md §5 & §7.3; PROJECT.md §F2; 2026-09-24 Critical Update (Late Oct 2026).
"""

import unittest

try:
    from crypto_engine.valuation import calculate_tts
    from crypto_engine.matrix import evaluate_binary_matrix
    from crypto_engine.quant.volatility_cushion import calculate_volatility_cushion
    HAS_SCENARIO_4 = True
except ImportError:
    HAS_SCENARIO_4 = False


class TestScenario30DayGlidepath(unittest.TestCase):
    """Simulates the 30-day progression of the glidepath towards the Late October 2026 deadline."""

    def test_glidepath_stepwise_execution(self):
        """Simulates 4 sequential stages:
        Stage 0 (Day 0, 24/09): Take Profit 50% executed -> Sol sold 100%, Stables withdrawn, 0.04155 BTC sold.
        Stage 1 (Day 1, 24/09): Tranche 1 (15% = 0.035327 BTC sold).
        Stage 2 (Day 6, 29/09): Tranche 2 (20% = 0.047102 BTC sold).
        Stage 3 (Day 14, 07/10): Tranche 3 (15% = 0.035327 BTC sold -> 100% Cashed out before 31/10).
        """
        if not HAS_SCENARIO_4:
            self.skipTest("crypto_engine modules not yet implemented (Milestones M1-M2)")

        # Stage 0: Initial full holdings
        q_btc = 0.159310
        q_sol = 55.28
        q_stables = 1415.0
        cash_vnd = 0.0

        p_btc = 84262.0
        p_sol = 115.72
        p2p = 25930.0

        # Step 0: Take Profit 50% (SOL sold, Stables withdrawn, 0.04155 BTC sold)
        cash_vnd += (55.28 * p_sol + 1415.0 + 0.04155 * p_btc) * p2p
        q_sol = 0.0
        q_stables = 0.0
        q_btc -= 0.04155
        self.assertAlmostEqual(q_btc, 0.11776, places=5)
        self.assertGreater(cash_vnd, 280000000.0)

        # Step 1: Tranche 1 (0.035327 BTC)
        cash_vnd += 0.035327 * p_btc * p2p
        q_btc -= 0.035327
        self.assertAlmostEqual(q_btc, 0.082433, places=5)

        # Step 2: Tranche 2 (0.047102 BTC)
        cash_vnd += 0.047102 * p_btc * p2p
        q_btc -= 0.047102
        self.assertAlmostEqual(q_btc, 0.035331, places=4)

        # Step 3: Tranche 3 (Final remaining 0.035331 BTC)
        cash_vnd += q_btc * p_btc * p2p
        q_btc = 0.0

        # Now 100% in cash
        final_snapshot = calculate_tts(
            btc_qty=q_btc, sol_qty=0.0, stables_usd=0.0,
            btc_price=p_btc, sol_price=p_sol, p2p_rate=p2p, withdrawn_vnd=cash_vnd
        )
        self.assertEqual(final_snapshot.crypto_vnd, 0.0)
        self.assertAlmostEqual(final_snapshot.tts_vnd, cash_vnd, delta=100.0)
        self.assertGreater(final_snapshot.tts_vnd, 540000000.0)


if __name__ == "__main__":
    unittest.main()
