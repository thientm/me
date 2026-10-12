import unittest
from unittest.mock import patch
from ops.telegram import notifier

class TestTelegramNotifier(unittest.TestCase):

    @patch('ops.telegram.client.send_message')
    def test_notify_crypto_review(self, mock_send):
        mock_send.return_value = {"ok": True}
        res = notifier.notify_crypto_review(
            tts_vnd=512500000,
            btc_price=84140,
            sol_price=113.0,
            p2p_rate=25895,
            floor_vnd=540000000,
            action_note="Bán toàn bộ SOL ra USDT"
        )
        self.assertTrue(res["ok"])
        mock_send.assert_called_once()
        text = mock_send.call_args[0][0]
        self.assertIn("CRYPTO DAILY REVIEW", text)
        self.assertIn("512.500.000 VND", text)
        self.assertIn("540.000.000 VND", text)
        self.assertIn("Thủng 27.500.000 VND", text)
        self.assertIn("Bán toàn bộ SOL ra USDT", text)

    @patch('ops.telegram.client.send_message')
    def test_notify_pipeline_status(self, mock_send):
        mock_send.return_value = {"ok": True}
        res = notifier.notify_pipeline_status(
            slot="12:00",
            channel="Mê Tech",
            slug="quinnipiac-ai-trust-crisis",
            gates={
                "Gate 1": True,
                "Gate 2": True,
                "Render": True,
                "Publish": True
            }
        )
        self.assertTrue(res["ok"])
        mock_send.assert_called_once()
        text = mock_send.call_args[0][0]
        self.assertIn("VIDEO PIPELINE — KHUNG GIỜ 12:00", text)
        self.assertIn("Mê Tech", text)
        self.assertIn("quinnipiac-ai-trust-crisis", text)
        self.assertIn("Gate 1: ✅ PASS", text)

    @patch('ops.telegram.client.send_message')
    def test_notify_alert(self, mock_send):
        mock_send.return_value = {"ok": True}
        res = notifier.notify_alert(
            source="Mê Tech Video Pipeline",
            error_msg="Chrome CDP port 9222 offline",
            action_needed="Khởi động lại trình duyệt Chrome với remote debugging port"
        )
        self.assertTrue(res["ok"])
        mock_send.assert_called_once()
        text = mock_send.call_args[0][0]
        self.assertIn("CẢNH BÁO HỆ THỐNG", text)
        self.assertIn("Mê Tech Video Pipeline", text)
        self.assertIn("Chrome CDP port 9222 offline", text)

if __name__ == '__main__':
    unittest.main()
