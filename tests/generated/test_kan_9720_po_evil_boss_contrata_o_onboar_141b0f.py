"""
Pytest unit test suite for UI Solution: kan_9720_po_evil_boss_contrata_o_onboar_141b0f.
"""
import pytest
from flose.solutions.kan_9720_po_evil_boss_contrata_o_onboar_141b0f import Kan9720PoEvilBossContrataOOnboar141b0fSolution

def test_hex_to_hsl_conversion():
    sol = Kan9720PoEvilBossContrataOOnboar141b0fSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9720PoEvilBossContrataOOnboar141b0fSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
