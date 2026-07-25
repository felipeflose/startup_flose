"""
Pytest unit test suite for UI Solution: kan_9799_po_evil_boss_refatorar_ui_fron_b1e9bd.
"""
import pytest
from flose.solutions.kan_9799_po_evil_boss_refatorar_ui_fron_b1e9bd import Kan9799PoEvilBossRefatorarUiFronB1e9bdSolution

def test_hex_to_hsl_conversion():
    sol = Kan9799PoEvilBossRefatorarUiFronB1e9bdSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9799PoEvilBossRefatorarUiFronB1e9bdSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
