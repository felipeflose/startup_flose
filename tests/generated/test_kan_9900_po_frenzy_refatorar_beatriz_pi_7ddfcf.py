"""
Pytest unit test suite for UI Solution: kan_9900_po_frenzy_refatorar_beatriz_pi_7ddfcf.
"""
import pytest
from flose.solutions.kan_9900_po_frenzy_refatorar_beatriz_pi_7ddfcf import Kan9900PoFrenzyRefatorarBeatrizPi7ddfcfSolution

def test_hex_to_hsl_conversion():
    sol = Kan9900PoFrenzyRefatorarBeatrizPi7ddfcfSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9900PoFrenzyRefatorarBeatrizPi7ddfcfSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
