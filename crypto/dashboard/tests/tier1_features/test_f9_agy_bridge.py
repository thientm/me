"""
Tier 1: Feature F9 — agy CLI Bridge & Subprocess Runner Tests.
Authoritative source: PROJECT.md §F9; spec_miner_agy_1/report.md §1 & §3.
"""

import unittest

try:
    from crypto_dashboard.agy_bridge import generate_agy_command, execute_agy_cli
    HAS_F9 = True
except ImportError:
    HAS_F9 = False


class TestF9AgyBridge(unittest.TestCase):
    """Verifies tokenless agy CLI command generation and subprocess runner."""

    def test_f9_01_command_generation_uses_agy_binary(self):
        """Authoritative Source: spec_miner_agy_1/report.md §1.1:
        Binary path is /Users/thien.tm/.local/bin/agy or 'agy'.
        """
        if not HAS_F9:
            self.skipTest("crypto_dashboard.agy_bridge not implemented yet (Milestone M3)")

        cmd = generate_agy_command(action="review")
        self.assertTrue("agy" in cmd[0])

    def test_f9_02_command_includes_dangerously_skip_permissions(self):
        """Authoritative Source: spec_miner_agy_1/report.md §1.2:
        --dangerously-skip-permissions is required for headless non-interactive execution.
        """
        if not HAS_F9:
            self.skipTest("crypto_dashboard.agy_bridge not implemented yet (Milestone M3)")

        cmd = generate_agy_command(action="review")
        self.assertIn("--dangerously-skip-permissions", cmd)

    def test_f9_03_command_includes_output_format_json(self):
        """Authoritative Source: spec_miner_agy_1/report.md §1.2:
        --output-format json ensures structured output.
        """
        if not HAS_F9:
            self.skipTest("crypto_dashboard.agy_bridge not implemented yet (Milestone M3)")

        cmd = generate_agy_command(action="review")
        self.assertIn("--output-format", cmd)
        self.assertEqual(cmd[cmd.index("--output-format") + 1], "json")

    def test_f9_04_command_includes_workspace_directory(self):
        """Authoritative Source: spec_miner_agy_1/report.md §1.2:
        --add-dir adds Personal OS workspace directory.
        """
        if not HAS_F9:
            self.skipTest("crypto_dashboard.agy_bridge not implemented yet (Milestone M3)")

        cmd = generate_agy_command(action="review", add_dirs=["/Users/thien.tm/Documents/me/crypto"])
        self.assertIn("--add-dir", cmd)
        self.assertIn("/Users/thien.tm/Documents/me/crypto", cmd)

    def test_f9_05_execution_mock_or_dry_run(self):
        """Authoritative Source: PROJECT.md §F9:
        Subprocess runner handles errors gracefully and returns execution status.
        """
        if not HAS_F9:
            self.skipTest("crypto_dashboard.agy_bridge not implemented yet (Milestone M3)")

        # Test dry-run execution
        result = execute_agy_cli(action="review", dry_run=True)
        self.assertIn("command", result)
        self.assertTrue(result.get("is_dry_run", False) or result.get("status") == "dry_run")


if __name__ == "__main__":
    unittest.main()
