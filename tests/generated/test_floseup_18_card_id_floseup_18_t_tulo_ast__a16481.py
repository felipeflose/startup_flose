"""
Pytest unit test suite for UI Solution: floseup_18_card_id_floseup_18_t_tulo_ast__a16481.
"""
import pytest
from flose.solutions.floseup_18_card_id_floseup_18_t_tulo_ast__a16481 import Floseup18CardIdFloseup18TTuloAstA16481Solution

def test_hex_to_hsl_conversion():
    sol = Floseup18CardIdFloseup18TTuloAstA16481Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup18CardIdFloseup18TTuloAstA16481Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
