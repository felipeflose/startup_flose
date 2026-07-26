"""
Pytest unit test suite for UI Solution: floseup_28_card_id_floseup_28_t_tulo_ast__ead2ec.
"""
import pytest
from flose.solutions.floseup_28_card_id_floseup_28_t_tulo_ast__ead2ec import Floseup28CardIdFloseup28TTuloAstEad2ecSolution

def test_hex_to_hsl_conversion():
    sol = Floseup28CardIdFloseup28TTuloAstEad2ecSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup28CardIdFloseup28TTuloAstEad2ecSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
