import unittest
from ops.publish.config import get_channel_config, ChannelConfig

class TestConfig(unittest.TestCase):
    def test_get_me_tech_config(self):
        cfg = get_channel_config("me-tech")
        self.assertIsInstance(cfg, ChannelConfig)
        self.assertEqual(cfg.name, "me-tech")
        self.assertEqual(cfg.cdp_port, 9333)
        self.assertEqual(cfg.yt_channel_id, "UCnElgDX9q_AYGdFc2oDuWUA")
        self.assertEqual(cfg.fb_type, "page_business_suite")
        self.assertEqual(cfg.fb_asset_id, "403727472998689")

    def test_get_thien_tran_config(self):
        cfg = get_channel_config("thien-tran")
        self.assertEqual(cfg.name, "thien-tran")
        self.assertEqual(cfg.cdp_port, 9444)
        self.assertEqual(cfg.fb_cdp_port, 9333)
        self.assertEqual(cfg.yt_channel_id, "UCvoMD_dBm8z1i-Zd8Pwu7mQ")
        self.assertEqual(cfg.fb_type, "personal_profile")

    def test_get_tam_an_lac_config(self):
        cfg = get_channel_config("tam-an-lac")
        self.assertEqual(cfg.name, "tam-an-lac")
        self.assertEqual(cfg.cdp_port, 9555)
        self.assertEqual(cfg.fb_cdp_port, 9333)
        self.assertEqual(cfg.yt_channel_id, "UCjEteQMJ4zzFV9_iKvChpvA")
        self.assertEqual(cfg.fb_type, "page_business_suite")

    def test_unknown_channel_raises(self):
        with self.assertRaises(ValueError):
            get_channel_config("unknown_channel")

if __name__ == "__main__":
    unittest.main()
