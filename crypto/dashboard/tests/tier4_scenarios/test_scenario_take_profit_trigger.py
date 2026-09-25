"""
Tier 4: Scenario 2 — Take Profit Trigger at >= 540M VND.
Authoritative source: 2026-09-24 Critical Update:
'Take-profit band starts exactly at >= 540tr VND. (TTS >= 540tr -> Take Profit 50% triggers)'.
"""

import unittest

try:
    from crypto_engine.matrix import evaluate_binary_matrix
    from crypto_engine.valuation import calculate_tts
    HAS_SCENARIO_2 = True
except ImportError:
    HAS_SCENARIO_2 = False


class TestScenarioTakeProfitTrigger(unittest.TestCase):
    """Simulates the take-profit execution mechanics when TTS crosses the 540tr threshold."""

    def test_take_profit_50_pct_execution_math(self):
        """At TTS = 550,643,256 VND:
        - 50% target to cash out = ~275,321,628 VND.
        - Stables: withdraw 100% of $1,415 = 36,690,950 VND.
        - SOL: sell 100% of 55.28 SOL @ $115.72 * 25,930 = 165,874,131 VND.
        - Remainder to reach 50% = 275,321,628 - (36,690,950 + 165,874,131) = 72,756,547 VND.
        - BTC sold to fulfill remainder = 72,756,547 / (84,262 * 25,930) = ~0.0333 BTC.
        - Total cashed out to bank: ~275M VND.
        - Floor cushion is permanently locked into bank cash.
        """
        if not HAS_SCENARIO_2:
            self.skipTest("crypto_engine modules not yet implemented (Milestone M1)")

        evaluation = evaluate_binary_matrix(
            tts_vnd=550643256.0,
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0
        )
        self.assertEqual(evaluation.active_band, "TAKE_PROFIT_540M")
        self.assertTrue(evaluation.urgent_action_required)

        # Check order sheet amounts
        orders = evaluation.orders_sheet
        sol_order = next((o for o in orders if o["symbol"] == "SOL"), None)
        usdt_order = next((o for o in orders if o["symbol"] == "USDT"), None)
        btc_order = next((o for o in orders if o["symbol"] == "BTC"), None)

        self.assertIsNotNone(sol_order)
        self.assertIsNotNone(usdt_order)
        self.assertIsNotNone(btc_order)

        self.assertEqual(sol_order["qty"], 55.28)
        self.assertEqual(usdt_order["qty"], 1415.0)
        self.assertGreater(btc_order["qty"], 0.0)


if __name__ == "__main__":
    unittest.main()
