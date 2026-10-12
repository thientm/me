import os
import json
import tempfile
import unittest

from ops.render.validator import validate_motion_deck, validate_zen_meditation

class TestRenderValidator(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root = self.tmp_dir.name
        self.shots_dir = os.path.join(self.root, "shots")
        os.makedirs(self.shots_dir, exist_ok=True)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_motion_deck_valid(self):
        shot_img = os.path.join(self.shots_dir, "test_shot.png")
        with open(shot_img, "w") as f:
            f.write("img")

        content = {
            "slug": "valid-slug",
            "brand": "Mê Tech",
            "kicker": "TIN HOT",
            "date": "12.10.2026",
            "outro": "Outro text",
            "segments": [
                {
                    "id": "hook",
                    "group": "intro",
                    "mode": "say",
                    "say": "AI vừa có bước tiến lớn hôm nay.",
                    "words": ["AI", "vừa", "có", "bước", "tiến", "lớn", "hôm", "nay"],
                    "weights": [1, 1, 1, 1, 1, 1, 1, 1]
                },
                {
                    "id": "evidence",
                    "group": "body",
                    "mode": "shot",
                    "shot": "test_shot.png",
                    "src": "Reuters",
                    "say": "Báo cáo xác nhận số liệu.",
                    "words": ["Báo", "cáo", "xác", "nhận", "số", "liệu"],
                    "weights": [1, 1, 1, 1, 1, 1]
                },
                {
                    "id": "outro",
                    "group": "outro",
                    "mode": "outro",
                    "words": [],
                    "weights": []
                }
            ]
        }
        cpath = os.path.join(self.root, "content.json")
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(content, f)

        err, warn, dur = validate_motion_deck(cpath, shots_dir=self.shots_dir)
        self.assertEqual(err, [])
        self.assertGreater(dur, 0)

    def test_motion_deck_missing_shot(self):
        content = {
            "slug": "missing-shot-slug",
            "brand": "Mê Tech",
            "kicker": "TIN",
            "date": "12.10.2026",
            "outro": "Outro",
            "segments": [
                {
                    "id": "evidence",
                    "group": "body",
                    "mode": "shot",
                    "shot": "nonexistent.png",
                    "src": "Reuters",
                    "say": "Báo cáo xác nhận.",
                    "words": ["Báo", "cáo"],
                    "weights": [1, 1]
                },
                {"id": "outro", "group": "outro", "mode": "outro", "words": [], "weights": []}
            ]
        }
        cpath = os.path.join(self.root, "content.json")
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(content, f)

        err, warn, dur = validate_motion_deck(cpath, shots_dir=self.shots_dir)
        self.assertTrue(any("nonexistent.png" in e for e in err))

    def test_motion_deck_weights_mismatch(self):
        content = {
            "slug": "mismatch-slug",
            "brand": "Mê Tech",
            "kicker": "TIN",
            "date": "12.10.2026",
            "outro": "Outro",
            "segments": [
                {
                    "id": "s1",
                    "group": "body",
                    "mode": "say",
                    "say": "Một hai ba.",
                    "words": ["Một", "hai", "ba"],
                    "weights": [1, 1] # length 2 != 3
                },
                {"id": "outro", "group": "outro", "mode": "outro", "words": [], "weights": []}
            ]
        }
        cpath = os.path.join(self.root, "content.json")
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(content, f)

        err, warn, dur = validate_motion_deck(cpath, shots_dir=self.shots_dir)
        self.assertTrue(any("weights" in e for e in err))

    def test_zen_meditation_valid(self):
        content_dir = os.path.join(self.root, "001_zen")
        os.makedirs(content_dir, exist_ok=True)
        with open(os.path.join(content_dir, "img_1.jpg"), "w") as f:
            f.write("img")

        script = {
            "slug": "001_zen",
            "voice": "Thiền Tâm Đức",
            "lead_in": 0.5,
            "gap": 0.5,
            "tail": 3.0,
            "segments": [
                {"id": "s1", "text": "Hít một hơi thật sâu và thở ra nhẹ nhàng."},
                {"id": "s2", "text": "Mọi ưu phiền xin hãy để lại sau lưng."}
            ]
        }
        cpath = os.path.join(content_dir, "script.json")
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(script, f)

        err, warn, dur = validate_zen_meditation(cpath, content_dir=content_dir)
        self.assertEqual(err, [])
        self.assertGreater(dur, 0)

    def test_zen_meditation_missing_images(self):
        content_dir = os.path.join(self.root, "002_zen")
        os.makedirs(content_dir, exist_ok=True)
        script = {
            "slug": "002_zen",
            "voice": "Thiền Tâm Đức",
            "segments": [{"id": "s1", "text": "Hít thở đều đặn."}]
        }
        cpath = os.path.join(content_dir, "script.json")
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(script, f)

        err, warn, dur = validate_zen_meditation(cpath, content_dir=content_dir)
        self.assertTrue(any("hình ảnh" in e.lower() or "image" in e.lower() for e in err))

if __name__ == "__main__":
    unittest.main()
