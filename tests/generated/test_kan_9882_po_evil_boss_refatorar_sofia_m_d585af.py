"""
Pytest unit test suite for UI Solution: kan_9882_po_evil_boss_refatorar_sofia_m_d585af.
"""
import pytest
from flose.solutions.kan_9882_po_evil_boss_refatorar_sofia_m_d585af import Kan9882PoEvilBossRefatorarSofiaMD585afSolution

def test_hex_to_hsl_conversion():
    sol = Kan9882PoEvilBossRefatorarSofiaMD585afSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9882PoEvilBossRefatorarSofiaMD585afSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
