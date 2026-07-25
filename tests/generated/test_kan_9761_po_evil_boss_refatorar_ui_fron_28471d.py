"""
Pytest unit test suite for UI Solution: kan_9761_po_evil_boss_refatorar_ui_fron_28471d.
"""
import pytest
from flose.solutions.kan_9761_po_evil_boss_refatorar_ui_fron_28471d import Kan9761PoEvilBossRefatorarUiFron28471dSolution

def test_hex_to_hsl_conversion():
    sol = Kan9761PoEvilBossRefatorarUiFron28471dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9761PoEvilBossRefatorarUiFron28471dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
