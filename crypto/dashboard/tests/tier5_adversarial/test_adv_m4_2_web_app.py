"""
Tier 5: Adversarial Stress Testing — M4-2 Web Cockpit Client Logic (app.js).
Author: challenger_m4_2 (teamwork_preview_challenger)
Target: src/crypto_dashboard/web/app.js, src/crypto_dashboard/web/index.html,
        src/crypto_dashboard/api_handlers.py

Empirically tests and stress-tests:
1. Asset Budget: app.js size < 200KB.
2. API Endpoints: Verification of /api/status, /api/matrix, /api/simulate, /api/macro,
   /api/trend, /api/agy/command, /api/agy/execute.
3. Simulation Math & Cross-Verification with Python Backend:
   - Equivalence test between app.js calculateLocalSimulation() and api_handlers.py run_simulation().
   - Stables double-counting detection (+36.65M VND discrepancy).
   - False safety window probe (TTS < 540M but client reports is_floor_breached = false).
   - Extreme price shock (100% crash: $0 BTC/SOL).
   - Negative shock beyond -100% clamping behavior.
4. Timer Countdown Boundary Conditions:
   - Expired countdown (remaining_seconds <= 0) displays "ĐÃ ĐẾN HẠN".
   - Non-numeric / undefined input NaN vulnerability probe.
5. Real Estate Debt Ceiling & Zero-Fallback Boundary:
   - Over-ceiling borrow needed (>615M VND) triggers negative cushion and danger styling.
   - Zero borrow needed (self-equity >= 3.1B) falsy || fallback probe.
6. Offline Fallback Oracle:
   - Data structure parity between OfflineOracle and live REST API endpoints.
7. DOM ID Integrity:
   - Verification that all getElementById targets in app.js exist in index.html.
"""

import os
import sys
import json
import subprocess
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from crypto_engine.config import (
    HARD_FLOOR_VND,
    FALLBACK_BTC_PRICE,
    FALLBACK_SOL_PRICE,
    FALLBACK_P2P_RATE,
    FALLBACK_BTC_QTY,
    FALLBACK_SOL_QTY,
    FALLBACK_STABLES_USD,
)
from crypto_dashboard.api_handlers import run_simulation, KNOWN_ROUTES

WEB_DIR = os.path.join(SRC_DIR, "crypto_dashboard", "web")
APP_JS = os.path.join(WEB_DIR, "app.js")
INDEX_HTML = os.path.join(WEB_DIR, "index.html")


