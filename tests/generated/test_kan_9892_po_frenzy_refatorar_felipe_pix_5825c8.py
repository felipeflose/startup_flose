"""
Pytest unit test suite for UI Solution: kan_9892_po_frenzy_refatorar_felipe_pix_5825c8.
"""
import pytest
from flose.solutions.kan_9892_po_frenzy_refatorar_felipe_pix_5825c8 import Kan9892PoFrenzyRefatorarFelipePix5825c8Solution

def test_hex_to_hsl_conversion():
    sol = Kan9892PoFrenzyRefatorarFelipePix5825c8Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9892PoFrenzyRefatorarFelipePix5825c8Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
