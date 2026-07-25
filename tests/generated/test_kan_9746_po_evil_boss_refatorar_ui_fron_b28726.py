"""
Pytest unit test suite for UI Solution: kan_9746_po_evil_boss_refatorar_ui_fron_b28726.
"""
import pytest
from flose.solutions.kan_9746_po_evil_boss_refatorar_ui_fron_b28726 import Kan9746PoEvilBossRefatorarUiFronB28726Solution

def test_hex_to_hsl_conversion():
    sol = Kan9746PoEvilBossRefatorarUiFronB28726Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9746PoEvilBossRefatorarUiFronB28726Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
