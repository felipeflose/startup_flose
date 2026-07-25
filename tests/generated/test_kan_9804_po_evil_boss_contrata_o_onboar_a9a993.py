"""
Pytest unit test suite for UI Solution: kan_9804_po_evil_boss_contrata_o_onboar_a9a993.
"""
import pytest
from flose.solutions.kan_9804_po_evil_boss_contrata_o_onboar_a9a993 import Kan9804PoEvilBossContrataOOnboarA9a993Solution

def test_hex_to_hsl_conversion():
    sol = Kan9804PoEvilBossContrataOOnboarA9a993Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9804PoEvilBossContrataOOnboarA9a993Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
