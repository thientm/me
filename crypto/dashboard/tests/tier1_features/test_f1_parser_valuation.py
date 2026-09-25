"""
Tier 1: Feature F1 — Data Parser & Valuation Core Tests.
Authoritative source: PROJECT.md §1 & §Interface Contracts; ORIGINAL_REQUEST.md §R1.
"""

import os
import unittest
from tests.fixtures import MOCK_CRYPTO_PLAN_PATH, MOCK_LOGS_PATH, MOCK_CACHE_RATES_PATH

try:
    from crypto_engine.parser import parse_crypto_plan, parse_logs
    from crypto_engine.valuation import calculate_tts, ValuationSnapshot, get_rates
    HAS_F1 = True
except ImportError:
    HAS_F1 = False


class TestF1ParserValuation(unittest.TestCase):
    """Verifies Data Parser & Valuation Core functionality."""

    def test_f1_01_parse_crypto_plan_holdings(self):
        """Authoritative Source: Section 2 table in mock_crypto_plan.md.
        Expected: BTC=0.159310, SOL=55.28, Stables=1415.0, initial capital=650,000,000.
        """
        if not HAS_F1:
            self.skipTest("crypto_engine.parser not implemented yet (Milestone M1)")

        holdings = parse_crypto_plan(MOCK_CRYPTO_PLAN_PATH)
        self.assertIsInstance(holdings, dict)
        self.assertAlmostEqual(holdings.get("btc_qty", 0.0), 0.159310, places=5)
        self.assertAlmostEqual(holdings.get("sol_qty", 0.0), 55.28, places=2)
        self.assertAlmostEqual(holdings.get("stables_usd", 0.0), 1415.0, places=1)
        self.assertEqual(holdings.get("base_capital_vnd"), 650000000)

    def test_f1_02_parse_logs_cashout_progress(self):
        """Authoritative Source: mock_logs.md transaction entries.
        Expected: cashed out VND = 0, missed recommendations count = 13.
        """
        if not HAS_F1:
            self.skipTest("crypto_engine.parser not implemented yet (Milestone M1)")

        logs_data = parse_logs(MOCK_LOGS_PATH)
        self.assertIsInstance(logs_data, dict)
        self.assertEqual(logs_data.get("withdrawn_vnd", 0), 0)
        self.assertGreaterEqual(logs_data.get("missed_recommendations_count", 0), 13)

    def test_f1_03_tts_calculation_mathematical_oracle(self):
        """Authoritative Source: TTS Formula in PROJECT.md:
        TTS = withdrawn_vnd + (btc*price_btc + sol*price_sol + stables) * p2p_rate
        Inputs: BTC 0.159310 @ $84,262, SOL 55.28 @ $115.72, Stables 1,415.0, P2P 25,930, withdrawn 0.
        Expected: 0 + (13423.77922 + 6396.999999 + 1415.0) * 25930 = 21235.77922 * 25930 = 550,643,755 VND (+-5,000 VND rounding).
        """
        if not HAS_F1:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        snapshot = calculate_tts(
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0,
            btc_price=84262.0,
            sol_price=115.72,
            p2p_rate=25930.0,
            withdrawn_vnd=0.0
        )
        expected_crypto_usd = 0.159310 * 84262.0 + 55.28 * 115.72 + 1415.0
        expected_tts_vnd = expected_crypto_usd * 25930.0
        self.assertAlmostEqual(snapshot.tts_vnd, expected_tts_vnd, delta=1000.0)

    def test_f1_04_valuation_snapshot_contract(self):
        """Authoritative Source: PROJECT.md §Interface Contracts - ValuationSnapshot.
        Must have required fields: btc_qty, sol_qty, stables_usd, btc_price, sol_price,
        p2p_rate, crypto_vnd, withdrawn_vnd, tts_vnd, timestamp, data_source.
        """
        if not HAS_F1:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        snapshot = calculate_tts(
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0,
            btc_price=84262.0,
            sol_price=115.72,
            p2p_rate=25930.0,
            withdrawn_vnd=0.0
        )
        required_fields = [
            "btc_qty", "sol_qty", "stables_usd", "btc_price", "sol_price",
            "p2p_rate", "crypto_vnd", "withdrawn_vnd", "tts_vnd", "timestamp", "data_source"
        ]
        for field in required_fields:
            self.assertTrue(hasattr(snapshot, field), f"ValuationSnapshot missing field {field}")

    def test_f1_05_cached_rates_fallback(self):
        """Authoritative Source: PROJECT.md §1 & §4.
        When offline=True, get_rates must load from mock_cache_rates.json without network calls.
        """
        if not HAS_F1:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        rates = get_rates(cache_path=MOCK_CACHE_RATES_PATH, offline_only=True)
        self.assertIn("BTCUSDT", rates)
        self.assertIn("SOLUSDT", rates)
        self.assertIn("USDT_VND_P2P", rates)
        self.assertEqual(rates["BTCUSDT"], 84262.0)
        self.assertEqual(rates["SOLUSDT"], 115.72)
        self.assertEqual(rates["USDT_VND_P2P"], 25930.0)


if __name__ == "__main__":
    unittest.main()
