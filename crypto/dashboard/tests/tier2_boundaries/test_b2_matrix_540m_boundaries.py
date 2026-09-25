"""
Tier 2: Feature F2 Boundaries — Binary Decision Matrix 540tr Threshold Corner Cases.
Authoritative source: 2026-09-24 Critical Update:
- Hard Floor: 540,000,000 VND.
- Take Profit starts at >= 540,000,000 VND. Middle bands removed.
"""

import unittest

try:
    from crypto_engine.matrix import evaluate_binary_matrix
    HAS_F2 = True
except ImportError:
    HAS_F2 = False


class TestB2Matrix540mBoundaries(unittest.TestCase):
    """Verifies precision boundaries around 540,000,000 VND threshold."""

    def test_b2_01_exact_540m_boundary_triggers_take_profit(self):
        """Authoritative Source: 'Take-profit band now starts exactly at >= 540tr VND.'
        At exactly 540,000,000.0 VND -> TAKE_PROFIT_540M.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=540000000.0, btc_qty=0.1, sol_qty=10.0, stables_usd=100.0)
        self.assertEqual(evaluation.active_band, "TAKE_PROFIT_540M")
        self.assertEqual(evaluation.distance_to_floor_vnd, 0.0)

    def test_b2_02_one_vnd_below_540m_triggers_hard_floor_breach(self):
        """Authoritative Source: 'If TTS < 540tr -> Hard Floor triggers.'
        At 539,999,999.0 VND -> HARD_FLOOR_BREACH.
        """
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=539999999.0, btc_qty=0.1, sol_qty=10.0, stables_usd=100.0)
        self.assertEqual(evaluation.active_band, "HARD_FLOOR_BREACH")
        self.assertEqual(evaluation.distance_to_floor_vnd, -1.0)
        self.assertTrue(evaluation.urgent_action_required)

    def test_b2_03_one_vnd_above_540m_triggers_take_profit(self):
        """At 540,000,001.0 VND -> TAKE_PROFIT_540M."""
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=540000001.0, btc_qty=0.1, sol_qty=10.0, stables_usd=100.0)
        self.assertEqual(evaluation.active_band, "TAKE_PROFIT_540M")
        self.assertEqual(evaluation.distance_to_floor_vnd, 1.0)

    def test_b2_04_zero_tts_crash_boundary(self):
        """At 0 VND -> HARD_FLOOR_BREACH with distance -540,000,000 VND."""
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=0.0, btc_qty=0.0, sol_qty=0.0, stables_usd=0.0)
        self.assertEqual(evaluation.active_band, "HARD_FLOOR_BREACH")
        self.assertEqual(evaluation.distance_to_floor_vnd, -540000000.0)

    def test_b2_05_extreme_bull_spike_boundary(self):
        """At 1,000,000,000 VND (1 billion) -> TAKE_PROFIT_540M with distance +460,000,000 VND."""
        if not HAS_F2:
            self.skipTest("crypto_engine.matrix not implemented yet (Milestone M1)")

        evaluation = evaluate_binary_matrix(tts_vnd=1000000000.0, btc_qty=0.5, sol_qty=100.0, stables_usd=5000.0)
        self.assertEqual(evaluation.active_band, "TAKE_PROFIT_540M")
        self.assertEqual(evaluation.distance_to_floor_vnd, 460000000.0)


if __name__ == "__main__":
    unittest.main()
