"""
Tier 1: Feature F3 — Section 7.5 Review & Append-only Logger Tests.
Authoritative source: PROJECT.md §F3; ORIGINAL_REQUEST.md §R1; AGENTS.md rule on logs/*.md.
"""

import os
import tempfile
import unittest

try:
    from crypto_engine.logger import format_section_7_5_review, append_review_log
    HAS_F3 = True
except ImportError:
    HAS_F3 = False


class TestF3Logger(unittest.TestCase):
    """Verifies Section 7.5 Review generation and Append-Only Logger adherence."""

    def test_f3_01_section_7_5_review_format_contains_required_headers(self):
        """Authoritative Source: Section 7.5 in crypto-plan.md:
        Headers required: ### Input, ### Research, ### Quyết định, ### Đối chiếu BĐS, ### Kịch bản & Insight.
        """
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        review_text = format_section_7_5_review(
            tts_vnd=550643256.0,
            withdrawn_vnd=0.0,
            active_band="TAKE_PROFIT_540M",
            action_summary="Bán 50% coin (xả sạch SOL, rút Stables)",
            borrow_needed_vnd=544356744.0,
            date_str="2026-09-24"
        )
        self.assertIn("### Input", review_text)
        self.assertIn("### Research", review_text)
        self.assertIn("### Quyết định", review_text)
        self.assertIn("### Đối chiếu BĐS", review_text)
        self.assertIn("### Kịch bản & Insight", review_text)

    def test_f3_02_append_only_strictly_preserves_existing_content(self):
        """Authoritative Source: /Users/thien.tm/Documents/me/AGENTS.md:
        'logs/*.md: append-only, 1 file/tháng. KHÔNG sửa hoặc xoá entry cũ — chỉ thêm entry mới.'
        """
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        initial_content = "# Log Giao dịch Crypto - Tháng 09/2026\n\n## 2026-09-04: Cập nhật cũ\n- Giữ nguyên."
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md") as temp_file:
            temp_file.write(initial_content)
            temp_path = temp_file.name

        try:
            append_review_log(
                log_path=temp_path,
                review_content="## 2026-09-24: Review mới\n- Bán 50%."
            )
            with open(temp_path, "r", encoding="utf-8") as f:
                new_content = f.read()

            # Must start with initial content (never truncated or overwritten)
            self.assertTrue(new_content.startswith(initial_content))
            self.assertIn("## 2026-09-24: Review mới", new_content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_f3_03_timestamp_and_date_in_review_header(self):
        """Authoritative Source: Section 7.5:
        Entry header must contain clear date (e.g. ## 2026-09-24 or ## Tuần 24/09).
        """
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        review_text = format_section_7_5_review(
            tts_vnd=550643256.0,
            withdrawn_vnd=0.0,
            active_band="TAKE_PROFIT_540M",
            action_summary="Bán 50% coin",
            borrow_needed_vnd=544356744.0,
            date_str="2026-09-24"
        )
        self.assertIn("2026-09-24", review_text)

    def test_f3_04_review_records_540m_band_and_tts(self):
        """Authoritative Source: 2026-09-24 Critical Update:
        Review content must explicitly state TTS (550,6tr) and comparison with 540tr Hard Floor.
        """
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        review_text = format_section_7_5_review(
            tts_vnd=550643256.0,
            withdrawn_vnd=0.0,
            active_band="TAKE_PROFIT_540M",
            action_summary="Bán 50% coin",
            borrow_needed_vnd=544356744.0,
            date_str="2026-09-24"
        )
        self.assertIn("550", review_text)
        self.assertIn("540", review_text)

    def test_f3_05_dry_run_mode_does_not_modify_disk(self):
        """Authoritative Source: PROJECT.md §CLI review --dry-run flag:
        When dry_run=True, no disk write occurs.
        """
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md") as temp_file:
            temp_file.write("Original content")
            temp_path = temp_file.name

        try:
            append_review_log(
                log_path=temp_path,
                review_content="Should not be written",
                dry_run=True
            )
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(content, "Original content")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
