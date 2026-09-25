"""
Tier 3: Interaction 2 — Matrix Evaluation -> Section 7.5 Logger Pipeline.
Authoritative source: PROJECT.md §F2 & §F3; AGENTS.md rule on logs/*.md.
"""

import os
import tempfile
import unittest

try:
    from crypto_engine.matrix import evaluate_binary_matrix
    from crypto_engine.logger import format_section_7_5_review, append_review_log
    HAS_MATRIX_LOGGER = True
except ImportError:
    HAS_MATRIX_LOGGER = False


class TestInteractionMatrixLogger(unittest.TestCase):
    """Verifies seamless data flow from Matrix evaluation output directly into Logger append."""

    def test_matrix_evaluation_to_logger_append(self):
        """Matrix evaluation generates active band which directly populates formatted log review."""
        if not HAS_MATRIX_LOGGER:
            self.skipTest("crypto_engine modules not yet implemented (Milestone M1)")

        evaluation = evaluate_binary_matrix(
            tts_vnd=550643256.0,
            btc_qty=0.159310,
            sol_qty=55.28,
            stables_usd=1415.0
        )
        self.assertEqual(evaluation.active_band, "TAKE_PROFIT_540M")

        # Format review using evaluation output
        review_text = format_section_7_5_review(
            tts_vnd=550643256.0,
            withdrawn_vnd=0.0,
            active_band=evaluation.active_band,
            action_summary="Bán 50% coin theo lệnh TAKE_PROFIT_540M",
            borrow_needed_vnd=544356744.0,
            date_str="2026-09-24"
        )
        self.assertIn("TAKE_PROFIT_540M", review_text)

        # Append to temporary log file
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write("# Month Log Baseline\n")
            temp_path = f.name

        try:
            append_review_log(temp_path, review_text)
            with open(temp_path, "r", encoding="utf-8") as f:
                saved = f.read()

            self.assertIn("TAKE_PROFIT_540M", saved)
            self.assertTrue("550.643.256" in saved or "550,643,256" in saved or "550.6tr" in saved)
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
