"""
Tier 5: Adversarial Stress Testing — M2-2 BHT-Ticker & AVC-Meter.
Written by challenger_m2_2 for empirical verification of:
1. Negative and zero delay in hesitation tax (hours_delayed = -10, 0, 10000).
2. Commitment device at exact boundary points: 0s, 599s, 600s, 601s.
3. Volatility cushion when TTS is severely below 540tr floor (TTS = 100M VND, cushion = -440M VND).
4. Zero daily ATR (portfolio_daily_atr_pct = 0.0) — ZeroDivisionError prevention.
5. Zero crypto (crypto_vnd = 0.0) — 100% cash portfolios.
6. CPPI limits, negative k_factor, degenerate net worth (TTS <= 0), and property fuzzing.
"""

import unittest
import math
import random

from crypto_engine.quant.hesitation_tax import (
    calculate_hesitation_tax,
    get_commitment_device_status,
    COMMITMENT_DEVICE_SECONDS,
    DEFAULT_LAND_FEE_VND,
    LAND_2027_HAZARD_MAX_VND,
)
from crypto_engine.quant.volatility_cushion import (
    calculate_volatility_cushion,
    DEFAULT_HARD_FLOOR_VND,
    DEFAULT_PORTFOLIO_ATR_PCT,
    DEFAULT_CPPI_MULTIPLIER,
)


