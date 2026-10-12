import unittest
from unittest.mock import patch, MagicMock
import os
import json
import urllib.error
from ops.telegram import config
from ops.telegram import client

class TestTelegramClient(unittest.TestCase):
    def setUp(self):
        self.patch_token = patch.object(config, 'TELEGRAM_BOT_TOKEN', 'test_token')
        self.patch_chat_id = patch.object(config, 'TELEGRAM_CHAT_ID', '123456789')
        self.patch_token.start()
        self.patch_chat_id.start()

    def tearDown(self):
        self.patch_token.stop()
        self.patch_chat_id.stop()

    @patch('urllib.request.urlopen')
    def test_send_message_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'ok': True, 'result': {'message_id': 100}}).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = client.send_message("<b>Hello</b>")
        self.assertTrue(res['ok'])
        self.assertEqual(res['result']['message_id'], 100)

    @patch('urllib.request.urlopen')
    def test_send_message_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.telegram.org",
            code=400,
            msg="Bad Request",
            hdrs={},
            fp=MagicMock(read=lambda: b'{"ok":false,"description":"Bad Request"}')
        )

        res = client.send_message("Test fail")
        self.assertFalse(res['ok'])
        self.assertIn("Bad Request", res['description'])

    def test_send_message_dry_run(self):
        res = client.send_message("Dry run test", dry_run=True)
        self.assertTrue(res['ok'])
        self.assertTrue(res.get('dry_run'))

    def test_send_message_unconfigured(self):
        with patch.object(config, 'TELEGRAM_BOT_TOKEN', ''):
            res = client.send_message("Unconfigured test")
            self.assertFalse(res['ok'])
            self.assertIn("not configured", res['description'].lower())

if __name__ == '__main__':
    unittest.main()
