"""
Pytest unit test suite for UI Solution: kan_9908_onboarding_subst_novo_colabora_3d8c11.
"""
import pytest
from flose.solutions.kan_9908_onboarding_subst_novo_colabora_3d8c11 import Kan9908OnboardingSubstNovoColabora3d8c11Solution

def test_hex_to_hsl_conversion():
    sol = Kan9908OnboardingSubstNovoColabora3d8c11Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9908OnboardingSubstNovoColabora3d8c11Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