class TestAdversarialBHTandAVC(unittest.TestCase):
    """Adversarial stress harness for BHT-Ticker and AVC-Meter."""

    # -------------------------------------------------------------------------
    # 1. HESITATION TAX: NEGATIVE & ZERO DELAY STRESS TESTS
    # -------------------------------------------------------------------------

    def test_adv_01_hesitation_tax_negative_delays(self):
        """Negative delay hours must be clamped to 0.0 and produce zero late penalty."""
        for neg_hours in [-0.0001, -1.0, -10.0, -168.0, -1_000_000.0]:
            result = calculate_hesitation_tax(hours_delayed=neg_hours)
            self.assertEqual(
                result["hours_delayed"],
                0.0,
                f"Negative hours {neg_hours} was not clamped to 0.0",
            )
            self.assertEqual(
                result["tax_late_penalty_vnd"],
                0.0,
                f"Negative hours {neg_hours} produced non-zero tax penalty",
            )
            self.assertEqual(
                result["land_2027_hazard_exposure_vnd"],
                0.0,
                f"Negative hours {neg_hours} accrued 2027 land hazard",
            )
            self.assertEqual(result["total_hesitation_tax_vnd"], 0.0)
            self.assertEqual(result["status_level"], "NORMAL")

    def test_adv_02_hesitation_tax_exact_zero_delay(self):
        """Exact zero delay must have zero penalty but retain statutory hourly burn rate."""
        result = calculate_hesitation_tax(hours_delayed=0.0)
        self.assertEqual(result["hours_delayed"], 0.0)
        self.assertEqual(result["tax_late_penalty_vnd"], 0.0)
        self.assertEqual(result["land_2027_hazard_exposure_vnd"], 0.0)
        self.assertEqual(result["total_hesitation_tax_vnd"], 0.0)
        self.assertEqual(result["burn_rate_vnd_per_hour"], 38750.0)
        self.assertAlmostEqual(result["burn_rate_vnd_per_second"], 10.7639, places=4)
        self.assertEqual(result["status_level"], "NORMAL")

    def test_adv_03_hesitation_tax_extreme_large_delays(self):
        """Extreme large delays (10,000h, 1M h) must scale penalty linearly and cap hazard at 370M."""
        for large_hours in [888.0, 1000.0, 10000.0, 1_000_000.0]:
            result = calculate_hesitation_tax(hours_delayed=large_hours)
            expected_penalty = round(large_hours * 38750.0, 2)
            self.assertEqual(result["tax_late_penalty_vnd"], expected_penalty)
            self.assertEqual(
                result["land_2027_hazard_exposure_vnd"],
                LAND_2027_HAZARD_MAX_VND,
                f"Hazard for {large_hours}h exceeded or did not reach max cap 370M",
            )
            self.assertEqual(
                result["total_hesitation_tax_vnd"],
                round(expected_penalty + LAND_2027_HAZARD_MAX_VND, 2),
            )
            self.assertEqual(result["status_level"], "WARNING")

    def test_adv_04_hesitation_tax_negative_land_fee_and_unexecuted(self):
        """Negative land fee and negative unexecuted counts must be clamped to safe non-negative values."""
        result = calculate_hesitation_tax(
            land_fee_vnd=-3_100_000_000.0,
            hours_delayed=10.0,
            unexecuted_count=-5,
            market_slippage_loss_vnd=-500_000.0,
        )
        self.assertEqual(result["land_fee_vnd"], 0.0)
        self.assertEqual(result["burn_rate_vnd_per_hour"], 0.0)
        self.assertEqual(result["burn_rate_vnd_per_second"], 0.0)
        self.assertEqual(result["tax_late_penalty_vnd"], 0.0)
        self.assertEqual(result["unexecuted_count"], 0)
        self.assertEqual(result["market_slippage_loss_vnd"], 0.0)

    def test_adv_05_hesitation_tax_status_escalation_thresholds(self):
        """Verify exact status escalation boundaries at unexecuted counts: 0..2 (NORMAL), 3..12 (WARNING), >=13 (DEFCON_1)."""
        # Normal range
        for c in [0, 1, 2]:
            res = calculate_hesitation_tax(hours_delayed=0.0, unexecuted_count=c)
            self.assertEqual(res["status_level"], "NORMAL", f"Count {c} should be NORMAL")

        # Warning range
        for c in [3, 5, 12]:
            res = calculate_hesitation_tax(hours_delayed=0.0, unexecuted_count=c)
            self.assertEqual(res["status_level"], "WARNING", f"Count {c} should be WARNING")

        # DEFCON-1 paralysis
        for c in [13, 14, 50, 100]:
            res = calculate_hesitation_tax(hours_delayed=0.0, unexecuted_count=c)
            self.assertEqual(res["status_level"], "DEFCON_1_PARALYSIS", f"Count {c} should be DEFCON_1_PARALYSIS")

    # -------------------------------------------------------------------------
    # 2. COMMITMENT DEVICE: EXACT BOUNDARY POINTS (0s, 599s, 600s, 601s)
    # -------------------------------------------------------------------------

    def test_adv_06_commitment_device_boundary_seconds_0_599_600_601(self):
        """Exhaustively verify 10-minute commitment device status at critical boundary seconds."""
        # Point 1: Exact Start (0s)
        s0 = get_commitment_device_status(elapsed_seconds=0)
        self.assertEqual(s0["total_duration_seconds"], 600)
        self.assertEqual(s0["elapsed_seconds"], 0)
        self.assertEqual(s0["remaining_seconds"], 600)
        self.assertFalse(s0["is_expired"])
        self.assertEqual(s0["status"], "ACTIVE")
        self.assertEqual(s0["progress_pct"], 0.0)

        # Point 2: Penultimate Second (599s)
        s599 = get_commitment_device_status(elapsed_seconds=599)
        self.assertEqual(s599["remaining_seconds"], 1)
        self.assertFalse(s599["is_expired"])
        self.assertEqual(s599["status"], "ACTIVE")
        self.assertEqual(s599["progress_pct"], round(599 / 600.0, 4))

        # Point 3: Deadline Second (600s)
        s600 = get_commitment_device_status(elapsed_seconds=600)
        self.assertEqual(s600["remaining_seconds"], 0)
        self.assertEqual(s600["progress_pct"], 1.0)
        # Note: In worker implementation, is_expired is strictly elapsed_seconds > safe_total (600 > 600 is False).
        # Therefore, at second 600 remaining is 0, is_expired is False, and status is ACTIVE.
        self.assertFalse(s600["is_expired"])
        self.assertEqual(s600["status"], "ACTIVE")

        # Point 4: Expiration Second (601s)
        s601 = get_commitment_device_status(elapsed_seconds=601)
        self.assertEqual(s601["remaining_seconds"], 0)
        self.assertTrue(s601["is_expired"])
        self.assertEqual(s601["status"], "EXPIRED")
        self.assertEqual(s601["progress_pct"], 1.0)

    def test_adv_07_commitment_device_negative_and_zero_duration(self):
        """Verify negative elapsed times and zero/negative total duration safeguards."""
        # Negative elapsed seconds clamped to 0
        s_neg = get_commitment_device_status(elapsed_seconds=-100)
        self.assertEqual(s_neg["elapsed_seconds"], 0)
        self.assertEqual(s_neg["remaining_seconds"], 600)
        self.assertFalse(s_neg["is_expired"])

        # Zero or negative total duration clamped to at least 1 second (no ZeroDivisionError)
        for d in [0, -1, -600]:
            s_zero_dur = get_commitment_device_status(elapsed_seconds=0, total_duration_seconds=d)
            self.assertEqual(s_zero_dur["total_duration_seconds"], 1)
            self.assertEqual(s_zero_dur["remaining_seconds"], 1)
            self.assertFalse(s_zero_dur["is_expired"])

    # -------------------------------------------------------------------------
    # 3. VOLATILITY CUSHION: SEVERELY NEGATIVE CUSHION (TTS = 100M VND)
    # -------------------------------------------------------------------------

    def test_adv_08_volatility_cushion_severely_negative_tts_100m(self):
        """TTS = 100M VND vs 540M floor (cushion = -440M VND):
        - Risk zone MUST be RED_DANGER.
        - Action required MUST be URGENT_DE_RISK_50_PCT.
        - CPPI safe capacity is negative, and excess risk must safely equal crypto_vnd (all crypto is excess risk).
        """
        result = calculate_volatility_cushion(
            tts_vnd=100_000_000.0,
            crypto_vnd=80_000_000.0,
            portfolio_daily_atr_pct=0.0310,
            hard_floor_vnd=540_000_000.0,
            k_factor=3.0,
        )

        expected_cushion = -440_000_000.0
        expected_daily_noise = 80_000_000.0 * 0.0310  # 2,480,000 VND
        expected_vcr = expected_cushion / expected_daily_noise  # -177.419...
        expected_safe_cppi = expected_cushion / (3.0 * 0.0310)  # -4,731,182,795.70 VND

        self.assertEqual(result["cushion_vnd"], expected_cushion)
        self.assertEqual(result["daily_noise_vnd"], expected_daily_noise)
        self.assertAlmostEqual(result["vcr_days"], expected_vcr, places=2)
        self.assertEqual(result["risk_zone"], "RED_DANGER")
        self.assertEqual(result["action_required"], "URGENT_DE_RISK_50_PCT")
        self.assertAlmostEqual(result["cppi_max_safe_crypto_vnd"], expected_safe_cppi, delta=100.0)
        # Safe capacity is negative, so max(0, -4.73B) = 0. Excess risk = crypto - 0 = 80M VND
        self.assertEqual(result["excess_risk_vnd"], 80_000_000.0)

    # -------------------------------------------------------------------------
    # 4. VOLATILITY CUSHION: ZERO DAILY ATR (ZERO DIVISION SAFEGUARDS)
    # -------------------------------------------------------------------------

    def test_adv_09_volatility_cushion_zero_daily_atr(self):
        """Zero daily ATR (portfolio_daily_atr_pct = 0.0) must not cause ZeroDivisionError.
        - When cushion > 0: vcr_days = 999.0, risk_zone = GREEN_SAFE.
        - When cushion < 0: vcr_days = -999.0, risk_zone = RED_DANGER.
        - When cushion == 0: vcr_days = 0.0, risk_zone = RED_DANGER.
        """
        # Case A: Cushion positive (+10M) with 0 ATR
        res_pos = calculate_volatility_cushion(
            tts_vnd=550_000_000.0,
            crypto_vnd=400_000_000.0,
            portfolio_daily_atr_pct=0.0,
            hard_floor_vnd=540_000_000.0,
        )
        self.assertEqual(res_pos["daily_noise_vnd"], 0.0)
        self.assertEqual(res_pos["vcr_days"], 999.0)
        self.assertEqual(res_pos["risk_zone"], "GREEN_SAFE")
        self.assertEqual(res_pos["action_required"], "HOLD_OR_GLIDEPATH")

        # Case B: Cushion negative (-40M) with 0 ATR
        res_neg = calculate_volatility_cushion(
            tts_vnd=500_000_000.0,
            crypto_vnd=400_000_000.0,
            portfolio_daily_atr_pct=0.0,
            hard_floor_vnd=540_000_000.0,
        )
        self.assertEqual(res_neg["daily_noise_vnd"], 0.0)
        self.assertEqual(res_neg["vcr_days"], -999.0)
        self.assertEqual(res_neg["risk_zone"], "RED_DANGER")
        self.assertEqual(res_neg["action_required"], "URGENT_DE_RISK_50_PCT")

        # Case C: Exact floor breach (0 cushion) with 0 ATR
        res_zero = calculate_volatility_cushion(
            tts_vnd=540_000_000.0,
            crypto_vnd=400_000_000.0,
            portfolio_daily_atr_pct=0.0,
            hard_floor_vnd=540_000_000.0,
        )
        self.assertEqual(res_zero["daily_noise_vnd"], 0.0)
        self.assertEqual(res_zero["vcr_days"], 0.0)
        self.assertEqual(res_zero["risk_zone"], "RED_DANGER")

    # -------------------------------------------------------------------------
    # 5. VOLATILITY CUSHION: ZERO CRYPTO (100% CASH PORTFOLIO)
    # -------------------------------------------------------------------------

    def test_adv_10_volatility_cushion_zero_crypto(self):
        """100% cash portfolio (crypto_vnd = 0.0) must not cause ZeroDivisionError."""
        # Case A: 100% cash with TTS > floor
        res_cash_safe = calculate_volatility_cushion(
            tts_vnd=600_000_000.0,
            crypto_vnd=0.0,
            portfolio_daily_atr_pct=0.0310,
            hard_floor_vnd=540_000_000.0,
        )
        self.assertEqual(res_cash_safe["daily_noise_vnd"], 0.0)
        self.assertEqual(res_cash_safe["vcr_days"], 999.0)
        self.assertEqual(res_cash_safe["risk_zone"], "GREEN_SAFE")
        self.assertEqual(res_cash_safe["excess_risk_vnd"], 0.0)

        # Case B: 100% cash with TTS < floor (severe distress)
        res_cash_breach = calculate_volatility_cushion(
            tts_vnd=500_000_000.0,
            crypto_vnd=0.0,
            portfolio_daily_atr_pct=0.0310,
            hard_floor_vnd=540_000_000.0,
        )
        self.assertEqual(res_cash_breach["daily_noise_vnd"], 0.0)
        self.assertEqual(res_cash_breach["vcr_days"], -999.0)
        self.assertEqual(res_cash_breach["risk_zone"], "RED_DANGER")
        self.assertEqual(res_cash_breach["excess_risk_vnd"], 0.0)

    # -------------------------------------------------------------------------
    # 6. CPPI LIMITS & DEGENERATE PORTFOLIO INPUTS
    # -------------------------------------------------------------------------

    def test_adv_11_cppi_multiplier_edge_cases(self):
        """k_factor = 0 or negative must be clamped to at least 0.1, preventing ZeroDivisionError."""
        for bad_k in [0.0, -1.0, -100.0]:
            res = calculate_volatility_cushion(
                tts_vnd=550_000_000.0,
                crypto_vnd=400_000_000.0,
                portfolio_daily_atr_pct=0.0310,
                hard_floor_vnd=540_000_000.0,
                k_factor=bad_k,
            )
            # Safe k is clamped to 0.1
            expected_safe_cap = 10_000_000.0 / (0.1 * 0.0310)
            self.assertAlmostEqual(res["cppi_max_safe_crypto_vnd"], expected_safe_cap, delta=100.0)

    def test_adv_12_degenerate_tts_inputs(self):
        """TTS = 0 or negative net worth (TTS < 0) must evaluate safely with cushion_pct = 0.0."""
        for degen_tts in [0.0, -50_000_000.0, -1_000_000_000.0]:
            res = calculate_volatility_cushion(
                tts_vnd=degen_tts,
                crypto_vnd=0.0,
                portfolio_daily_atr_pct=0.0310,
                hard_floor_vnd=540_000_000.0,
            )
            self.assertEqual(res["cushion_pct"], 0.0)
            self.assertEqual(res["risk_zone"], "RED_DANGER")
            self.assertEqual(res["vcr_days"], -999.0)

    # -------------------------------------------------------------------------
    # 7. FUZZING / MONTE CARLO RANDOM PARAMETER SWEEP
    # -------------------------------------------------------------------------

    def test_adv_13_stress_fuzzing_500_iterations(self):
        """Runs 500 randomized parameter combinations across both modules to ensure no unexpected crashes."""
        random.seed(42)
        for _ in range(500):
            # Fuzz hesitation tax
            hours = random.uniform(-100.0, 20000.0)
            fee = random.uniform(-1e9, 1e10)
            unexec = random.randint(-10, 50)
            slip = random.uniform(-1e7, 1e8)

            tax_res = calculate_hesitation_tax(
                land_fee_vnd=fee,
                hours_delayed=hours,
                unexecuted_count=unexec,
                market_slippage_loss_vnd=slip,
            )
            self.assertIn(tax_res["status_level"], ["NORMAL", "WARNING", "DEFCON_1_PARALYSIS"])
            self.assertGreaterEqual(tax_res["tax_late_penalty_vnd"], 0.0)
            self.assertGreaterEqual(tax_res["land_2027_hazard_exposure_vnd"], 0.0)
            self.assertLessEqual(tax_res["land_2027_hazard_exposure_vnd"], LAND_2027_HAZARD_MAX_VND)

            # Fuzz commitment device
            elapsed = random.randint(-100, 2000)
            total = random.randint(-50, 1200)
            comm_res = get_commitment_device_status(elapsed_seconds=elapsed, total_duration_seconds=total)
            self.assertIn(comm_res["status"], ["ACTIVE", "EXPIRED"])
            self.assertGreaterEqual(comm_res["remaining_seconds"], 0)

            # Fuzz volatility cushion
            tts = random.uniform(-1e8, 2e9)
            crypto = random.uniform(0.0, max(0.0, tts) + 1e8)
            atr_pct = random.uniform(0.0, 0.5)
            floor = random.uniform(1e8, 1e9)
            k = random.uniform(-5.0, 10.0)

            cush_res = calculate_volatility_cushion(
                tts_vnd=tts,
                crypto_vnd=crypto,
                portfolio_daily_atr_pct=atr_pct,
                hard_floor_vnd=floor,
                k_factor=k,
            )
            self.assertIn(cush_res["risk_zone"], ["RED_DANGER", "YELLOW_CAUTION", "GREEN_SAFE"])
            self.assertIn(cush_res["action_required"], ["URGENT_DE_RISK_50_PCT", "TRIM_RISK_TO_SAFE_CAP", "HOLD_OR_GLIDEPATH"])
            self.assertGreaterEqual(cush_res["excess_risk_vnd"], 0.0)


if __name__ == "__main__":
    unittest.main()
