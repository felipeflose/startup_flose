"""
Pytest unit test suite for UI Solution: kan_9752_po_evil_boss_contrata_o_onboar_1e4a78.
"""
import pytest
from flose.solutions.kan_9752_po_evil_boss_contrata_o_onboar_1e4a78 import Kan9752PoEvilBossContrataOOnboar1e4a78Solution

def test_hex_to_hsl_conversion():
    sol = Kan9752PoEvilBossContrataOOnboar1e4a78Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9752PoEvilBossContrataOOnboar1e4a78Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
