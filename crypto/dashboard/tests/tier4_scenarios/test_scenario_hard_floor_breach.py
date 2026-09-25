"""
Tier 4: Scenario 3 — Hard Floor Breach (< 540M VND) Emergency Exit.
Authoritative source: 2026-09-24 Critical Update:
'If TTS < 540tr -> Hard Floor triggers. EMERGENCY: Market Sell ALL immediately.'
"""

import unittest

try:
    from crypto_engine.matrix import evaluate_binary_matrix
    from crypto_engine.valuation import calculate_tts
    HAS_SCENARIO_3 = True
except ImportError:
    HAS_SCENARIO_3 = False


class TestScenarioHardFloorBreach(unittest.TestCase):
    """Simulates market crash penetrating 540tr Hard Floor and triggering emergency liquidation."""

    def test_flash_crash_hard_floor_breach_liquidation(self):
        """BTC drops to $72,000, SOL drops to $85, P2P = 25,800.
        TTS = (0.159310 * 72000 + 55.28 * 85 + 1415) * 25800 = 453,670,296 VND.
        TTS < 540,000,000 -> Active band is HARD_FLOOR_BREACH.
        All coins must be sold immediately with market orders.
        """
        if not HAS_SCENARIO_3:
            self.skipTest("crypto_engine modules not yet implemented (Milestone M1)")

        snapshot = calculate_tts(
            btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0,
            btc_price=72000.0, sol_price=85.0, p2p_rate=25800.0, withdrawn_vnd=0.0
        )
        self.assertLess(snapshot.tts_vnd, 540000000.0)

        evaluation = evaluate_binary_matrix(
            tts_vnd=snapshot.tts_vnd,
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0
        )
        self.assertEqual(evaluation.active_band, "HARD_FLOOR_BREACH")
        self.assertTrue(evaluation.urgent_action_required)
        self.assertLess(evaluation.distance_to_floor_vnd, 0)

        # All assets must have 100% sell/withdraw orders
        orders = evaluation.orders_sheet
        btc_order = next((o for o in orders if o["symbol"] == "BTC"), None)
        sol_order = next((o for o in orders if o["symbol"] == "SOL"), None)
        usdt_order = next((o for o in orders if o["symbol"] == "USDT"), None)

        self.assertIsNotNone(btc_order)
        self.assertIsNotNone(sol_order)
        self.assertIsNotNone(usdt_order)

        self.assertEqual(btc_order["qty"], 0.159310)
        self.assertEqual(sol_order["qty"], 55.28)
        self.assertEqual(usdt_order["qty"], 1415.0)


if __name__ == "__main__":
    unittest.main()
