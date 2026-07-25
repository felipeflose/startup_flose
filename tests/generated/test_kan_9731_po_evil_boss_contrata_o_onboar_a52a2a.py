"""
Pytest unit test suite for UI Solution: kan_9731_po_evil_boss_contrata_o_onboar_a52a2a.
"""
import pytest
from flose.solutions.kan_9731_po_evil_boss_contrata_o_onboar_a52a2a import Kan9731PoEvilBossContrataOOnboarA52a2aSolution

def test_hex_to_hsl_conversion():
    sol = Kan9731PoEvilBossContrataOOnboarA52a2aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9731PoEvilBossContrataOOnboarA52a2aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
