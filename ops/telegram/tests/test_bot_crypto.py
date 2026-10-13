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
        self.assertEqual(metrics["floor_vnd"], 500_000_000.0)

    def test_run_master_review_all_execution(self):
        """Verify run_master_review_all returns all cross-domain components."""
        from crypto.dashboard.data_collector import run_master_review_all

        all_data = run_master_review_all()
        self.assertIn("crypto", all_data)
        self.assertIn("snapshot", all_data)
        self.assertIn("matrix", all_data)
        self.assertIn("bds_gap", all_data)
        self.assertIn("pipeline", all_data)
        self.assertEqual(all_data["bds_gap"]["total_budget_vnd"], 3_100_000_000.0)

    @patch("ops.telegram.notifier.notify_crypto_review")
    @patch("ops.telegram.client.send_message")
    def test_handle_command_crypto_pure_crypto(self, mock_send, mock_notify):
        """Verify /crypto command focuses strictly on crypto portfolio & risk management."""
        from ops.telegram.bot import handle_command

        handle_command("/crypto", chat_id="12345")

        mock_send.assert_called_with("⏳ Đang tra cứu danh mục Crypto & tính toán quản trị rủi ro...", chat_id="12345")
        mock_notify.assert_called_once()
        kwargs = mock_notify.call_args.kwargs
        self.assertEqual(kwargs.get("chat_id"), "12345")
        self.assertIn("crypto_data", kwargs)
        self.assertNotEqual(kwargs.get("tts_vnd"), 742_000_000)

    @patch("ops.telegram.notifier.notify_master_review")
    @patch("ops.telegram.client.send_message")
    def test_handle_command_review_all(self, mock_send, mock_notify_master):
        """Verify /review command triggers Master Review ALL."""
        from ops.telegram.bot import handle_command

        handle_command("/review", chat_id="12345")

        mock_send.assert_called_with("⏳ Đang chạy Personal OS Master Review (ALL: Tài chính, BĐS, Crypto, Video)...", chat_id="12345")
        mock_notify_master.assert_called_once()
        kwargs = mock_notify_master.call_args.kwargs
        self.assertEqual(kwargs.get("chat_id"), "12345")
        self.assertIn("bds_gap", kwargs.get("review_all_data", {}))
        self.assertIn("pipeline", kwargs.get("review_all_data", {}))
