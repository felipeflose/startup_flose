"""
Pytest unit test suite for UI Solution: kan_9853_po_frenzy_contrata_o_onboardin_e8ac4c.
"""
import pytest
from flose.solutions.kan_9853_po_frenzy_contrata_o_onboardin_e8ac4c import Kan9853PoFrenzyContrataOOnboardinE8ac4cSolution

def test_hex_to_hsl_conversion():
    sol = Kan9853PoFrenzyContrataOOnboardinE8ac4cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9853PoFrenzyContrataOOnboardinE8ac4cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
