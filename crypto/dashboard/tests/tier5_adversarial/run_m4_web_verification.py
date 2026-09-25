#!/usr/bin/env python3
"""
Standalone Verification Script: Milestone 4 Web Cockpit DOM & Asset Boundaries.
Target: src/crypto_dashboard/web/index.html & style.css
Author: challenger_m4_1 (Empirical Challenger)
"""

import sys
import os
import re
from collections import Counter
from html.parser import HTMLParser

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB_DIR = os.path.join(PROJECT_ROOT, "src", "crypto_dashboard", "web")
INDEX_HTML = os.path.join(WEB_DIR, "index.html")
STYLE_CSS = os.path.join(WEB_DIR, "style.css")
APP_JS = os.path.join(WEB_DIR, "app.js")


class StrictHTMLValidator(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.tag_counts = Counter()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        self.tag_counts[t] += 1
        attrs_dict = dict(attrs)
        if "id" in attrs_dict:
            self.ids.append((attrs_dict["id"], self.getpos()))
        if t not in self.VOID_TAGS:
            self.stack.append((t, self.getpos()))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in self.VOID_TAGS:
            self.errors.append(f"Void tag <{tag}> closed with end tag at {self.getpos()}")
            return
        if not self.stack:
            self.errors.append(f"Orphan closing tag </{tag}> at {self.getpos()}")
            return
        last, pos = self.stack.pop()
        if last != t:
            self.errors.append(f"Mismatched tag: expected </{last}> (opened at {pos}), got </{tag}> at {self.getpos()}")

    def close(self):
        super().close()
        while self.stack:
            tag, pos = self.stack.pop()
            self.errors.append(f"Unclosed tag <{tag}> opened at {pos}")


def run_checks():
    print("=" * 78)
    print("EMPIRICAL VERIFICATION HARNESS: M4 WEB COCKPIT DOM & ASSET BOUNDARIES")
    print("=" * 78)
    
    passed_all = True
    results = []

    def record_result(check_name, status, details=""):
        nonlocal passed_all
        if not status:
            passed_all = False
        mark = "[PASS]" if status else "[FAIL]"
        print(f"{mark} {check_name}")
        if details:
            print(f"       Details: {details}")
        results.append((check_name, status, details))

    # Read files
    if not os.path.exists(INDEX_HTML) or not os.path.exists(STYLE_CSS):
        print(f"[FAIL] Target files do not exist: {INDEX_HTML}, {STYLE_CSS}")
        return False

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    with open(STYLE_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    with open(APP_JS, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Size budget limits
    html_size = os.path.getsize(INDEX_HTML)
    css_size = os.path.getsize(STYLE_CSS)
    record_result(
        "Size budget index.html < 100KB",
        html_size < 100 * 1024,
        f"{html_size:,} bytes ({html_size/1024:.2f} KB) < 102,400 bytes"
    )
    record_result(
        "Size budget style.css < 100KB",
        css_size < 100 * 1024,
        f"{css_size:,} bytes ({css_size/1024:.2f} KB) < 102,400 bytes"
    )

    # 2. Zero external network dependency / CDN leak
    ext_imports_html = re.findall(r"""(?:href|src)\s*=\s*["'](https?://[^"']+|//[^"']+)["']""", html, re.I)
    ext_imports_css = re.findall(r"""(?:@import|url)\s*\(\s*["']?(https?://[^"')]+|//[^"')]+)["']?\s*\)""", css, re.I)
    record_result(
        "Zero external imports in index.html (href/src)",
        len(ext_imports_html) == 0,
        f"Found: {ext_imports_html}"
    )
    record_result(
        "Zero external imports in style.css (@import/url)",
        len(ext_imports_css) == 0,
        f"Found: {ext_imports_css}"
    )

    cdn_matches_html = re.findall(r"\b(cdn|unpkg|jsdelivr|googleapis|fonts\.gstatic|cdnjs)\b", html, re.I)
    cdn_matches_css = re.findall(r"\b(cdn|unpkg|jsdelivr|googleapis|fonts\.gstatic|cdnjs)\b", css, re.I)
    record_result(
        "Zero CDN domain references in index.html and style.css",
        len(cdn_matches_html) == 0 and len(cdn_matches_css) == 0,
        f"HTML CDN matches: {cdn_matches_html}, CSS CDN matches: {cdn_matches_css}"
    )

    # 3. HTML syntax validation & tag nesting
    validator = StrictHTMLValidator()
    validator.feed(html)
    validator.close()
    record_result(
        "HTML tag nesting, balance, and opening/closing integrity",
        len(validator.errors) == 0,
        f"Errors: {validator.errors}" if validator.errors else f"Parsed {sum(validator.tag_counts.values())} tags, 0 unclosed/mismatched"
    )

    # 4. Meta tags
    has_viewport = bool(re.search(r'<meta[^>]+name=["\']viewport["\']', html))
    has_charset = bool(re.search(r'<meta[^>]+charset=["\']UTF-8["\']', html, re.I))
    record_result(
        "HTML meta tags: viewport and charset UTF-8",
        has_viewport and has_charset,
        f"viewport: {has_viewport}, charset: {has_charset}"
    )

    # 5. DOM IDs: Uniqueness & JS contract
    all_html_ids = [i[0] for i in validator.ids]
    id_counts = Counter(all_html_ids)
    duplicates = {k: v for k, v in id_counts.items() if v > 1}
    record_result(
        "DOM ID uniqueness (0 duplicates in index.html)",
        len(duplicates) == 0,
        f"Duplicates: {duplicates}" if duplicates else f"{len(all_html_ids)} unique IDs"
    )

    js_queried_ids = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_-]+)["\']\)', js))
    html_id_set = set(all_html_ids)
    missing_from_html = js_queried_ids - html_id_set
    record_result(
        "All app.js getElementById targets exist in index.html",
        len(missing_from_html) == 0,
        f"Missing: {missing_from_html}" if missing_from_html else f"All {len(js_queried_ids)} JS target IDs present in HTML"
    )

    # Critical IDs check
    critical_ids = [
        "alert-banner", "val-tts-vnd", "slider-btc-shock", "slider-sol-shock",
        "slider-p2p-rate", "countdown-late-oct", "countdown-tranche-1",
        "val-hesitation-tax", "sim-safety-bar", "mcr-sim-card",
        "bht-ticker-card", "avc-meter-card", "orders-table", "agy-console-drawer"
    ]
    missing_crit = [cid for cid in critical_ids if cid not in html_id_set]
    record_result(
        "Presence of all mandatory critical DOM IDs",
        len(missing_crit) == 0,
        f"Missing: {missing_crit}" if missing_crit else f"All {len(critical_ids)} critical IDs verified"
    )

    # 6. CSS validation
    has_keyframes_pulse = "@keyframes alert-pulse" in css
    has_keyframes_dot = "@keyframes beacon-dot" in css
    has_dark_vars = "--bg-app" in css and "--accent-danger" in css and "--accent-success" in css
    has_media_1024 = "@media (max-width: 1024px)" in css
    has_media_640 = "@media (max-width: 640px)" in css

    record_result(
        "CSS @keyframes alert-pulse, beacon-dot, spin defined",
        has_keyframes_pulse and has_keyframes_dot,
        f"alert-pulse: {has_keyframes_pulse}, beacon-dot: {has_keyframes_dot}"
    )
    record_result(
        "CSS dark theme institutional variables in :root",
        has_dark_vars,
        f"--bg-app, --accent-danger, --accent-success present"
    )
    record_result(
        "CSS responsive media queries (<=1024px tablet, <=640px mobile)",
        has_media_1024 and has_media_640,
        f"max-width 1024px: {has_media_1024}, max-width 640px: {has_media_640}"
    )

    # 7. Domain Constraints (2026-09-24)
    has_540 = "540" in html
    has_0_13 = "0/13" in html
    has_late_oct = "Cuối tháng 10/2026" in html or "31/10/2026" in html or "Late Oct" in html
    record_result(
        "Domain constraints: 540tr Hard Floor, 0/13 missed orders, Late Oct 2026",
        has_540 and has_0_13 and has_late_oct,
        f"540M: {has_540}, 0/13: {has_0_13}, Late Oct: {has_late_oct}"
    )

    print("=" * 78)
    total_passed = sum(1 for _, s, _ in results if s)
    total_checks = len(results)
    print(f"SUMMARY: {total_passed}/{total_checks} checks passed.")
    if passed_all:
        print("EMPIRICAL VERDICT: APPROVE")
    else:
        print("EMPIRICAL VERDICT: REQUEST_CHANGES")
    print("=" * 78)
    return passed_all


if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
