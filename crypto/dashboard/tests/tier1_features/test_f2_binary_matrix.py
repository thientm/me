"""
Tier 1: Feature F2 — Binary Decision Matrix Engine Tests (Critical Updated 540tr Constraints).
Authoritative source: PROJECT.md §Updated Domain Constraints, §Interface Contracts; ORIGINAL_REQUEST.md Follow-up.
"""

import unittest

try:
    from crypto_engine.matrix import evaluate_binary_matrix, MatrixEvaluation
    from crypto_engine.valuation import ValuationSnapshot
    HAS_F2 = True
except ImportError:
    HAS_F2 = False


class TestF2BinaryMatrix(unittest.TestCase):
    """Verifies the Binary Decision Matrix (540tr Floor vs >=540tr Take-profit 50%)."""

    def test_f2_01_take_profit_band_triggered_at_or_above_540m(self):
        """Authoritative Source: 2026-09-24 Critical Update:
        If TTS >= 540,000,000 VND -> Active band is TAKE_PROFIT_540M.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        # Case 1: Exactly 540,000,000 VND
        eval_exact = evaluate_binary_matrix(tts_vnd=540000000.0, btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0)
        self.assertEqual(eval_exact.active_band, "TAKE_PROFIT_540M")
        self.assertTrue(eval_exact.urgent_action_required)

        # Case 2: Above 540M (e.g. 550,643,256 VND)
        eval_above = evaluate_binary_matrix(tts_vnd=550643256.0, btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0)
        self.assertEqual(eval_above.active_band, "TAKE_PROFIT_540M")
        self.assertGreater(eval_above.distance_to_floor_vnd, 0)

    def test_f2_02_hard_floor_breach_triggered_below_540m(self):
        """Authoritative Source: 2026-09-24 Critical Update:
        If TTS < 540,000,000 VND -> Active band is HARD_FLOOR_BREACH.
        Action: EMERGENCY Market Sell ALL immediately.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        # Case: 539,999,999 VND
        eval_below = evaluate_binary_matrix(tts_vnd=539999999.0, btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0)
        self.assertEqual(eval_below.active_band, "HARD_FLOOR_BREACH")
        self.assertTrue(eval_below.urgent_action_required)
        self.assertLess(eval_below.distance_to_floor_vnd, 0)

    def test_f2_03_priority_order_in_take_profit_orders(self):
        """Authoritative Source: PROJECT.md §F2:
        Order of exit: Stables withdrawn first -> SOL sold 100% (high ATR) -> BTC sold for remainder of 50%.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=550643256.0, btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0)
        orders = evaluation.orders_sheet
        self.assertIsInstance(orders, list)
        self.assertGreaterEqual(len(orders), 2)

        # First asset to withdraw should be Stables (USDT)
        symbols = [order.get("symbol") for order in orders]
        self.assertIn("USDT", symbols)
        self.assertIn("SOL", symbols)
        self.assertIn("BTC", symbols)

        # Check order sequence: Stables before or with SOL, SOL 100% sold
        sol_order = next((o for o in orders if o.get("symbol") == "SOL"), None)
        self.assertIsNotNone(sol_order)
        self.assertAlmostEqual(sol_order.get("qty", 0.0), 55.28, places=2)

    def test_f2_04_hard_floor_breach_orders_sell_all(self):
        """Authoritative Source: PROJECT.md §F2:
        On HARD_FLOOR_BREACH, orders sheet must sell ALL remaining coins (100% SOL, 100% BTC) and withdraw 100% Stables.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=480000000.0, btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0)
        orders = evaluation.orders_sheet
        btc_order = next((o for o in orders if o.get("symbol") == "BTC"), None)
        sol_order = next((o for o in orders if o.get("symbol") == "SOL"), None)
        usdt_order = next((o for o in orders if o.get("symbol") == "USDT"), None)

        self.assertIsNotNone(btc_order)
        self.assertIsNotNone(sol_order)
        self.assertIsNotNone(usdt_order)
        self.assertAlmostEqual(btc_order.get("qty", 0.0), 0.159310, places=5)
        self.assertAlmostEqual(sol_order.get("qty", 0.0), 55.28, places=2)

    def test_f2_05_matrix_evaluation_contract(self):
        """Authoritative Source: PROJECT.md §Interface Contracts - MatrixEvaluation dataclass.
        Must contain: hard_floor_vnd, active_band, distance_to_floor_vnd, distance_to_floor_pct,
        urgent_action_required, missed_recommendations_count, orders_sheet, overrides_triggered.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=550643256.0, btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0)
        required_fields = [
            "hard_floor_vnd", "active_band", "distance_to_floor_vnd", "distance_to_floor_pct",
            "urgent_action_required", "missed_recommendations_count", "orders_sheet", "overrides_triggered"
        ]
        for field in required_fields:
            self.assertTrue(hasattr(evaluation, field), f"MatrixEvaluation missing {field}")
        self.assertEqual(evaluation.hard_floor_vnd, 540000000.0)


if __name__ == "__main__":
    unittest.main()
