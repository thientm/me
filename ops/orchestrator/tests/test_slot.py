import os
import json
import datetime as dt
import tempfile
import unittest

from ops.orchestrator.slot import check_channel_slot, check_all_channels, get_current_slot

class TestOrchestratorSlot(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root = self.tmp_dir.name
        self.today = dt.date(2026, 10, 12)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_get_current_slot(self):
        t1 = dt.datetime(2026, 10, 12, 7, 30)
        self.assertEqual(get_current_slot(t1), 8)

        t2 = dt.datetime(2026, 10, 12, 11, 45)
        self.assertEqual(get_current_slot(t2), 12)

        t3 = dt.datetime(2026, 10, 12, 19, 15)
        self.assertEqual(get_current_slot(t3), 20)

    def test_check_channel_slot_done(self):
        log_dir = os.path.join(self.root, "me-tech", "logs")
        os.makedirs(log_dir, exist_ok=True)
        posted_data = {
            "test-slug:youtube": {"luc": "12.10.2026 08:05", "ghi_chu": "hen 08:00"},
            "test-slug:tiktok": {"luc": "12.10.2026 08:35", "ghi_chu": "hen 08:30"},
            "test-slug:facebook": {"luc": "12.10.2026 08:05", "ghi_chu": "dang ngay"}
        }
        with open(os.path.join(log_dir, "posted.json"), "w", encoding="utf-8") as f:
            json.dump(posted_data, f)

        res = check_channel_slot("me-tech", slot=8, today=self.today, root_dir=self.root)
        self.assertEqual(res["status"], "done")
        self.assertEqual(res["slug"], "test-slug")
        self.assertEqual(len(res["posted"]), 3)
        self.assertEqual(res["missing"], [])

    def test_check_channel_slot_partial(self):
        log_dir = os.path.join(self.root, "me-tech", "logs")
        os.makedirs(log_dir, exist_ok=True)
        posted_data = {
            "partial-slug:youtube": {"luc": "12.10.2026 12:05", "ghi_chu": "hen 12:00"}
        }
        with open(os.path.join(log_dir, "posted.json"), "w", encoding="utf-8") as f:
            json.dump(posted_data, f)

        res = check_channel_slot("me-tech", slot=12, today=self.today, root_dir=self.root)
        self.assertEqual(res["status"], "partial")
        self.assertEqual(res["slug"], "partial-slug")
        self.assertIn("youtube", res["posted"])
        self.assertIn("tiktok", res["missing"])
        self.assertIn("facebook", res["missing"])

    def test_check_channel_slot_none(self):
        res = check_channel_slot("tam-an-lac", slot=20, today=self.today, root_dir=self.root)
        self.assertEqual(res["status"], "none")
        self.assertIsNone(res["slug"])
        self.assertEqual(len(res["missing"]), 3)

    def test_check_all_channels(self):
        res = check_all_channels(slot=8, today=self.today, root_dir=self.root)
        self.assertIn("me-tech", res)
        self.assertIn("thien-tran", res)
        self.assertIn("tam-an-lac", res)

if __name__ == "__main__":
    unittest.main()
