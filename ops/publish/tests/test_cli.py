import os
import unittest
import tempfile
import json
from unittest.mock import patch, MagicMock

from ops.publish.meta_loader import MetaData
from ops.publish.cli import validate_meta, check_cdp_connection, run_dry_run, build_parser, main

class TestPublishCli(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root_dir = self.tmp_dir.name
        self.video_file = os.path.join(self.root_dir, "test.mp4")
        with open(self.video_file, "w") as f:
            f.write("dummy video")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_build_parser(self):
        parser = build_parser()
        args = parser.parse_args(["--channel", "me-tech", "--slug", "my-slug", "--dry-run", "--platform", "yt", "--at", "08:00"])
        self.assertEqual(args.channel, "me-tech")
        self.assertEqual(args.slug, "my-slug")
        self.assertTrue(args.dry_run)
        self.assertEqual(args.platform, "yt")
        self.assertEqual(args.at, "08:00")

    def test_validate_meta_valid(self):
        meta = MetaData(
            video_path=self.video_file,
            yt_title="A Valid Title Under 100 Chars",
            yt_desc="Some desc",
            fb_caption="Some fb caption",
            tt_caption="Some tt caption #hashtag",
            slug="test-slug",
            channel="me-tech"
        )
        errors, warnings = validate_meta(meta)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_validate_meta_missing_video(self):
        meta = MetaData(
            video_path=os.path.join(self.root_dir, "nonexistent.mp4"),
            yt_title="Title",
            yt_desc="Desc",
            fb_caption="FB",
            tt_caption="TT",
            slug="test-slug",
            channel="me-tech"
        )
        errors, warnings = validate_meta(meta)
        self.assertTrue(any("nonexistent.mp4" in e for e in errors))

    def test_validate_meta_long_title(self):
        meta = MetaData(
            video_path=self.video_file,
            yt_title="A" * 105,
            yt_desc="Desc",
            fb_caption="FB",
            tt_caption="TT",
            slug="test-slug",
            channel="me-tech"
        )
        errors, warnings = validate_meta(meta)
        self.assertTrue(any("100" in e for e in errors))

    @patch("urllib.request.urlopen")
    def test_check_cdp_connection(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_resp
        self.assertTrue(check_cdp_connection(9333))

        mock_urlopen.side_effect = Exception("Connection refused")
        self.assertFalse(check_cdp_connection(9333))

    @patch("ops.publish.cli.check_cdp_connection")
    @patch("ops.publish.cli.load_meta")
    def test_run_dry_run_success(self, mock_load_meta, mock_cdp):
        mock_load_meta.return_value = MetaData(
            video_path=self.video_file,
            yt_title="Valid Title",
            yt_desc="Desc",
            fb_caption="FB",
            tt_caption="TT",
            slug="test-slug",
            channel="me-tech"
        )
        mock_cdp.return_value = True

        result = run_dry_run(channel="me-tech", slug="test-slug", platform="all")
        self.assertTrue(result["valid"])
        self.assertTrue(result["video_exists"])
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["cdp"]["main_connected"])
        self.assertEqual(result["meta"]["yt_title_len"], len("Valid Title"))

    @patch("ops.publish.cli.run_dry_run")
    def test_main_dry_run_exit_code(self, mock_dry_run):
        mock_dry_run.return_value = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "channel": "me-tech",
            "slug": "test-slug",
            "platform": "all",
            "video_path": self.video_file,
            "video_exists": True,
            "meta": {"yt_title": "T", "yt_title_len": 1, "tt_caption_len": 1, "fb_caption_len": 1},
            "cdp": {"main_port": 9333, "main_connected": True, "fb_port": 9333, "fb_connected": True}
        }
        ret = main(["--channel", "me-tech", "--slug", "test-slug", "--dry-run"])
        self.assertEqual(ret, 0)

        mock_dry_run.return_value["valid"] = False
        mock_dry_run.return_value["errors"] = ["Video missing"]
        ret = main(["--channel", "me-tech", "--slug", "test-slug", "--dry-run"])
        self.assertEqual(ret, 1)

if __name__ == "__main__":
    unittest.main()
