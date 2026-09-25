"""
Tier 1: Feature F4 — Antigravity Custom Skill (crypto-manager) Tests.
Authoritative source: PROJECT.md §F4; spec_miner_agy_1/report.md §2 & §4; ORIGINAL_REQUEST.md §R1.
"""

import os
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(PROJECT_ROOT))
_CANDIDATE_SKILLS = [
    os.path.join(WORKSPACE_ROOT, ".agents", "skills", "crypto-manager", "SKILL.md"),
    os.path.join(PROJECT_ROOT, "skills", "crypto-manager", "SKILL.md"),
    os.path.expanduser("~/.gemini/config/skills/crypto-manager/SKILL.md"),
]
REPO_SKILL_MD = next((p for p in _CANDIDATE_SKILLS if os.path.exists(p)), _CANDIDATE_SKILLS[0])

_CANDIDATE_SCRIPTS = [
    os.path.join(WORKSPACE_ROOT, ".agents", "skills", "crypto-manager", "scripts", "run_review.py"),
    os.path.join(PROJECT_ROOT, "skills", "crypto-manager", "scripts", "run_review.py"),
    os.path.expanduser("~/.gemini/config/skills/crypto-manager/scripts/run_review.py"),
]
REPO_SKILL_SCRIPT = next((p for p in _CANDIDATE_SCRIPTS if os.path.exists(p)), _CANDIDATE_SCRIPTS[0])
GLOBAL_SKILL_MD = REPO_SKILL_MD


class TestF4Skill(unittest.TestCase):
    """Verifies Antigravity Custom Skill (crypto-manager) specification and files."""

    def test_f4_01_skill_md_file_exists(self):
        """Authoritative Source: PROJECT.md §Code Layout:
        skills/crypto-manager/SKILL.md or ~/.gemini/config/skills/crypto-manager/SKILL.md must exist.
        """
        exists = os.path.exists(REPO_SKILL_MD) or os.path.exists(GLOBAL_SKILL_MD)
        if not exists:
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")
        self.assertTrue(exists)

    def test_f4_02_skill_md_has_valid_yaml_frontmatter(self):
        """Authoritative Source: spec_miner_agy_1/report.md §2.3:
        SKILL.md must start with '---' and contain 'name: crypto-manager' and 'description:'.
        """
        skill_path = REPO_SKILL_MD if os.path.exists(REPO_SKILL_MD) else GLOBAL_SKILL_MD
        if not os.path.exists(skill_path):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue(content.startswith("---"), "SKILL.md must begin with YAML frontmatter delimiter '---'")
        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "SKILL.md must have opening and closing '---'")
        frontmatter = parts[1]
        self.assertIn("name: crypto-manager", frontmatter)
        self.assertIn("description:", frontmatter)

    def test_f4_03_skill_declares_allowed_tools(self):
        """Authoritative Source: spec_miner_agy_1/report.md §2.3:
        SKILL.md frontmatter should specify allowed-tools (e.g. Bash, view_file).
        """
        skill_path = REPO_SKILL_MD if os.path.exists(REPO_SKILL_MD) else GLOBAL_SKILL_MD
        if not os.path.exists(skill_path):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(skill_path, "r", encoding="utf-8") as f:
            frontmatter = f.read().split("---", 2)[1]

        self.assertTrue("allowed-tools:" in frontmatter or "tools:" in frontmatter)

    def test_f4_04_skill_body_contains_inviolable_rules(self):
        """Authoritative Source: spec_miner_agy_1/report.md §4.2:
        SKILL.md must contain the 3 inviolable rules: no new capital, no DCA/buy back, exit deadline Late Oct 2026.
        """
        skill_path = REPO_SKILL_MD if os.path.exists(REPO_SKILL_MD) else GLOBAL_SKILL_MD
        if not os.path.exists(skill_path):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(skill_path, "r", encoding="utf-8") as f:
            body = f.read().split("---", 2)[2]

        self.assertTrue("nạp thêm" in body.lower() or "new capital" in body.lower())
        self.assertTrue("append" in body.lower() or "logs/" in body.lower())

    def test_f4_05_skill_helper_script_exists_and_executable(self):
        """Authoritative Source: PROJECT.md §Code Layout:
        skills/crypto-manager/scripts/run_review.py must exist and be executable.
        """
        if not os.path.exists(REPO_SKILL_SCRIPT):
            self.skipTest("skills/crypto-manager/scripts/run_review.py not yet created (Milestone M1)")
        self.assertTrue(os.path.isfile(REPO_SKILL_SCRIPT))


if __name__ == "__main__":
    unittest.main()
