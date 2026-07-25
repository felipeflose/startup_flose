"""
Pytest unit test suite for UI Solution: kan_9924_onboarding_subst_novo_colabora_d662de.
"""
import pytest
from flose.solutions.kan_9924_onboarding_subst_novo_colabora_d662de import Kan9924OnboardingSubstNovoColaboraD662deSolution

def test_hex_to_hsl_conversion():
    sol = Kan9924OnboardingSubstNovoColaboraD662deSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9924OnboardingSubstNovoColaboraD662deSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
