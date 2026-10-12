import os
import unittest
from ops.render.config import get_render_config, RenderSpec

class TestRenderConfig(unittest.TestCase):
    def test_me_tech_config(self):
        spec = get_render_config("me-tech", "test-slug", root_dir="/mock/root")
        self.assertEqual(spec.channel, "me-tech")
        self.assertEqual(spec.slug, "test-slug")
        self.assertEqual(spec.engine_type, "motion_deck")
        self.assertEqual(spec.content_path, "/mock/root/me-tech/pipeline/content/test-slug.json")
        self.assertEqual(spec.output_video, "/mock/root/me-tech/render/test-slug.mp4")
        self.assertEqual(spec.shots_dir, "/mock/root/me-tech/pipeline/shots")

    def test_thien_tran_config(self):
        spec = get_render_config("thien-tran", "test-slug", root_dir="/mock/root")
        self.assertEqual(spec.channel, "thien-tran")
        self.assertEqual(spec.slug, "test-slug")
        self.assertEqual(spec.engine_type, "motion_deck")
        self.assertEqual(spec.content_path, "/mock/root/thien-tran/content/test-slug.json")
        self.assertEqual(spec.output_video, "/mock/root/thien-tran/render/test-slug.mp4")
        self.assertEqual(spec.shots_dir, "/mock/root/thien-tran/shots")

    def test_tam_an_lac_config(self):
        spec = get_render_config("tam-an-lac", "038_bua_trua", root_dir="/mock/root")
        self.assertEqual(spec.channel, "tam-an-lac")
        self.assertEqual(spec.slug, "038_bua_trua")
        self.assertEqual(spec.engine_type, "zen_meditation")
        self.assertEqual(spec.content_path, "/mock/root/tam-an-lac/content/038_bua_trua/script.json")
        self.assertEqual(spec.output_video, "/mock/root/tam-an-lac/content/038_bua_trua/video.mp4")
        self.assertEqual(spec.content_dir, "/mock/root/tam-an-lac/content/038_bua_trua")

    def test_unknown_channel(self):
        with self.assertRaises(ValueError):
            get_render_config("unknown-channel", "test-slug")

if __name__ == "__main__":
    unittest.main()
