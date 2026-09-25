"""
Tier 3: Interaction 3 — Quant Engine -> Server REST API Pipeline.
Authoritative source: PROJECT.md §F5, §F6 & §F8.
"""

import unittest

try:
    from crypto_dashboard.api_handlers import handle_api_route
    HAS_QUANT_API = True
except ImportError:
    HAS_QUANT_API = False


class TestInteractionQuantAPIs(unittest.TestCase):
    """Verifies that MCR-Sim, BHT-Ticker, and AVC-Meter data correctly surface via /api/trend."""

    def test_api_trend_integrates_all_quant_innovations(self):
        """GET /api/trend must return combined payload with mcr_sim, bht_ticker, and avc_meter."""
        if not HAS_QUANT_API:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        code, body = handle_api_route("GET", "/api/trend", None)
        self.assertEqual(code, 200)
        self.assertEqual(body.get("status"), "ok")

        data = body.get("data", {})
        # 1. Check MCR-Sim
        self.assertIn("mcr_sim", data)
        self.assertIn("prob_ruin", data["mcr_sim"])

        # 2. Check BHT-Ticker
        self.assertIn("bht_ticker", data)
        self.assertIn("burn_rate_vnd_per_hour", data["bht_ticker"])
        self.assertAlmostEqual(data["bht_ticker"]["burn_rate_vnd_per_hour"], 38750.0, delta=1.0)

        # 3. Check AVC-Meter
        self.assertIn("avc_meter", data)
        self.assertIn("vcr_days", data["avc_meter"])
        self.assertIn("risk_zone", data["avc_meter"])


if __name__ == "__main__":
    unittest.main()
