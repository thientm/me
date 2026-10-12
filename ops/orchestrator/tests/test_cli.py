import unittest
from unittest.mock import patch, MagicMock

from ops.orchestrator.cli import build_parser, run_orchestration_dashboard, main

class TestOrchestratorCli(unittest.TestCase):
    def test_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args([])
        self.assertEqual(args.channel, "all")
        self.assertFalse(args.dry_run)

    def test_parser_custom(self):
        parser = build_parser()
        args = parser.parse_args(["--channel", "me-tech", "--slot", "12", "--dry-run"])
        self.assertEqual(args.channel, "me-tech")
        self.assertEqual(args.slot, 12)
        self.assertTrue(args.dry_run)

    @patch("ops.orchestrator.cli.check_all_channels")
    def test_run_orchestration_dashboard(self, mock_check_all):
        mock_check_all.return_value = {
            "me-tech": {"channel": "me-tech", "slot": 8, "status": "done", "slug": "slug1", "posted": ["yt", "tt", "fb"], "missing": []},
            "thien-tran": {"channel": "thien-tran", "slot": 8, "status": "none", "slug": None, "posted": [], "missing": ["yt", "tt", "fb"]},
            "tam-an-lac": {"channel": "tam-an-lac", "slot": 8, "status": "done", "slug": "slug3", "posted": ["yt", "tt", "fb"], "missing": []}
        }

        dash = run_orchestration_dashboard(slot=8, channel="all")
        self.assertIn("me-tech", dash["channels"])
        self.assertEqual(dash["slot"], 8)
        self.assertTrue(dash["ok"])

    @patch("ops.orchestrator.cli.run_orchestration_dashboard")
    def test_main_exit_code(self, mock_dash):
        mock_dash.return_value = {"ok": True, "slot": 8, "timestamp": "12.10.2026", "channels": {}}
        ret = main(["--dry-run"])
        self.assertEqual(ret, 0)

if __name__ == "__main__":
    unittest.main()
