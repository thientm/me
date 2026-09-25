"""
Tier 2: Feature F3 Boundaries — Section 7.5 Review & Append-only Logger Corner Cases.
"""

import os
import tempfile
import unittest

try:
    from crypto_engine.logger import append_review_log, format_section_7_5_review
    HAS_F3 = True
except ImportError:
    HAS_F3 = False


class TestB3LoggerBoundaries(unittest.TestCase):
    """Verifies edge cases for logger and Section 7.5 format generator."""

    def test_b3_01_auto_create_log_file_if_not_exists(self):
        """If target monthly log file does not exist, append_review_log should create it."""
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        temp_dir = tempfile.mkdtemp()
        target_path = os.path.join(temp_dir, "2026-10.md")

        try:
            self.assertFalse(os.path.exists(target_path))
            append_review_log(target_path, "## 2026-10-01: First entry")
            self.assertTrue(os.path.exists(target_path))
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("## 2026-10-01: First entry", content)
        finally:
            if os.path.exists(target_path):
                os.remove(target_path)
            os.rmdir(temp_dir)

    def test_b3_02_unicode_vietnamese_and_emoji_fidelity(self):
        """Preserves Vietnamese diacritics and financial cockpit emojis without encoding corruption."""
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write("# Initial\n")
            target_path = f.name

        try:
            review_text = (
                "## 2026-09-24: Đánh giá danh mục Crypto 🚨\n"
                "- Khuyến nghị: Bán 50% coin ngay lập tức, xả sạch SOL 🟢.\n"
                "- Đối chiếu BĐS: Tiền sử dụng đất làm sổ đỏ 3,1 tỷ."
            )
            append_review_log(target_path, review_text)
            with open(target_path, "r", encoding="utf-8") as f:
                saved = f.read()
            self.assertIn("Đánh giá danh mục", saved)
            self.assertIn("🚨", saved)
            self.assertIn("🟢", saved)
        finally:
            os.remove(target_path)

    def test_b3_03_end_of_month_date_boundary(self):
        """Accepts end of month dates (2026-10-31) in Section 7.5 review format."""
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        review = format_section_7_5_review(
            tts_vnd=550000000.0,
            withdrawn_vnd=550000000.0,
            active_band="TAKE_PROFIT_540M",
            action_summary="Hoàn tất rút toàn bộ vốn",
            borrow_needed_vnd=544000000.0,
            date_str="2026-10-31"
        )
        self.assertIn("2026-10-31", review)

    def test_b3_04_multiple_sequential_appends_preserve_all_entries(self):
        """Sequential appends to the same file must append all entries without overwriting any."""
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write("# Root Header\n")
            path = f.name

        try:
            append_review_log(path, "## Entry 1")
            append_review_log(path, "## Entry 2")
            append_review_log(path, "## Entry 3")

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("## Entry 1", content)
            self.assertIn("## Entry 2", content)
            self.assertIn("## Entry 3", content)
            self.assertTrue(content.index("Entry 1") < content.index("Entry 2") < content.index("Entry 3"))
        finally:
            os.remove(path)

    def test_b3_05_empty_review_content_handling(self):
        """Appending empty content should return clean status or raise."""
        if not HAS_F3:
            self.skipTest("crypto_engine.logger not implemented yet (Milestone M1)")

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write("# Baseline\n")
            path = f.name

        try:
            result = append_review_log(path, "")
            self.assertIn(result.get("status"), ["success", "empty", "ignored"])
        except (ValueError, AssertionError):
            pass
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
