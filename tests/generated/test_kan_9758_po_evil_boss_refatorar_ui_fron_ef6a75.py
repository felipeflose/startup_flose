"""
Pytest unit test suite for UI Solution: kan_9758_po_evil_boss_refatorar_ui_fron_ef6a75.
"""
import pytest
from flose.solutions.kan_9758_po_evil_boss_refatorar_ui_fron_ef6a75 import Kan9758PoEvilBossRefatorarUiFronEf6a75Solution

def test_hex_to_hsl_conversion():
    sol = Kan9758PoEvilBossRefatorarUiFronEf6a75Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9758PoEvilBossRefatorarUiFronEf6a75Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
