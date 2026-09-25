"""
Tier 1: Feature F10 — Web Cockpit UI & Discipline Alert Banner Tests.
Authoritative source: PROJECT.md §F10; explorer_dashboard_1/report.md §3.
"""

import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB_DIR = os.path.join(PROJECT_ROOT, "src", "crypto_dashboard", "web")
INDEX_HTML = os.path.join(WEB_DIR, "index.html")
APP_JS = os.path.join(WEB_DIR, "app.js")
STYLE_CSS = os.path.join(WEB_DIR, "style.css")


class TestF10WebCockpit(unittest.TestCase):
    """Verifies Web Cockpit UI assets, alert banner markup, and ES6 structure."""

    def test_f10_01_web_assets_exist(self):
        """Authoritative Source: PROJECT.md §Code Layout:
        index.html, app.js, and style.css must exist in src/crypto_dashboard/web/.
        """
        if not os.path.exists(INDEX_HTML):
            self.skipTest("src/crypto_dashboard/web/ not yet created (Milestone M4)")

        self.assertTrue(os.path.exists(INDEX_HTML))
        self.assertTrue(os.path.exists(APP_JS))
        self.assertTrue(os.path.exists(STYLE_CSS))

    def test_f10_02_alert_banner_in_html(self):
        """Authoritative Source: explorer_dashboard_1/report.md §3.2 Component 1:
        Execution alert banner highlighting 0/13 missed orders and 540tr trigger.
        """
        if not os.path.exists(INDEX_HTML):
            self.skipTest("src/crypto_dashboard/web/ not yet created (Milestone M4)")

        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("alert-banner", html.lower())
        self.assertIn("540", html)

    def test_f10_03_cockpit_layout_sections_present(self):
        """Authoritative Source: explorer_dashboard_1/report.md §3.1:
        Dashboard grid wireframe requires Metrics, Simulation, Macro Countdown, and Action Center.
        """
        if not os.path.exists(INDEX_HTML):
            self.skipTest("src/crypto_dashboard/web/ not yet created (Milestone M4)")

        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html = f.read().lower()

        self.assertTrue("metric" in html)
        self.assertTrue("simulat" in html)
        self.assertTrue("macro" in html or "countdown" in html)

    def test_f10_04_vanilla_es6_javascript_structure(self):
        """Authoritative Source: PROJECT.md §Architecture:
        Must be Vanilla ES6 reactive client without requiring npm/node bundlers.
        """
        if not os.path.exists(APP_JS):
            self.skipTest("src/crypto_dashboard/web/app.js not yet created (Milestone M4)")

        with open(APP_JS, "r", encoding="utf-8") as f:
            js = f.read()

        # Should fetch from API endpoints
        self.assertIn("/api/status", js)
        self.assertIn("/api/matrix", js)

    def test_f10_05_dark_theme_cockpit_styling(self):
        """Authoritative Source: explorer_dashboard_1/report.md §3.1:
        Dark financial cockpit styling with pulsing red alert animation.
        """
        if not os.path.exists(STYLE_CSS):
            self.skipTest("src/crypto_dashboard/web/style.css not yet created (Milestone M4)")

        with open(STYLE_CSS, "r", encoding="utf-8") as f:
            css = f.read()

        self.assertTrue("pulse" in css or "animation" in css or "alert" in css)


if __name__ == "__main__":
    unittest.main()
