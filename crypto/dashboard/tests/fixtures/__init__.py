"""
Fixtures module providing helper access to mock files.
"""
import os

FIXTURES_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_CRYPTO_PLAN_PATH = os.path.join(FIXTURES_DIR, "mock_crypto_plan.md")
MOCK_LOGS_PATH = os.path.join(FIXTURES_DIR, "mock_logs.md")
MOCK_CACHE_RATES_PATH = os.path.join(FIXTURES_DIR, "mock_cache_rates.json")
