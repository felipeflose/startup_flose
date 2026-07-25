"""
Pytest unit test suite for UI Solution: kan_9700_po_evil_boss_refatorar_ui_fron_4f7fa3.
"""
import pytest
from flose.solutions.kan_9700_po_evil_boss_refatorar_ui_fron_4f7fa3 import Kan9700PoEvilBossRefatorarUiFron4f7fa3Solution

def test_hex_to_hsl_conversion():
    sol = Kan9700PoEvilBossRefatorarUiFron4f7fa3Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9700PoEvilBossRefatorarUiFron4f7fa3Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
