"""
Tier 3: Interaction 4 — CLI -> Server -> agy Bridge Pipeline.
Authoritative source: PROJECT.md §F7, §F8 & §F9; ORIGINAL_REQUEST.md §R3.
"""

import unittest

try:
    from crypto_dashboard.api_handlers import handle_api_route
    from crypto_dashboard.agy_bridge import generate_agy_command
    HAS_CLI_SERVER_BRIDGE = True
except ImportError:
    HAS_CLI_SERVER_BRIDGE = False


class TestInteractionCLIServerBridge(unittest.TestCase):
    """Verifies that API endpoint /api/agy/command produces valid agy CLI execution strings."""

    def test_api_agy_command_endpoint_generates_executable_command(self):
        """POST /api/agy/command with action='review' returns tokenless agy shell command."""
        if not HAS_CLI_SERVER_BRIDGE:
            self.skipTest("crypto_dashboard modules not implemented yet (Milestone M3)")

        payload = {"action": "review"}
        code, body = handle_api_route("POST", "/api/agy/command", payload)
        self.assertEqual(code, 200)

        data = body.get("data", {})
        command_str = data.get("command", "")
        self.assertTrue("agy" in command_str)
        self.assertTrue("-p" in command_str or "--print" in command_str)
        self.assertTrue("--dangerously-skip-permissions" in command_str)


if __name__ == "__main__":
    unittest.main()
