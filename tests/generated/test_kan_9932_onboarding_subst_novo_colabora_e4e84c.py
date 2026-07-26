"""
Pytest unit test suite for UI Solution: kan_9932_onboarding_subst_novo_colabora_e4e84c.
"""
import pytest
from flose.solutions.kan_9932_onboarding_subst_novo_colabora_e4e84c import Kan9932OnboardingSubstNovoColaboraE4e84cSolution

def test_hex_to_hsl_conversion():
    sol = Kan9932OnboardingSubstNovoColaboraE4e84cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9932OnboardingSubstNovoColaboraE4e84cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
