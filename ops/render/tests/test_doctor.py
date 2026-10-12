import unittest
from unittest.mock import patch, MagicMock
from ops.render.doctor import check_environment

class TestRenderDoctor(unittest.TestCase):
    @patch("shutil.which")
    @patch("os.path.exists")
    def test_doctor_all_passed(self, mock_exists, mock_which):
        mock_which.return_value = "/usr/local/bin/dummy"
        mock_exists.return_value = True

        res = check_environment()
        self.assertTrue(res["ok"])
        self.assertEqual(res["issues"], [])
        self.assertTrue(res["checks"]["ffmpeg"])
        self.assertTrue(res["checks"]["uv"])
        self.assertTrue(res["checks"]["font"])

    @patch("shutil.which")
    @patch("os.path.exists")
    def test_doctor_missing_ffmpeg(self, mock_exists, mock_which):
        def fake_which(cmd):
            return None if cmd == "ffmpeg" else "/usr/local/bin/dummy"
        mock_which.side_effect = fake_which
        mock_exists.return_value = True

        res = check_environment()
        self.assertFalse(res["ok"])
        self.assertIn("ffmpeg", res["issues"][0].lower())

    @patch("shutil.which")
    @patch("os.path.exists")
    def test_doctor_missing_font(self, mock_exists, mock_which):
        mock_which.return_value = "/usr/local/bin/dummy"
        def fake_exists(path):
            if "BeVietnamPro" in path:
                return False
            return True
        mock_exists.side_effect = fake_exists

        res = check_environment()
        self.assertFalse(res["ok"])
        self.assertTrue(any("font" in i.lower() for i in res["issues"]))

if __name__ == "__main__":
    unittest.main()
