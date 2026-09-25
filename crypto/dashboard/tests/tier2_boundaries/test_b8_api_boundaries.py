"""
Tier 2: Feature F8 Boundaries — REST API Route Corner Cases.
"""

import unittest

try:
    from crypto_dashboard.api_handlers import handle_api_route
    HAS_F8 = True
except ImportError:
    HAS_F8 = False


class TestB8APIBoundaries(unittest.TestCase):
    """Verifies edge cases for REST API router and error codes."""

    def test_b8_01_unknown_route_returns_404(self):
        """Request to nonexistent endpoint returns HTTP 404."""
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        code, body = handle_api_route("GET", "/api/nonexistent", None)
        self.assertEqual(code, 404)
        self.assertEqual(body.get("status"), "error")

    def test_b8_02_unsupported_method_returns_405(self):
        """Sending DELETE or PUT to GET-only endpoint returns 405 Method Not Allowed."""
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        code, body = handle_api_route("DELETE", "/api/status", None)
        self.assertEqual(code, 405)

    def test_b8_03_malformed_json_body_returns_400(self):
        """Invalid body payload in POST /api/simulate returns 400 Bad Request."""
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        code, body = handle_api_route("POST", "/api/simulate", "not-a-dict")
        self.assertEqual(code, 400)

    def test_b8_04_missing_required_fields_in_simulate_post(self):
        """POST /api/simulate with missing required fields returns 400."""
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        code, body = handle_api_route("POST", "/api/simulate", {})
        self.assertIn(code, [400, 422])

    def test_b8_05_extreme_simulation_shocks_bounds(self):
        """Simulation handles 100% loss without crashing or returning negative balances."""
        if not HAS_F8:
            self.skipTest("crypto_dashboard.api_handlers not implemented yet (Milestone M3)")

        payload = {"btc_shock_pct": -100.0, "sol_shock_pct": -100.0, "p2p_rate": 25930.0, "sell_50_pct": False}
        code, body = handle_api_route("POST", "/api/simulate", payload)
        self.assertEqual(code, 200)
        data = body.get("data", {})
        self.assertGreaterEqual(data.get("simulated_tts_vnd", 0.0), 0.0)


if __name__ == "__main__":
    unittest.main()
