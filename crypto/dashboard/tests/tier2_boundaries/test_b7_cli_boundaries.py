"""
Tier 2: Feature F7 Boundaries — CLI Interface Corner Cases.
"""

import unittest

try:
    from crypto_dashboard.cli import create_parser
    HAS_F7 = True
except ImportError:
    HAS_F7 = False


class TestB7CLIBoundaries(unittest.TestCase):
    """Verifies edge cases for CLI argument parsing and error exits."""

    def setUp(self):
        if not HAS_F7:
            self.skipTest("crypto_dashboard.cli not implemented yet (Milestone M3)")
        self.parser = create_parser()

    def test_b7_01_missing_command_exits_with_help_or_error(self):
        """CLI without subcommand raises SystemExit or prints help."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_b7_02_unknown_flag_raises_system_exit(self):
        """Passing unrecognized flag causes argparse to exit cleanly."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["status", "--nonexistent-flag"])

    def test_b7_03_invalid_port_type_rejected(self):
        """Passing non-integer string as port to serve causes SystemExit."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["serve", "--port", "abc"])

    def test_b7_04_negative_shock_parsed_correctly(self):
        """Negative float numbers for shock percentages parse cleanly without conflict."""
        args = self.parser.parse_args(["simulate", "--btc-shock=-25.5"])
        self.assertEqual(args.btc_shock, -25.5)

    def test_b7_05_unknown_subcommand_rejected(self):
        """Passing an unrecognized subcommand (e.g. 'delete') is rejected."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["delete"])


if __name__ == "__main__":
    unittest.main()
