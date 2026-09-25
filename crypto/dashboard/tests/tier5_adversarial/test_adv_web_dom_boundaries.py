"""
Tier 5: Adversarial Stress Testing — M4 Web Cockpit DOM & Asset Boundaries.
Author: challenger_m4_1 (teamwork_preview_challenger)
Target: src/crypto_dashboard/web/index.html, src/crypto_dashboard/web/style.css

Empirically verifies:
1. Asset Budgets & Bloat:
   - index.html < 100KB, style.css < 100KB, zero large inline data URIs or base64 blobs.
2. Zero External Dependency / CDN Leaks:
   - Grep for http://, https://, cdn, unpkg, jsdelivr, googleapis, fonts, cdnjs.
   - Asserts 0 external resource imports (fonts, scripts, css links).
   - Only relative local imports (style.css, app.js) and standard XMLNS.
3. Strict HTML5 Syntax & Tag Nesting:
   - Full stack-based HTML parser validating 100% balanced tags (including SVG elements).
   - Zero unclosed or mismatched tags, valid DOCTYPE, charset UTF-8, responsive viewport.
4. DOM ID Integrity & JavaScript Contract:
   - ID uniqueness (0 duplicate IDs across DOM tree).
   - 100% of the 72 DOM IDs queried by app.js exist in index.html.
   - Presence and integrity of all critical financial cockpit IDs.
5. Interactive Controls & Accessibility:
   - Input slider attribute ranges (min, max, step, value).
   - ARIA roles, aria-label, aria-live, and <label for="..."> associations.
6. Vector Graphics (SVG) Self-Containment:
   - MCR-Sim, BHT-Ticker, AVC-Meter pure vector SVGs with viewBox and no external raster images.
7. CSS Institutional Styling & Responsive Layout:
   - CSS brace balancing and syntax integrity.
   - Keyframe animations (@keyframes alert-pulse, pulse, beacon-dot, spin).
   - CSS custom property design system (:root variables).
   - Responsive breakpoints (<=1024px, <=640px) adapting grid columns.
8. Domain Rule Conformance:
   - Hard Floor 540tr, Take-Profit >=540tr, 0/13 missed orders, Late Oct 2026 deadline,
     38,750 VND/hr hesitation tax, 615tr BĐS debt ceiling.
"""

from collections import Counter
from html.parser import HTMLParser
import os
import re
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB_DIR = os.path.join(PROJECT_ROOT, "src", "crypto_dashboard", "web")
INDEX_HTML = os.path.join(WEB_DIR, "index.html")
STYLE_CSS = os.path.join(WEB_DIR, "style.css")
APP_JS = os.path.join(WEB_DIR, "app.js")


class StrictHTMLValidator(HTMLParser):
    """Stack-based HTML validator that enforces proper nesting of non-void tags."""
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.tag_counts = Counter()
        self.ids_with_pos = []
        self.all_attrs = []

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        self.tag_counts[tag_lower] += 1
        attrs_dict = dict(attrs)
        self.all_attrs.append((tag_lower, attrs_dict, self.getpos()))

        if "id" in attrs_dict:
            self.ids_with_pos.append((attrs_dict["id"], self.getpos()))

        if tag_lower not in self.VOID_TAGS:
            self.stack.append((tag_lower, self.getpos()))

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self.VOID_TAGS:
            self.errors.append(f"Void tag <{tag}> closed with end tag at {self.getpos()}")
            return
        if not self.stack:
            self.errors.append(f"Orphan closing tag </{tag}> at {self.getpos()} (empty stack)")
            return
        last_tag, last_pos = self.stack.pop()
        if last_tag != tag_lower:
            self.errors.append(
                f"Mismatched tag: expected </{last_tag}> (opened at {last_pos}), "
                f"got </{tag}> at {self.getpos()}"
            )

    def close(self):
        super().close()
        while self.stack:
            tag, pos = self.stack.pop()
            self.errors.append(f"Unclosed tag <{tag}> opened at {pos}")


