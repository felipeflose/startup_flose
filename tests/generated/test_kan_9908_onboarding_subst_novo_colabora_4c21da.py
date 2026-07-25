"""
Pytest unit test suite for UI Solution: kan_9908_onboarding_subst_novo_colabora_4c21da.
"""
import pytest
from flose.solutions.kan_9908_onboarding_subst_novo_colabora_4c21da import Kan9908OnboardingSubstNovoColabora4c21daSolution

def test_hex_to_hsl_conversion():
    sol = Kan9908OnboardingSubstNovoColabora4c21daSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9908OnboardingSubstNovoColabora4c21daSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
