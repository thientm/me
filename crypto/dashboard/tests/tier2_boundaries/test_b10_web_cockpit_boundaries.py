"""
Tier 2: Feature F10 Boundaries — Web Cockpit UI Corner Cases.
"""

import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB_DIR = os.path.join(PROJECT_ROOT, "src", "crypto_dashboard", "web")
INDEX_HTML = os.path.join(WEB_DIR, "index.html")
APP_JS = os.path.join(WEB_DIR, "app.js")
STYLE_CSS = os.path.join(WEB_DIR, "style.css")


class TestB10WebCockpitBoundaries(unittest.TestCase):
    """Verifies web asset size, standards compliance, and offline self-containment."""

    def test_b10_01_index_html_file_size_budget(self):
        """index.html must be lightweight (< 100KB) for instant local loading."""
        if not os.path.exists(INDEX_HTML):
            self.skipTest("src/crypto_dashboard/web/index.html not yet created (Milestone M4)")

        size = os.path.getsize(INDEX_HTML)
        self.assertLess(size, 100 * 1024, "HTML file exceeds 100KB budget")

    def test_b10_02_viewport_meta_tag_present(self):
        """index.html must have responsive viewport meta tag."""
        if not os.path.exists(INDEX_HTML):
            self.skipTest("src/crypto_dashboard/web/index.html not yet created (Milestone M4)")

        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn('<meta name="viewport"', html)

    def test_b10_03_utf8_charset_declared(self):
        """index.html must declare UTF-8 charset for Vietnamese character rendering."""
        if not os.path.exists(INDEX_HTML):
            self.skipTest("src/crypto_dashboard/web/index.html not yet created (Milestone M4)")

        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertTrue('charset="UTF-8"' in html or 'charset="utf-8"' in html)

    def test_b10_04_js_asset_size_budget(self):
        """app.js must be lightweight (< 200KB) for zero-latency execution."""
        if not os.path.exists(APP_JS):
            self.skipTest("src/crypto_dashboard/web/app.js not yet created (Milestone M4)")

        size = os.path.getsize(APP_JS)
        self.assertLess(size, 200 * 1024, "JS file exceeds 200KB budget")

    def test_b10_05_css_asset_size_budget(self):
        """style.css must be lightweight (< 100KB)."""
        if not os.path.exists(STYLE_CSS):
            self.skipTest("src/crypto_dashboard/web/style.css not yet created (Milestone M4)")

        size = os.path.getsize(STYLE_CSS)
        self.assertLess(size, 100 * 1024, "CSS file exceeds 100KB budget")


if __name__ == "__main__":
    unittest.main()
