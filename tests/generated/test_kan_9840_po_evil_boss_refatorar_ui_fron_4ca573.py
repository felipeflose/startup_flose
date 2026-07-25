"""
Pytest unit test suite for UI Solution: kan_9840_po_evil_boss_refatorar_ui_fron_4ca573.
"""
import pytest
from flose.solutions.kan_9840_po_evil_boss_refatorar_ui_fron_4ca573 import Kan9840PoEvilBossRefatorarUiFron4ca573Solution

def test_hex_to_hsl_conversion():
    sol = Kan9840PoEvilBossRefatorarUiFron4ca573Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9840PoEvilBossRefatorarUiFron4ca573Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
