"""
Tier 3: Interaction 1 — Parser -> Valuation -> Binary Matrix Pipeline.
Authoritative source: PROJECT.md §1 & §Interface Contracts.
"""

import unittest
from tests.fixtures import MOCK_CRYPTO_PLAN_PATH, MOCK_LOGS_PATH, MOCK_CACHE_RATES_PATH

try:
    from crypto_engine.parser import parse_crypto_plan, parse_logs
    from crypto_engine.valuation import calculate_tts, get_rates
    from crypto_engine.matrix import evaluate_binary_matrix
    HAS_PIPELINE = True
except ImportError:
    HAS_PIPELINE = False


class TestInteractionParserValuationMatrix(unittest.TestCase):
    """Verifies end-to-end data pipeline from file parsing to matrix evaluation."""

    def test_pipeline_parse_to_valuation_to_matrix(self):
        """1. Parse mock_crypto_plan.md -> 2. Fetch cached rates -> 3. Calculate TTS -> 4. Evaluate Matrix."""
        if not HAS_PIPELINE:
            self.skipTest("crypto_engine modules not yet implemented (Milestone M1)")

        # Step 1: Parse
        holdings = parse_crypto_plan(MOCK_CRYPTO_PLAN_PATH)
        self.assertAlmostEqual(holdings["btc_qty"], 0.159310, places=5)
        self.assertAlmostEqual(holdings["sol_qty"], 55.28, places=2)

        # Step 2: Rates
        rates = get_rates(cache_path=MOCK_CACHE_RATES_PATH, offline_only=True)
        btc_price = rates["BTCUSDT"]
        sol_price = rates["SOLUSDT"]
        p2p_rate = rates["USDT_VND_P2P"]

        # Step 3: Valuation
        snapshot = calculate_tts(
            btc_qty=holdings["btc_qty"],
            sol_qty=holdings["sol_qty"],
            stables_usd=holdings["stables_usd"],
            btc_price=btc_price,
            sol_price=sol_price,
            p2p_rate=p2p_rate,
            withdrawn_vnd=0.0
        )
        self.assertGreater(snapshot.tts_vnd, 540000000.0)

        # Step 4: Binary Decision Matrix
        evaluation = evaluate_binary_matrix(
            tts_vnd=snapshot.tts_vnd,
            btc_qty=snapshot.btc_qty,
            sol_qty=snapshot.sol_qty,
            stables_usd=snapshot.stables_usd
        )
        self.assertEqual(evaluation.active_band, "TAKE_PROFIT_540M")
        self.assertTrue(evaluation.urgent_action_required)
        self.assertGreaterEqual(len(evaluation.orders_sheet), 2)

    def test_pipeline_with_low_rates_triggers_hard_floor(self):
        """Simulates low market rates flowing through pipeline into HARD_FLOOR_BREACH."""
        if not HAS_PIPELINE:
            self.skipTest("crypto_engine modules not yet implemented (Milestone M1)")

        holdings = parse_crypto_plan(MOCK_CRYPTO_PLAN_PATH)
        # Artificially low price
        snapshot = calculate_tts(
            btc_qty=holdings["btc_qty"],
            sol_qty=holdings["sol_qty"],
            stables_usd=holdings["stables_usd"],
            btc_price=70000.0,
            sol_price=90.0,
            p2p_rate=25000.0,
            withdrawn_vnd=0.0
        )
        self.assertLess(snapshot.tts_vnd, 540000000.0)

        evaluation = evaluate_binary_matrix(
            tts_vnd=snapshot.tts_vnd,
            btc_qty=snapshot.btc_qty,
            sol_qty=snapshot.sol_qty,
            stables_usd=snapshot.stables_usd
        )
        self.assertEqual(evaluation.active_band, "HARD_FLOOR_BREACH")
        self.assertTrue(evaluation.urgent_action_required)


if __name__ == "__main__":
    unittest.main()
