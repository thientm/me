import unittest
from unittest.mock import patch, MagicMock

from ops.orchestrator.gates import evaluate_gate1, evaluate_gate2, GateResult

class TestOrchestratorGates(unittest.TestCase):
    @patch("ops.orchestrator.gates.get_render_config")
    @patch("ops.orchestrator.gates.validate_motion_deck")
    def test_gate1_success(self, mock_validate, mock_config):
        spec = MagicMock()
        spec.engine_type = "motion_deck"
        spec.content_path = "/mock/content.json"
        spec.shots_dir = "/mock/shots"
        mock_config.return_value = spec
        mock_validate.return_value = ([], [], 36.5)

        res = evaluate_gate1("me-tech", "test-slug")
        self.assertEqual(res.gate, 1)
        self.assertTrue(res.passed)
        self.assertEqual(res.est_duration, 36.5)
        self.assertEqual(res.errors, [])

    @patch("ops.orchestrator.gates.get_render_config")
    @patch("ops.orchestrator.gates.validate_motion_deck")
    def test_gate1_failure(self, mock_validate, mock_config):
        spec = MagicMock()
        spec.engine_type = "motion_deck"
        spec.content_path = "/mock/content.json"
        spec.shots_dir = "/mock/shots"
        mock_config.return_value = spec
        mock_validate.return_value = (["Missing hook"], [], 0.0)

        res = evaluate_gate1("me-tech", "test-slug")
        self.assertFalse(res.passed)
        self.assertEqual(res.errors, ["Missing hook"])

    @patch("ops.orchestrator.gates.run_publish_dry_run")
    def test_gate2_success(self, mock_publish_dry_run):
        mock_publish_dry_run.return_value = {
            "valid": True,
            "video_exists": True,
            "errors": [],
            "warnings": [],
            "meta": {"yt_title_len": 50, "tt_caption_len": 100},
            "cdp": {"main_connected": True}
        }

        res = evaluate_gate2("me-tech", "test-slug")
        self.assertEqual(res.gate, 2)
        self.assertTrue(res.passed)
        self.assertEqual(res.errors, [])

    @patch("ops.orchestrator.gates.run_publish_dry_run")
    def test_gate2_failure(self, mock_publish_dry_run):
        mock_publish_dry_run.return_value = {
            "valid": False,
            "video_exists": False,
            "errors": ["Video file not found"],
            "warnings": [],
            "meta": {"yt_title_len": 50, "tt_caption_len": 100},
            "cdp": {"main_connected": False}
        }

        res = evaluate_gate2("me-tech", "test-slug")
        self.assertFalse(res.passed)
        self.assertIn("Video file not found", res.errors)

if __name__ == "__main__":
    unittest.main()
