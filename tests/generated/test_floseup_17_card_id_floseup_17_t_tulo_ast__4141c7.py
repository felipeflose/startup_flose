"""
Pytest unit test suite for UI Solution: floseup_17_card_id_floseup_17_t_tulo_ast__4141c7.
"""
import pytest
from flose.solutions.floseup_17_card_id_floseup_17_t_tulo_ast__4141c7 import Floseup17CardIdFloseup17TTuloAst4141c7Solution

def test_hex_to_hsl_conversion():
    sol = Floseup17CardIdFloseup17TTuloAst4141c7Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup17CardIdFloseup17TTuloAst4141c7Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
