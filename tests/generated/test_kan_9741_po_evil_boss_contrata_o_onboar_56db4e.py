"""
Pytest unit test suite for UI Solution: kan_9741_po_evil_boss_contrata_o_onboar_56db4e.
"""
import pytest
from flose.solutions.kan_9741_po_evil_boss_contrata_o_onboar_56db4e import Kan9741PoEvilBossContrataOOnboar56db4eSolution

def test_hex_to_hsl_conversion():
    sol = Kan9741PoEvilBossContrataOOnboar56db4eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9741PoEvilBossContrataOOnboar56db4eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