class TestAdvWebDomBoundaries(unittest.TestCase):
    """Adversarial boundary and contract stress test for Web Cockpit assets."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html_content = f.read()
        with open(STYLE_CSS, "r", encoding="utf-8") as f:
            cls.css_content = f.read()
        with open(APP_JS, "r", encoding="utf-8") as f:
            cls.js_content = f.read()

    # -------------------------------------------------------------------------
    # 1. ASSET BUDGETS & BLOAT TESTS
    # -------------------------------------------------------------------------

    def test_adv_01_index_html_size_budget_and_bloat(self):
        """index.html must be < 100KB, contain no base64 blobs or hidden bloat."""
        size = os.path.getsize(INDEX_HTML)
        self.assertLess(size, 100 * 1024, f"index.html exceeds 100KB: {size} bytes")
        self.assertGreater(size, 5 * 1024, f"index.html unexpectedly sparse: {size} bytes")

        # Check for large base64 data URIs (> 1KB)
        base64_blobs = re.findall(r"data:[^;]+;base64,[A-Za-z0-9+/=]{1000,}", self.html_content)
        self.assertEqual(len(base64_blobs), 0, "Disallowed large inline base64 blobs in HTML")

    def test_adv_02_style_css_size_budget_and_bloat(self):
        """style.css must be < 100KB with reasonable selector complexity."""
        size = os.path.getsize(STYLE_CSS)
        self.assertLess(size, 100 * 1024, f"style.css exceeds 100KB: {size} bytes")
        self.assertGreater(size, 3 * 1024, f"style.css unexpectedly small: {size} bytes")

        # Check for base64 embedded fonts/images in CSS
        base64_css = re.findall(r"data:[^;]+;base64,[A-Za-z0-9+/=]{500,}", self.css_content)
        self.assertEqual(len(base64_css), 0, "Disallowed embedded base64 assets in CSS")

    # -------------------------------------------------------------------------
    # 2. ZERO EXTERNAL NETWORK DEPENDENCY / CDN LEAK TESTS
    # -------------------------------------------------------------------------

    def test_adv_03_zero_external_network_dependencies(self):
        """Assert 0 external resource imports (fonts, scripts, css) and 0 CDN links."""
        # Check index.html for external href or src (http://, https://, //)
        external_imports = re.findall(
            r"""(?:href|src)\s*=\s*["'](https?://[^"']+|//[^"']+)["']""",
            self.html_content,
            re.IGNORECASE
        )
        self.assertEqual(
            external_imports, [],
            f"Found external resource imports in index.html: {external_imports}"
        )

        # Check style.css for external imports (@import, url)
        css_external_imports = re.findall(
            r"""(?:@import|url)\s*\(\s*["']?(https?://[^"')]+|//[^"')]+)["']?\s*\)""",
            self.css_content,
            re.IGNORECASE
        )
        self.assertEqual(
            css_external_imports, [],
            f"Found external resource imports in style.css: {css_external_imports}"
        )

        # Grep for CDN domain names in both files
        cdn_patterns = [
            r"\bcdn\b", r"\bunpkg\b", r"\bjsdelivr\b", r"\bgoogleapis\b",
            r"\bfonts\.gstatic\b", r"\bcdnjs\b", r"\bcloudflare\b"
        ]
        for pat in cdn_patterns:
            html_matches = re.findall(pat, self.html_content, re.IGNORECASE)
            self.assertEqual(len(html_matches), 0, f"Found CDN pattern {pat} in index.html")
            css_matches = re.findall(pat, self.css_content, re.IGNORECASE)
            self.assertEqual(len(css_matches), 0, f"Found CDN pattern {pat} in style.css")

    def test_adv_04_only_local_relative_asset_links(self):
        """Verify HTML only links to relative local files style.css and app.js."""
        # Find all link stylesheet hrefs
        link_hrefs = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']', self.html_content)
        for href in link_hrefs:
            self.assertEqual(href, "style.css", f"Unexpected stylesheet link: {href}")

        # Find all script srcs
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', self.html_content)
        for src in script_srcs:
            self.assertEqual(src, "app.js", f"Unexpected script src: {src}")

    # -------------------------------------------------------------------------
    # 3. HTML5 SYNTAX & SEMANTIC STRUCTURE TESTS
    # -------------------------------------------------------------------------

    def test_adv_05_doctype_charset_viewport_meta(self):
        """Verify <!DOCTYPE html>, <html lang="vi">, UTF-8 charset, and responsive viewport."""
        self.assertTrue(
            self.html_content.strip().startswith("<!DOCTYPE html>"),
            "index.html must start with standard <!DOCTYPE html>"
        )
        self.assertRegex(
            self.html_content,
            r'<html[^>]+lang=["\']vi["\']',
            "index.html must declare lang='vi'"
        )
        self.assertRegex(
            self.html_content,
            r'<meta[^>]+charset=["\']UTF-8["\']',
            "index.html must declare UTF-8 charset"
        )
        self.assertRegex(
            self.html_content,
            r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']*width=device-width[^"\']*["\']',
            "index.html must declare responsive viewport with width=device-width"
        )

    def test_adv_06_strict_tag_nesting_and_balance(self):
        """Stack-based parser must find 0 tag nesting or unclosed tag errors."""
        validator = StrictHTMLValidator()
        validator.feed(self.html_content)
        validator.close()

        self.assertEqual(
            validator.errors, [],
            f"HTML tag nesting errors found: {validator.errors}"
        )
        self.assertGreater(validator.tag_counts["div"], 10, "Expected multiple structural divs")
        self.assertGreater(validator.tag_counts["section"], 2, "Expected semantic section tags")

    # -------------------------------------------------------------------------
    # 4. DOM ID INTEGRITY & JAVASCRIPT CONTRACT TESTS
    # -------------------------------------------------------------------------

    def test_adv_07_dom_id_uniqueness(self):
        """Assert exactly 0 duplicate element IDs across the entire DOM tree."""
        all_ids = re.findall(r'\bid=["\']([a-zA-Z0-9_-]+)["\']', self.html_content)
        counts = Counter(all_ids)
        duplicates = {k: v for k, v in counts.items() if v > 1}
        self.assertEqual(duplicates, {}, f"Duplicate element IDs found in index.html: {duplicates}")

    def test_adv_08_all_app_js_queried_ids_exist_in_html(self):
        """Assert 100% of the IDs queried via document.getElementById in app.js exist in index.html."""
        js_ids = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_-]+)["\']\)', self.js_content))
        html_ids = set(re.findall(r'\bid=["\']([a-zA-Z0-9_-]+)["\']', self.html_content))

        self.assertGreater(len(js_ids), 50, f"Expected >50 IDs in app.js, found {len(js_ids)}")
        missing_ids = js_ids - html_ids
        self.assertEqual(
            missing_ids, set(),
            f"app.js queries IDs that do not exist in index.html: {missing_ids}"
        )

    def test_adv_09_critical_financial_cockpit_dom_ids_presence(self):
        """Verify presence of specific mandatory DOM IDs required by PROJECT.md specifications."""
        mandatory_ids = [
            "alert-banner",
            "val-tts-vnd",
            "val-tts-usd",
            "val-floor-badge",
            "val-floor-cushion",
            "val-cashout-progress",
            "cashout-progress-bar",
            "portfolio-summary",
            "portfolio-table",
            "val-hesitation-tax",
            "slider-btc-shock",
            "slider-sol-shock",
            "slider-p2p-rate",
            "sim-safety-bar",
            "countdown-tranche-1",
            "countdown-tranche-2",
            "countdown-bds-debt",
            "countdown-pce",
            "countdown-late-oct",
            "bds-ceiling-bar",
            "bds-status-badge",
            "mcr-sim-card",
            "bht-ticker-card",
            "bht-countdown-circle",
            "avc-meter-card",
            "avc-needle",
            "orders-table",
            "agy-console-drawer",
            "btn-copy-orders",
            "btn-run-agy",
        ]
        html_ids = set(re.findall(r'\bid=["\']([a-zA-Z0-9_-]+)["\']', self.html_content))
        for mid in mandatory_ids:
            self.assertIn(mid, html_ids, f"Mandatory DOM ID missing: #{mid}")

    # -------------------------------------------------------------------------
    # 5. INTERACTIVE CONTROLS & ATTRIBUTE BOUNDARIES
    # -------------------------------------------------------------------------

    def test_adv_10_slider_input_attribute_constraints(self):
        """Stress-test What-If simulation slider input boundaries."""
        validator = StrictHTMLValidator()
        validator.feed(self.html_content)
        validator.close()

        inputs = {
            attrs["id"]: attrs
            for tag, attrs, pos in validator.all_attrs
            if tag == "input" and "id" in attrs
        }

        # BTC shock slider: min=-50, max=20, step=1, value=0
        self.assertIn("slider-btc-shock", inputs)
        btc = inputs["slider-btc-shock"]
        self.assertEqual(btc.get("type"), "range")
        self.assertEqual(int(btc.get("min")), -50)
        self.assertEqual(int(btc.get("max")), 20)
        self.assertEqual(int(btc.get("step")), 1)
        self.assertEqual(int(btc.get("value")), 0)

        # SOL shock slider: min=-60, max=30, step=1, value=0
        self.assertIn("slider-sol-shock", inputs)
        sol = inputs["slider-sol-shock"]
        self.assertEqual(sol.get("type"), "range")
        self.assertEqual(int(sol.get("min")), -60)
        self.assertEqual(int(sol.get("max")), 30)
        self.assertEqual(int(sol.get("step")), 1)
        self.assertEqual(int(sol.get("value")), 0)

        # P2P rate slider: min=24000, max=27000, step=50, value=25930
        self.assertIn("slider-p2p-rate", inputs)
        p2p = inputs["slider-p2p-rate"]
        self.assertEqual(p2p.get("type"), "range")
        self.assertEqual(int(p2p.get("min")), 24000)
        self.assertEqual(int(p2p.get("max")), 27000)
        self.assertEqual(int(p2p.get("step")), 50)
        self.assertEqual(int(p2p.get("value")), 25930)

    def test_adv_11_accessibility_and_semantic_roles(self):
        """Verify ARIA accessibility roles and label bindings."""
        # Alert banner role="alert"
        self.assertRegex(
            self.html_content,
            r'<aside[^>]+id=["\']alert-banner["\'][^>]+role=["\']alert["\']',
            "Alert banner must have role='alert'"
        )

        # Toast container aria-live="polite"
        self.assertRegex(
            self.html_content,
            r'<div[^>]+id=["\']toast-container["\'][^>]+aria-live=["\']polite["\']',
            "Toast container must have aria-live='polite'"
        )

        # Labels associated with slider inputs
        self.assertIn('for="slider-btc-shock"', self.html_content)
        self.assertIn('for="slider-sol-shock"', self.html_content)
        self.assertIn('for="slider-p2p-rate"', self.html_content)

    # -------------------------------------------------------------------------
    # 6. VECTOR GRAPHICS (SVG) SELF-CONTAINMENT TESTS
    # -------------------------------------------------------------------------

    def test_adv_12_svg_graphics_self_containment(self):
        """Verify MCR-Sim, BHT-Ticker, and AVC-Meter are pure self-contained SVGs."""
        # Check SVG presence
        svg_matches = re.findall(r'<svg[^>]*>', self.html_content)
        self.assertGreaterEqual(len(svg_matches), 3, "Expected at least 3 SVG graphics")

        for svg in svg_matches:
            self.assertIn("viewBox", svg, f"SVG missing responsive viewBox: {svg}")

        # Ensure no external raster image links in SVG (<image xlink:href="...">)
        raster_in_svg = re.findall(r'<image[^>]+(?:xlink:href|href)=["\']([^"\']+)["\']', self.html_content)
        self.assertEqual(raster_in_svg, [], f"Disallowed raster images in SVG: {raster_in_svg}")

    # -------------------------------------------------------------------------
    # 7. CSS SYNTAX, VARIABLES, KEYFRAMES & RESPONSIVE LAYOUT
    # -------------------------------------------------------------------------

    def test_adv_13_css_balanced_braces_and_syntax(self):
        """Verify CSS contains zero unbalanced braces or syntax errors."""
        brace_stack = []
        errors = []
        in_comment = False
        in_string = False
        str_char = ""

        lines = self.css_content.splitlines()
        for line_no, line in enumerate(lines, 1):
            i = 0
            while i < len(line):
                if not in_comment and not in_string:
                    if line[i:i+2] == "/*":
                        in_comment = True
                        i += 2
                        continue
                    elif line[i] in ('"', "'"):
                        in_string = True
                        str_char = line[i]
                        i += 1
                        continue
                    elif line[i] == "{":
                        brace_stack.append((line_no, i+1))
                    elif line[i] == "}":
                        if not brace_stack:
                            errors.append(f"Unmatched closing brace at line {line_no}:{i+1}")
                        else:
                            brace_stack.pop()
                elif in_comment:
                    if line[i:i+2] == "*/":
                        in_comment = False
                        i += 2
                        continue
                elif in_string:
                    if line[i] == "\\" and i + 1 < len(line):
                        i += 2
                        continue
                    elif line[i] == str_char:
                        in_string = False
                i += 1

        while brace_stack:
            ln, col = brace_stack.pop()
            errors.append(f"Unclosed open brace from line {ln}:{col}")

        self.assertEqual(errors, [], f"CSS brace errors: {errors}")

    def test_adv_14_css_keyframes_animations_present(self):
        """Verify required keyframe animations are defined with keyframe steps."""
        required_keyframes = ["alert-pulse", "pulse", "beacon-dot", "spin"]
        for kf in required_keyframes:
            self.assertIn(
                f"@keyframes {kf}",
                self.css_content,
                f"Missing required @keyframes {kf} in style.css"
            )

        # Check alert-pulse has 0%, 50%, 100% using brace-counting
        idx = self.css_content.find("@keyframes alert-pulse")
        self.assertNotEqual(idx, -1, "Missing @keyframes alert-pulse")
        open_brace = self.css_content.find("{", idx)
        count = 1
        i = open_brace + 1
        while i < len(self.css_content) and count > 0:
            if self.css_content[i] == "{":
                count += 1
            elif self.css_content[i] == "}":
                count -= 1
            i += 1
        alert_pulse_block = self.css_content[idx:i]
        self.assertIn("0%", alert_pulse_block)
        self.assertIn("50%", alert_pulse_block)
        self.assertIn("100%", alert_pulse_block)

    def test_adv_15_css_custom_properties_dark_theme(self):
        """Verify dark theme CSS custom properties in :root."""
        required_vars = [
            "--bg-app",
            "--bg-card",
            "--border-card",
            "--text-primary",
            "--accent-danger",
            "--accent-warning",
            "--accent-success",
            "--font-sans",
            "--font-mono",
        ]
        root_match = re.search(r":root\s*\{([^}]+)\}", self.css_content)
        self.assertIsNotNone(root_match, "Missing :root declaration in style.css")
        root_body = root_match.group(1)
        for var in required_vars:
            self.assertIn(var, root_body, f"Missing CSS variable {var} in :root")

    def test_adv_16_css_responsive_media_queries(self):
        """Verify responsive breakpoints for tablet (<=1024px) and mobile (<=640px)."""
        self.assertIn(
            "@media (max-width: 1024px)",
            self.css_content,
            "Missing @media (max-width: 1024px) breakpoint"
        )
        self.assertIn(
            "@media (max-width: 640px)",
            self.css_content,
            "Missing @media (max-width: 640px) breakpoint"
        )

    # -------------------------------------------------------------------------
    # 8. DOMAIN RULE CONFORMANCE (2026-09-24 UPDATE)
    # -------------------------------------------------------------------------

    def test_adv_17_domain_rules_hard_floor_540m(self):
        """Assert 540tr Hard Floor is prominently featured in index.html markup."""
        self.assertIn("540", self.html_content)
        self.assertIn("540.000.000", self.html_content)
        self.assertIn("SÀN CỨNG 540TR", self.html_content.upper())

    def test_adv_18_domain_rules_missed_orders_warning(self):
        """Assert 0/13 missed orders and delay warning are in the banner markup."""
        self.assertIn("0/13", self.html_content)
        self.assertIn("50 NGÀY", self.html_content)

    def test_adv_19_domain_rules_cashout_deadline_late_oct_2026(self):
        """Assert Late October 2026 (31/10/2026) cashout deadline is documented."""
        self.assertTrue(
            "31/10" in self.html_content or "31/10/2026" in self.html_content or "Late Oct" in self.html_content or "Cuối tháng 10/2026" in self.html_content,
            "Late October 2026 deadline missing from index.html"
        )

    def test_adv_20_domain_rules_statutory_bht_and_bds_debt_ceiling(self):
        """Assert 38.750 đ/hr hesitation tax and 615tr BĐS debt ceiling appear in markup."""
        self.assertIn("38.750", self.html_content)
        self.assertIn("615", self.html_content)


if __name__ == "__main__":
    unittest.main()
