import unittest
from ops.orchestrator.brainstorm import get_brainstorm_prompt, generate_scaffold

class TestOrchestratorBrainstorm(unittest.TestCase):
    def test_me_tech_prompt(self):
        prompt = get_brainstorm_prompt("me-tech", topic="Claude 3.7 Sonnet Released")
        self.assertIn("Mê Tech", prompt)
        self.assertIn("Claude 3.7 Sonnet Released", prompt)
        self.assertIn("AI dễ hiểu", prompt)
        self.assertIn("hook", prompt.lower())

    def test_thien_tran_prompt(self):
        prompt = get_brainstorm_prompt("thien-tran", topic="OpenAI Orion Benchmark")
        self.assertIn("Thiện Trần", prompt)
        self.assertIn("FACT", prompt)
        self.assertIn("INFERENCE", prompt)
        self.assertIn("OPINION", prompt)
        self.assertIn("Hype", prompt)

    def test_tam_an_lac_prompt(self):
        prompt = get_brainstorm_prompt("tam-an-lac", topic="Áp lực đầu tuần")
        self.assertIn("Tâm An Lạc", prompt)
        self.assertIn("Phật dạy", prompt)
        self.assertIn("hình ảnh", prompt.lower())

    def test_generate_scaffold_me_tech(self):
        scaffold = generate_scaffold("me-tech", slug="test-ai", title="AI Mới")
        self.assertEqual(scaffold["slug"], "test-ai")
        self.assertEqual(scaffold["brand"], "MÊ TECH")
        self.assertIn("segments", scaffold)
        self.assertEqual(scaffold["segments"][-1]["mode"], "outro")

    def test_generate_scaffold_tam_an_lac(self):
        scaffold = generate_scaffold("tam-an-lac", slug="test-zen", title="Bình An")
        self.assertEqual(scaffold["slug"], "test-zen")
        self.assertEqual(scaffold["voice"], "Thiền Tâm Đức")
        self.assertIn("segments", scaffold)

if __name__ == "__main__":
    unittest.main()
