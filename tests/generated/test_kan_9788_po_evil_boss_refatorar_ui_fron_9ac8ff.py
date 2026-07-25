"""
Pytest unit test suite for UI Solution: kan_9788_po_evil_boss_refatorar_ui_fron_9ac8ff.
"""
import pytest
from flose.solutions.kan_9788_po_evil_boss_refatorar_ui_fron_9ac8ff import Kan9788PoEvilBossRefatorarUiFron9ac8ffSolution

def test_hex_to_hsl_conversion():
    sol = Kan9788PoEvilBossRefatorarUiFron9ac8ffSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9788PoEvilBossRefatorarUiFron9ac8ffSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