def run_node_eval(js_code: str) -> dict:
    """Executes JavaScript code inside a Node.js VM with headless DOM and app.js loaded."""
    wrapper = f"""
const fs = require('fs');
const vm = require('vm');

const domElements = {{}};
const mockDoc = {{
  getElementById: (id) => {{
    if (!domElements[id]) {{
      domElements[id] = {{
        textContent: '',
        innerHTML: '',
        className: '',
        style: {{}},
        setAttribute: () => {{}},
        addEventListener: () => {{}},
        querySelector: () => ({{ innerHTML: '' }})
      }};
    }}
    return domElements[id];
  }},
  addEventListener: () => {{}},
  createElement: () => ({{ textContent: '', innerHTML: '', style: {{}}, appendChild: () => {{}}, remove: () => {{}} }}),
  body: {{ appendChild: () => {{}}, removeChild: () => {{}} }},
  hidden: false
}};

const sandbox = {{
  document: mockDoc,
  window: {{}},
  navigator: {{}},
  setInterval: () => {{}},
  setTimeout: () => {{}},
  fetch: () => Promise.resolve({{ ok: true, json: () => Promise.resolve({{}}) }}),
  console: {{ log: () => {{}}, error: () => {{}} }}
}};

const appJsCode = fs.readFileSync('{APP_JS}', 'utf-8');
vm.createContext(sandbox);
vm.runInContext(appJsCode, sandbox);

const output = vm.runInContext(`
  (() => {{
    {js_code}
  }})()
`, sandbox);

process.stdout.write(JSON.stringify(output !== undefined ? output : null));
"""
    result = subprocess.run(
        ["node", "-e", wrapper],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    if result.returncode != 0:
        raise RuntimeError(f"Node execution failed with exit code {result.returncode}:\n{result.stderr}")
    return json.loads(result.stdout)


class TestAdversarialWebApp(unittest.TestCase):
    """Adversarial stress test suite for Web Cockpit client logic (app.js)."""

    # -------------------------------------------------------------------------
    # 1. ASSET BUDGET & STRUCTURE
    # -------------------------------------------------------------------------
    def test_adv_01_app_js_asset_budget(self):
        """app.js must be within the strict 200KB asset budget for zero-dependency SPA."""
        self.assertTrue(os.path.exists(APP_JS), "app.js does not exist")
        file_size = os.path.getsize(APP_JS)
        self.assertLess(file_size, 200 * 1024, f"app.js size {file_size}B exceeds 200KB budget")
        # Ensure substantial logic exists
        self.assertGreater(file_size, 10 * 1024, f"app.js size {file_size}B is too small")

    # -------------------------------------------------------------------------
    # 2. API ENDPOINTS AUDIT
    # -------------------------------------------------------------------------
    def test_adv_02_api_endpoints_coverage_in_app_js(self):
        """
        Verify all required REST API endpoints are referenced in app.js:
        /api/status, /api/matrix, /api/simulate, /api/macro, /api/trend, /api/agy/command, /api/agy/execute.
        """
        with open(APP_JS, "r", encoding="utf-8") as f:
            content = f.read()

        required_endpoints = [
            "/api/status",
            "/api/matrix",
            "/api/simulate",
            "/api/macro",
            "/api/trend",
            "/api/agy/command",
            "/api/agy/execute",
        ]
        for ep in required_endpoints:
            self.assertIn(ep, content, f"Required API endpoint '{ep}' not found in app.js")

    # -------------------------------------------------------------------------
    # 3. MATHEMATICAL EQUIVALENCE & STABLES DOUBLE-COUNTING STRESS
    # -------------------------------------------------------------------------
    def test_adv_03_zero_shock_simulation_discrepancy(self):
        """
        Empirically verifies the mathematical discrepancy between app.js calculateLocalSimulation()
        and api_handlers.py run_simulation() at 0% price shock.
        Remediated: Discrepancy is 0.0 VND (exact parity, delta <= 1.0 VND).
        """
        # 1. Server-side run_simulation at baseline
        py_res = run_simulation(
            btc_price=FALLBACK_BTC_PRICE,
            sol_price=FALLBACK_SOL_PRICE,
            p2p_rate=FALLBACK_P2P_RATE,
            btc_qty=FALLBACK_BTC_QTY,
            sol_qty=FALLBACK_SOL_QTY,
            stables_usd=FALLBACK_STABLES_USD,
            hard_floor_vnd=HARD_FLOOR_VND,
            withdrawn_vnd=0.0
        )
        py_sim_tts = py_res["simulated_tts_vnd"]  # ~550,643,796.66 VND

        # 2. Client-side calculateLocalSimulation at 0 shock
        js_code = """
        State.simInputs.btcShockPct = 0;
        State.simInputs.solShockPct = 0;
        State.simInputs.p2pRate = 25930;
        calculateLocalSimulation();
        return State.simResult;
        """
        js_res = run_node_eval(js_code)
        js_sim_tts = js_res["simulated_tts_vnd"]  # ~550,643,796.66 VND

        discrepancy = js_sim_tts - py_sim_tts
        # Remediated: Stables double-counting eliminated; exact mathematical parity verified
        self.assertAlmostEqual(discrepancy, 0.0, delta=1.0,
            msg=f"Discrepancy {discrepancy} differs from expected 0.0 VND parity")

    def test_adv_04_false_safety_window_probe(self):
        """
        Adversarial Scenario: A -6% market drop pushes true TTS below the 540M Hard Floor (519.8M VND),
        requiring emergency liquidation.
        Remediated: app.js correctly detects the breach (is_floor_breached = True, tts < 540M).
        """
        # True valuation at -6% shock
        shock_pct = -6.0
        btc_shocked = FALLBACK_BTC_PRICE * (1.0 + shock_pct / 100.0)
        sol_shocked = FALLBACK_SOL_PRICE * (1.0 + shock_pct / 100.0)

        py_res = run_simulation(
            btc_price=btc_shocked,
            sol_price=sol_shocked,
            p2p_rate=FALLBACK_P2P_RATE,
            btc_qty=FALLBACK_BTC_QTY,
            sol_qty=FALLBACK_SOL_QTY,
            stables_usd=FALLBACK_STABLES_USD,
            hard_floor_vnd=HARD_FLOOR_VND,
            withdrawn_vnd=0.0
        )
        # Python correctly identifies breach (< 540M)
        self.assertTrue(py_res["is_floor_breached"], "Python server correctly flags breach at -6%")
        self.assertLess(py_res["simulated_tts_vnd"], 540000000.0)

        # In app.js:
        js_code = f"""
        State.simInputs.btcShockPct = {shock_pct};
        State.simInputs.solShockPct = {shock_pct};
        State.simInputs.p2pRate = 25930;
        calculateLocalSimulation();
        return State.simResult;
        """
        js_res = run_node_eval(js_code)

        # REMEDIATED: app.js correctly reports floor IS breached
        self.assertTrue(js_res["is_floor_breached"], "app.js correctly flags floor breached at -6%")
        self.assertLess(js_res["simulated_tts_vnd"], 540000000.0)

    def test_adv_05_total_market_crash_100_pct(self):
        """When market crashes 100% (-100% BTC and SOL), simulation must survive without NaN."""
        js_code = """
        State.simInputs.btcShockPct = -100;
        State.simInputs.solShockPct = -100;
        State.simInputs.p2pRate = 25930;
        calculateLocalSimulation();
        return State.simResult;
        """
        js_res = run_node_eval(js_code)
        self.assertTrue(js_res["is_floor_breached"])
        self.assertTrue(js_res["scenario_a"]["is_breached"])
        self.assertTrue(js_res["scenario_b"]["is_breached"])
        self.assertFalse(any(isinstance(v, str) and "NaN" in v for v in [
            str(js_res["simulated_tts_vnd"]),
            str(js_res["distance_to_floor_vnd"])
        ]))

    def test_adv_06_negative_shock_beyond_100_percent(self):
        """
        Adversarial input: shock of -150% (spot price clamped to >= 0).
        Examines whether app.js clamps simBtcPrice to >= 0.
        """
        js_code = """
        State.simInputs.btcShockPct = -150;
        State.simInputs.solShockPct = -150;
        State.simInputs.p2pRate = 25930;
        calculateLocalSimulation();
        return {
          btcPrice: State.simInputs.btcPrice,
          solPrice: State.simInputs.solPrice,
          simulated_tts_vnd: State.simResult.simulated_tts_vnd
        };
        """
        js_res = run_node_eval(js_code)
        # REMEDIATED: app.js clamps simBtcPrice and simSolPrice to >= 0
        self.assertGreaterEqual(js_res["btcPrice"], 0.0, "BTC price clamped to >= 0")
        self.assertGreaterEqual(js_res["solPrice"], 0.0, "SOL price clamped to >= 0")
        self.assertGreaterEqual(js_res["simulated_tts_vnd"], 0.0)

    # -------------------------------------------------------------------------
    # 4. TIMER COUNTDOWN BOUNDARY CONDITIONS
    # -------------------------------------------------------------------------
    def test_adv_07_countdown_timer_boundary_zero_and_negative(self):
        """Timer countdown <= 0 must format to 'ĐÃ ĐẾN HẠN'."""
        js_code = """
        return {
          neg100: formatDuration(-100),
          neg1: formatDuration(-1),
          zero: formatDuration(0),
          halfSec: formatDuration(0.4),
          pos10: formatDuration(10),
          pos3600: formatDuration(3600),
          pos90000: formatDuration(90000)
        };
        """
        js_res = run_node_eval(js_code)
        self.assertEqual(js_res["neg100"], "ĐÃ ĐẾN HẠN")
        self.assertEqual(js_res["neg1"], "ĐÃ ĐẾN HẠN")
        self.assertEqual(js_res["zero"], "ĐÃ ĐẾN HẠN")
        self.assertEqual(js_res["pos10"], "00h 00m 10s")
        self.assertEqual(js_res["pos3600"], "01h 00m 00s")
        self.assertEqual(js_res["pos90000"], "1d 01h 00m")

    def test_adv_08_countdown_timer_nan_vulnerability(self):
        """
        formatDuration checks nullish and isNaN, returning 'ĐÃ ĐẾN HẠN' when passed undefined, NaN, or invalid input.
        """
        js_code = """
        return {
          undef: formatDuration(undefined),
          nanVal: formatDuration(NaN),
          strVal: formatDuration("invalid_string")
        };
        """
        js_res = run_node_eval(js_code)
        # REMEDIATED: formatDuration safely guards against undefined, NaN, and invalid strings
        self.assertEqual(js_res["undef"], "ĐÃ ĐẾN HẠN")
        self.assertEqual(js_res["nanVal"], "ĐÃ ĐẾN HẠN")
        self.assertEqual(js_res["strVal"], "ĐÃ ĐẾN HẠN")

    # -------------------------------------------------------------------------
    # 5. REAL ESTATE DEBT CEILING & BORROW GAUGE BOUNDARIES
    # -------------------------------------------------------------------------
    def test_adv_09_bds_debt_ceiling_cushion_breach(self):
        """When borrow needed exceeds 615M ceiling, badge gets 'badge-danger' and negative cushion."""
        js_code = """
        State.bdsGap = {
          total_budget_vnd: 3100000000,
          total_self_equity_vnd: 2400000000,
          borrow_needed_vnd: 700000000,
          borrow_ceiling_vnd: 615000000,
          cushion_vnd: -85000000,
          is_within_ceiling: false
        };
        renderBdsDebtGauge();
        const badge = document.getElementById("bds-status-badge");
        const bar = document.getElementById("bds-ceiling-bar");
        return {
          badgeClass: badge.className,
          badgeText: badge.textContent,
          barClass: bar.className,
          barWidth: bar.style.width
        };
        """
        js_res = run_node_eval(js_code)
        self.assertEqual(js_res["badgeClass"], "badge badge-danger")
        self.assertIn("VƯỢT TRẦN NỢ", js_res["badgeText"])
        self.assertEqual(js_res["barClass"], "progress-fill bg-danger")
        self.assertEqual(js_res["barWidth"], "100%")

    def test_adv_10_bds_borrow_zero_falsy_fallback_probe(self):
        """
        Line 559: 'const borrowNeeded = (gap && gap.borrow_needed_vnd != null) ? gap.borrow_needed_vnd : 544356744;'
        When borrow_needed_vnd is 0 (full equity), 0 is preserved and does not fall back to 544.4M.
        """
        js_code = """
        State.bdsGap = {
          total_budget_vnd: 3100000000,
          total_self_equity_vnd: 3100000000,
          borrow_needed_vnd: 0,
          borrow_ceiling_vnd: 615000000,
          cushion_vnd: 615000000,
          is_within_ceiling: true
        };
        renderBdsDebtGauge();
        const badge = document.getElementById("bds-status-badge");
        return {
          badgeText: badge.textContent
        };
        """
        js_res = run_node_eval(js_code)
        # REMEDIATED: 0 borrow needed preserves full 615tr cushion
        has_full_cushion = "615,0tr" in js_res["badgeText"] or "615tr" in js_res["badgeText"]
        self.assertTrue(has_full_cushion, f"Expected 615tr cushion in badgeText, got: {js_res['badgeText']}")
        self.assertNotIn("70,6tr", js_res["badgeText"])

    # -------------------------------------------------------------------------
    # 6. OFFLINE ORACLE INTEGRITY
    # -------------------------------------------------------------------------
    def test_adv_11_offline_oracle_schema_parity(self):
        """OfflineOracle must have all required keys to ensure crash-free offline start."""
        js_code = """
        return {
          hasStatus: Boolean(OfflineOracle.status),
          hasValuation: Boolean(OfflineOracle.status.valuation),
          hasPortfolio: Boolean(OfflineOracle.status.portfolio && OfflineOracle.status.portfolio.length === 3),
          hasMarketRates: Boolean(OfflineOracle.status.market_rates),
          hasDisciplineGate: Boolean(OfflineOracle.status.discipline_gate),
          hasMatrix: Boolean(OfflineOracle.matrix && OfflineOracle.matrix.orders_sheet),
          hasMacro: Boolean(OfflineOracle.macro && OfflineOracle.macro.events && OfflineOracle.macro.bds_financial_gap),
          hasTrend: Boolean(OfflineOracle.trend && OfflineOracle.trend.mcr_sim && OfflineOracle.trend.bht_ticker && OfflineOracle.trend.avc_meter)
        };
        """
        js_res = run_node_eval(js_code)
        for k, v in js_res.items():
            self.assertTrue(v, f"OfflineOracle missing schema key: {k}")

    # -------------------------------------------------------------------------
    # 7. DOM ID ALIGNMENT
    # -------------------------------------------------------------------------
    def test_adv_12_all_get_element_by_id_exist_in_html(self):
        """Every single document.getElementById(id) referenced in app.js must exist in index.html."""
        import re
        with open(APP_JS, "r", encoding="utf-8") as f:
            app_code = f.read()
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html_code = f.read()

        id_matches = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', app_code))
        self.assertGreater(len(id_matches), 50, "Should have found >50 getElementById calls")

        missing_ids = []
        for dom_id in id_matches:
            if f'id="{dom_id}"' not in html_code and f"id='{dom_id}'" not in html_code:
                missing_ids.append(dom_id)

        self.assertEqual(len(missing_ids), 0, f"Missing DOM IDs in index.html: {missing_ids}")


if __name__ == "__main__":
    unittest.main()
