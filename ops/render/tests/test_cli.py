import os
import unittest
from unittest.mock import patch, MagicMock

from ops.render.cli import build_parser, run_dry_run, main

class TestRenderCli(unittest.TestCase):
    def test_parser_args(self):
        parser = build_parser()
        args = parser.parse_args(["--channel", "me-tech", "--slug", "my-slug", "--dry-run"])
        self.assertEqual(args.channel, "me-tech")
        self.assertEqual(args.slug, "my-slug")
        self.assertTrue(args.dry_run)

    @patch("ops.render.cli.get_render_config")
    @patch("ops.render.cli.validate_motion_deck")
    @patch("ops.render.cli.check_environment")
    def test_run_dry_run_success(self, mock_doctor, mock_validate, mock_config):
        spec = MagicMock()
        spec.engine_type = "motion_deck"
        spec.content_path = "/mock/content.json"
        spec.shots_dir = "/mock/shots"
        spec.output_video = "/mock/out.mp4"
        mock_config.return_value = spec
        mock_validate.return_value = ([], [], 35.5)
        mock_doctor.return_value = {"ok": True, "checks": {"ffmpeg": True}, "issues": []}

        res = run_dry_run("me-tech", "my-slug")
        self.assertTrue(res["valid"])
        self.assertEqual(res["est_duration"], 35.5)
        self.assertEqual(res["errors"], [])

    @patch("ops.render.cli.run_dry_run")
    def test_main_dry_run_exit_codes(self, mock_dry_run):
        mock_dry_run.return_value = {
            "valid": True,
            "channel": "me-tech",
            "slug": "test",
            "engine_type": "motion_deck",
            "content_path": "path",
            "output_video": "out",
            "est_duration": 34.0,
            "errors": [],
            "warnings": [],
            "doctor": {"ok": True, "checks": {"ffmpeg": True}, "issues": []}
        }
        ret = main(["--channel", "me-tech", "--slug", "test", "--dry-run"])
        self.assertEqual(ret, 0)

        mock_dry_run.return_value["valid"] = False
        mock_dry_run.return_value["errors"] = ["Missing file"]
        ret = main(["--channel", "me-tech", "--slug", "test", "--dry-run"])
        self.assertEqual(ret, 1)

if __name__ == "__main__":
    unittest.main()
