import unittest
from unittest.mock import patch, MagicMock

class TestBotCryptoIntegration(unittest.TestCase):

    def test_fetch_realtime_metrics_import_and_execution(self):
        """Verify crypto.dashboard.data_collector is importable and returns valid metrics."""
        from crypto.dashboard.data_collector import fetch_realtime_metrics

        metrics = fetch_realtime_metrics()
        self.assertIn("total_tts_vnd", metrics)
        self.assertIn("btc_price", metrics)
        self.assertIn("sol_price", metrics)
        self.assertIn("p2p_rate", metrics)
        self.assertIn("floor_vnd", metrics)
        self.assertIn("recommendation", metrics)

        self.assertGreater(metrics["total_tts_vnd"], 0)
        self.assertGreater(metrics["btc_price"], 0)
        self.assertGreater(metrics["sol_price"], 0)
        self.assertGreater(metrics["p2p_rate"], 0)
        self.assertEqual(metrics["floor_vnd"], 540_000_000.0)

    @patch("ops.telegram.notifier.notify_crypto_review")
    @patch("ops.telegram.client.send_message")
    def test_handle_command_crypto(self, mock_send, mock_notify):
        """Verify /crypto command uses real metrics and does not use hardcoded 742tr fallback."""
        from ops.telegram.bot import handle_command

        handle_command("/crypto", chat_id="12345")

        # Must send waiting message
        mock_send.assert_called_with("⏳ Đang tra cứu số dư và tỷ giá Crypto...", chat_id="12345")

        # Must call notify_crypto_review with real metrics
        mock_notify.assert_called_once()
        kwargs = mock_notify.call_args.kwargs
        self.assertNotEqual(kwargs.get("tts_vnd"), 742_000_000)
        self.assertNotEqual(kwargs.get("btc_price"), 64_250)
        self.assertEqual(kwargs.get("chat_id"), "12345")
