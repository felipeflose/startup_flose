"""
Pytest unit test suite for UI Solution: floseup_23_card_id_floseup_23_t_tulo_ast__b62633.
"""
import pytest
from flose.solutions.floseup_23_card_id_floseup_23_t_tulo_ast__b62633 import Floseup23CardIdFloseup23TTuloAstB62633Solution

def test_hex_to_hsl_conversion():
    sol = Floseup23CardIdFloseup23TTuloAstB62633Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup23CardIdFloseup23TTuloAstB62633Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
