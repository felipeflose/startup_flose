"""
Pytest unit test suite for UI Solution: kan_9920_onboarding_subst_novo_colabora_25c1c2.
"""
import pytest
from flose.solutions.kan_9920_onboarding_subst_novo_colabora_25c1c2 import Kan9920OnboardingSubstNovoColabora25c1c2Solution

def test_hex_to_hsl_conversion():
    sol = Kan9920OnboardingSubstNovoColabora25c1c2Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9920OnboardingSubstNovoColabora25c1c2Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
