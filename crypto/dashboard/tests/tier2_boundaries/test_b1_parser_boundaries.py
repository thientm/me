"""
Tier 2: Feature F1 Boundaries — Data Parser & Valuation Corner Cases.
"""

import os
import tempfile
import unittest

try:
    from crypto_engine.parser import parse_crypto_plan, parse_logs
    from crypto_engine.valuation import calculate_tts, get_rates
    HAS_F1 = True
except ImportError:
    HAS_F1 = False


class TestB1ParserBoundaries(unittest.TestCase):
    """Verifies edge cases and boundary conditions for parser and valuation."""

    def test_b1_01_empty_plan_file_raises_or_defaults(self):
        """Empty plan file should raise ValueError or return clean fallback defaults."""
        if not HAS_F1:
            self.skipTest("crypto_engine.parser not implemented yet (Milestone M1)")

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md") as f:
            f.write("")
            path = f.name

        try:
            result = parse_crypto_plan(path)
            self.assertIsInstance(result, dict)
            # When empty, it must flag is_fallback=True or have default quantities
            self.assertTrue(result.get("is_fallback", False) or result.get("btc_qty", 0.0) > 0)
        except (ValueError, KeyError):
            pass
        finally:
            os.remove(path)

    def test_b1_02_zero_coin_balances(self):
        """Zero coin balances should result in TTS = cash_withdrawn."""
        if not HAS_F1:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        snapshot = calculate_tts(
            btc_qty=0.0, sol_qty=0.0, stables_usd=0.0,
            btc_price=84000.0, sol_price=115.0, p2p_rate=25900.0, withdrawn_vnd=50000000.0
        )
        self.assertEqual(snapshot.crypto_vnd, 0.0)
        self.assertEqual(snapshot.tts_vnd, 50000000.0)

    def test_b1_03_malformed_rate_data_handled(self):
        """Malformed rate payload (e.g. non-numeric strings) should raise TypeError or ValueError."""
        if not HAS_F1:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        with self.assertRaises((TypeError, ValueError)):
            calculate_tts(
                btc_qty=0.1, sol_qty=1.0, stables_usd=10.0,
                btc_price="non_numeric_price", sol_price=100.0, p2p_rate=25000.0, withdrawn_vnd=0.0
            )

    def test_b1_04_extreme_p2p_rate_boundary(self):
        """Extreme P2P rate values (e.g. 10k or 50k) compute accurately without overflow."""
        if not HAS_F1:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        snapshot = calculate_tts(
            btc_qty=1.0, sol_qty=0.0, stables_usd=0.0,
            btc_price=100000.0, sol_price=100.0, p2p_rate=50000.0, withdrawn_vnd=0.0
        )
        self.assertEqual(snapshot.tts_vnd, 100000.0 * 50000.0)

    def test_b1_05_corrupted_log_file_handling(self):
        """Log file with no valid entries should report 0 withdrawn."""
        if not HAS_F1:
            self.skipTest("crypto_engine.parser not implemented yet (Milestone M1)")

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md") as f:
            f.write("# Corrupted log without any entries\nRandom junk text here.")
            path = f.name

        try:
            logs = parse_logs(path)
            self.assertEqual(logs.get("withdrawn_vnd", 0.0), 0.0)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
