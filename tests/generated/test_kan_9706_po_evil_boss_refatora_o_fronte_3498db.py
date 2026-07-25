"""
Pytest unit test suite for UI Solution: kan_9706_po_evil_boss_refatora_o_fronte_3498db.
"""
import pytest
from flose.solutions.kan_9706_po_evil_boss_refatora_o_fronte_3498db import Kan9706PoEvilBossRefatoraOFronte3498dbSolution

def test_hex_to_hsl_conversion():
    sol = Kan9706PoEvilBossRefatoraOFronte3498dbSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9706PoEvilBossRefatoraOFronte3498dbSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
