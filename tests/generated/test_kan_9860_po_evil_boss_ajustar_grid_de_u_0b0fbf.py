"""
Pytest unit test suite for UI Solution: kan_9860_po_evil_boss_ajustar_grid_de_u_0b0fbf.
"""
import pytest
from flose.solutions.kan_9860_po_evil_boss_ajustar_grid_de_u_0b0fbf import Kan9860PoEvilBossAjustarGridDeU0b0fbfSolution

def test_hex_to_hsl_conversion():
    sol = Kan9860PoEvilBossAjustarGridDeU0b0fbfSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9860PoEvilBossAjustarGridDeU0b0fbfSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
