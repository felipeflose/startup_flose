"""
Pytest unit test suite for UI Solution: kan_9880_po_evil_boss_refatorar_sofia_m_ddb6bc.
"""
import pytest
from flose.solutions.kan_9880_po_evil_boss_refatorar_sofia_m_ddb6bc import Kan9880PoEvilBossRefatorarSofiaMDdb6bcSolution

def test_hex_to_hsl_conversion():
    sol = Kan9880PoEvilBossRefatorarSofiaMDdb6bcSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9880PoEvilBossRefatorarSofiaMDdb6bcSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
