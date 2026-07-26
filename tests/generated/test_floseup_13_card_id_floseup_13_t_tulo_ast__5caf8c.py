"""
Pytest unit test suite for UI Solution: floseup_13_card_id_floseup_13_t_tulo_ast__5caf8c.
"""
import pytest
from flose.solutions.floseup_13_card_id_floseup_13_t_tulo_ast__5caf8c import Floseup13CardIdFloseup13TTuloAst5caf8cSolution

def test_hex_to_hsl_conversion():
    sol = Floseup13CardIdFloseup13TTuloAst5caf8cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup13CardIdFloseup13TTuloAst5caf8cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
