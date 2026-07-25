"""
Pytest unit test suite for UI Solution: kan_9700_po_evil_boss_refatorar_ui_fron_92d35e.
"""
import pytest
from flose.solutions.kan_9700_po_evil_boss_refatorar_ui_fron_92d35e import Kan9700PoEvilBossRefatorarUiFron92d35eSolution

def test_hex_to_hsl_conversion():
    sol = Kan9700PoEvilBossRefatorarUiFron92d35eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9700PoEvilBossRefatorarUiFron92d35eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
