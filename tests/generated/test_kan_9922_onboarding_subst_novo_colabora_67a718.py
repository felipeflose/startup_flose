"""
Pytest unit test suite for UI Solution: kan_9922_onboarding_subst_novo_colabora_67a718.
"""
import pytest
from flose.solutions.kan_9922_onboarding_subst_novo_colabora_67a718 import Kan9922OnboardingSubstNovoColabora67a718Solution

def test_hex_to_hsl_conversion():
    sol = Kan9922OnboardingSubstNovoColabora67a718Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9922OnboardingSubstNovoColabora67a718Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
