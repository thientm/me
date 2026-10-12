import os
import json
import tempfile
import unittest
from ops.publish.meta_loader import load_meta, MetaData

class TestMetaLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.base_dir = self.test_dir.name

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_from_json(self):
        slug = "sample_test_slug"
        content_dir = os.path.join(self.base_dir, "content", slug)
        os.makedirs(content_dir, exist_ok=True)
        video_path = os.path.join(content_dir, "video.mp4")
        with open(video_path, "w") as f:
            f.write("dummy video")

        meta_json_path = os.path.join(content_dir, "meta.json")
        json_data = {
            "video": video_path,
            "yt_title": "Test Title for YouTube #shorts",
            "yt_desc": "Test Description for YouTube",
            "fb_caption": "Test Facebook Caption",
            "tt_caption": "Test TikTok Caption"
        }
        with open(meta_json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f)

        meta = load_meta(channel="me-tech", slug=slug, root_dir=self.base_dir)
        self.assertIsInstance(meta, MetaData)
        self.assertEqual(meta.slug, slug)
        self.assertEqual(meta.channel, "me-tech")
        self.assertEqual(meta.yt_title, "Test Title for YouTube #shorts")
        self.assertEqual(meta.yt_desc, "Test Description for YouTube")
        self.assertEqual(meta.fb_caption, "Test Facebook Caption")
        self.assertEqual(meta.tt_caption, "Test TikTok Caption")
        self.assertEqual(meta.video_path, video_path)

    def test_fallback_to_legacy_meta_py(self):
        slug = "legacy_slug"
        legacy_dir = os.path.join(self.base_dir, "legacy_publish")
        os.makedirs(legacy_dir, exist_ok=True)
        video_path = os.path.join(self.base_dir, "video.mp4")
        with open(video_path, "w") as f:
            f.write("dummy")

        legacy_py = os.path.join(legacy_dir, f"meta_{slug}.py")
        with open(legacy_py, "w", encoding="utf-8") as f:
            f.write(f'''
VIDEO = "{video_path}"
YT_TITLE = "Legacy Title"
YT_DESC = "Legacy Desc"
FB_CAPTION = "Legacy FB"
TT_CAPTION = "Legacy TT"
''')

        meta = load_meta(channel="me-tech", slug=slug, root_dir=self.base_dir, legacy_dir=legacy_dir)
        self.assertEqual(meta.yt_title, "Legacy Title")
        self.assertEqual(meta.video_path, video_path)

if __name__ == "__main__":
    unittest.main()
