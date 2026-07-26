"""
Pytest unit test suite for UI Solution: floseup_27_card_id_floseup_27_t_tulo_ast__072b31.
"""
import pytest
from flose.solutions.floseup_27_card_id_floseup_27_t_tulo_ast__072b31 import Floseup27CardIdFloseup27TTuloAst072b31Solution

def test_hex_to_hsl_conversion():
    sol = Floseup27CardIdFloseup27TTuloAst072b31Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup27CardIdFloseup27TTuloAst072b31Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
