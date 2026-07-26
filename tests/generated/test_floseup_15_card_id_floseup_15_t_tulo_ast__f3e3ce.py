"""
Pytest unit test suite for UI Solution: floseup_15_card_id_floseup_15_t_tulo_ast__f3e3ce.
"""
import pytest
from flose.solutions.floseup_15_card_id_floseup_15_t_tulo_ast__f3e3ce import Floseup15CardIdFloseup15TTuloAstF3e3ceSolution

def test_hex_to_hsl_conversion():
    sol = Floseup15CardIdFloseup15TTuloAstF3e3ceSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup15CardIdFloseup15TTuloAstF3e3ceSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
