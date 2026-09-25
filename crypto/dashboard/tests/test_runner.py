#!/usr/bin/env python3
"""
Test Runner for Crypto Portfolio Management Skill and Dashboard.
Discovers and executes tests across all tiers (Tier 1 to Tier 4).
Returns exit code 0 on all pass, exit code 1 on failure.
"""

import os
import sys
import unittest
import time
import argparse

# Ensure src/ and project root are in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FormattedTestResult(unittest.TextTestResult):
    """Custom test result collector for structured reporting."""

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_records = []

    def startTest(self, test):
        super().startTest(test)
        self._start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - self._start_time
        self.test_records.append((test.id(), "PASS", elapsed, ""))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        elapsed = time.time() - self._start_time
        self.test_records.append((test.id(), "FAIL", elapsed, self._exc_info_to_string(err, test)))

    def addError(self, test, err):
        super().addError(test, err)
        elapsed = time.time() - self._start_time
        self.test_records.append((test.id(), "ERROR", elapsed, self._exc_info_to_string(err, test)))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        elapsed = time.time() - self._start_time
        self.test_records.append((test.id(), "SKIP", elapsed, reason))


def run_test_suite(tier: str = None, pattern: str = "test_*.py", verbosity: int = 1) -> int:
    """Discovers and runs test suites, reporting structured summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    tier_dirs = {
        "tier1": os.path.join(TESTS_DIR, "tier1_features"),
        "tier2": os.path.join(TESTS_DIR, "tier2_boundaries"),
        "tier3": os.path.join(TESTS_DIR, "tier3_interactions"),
        "tier4": os.path.join(TESTS_DIR, "tier4_scenarios"),
    }

    if tier and tier in tier_dirs:
        target_dir = tier_dirs[tier]
        if os.path.exists(target_dir):
            discovered = loader.discover(start_dir=target_dir, pattern=pattern, top_level_dir=PROJECT_ROOT)
            suite.addTests(discovered)
    else:
        for t_name, t_dir in tier_dirs.items():
            if os.path.exists(t_dir):
                discovered = loader.discover(start_dir=t_dir, pattern=pattern, top_level_dir=PROJECT_ROOT)
                suite.addTests(discovered)

    print("=" * 80)
    print(f"CRYPTO PORTFOLIO TEST RUNNER — E2E TEST SUITE")
    print(f"Target: {tier or 'All Tiers (Tiers 1-4)'} | Pattern: {pattern}")
    print("=" * 80)

    runner = unittest.TextTestRunner(verbosity=verbosity, resultclass=FormattedTestResult)
    start_total = time.time()
    result = runner.run(suite)
    total_elapsed = time.time() - start_total

    print("\n" + "=" * 80)
    print("TEST EXECUTION SUMMARY REPORT")
    print("=" * 80)
    print(f"Total Tests Run   : {result.testsRun}")
    print(f"Passed            : {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures          : {len(result.failures)}")
    print(f"Errors            : {len(result.errors)}")
    print(f"Skipped (Pending) : {len(result.skipped)}")
    print(f"Total Duration    : {total_elapsed:.3f}s")
    print("=" * 80)

    if result.failures:
        print("\n--- FAILURES ---")
        for test, msg in result.failures:
            print(f"\n[FAIL] {test.id()}:\n{msg}")

    if result.errors:
        print("\n--- ERRORS ---")
        for test, msg in result.errors:
            print(f"\n[ERROR] {test.id()}:\n{msg}")

    if result.wasSuccessful():
        print("\nOVERALL RESULT: [PASS] All executed tests passed successfully.\n")
        return 0
    else:
        print("\nOVERALL RESULT: [FAIL] Test failures or errors detected.\n")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Crypto Dashboard E2E Test Runner")
    parser.add_argument("--tier", choices=["tier1", "tier2", "tier3", "tier4"], default=None, help="Filter by tier")
    parser.add_argument("--pattern", default="test_*.py", help="Test filename glob pattern")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    verbosity = 2 if args.verbose else 1
    exit_code = run_test_suite(tier=args.tier, pattern=args.pattern, verbosity=verbosity)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
