"""
Pytest unit test suite for UI Solution: kan_9920_onboarding_subst_novo_colabora_d098c9.
"""
import pytest
from flose.solutions.kan_9920_onboarding_subst_novo_colabora_d098c9 import Kan9920OnboardingSubstNovoColaboraD098c9Solution

def test_hex_to_hsl_conversion():
    sol = Kan9920OnboardingSubstNovoColaboraD098c9Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9920OnboardingSubstNovoColaboraD098c9Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
