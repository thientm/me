import os
import unittest
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestCompatMeta(unittest.TestCase):
    def test_me_tech_meta_exports(self):
        cmd = [
            "python3", "-c",
            "import sys; sys.path.insert(0, 'me-tech/pipeline/publish'); import meta; "
            "assert hasattr(meta, 'VIDEO'); assert hasattr(meta, 'YT_TITLE'); "
            "assert hasattr(meta, 'FB_CAPTION'); assert hasattr(meta, 'TT_CAPTION'); print('OK')"
        ]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
        self.assertIn("OK", res.stdout)

    def test_thien_tran_meta_exports(self):
        cmd = [
            "python3", "-c",
            "import sys; sys.path.insert(0, 'thien-tran/publish'); import meta; "
            "assert hasattr(meta, 'VIDEO'); assert hasattr(meta, 'YT_TITLE'); "
            "assert hasattr(meta, 'FB_CAPTION'); assert hasattr(meta, 'TT_CAPTION'); print('OK')"
        ]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
        self.assertIn("OK", res.stdout)

    def test_tam_an_lac_meta_exports(self):
        cmd = [
            "python3", "-c",
            "import sys; sys.path.insert(0, 'tam-an-lac/_pubkit/a/publish'); import meta; "
            "assert hasattr(meta, 'VIDEO'); assert hasattr(meta, 'YT_TITLE'); "
            "assert hasattr(meta, 'FB_CAPTION'); assert hasattr(meta, 'TT_CAPTION'); print('OK')"
        ]
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
        self.assertIn("OK", res.stdout)

    def test_meta_reads_json_without_py_file(self):
        # Create a dummy content directory with meta.json only (no meta_<slug>.py)
        slug = "pure_json_test_slug"
        content_dir = os.path.join(REPO_ROOT, "me-tech", "content", slug)
        os.makedirs(content_dir, exist_ok=True)
        video_path = os.path.join(content_dir, "video.mp4")
        with open(video_path, "w") as f:
            f.write("dummy")
        with open(os.path.join(content_dir, "meta.json"), "w", encoding="utf-8") as f:
            f.write('{"video": "' + video_path + '", "yt_title": "Pure JSON Title", "yt_desc": "Desc", "fb_caption": "FB", "tt_caption": "TT"}')
        
        active_path = os.path.join(REPO_ROOT, "me-tech", "pipeline", "publish", "ACTIVE")
        if os.path.exists(active_path):
            with open(active_path, "r", encoding="utf-8") as f:
                orig_active = f.read()
        else:
            orig_active = ""
        try:
            with open(active_path, "w") as f:
                f.write(slug)
            cmd = [
                "python3", "-c",
                "import sys; sys.path.insert(0, 'me-tech/pipeline/publish'); import meta; "
                "assert meta.YT_TITLE == 'Pure JSON Title'; print('PASS_JSON')"
            ]
            res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
            self.assertIn("PASS_JSON", res.stdout)
        finally:
            if orig_active:
                with open(active_path, "w") as f:
                    f.write(orig_active)
            if os.path.exists(content_dir):
                import shutil
                shutil.rmtree(content_dir)


if __name__ == "__main__":
    unittest.main()
