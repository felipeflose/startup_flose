"""
Pytest unit test suite for UI Solution: floseup_26_card_id_floseup_26_t_tulo_ast__8ee80d.
"""
import pytest
from flose.solutions.floseup_26_card_id_floseup_26_t_tulo_ast__8ee80d import Floseup26CardIdFloseup26TTuloAst8ee80dSolution

def test_hex_to_hsl_conversion():
    sol = Floseup26CardIdFloseup26TTuloAst8ee80dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup26CardIdFloseup26TTuloAst8ee80dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
