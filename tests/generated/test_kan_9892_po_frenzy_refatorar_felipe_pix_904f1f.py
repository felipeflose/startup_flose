"""
Pytest unit test suite for UI Solution: kan_9892_po_frenzy_refatorar_felipe_pix_904f1f.
"""
import pytest
from flose.solutions.kan_9892_po_frenzy_refatorar_felipe_pix_904f1f import Kan9892PoFrenzyRefatorarFelipePix904f1fSolution

def test_hex_to_hsl_conversion():
    sol = Kan9892PoFrenzyRefatorarFelipePix904f1fSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9892PoFrenzyRefatorarFelipePix904f1fSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
