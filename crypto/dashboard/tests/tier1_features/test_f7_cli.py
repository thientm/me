"""
Tier 1: Feature F7 — CLI Interface Tests.
Authoritative source: PROJECT.md §F7; explorer_dashboard_1/report.md §2.
"""

import sys
import unittest
from io import StringIO
from unittest.mock import patch

try:
    from crypto_dashboard.cli import create_parser, handle_cli
    HAS_F7 = True
except ImportError:
    HAS_F7 = False


class TestF7CLI(unittest.TestCase):
    """Verifies CLI argument parsing and command handlers (status, review, simulate, serve)."""

    def setUp(self):
        if not HAS_F7:
            self.skipTest("crypto_dashboard.cli not implemented yet (Milestone M3)")
        self.parser = create_parser()

    def test_f7_01_cli_subcommands_recognized(self):
        """Authoritative Source: explorer_dashboard_1/report.md §2:
        Subcommands required: status, review, simulate, serve.
        """
        for cmd in ["status", "review", "simulate", "serve"]:
            args = self.parser.parse_args([cmd])
            self.assertEqual(args.command, cmd)

    def test_f7_02_status_command_flags(self):
        """Authoritative Source: explorer_dashboard_1/report.md §2.1:
        status accepts --offline (-o), --json, --verbose (-v).
        """
        args = self.parser.parse_args(["status", "--offline", "--json", "--verbose"])
        self.assertTrue(args.offline)
        self.assertTrue(args.json)
        self.assertTrue(args.verbose)

    def test_f7_03_review_command_flags(self):
        """Authoritative Source: explorer_dashboard_1/report.md §2.2:
        review accepts --save-log, --dry-run, --agy.
        """
        args = self.parser.parse_args(["review", "--save-log", "--dry-run", "--agy"])
        self.assertTrue(args.save_log)
        self.assertTrue(args.dry_run)
        self.assertTrue(args.agy)

    def test_f7_04_simulate_command_flags(self):
        """Authoritative Source: explorer_dashboard_1/report.md §2.3:
        simulate accepts --btc-shock, --sol-shock, --scenario.
        """
        args = self.parser.parse_args(["simulate", "--btc-shock", "-15", "--scenario", "hold100"])
        self.assertEqual(args.btc_shock, -15.0)
        self.assertEqual(args.scenario, "hold100")

    def test_f7_05_serve_command_flags(self):
        """Authoritative Source: explorer_dashboard_1/report.md §2.4:
        serve accepts --port, --host, --no-browser.
        """
        args = self.parser.parse_args(["serve", "--port", "8088", "--host", "0.0.0.0", "--no-browser"])
        self.assertEqual(args.port, 8088)
        self.assertEqual(args.host, "0.0.0.0")
        self.assertTrue(args.no_browser)


if __name__ == "__main__":
    unittest.main()
