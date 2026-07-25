"""
Pytest unit test suite for UI Solution: kan_9846_po_frenzy_refatorar_ui_fronten_f37dbb.
"""
import pytest
from flose.solutions.kan_9846_po_frenzy_refatorar_ui_fronten_f37dbb import Kan9846PoFrenzyRefatorarUiFrontenF37dbbSolution

def test_hex_to_hsl_conversion():
    sol = Kan9846PoFrenzyRefatorarUiFrontenF37dbbSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9846PoFrenzyRefatorarUiFrontenF37dbbSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
