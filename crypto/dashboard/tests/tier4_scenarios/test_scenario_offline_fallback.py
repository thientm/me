"""
Tier 4: Scenario 5 — Network Outage & SSL Fallback to Local Rate Cache.
Authoritative source: PROJECT.md §1 & §F1; explorer_dashboard_1/report.md §1.2.
"""

import unittest
from unittest.mock import patch
import urllib.error
from tests.fixtures import MOCK_CACHE_RATES_PATH

try:
    from crypto_engine.valuation import get_rates, calculate_tts
    HAS_SCENARIO_5 = True
except ImportError:
    HAS_SCENARIO_5 = False


class TestScenarioOfflineFallback(unittest.TestCase):
    """Simulates network disconnection and verifies seamless offline fallback."""

    def test_network_failure_falls_back_to_cache(self):
        """When urllib.request raises URLError / SSLError, get_rates gracefully falls back to local cache."""
        if not HAS_SCENARIO_5:
            self.skipTest("crypto_engine.valuation not implemented yet (Milestone M1)")

        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Network unreachable")):
            rates = get_rates(cache_path=MOCK_CACHE_RATES_PATH, offline_only=False)

        self.assertIsNotNone(rates)
        self.assertIn("BTCUSDT", rates)
        self.assertIn("SOLUSDT", rates)
        self.assertEqual(rates["BTCUSDT"], 84262.0)

        # Compute TTS with cached rates
        snapshot = calculate_tts(
            btc_qty=0.159310, sol_qty=55.28, stables_usd=1415.0,
            btc_price=rates["BTCUSDT"], sol_price=rates["SOLUSDT"],
            p2p_rate=rates["USDT_VND_P2P"], withdrawn_vnd=0.0,
            data_source="cache"
        )
        self.assertEqual(snapshot.data_source, "cache")
        self.assertAlmostEqual(snapshot.tts_vnd, 550643256.0, delta=5000.0)


if __name__ == "__main__":
    unittest.main()
