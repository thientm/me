"""
Tier 4: Scenario 1 — End-to-End Daily User Review Session.
Authoritative source: ORIGINAL_REQUEST.md §R1, §R2, §R3; PROJECT.md §1 & §Interface Contracts.
"""

import os
import tempfile
import unittest
from tests.fixtures import MOCK_CRYPTO_PLAN_PATH, MOCK_CACHE_RATES_PATH

try:
    from crypto_engine.parser import parse_crypto_plan
    from crypto_engine.valuation import calculate_tts, get_rates
    from crypto_engine.matrix import evaluate_binary_matrix
    from crypto_engine.logger import format_section_7_5_review, append_review_log
    from crypto_dashboard.agy_bridge import generate_agy_command
    HAS_SCENARIO_1 = True
except ImportError:
    HAS_SCENARIO_1 = False


class TestScenarioFullReviewFlow(unittest.TestCase):
    """Simulates a complete real-world user review workflow from start to finish."""

    def test_complete_user_review_session(self):
        """Workflow:
        1. User launches review session.
        2. System reads plan and measured holdings.
        3. Realtime or cached rates are obtained.
        4. Total net worth (TTS) is calculated.
        5. Binary decision matrix evaluated against 540tr rule.
        6. 10-minute Binance order sheet generated.
        7. Review block formatted and appended to logs.
        8. Tokenless agy shell command generated for local agent analysis.
        """
        if not HAS_SCENARIO_1:
            self.skipTest("Engine and dashboard modules not yet implemented (Milestones M1-M3)")

        # 1 & 2: Parse holdings
        holdings = parse_crypto_plan(MOCK_CRYPTO_PLAN_PATH)
        btc_qty = holdings["btc_qty"]
        sol_qty = holdings["sol_qty"]
        stables_usd = holdings["stables_usd"]

        # 3: Get rates
        rates = get_rates(cache_path=MOCK_CACHE_RATES_PATH, offline_only=True)
        btc_price = rates["BTCUSDT"]
        sol_price = rates["SOLUSDT"]
        p2p_rate = rates["USDT_VND_P2P"]

        # 4: Valuation
        snapshot = calculate_tts(
            btc_qty=btc_qty, sol_qty=sol_qty, stables_usd=stables_usd,
            btc_price=btc_price, sol_price=sol_price, p2p_rate=p2p_rate, withdrawn_vnd=0.0
        )
        self.assertAlmostEqual(snapshot.tts_vnd, 550643256.0, delta=5000.0)

        # 5: Binary Decision Matrix (540tr threshold)
        matrix = evaluate_binary_matrix(
            tts_vnd=snapshot.tts_vnd, btc_qty=btc_qty, sol_qty=sol_qty, stables_usd=stables_usd
        )
        self.assertEqual(matrix.active_band, "TAKE_PROFIT_540M")
        self.assertTrue(matrix.urgent_action_required)

        # 6: Order sheet
        orders = matrix.orders_sheet
        self.assertGreaterEqual(len(orders), 2)
        symbols = [o["symbol"] for o in orders]
        self.assertIn("SOL", symbols)
        self.assertIn("USDT", symbols)

        # 7: Format & Append review
        review = format_section_7_5_review(
            tts_vnd=snapshot.tts_vnd,
            withdrawn_vnd=0.0,
            active_band=matrix.active_band,
            action_summary="Bán 50% coin (xả sạch SOL, rút Stables)",
            borrow_needed_vnd=544356744.0,
            date_str="2026-09-24"
        )
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write("# Month Log\n")
            log_path = f.name

        try:
            append_review_log(log_path, review)
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("TAKE_PROFIT_540M", content)
            self.assertIn("### Đối chiếu BĐS", content)
        finally:
            os.remove(log_path)

        # 8: agy Command
        agy_cmd = generate_agy_command(action="review")
        self.assertIn("agy", agy_cmd[0])
        self.assertIn("--dangerously-skip-permissions", agy_cmd)


if __name__ == "__main__":
    unittest.main()
