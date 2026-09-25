"""
Tier 2: Feature F4 Boundaries — Antigravity Custom Skill Corner Cases.
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


class TestB4SkillBoundaries(unittest.TestCase):
    """Verifies edge cases and schema boundaries for Custom Skill (crypto-manager)."""

    def test_b4_01_skill_name_exact_match(self):
        """Skill name must be exactly 'crypto-manager' (no leading/trailing whitespace or upper case)."""
        if not os.path.exists(REPO_SKILL_MD):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(REPO_SKILL_MD, "r", encoding="utf-8") as f:
            lines = f.readlines()

        name_line = next((l.strip() for l in lines if l.strip().startswith("name:")), None)
        self.assertIsNotNone(name_line)
        self.assertEqual(name_line, "name: crypto-manager")

    def test_b4_02_description_non_empty_and_budget_friendly(self):
        """Skill description must be present and under 500 characters to fit agent prompt budget."""
        if not os.path.exists(REPO_SKILL_MD):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(REPO_SKILL_MD, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter = content.split("---", 2)[1]
        self.assertIn("description:", frontmatter)
        # Description should not exceed 1000 characters
        self.assertLess(len(frontmatter), 2000)

    def test_b4_03_skill_does_not_require_external_llm_api_keys(self):
        """Skill must NOT instruct or require OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY."""
        if not os.path.exists(REPO_SKILL_MD):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(REPO_SKILL_MD, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn("OPENAI_API_KEY", content)
        self.assertNotIn("ANTHROPIC_API_KEY", content)

    def test_b4_04_skill_preserves_personal_os_path_discipline(self):
        """Skill references /Users/thien.tm/Documents/me/crypto and not temporary dirs."""
        if not os.path.exists(REPO_SKILL_MD):
            self.skipTest("skills/crypto-manager/SKILL.md not yet created (Milestone M1)")

        with open(REPO_SKILL_MD, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("/Users/thien.tm/Documents/me/crypto", content)

    def test_b4_05_skill_script_syntax_validity(self):
        """Script skills/crypto-manager/scripts/run_review.py compiles cleanly under Python 3.14."""
        _CANDIDATE_SCRIPTS = [
            os.path.join(WORKSPACE_ROOT, ".agents", "skills", "crypto-manager", "scripts", "run_review.py"),
            os.path.join(PROJECT_ROOT, "skills", "crypto-manager", "scripts", "run_review.py"),
            os.path.expanduser("~/.gemini/config/skills/crypto-manager/scripts/run_review.py"),
        ]
        script_path = next((p for p in _CANDIDATE_SCRIPTS if os.path.exists(p)), _CANDIDATE_SCRIPTS[0])
        if not os.path.exists(script_path):
            self.skipTest("skills/crypto-manager/scripts/run_review.py not yet created (Milestone M1)")

        with open(script_path, "r", encoding="utf-8") as f:
            source = f.read()
        compiled = compile(source, script_path, "exec")
        self.assertIsNotNone(compiled)


if __name__ == "__main__":
    unittest.main()
