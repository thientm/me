"""
Tier 1: Feature F8 — Backend Server & REST APIs Tests.
Authoritative source: PROJECT.md §F8 & §Interface Contracts; explorer_dashboard_1/report.md §4.2.
"""

import json
import unittest

try:
    from crypto_dashboard.api_handlers import handle_api_route
    HAS_F8 = True
except ImportError:
    HAS_F8 = False


class TestF8ServerAPIs(unittest.TestCase):
    """Verifies Backend REST API routes and JSON schema response envelopes."""

    def test_f8_01_api_status_endpoint(self):
        """Authoritative Source: PROJECT.md §F8:
        GET /api/status returns valuation snapshot, portfolio weights, and active alert.
        """
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        status_code, body = handle_api_route("GET", "/api/status", None)
        self.assertEqual(status_code, 200)
        self.assertEqual(body.get("status"), "ok")
        self.assertIn("valuation", body.get("data", {}))
        self.assertIn("portfolio", body.get("data", {}))

    def test_f8_02_api_matrix_endpoint(self):
        """Authoritative Source: PROJECT.md §F8:
        GET /api/matrix returns Binary Decision Matrix evaluation (540tr rule) and orders sheet.
        """
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        status_code, body = handle_api_route("GET", "/api/matrix", None)
        self.assertEqual(status_code, 200)
        data = body.get("data", {})
        self.assertEqual(data.get("hard_floor_vnd"), 540000000.0)
        self.assertIn(data.get("active_band"), ["TAKE_PROFIT_540M", "HARD_FLOOR_BREACH"])
        self.assertIn("orders_sheet", data)

    def test_f8_03_api_simulate_endpoint(self):
        """Authoritative Source: PROJECT.md §F8:
        POST /api/simulate accepts shock percentages and returns simulation comparison.
        """
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        payload = {"btc_shock_pct": -15.0, "sol_shock_pct": -15.0, "p2p_rate": 25930.0, "sell_50_pct": True}
        status_code, body = handle_api_route("POST", "/api/simulate", payload)
        self.assertEqual(status_code, 200)
        data = body.get("data", {})
        self.assertIn("simulated_tts_vnd", data)
        self.assertIn("distance_to_floor_vnd", data)

    def test_f8_04_api_macro_endpoint(self):
        """Authoritative Source: PROJECT.md §F8:
        GET /api/macro returns countdown events (Tranche 1, PCE, BĐS 30/09, Late Oct 2026) and debt gap.
        """
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        status_code, body = handle_api_route("GET", "/api/macro", None)
        self.assertEqual(status_code, 200)
        data = body.get("data", {})
        self.assertIn("events", data)
        self.assertIn("bds_financial_gap", data)

    def test_f8_05_api_trend_endpoint(self):
        """Authoritative Source: PROJECT.md §F8:
        GET /api/trend returns MCR-Sim, BHT-Ticker, and AVC-Meter quant calculations.
        """
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        status_code, body = handle_api_route("GET", "/api/trend", None)
        self.assertEqual(status_code, 200)
        data = body.get("data", {})
        self.assertIn("mcr_sim", data)
        self.assertIn("bht_ticker", data)
        self.assertIn("avc_meter", data)


if __name__ == "__main__":
    unittest.main()
