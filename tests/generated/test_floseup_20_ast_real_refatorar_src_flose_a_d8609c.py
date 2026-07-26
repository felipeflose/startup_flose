"""
Pytest unit test suite for UI Solution: floseup_20_ast_real_refatorar_src_flose_a_d8609c.
"""
import pytest
from flose.solutions.floseup_20_ast_real_refatorar_src_flose_a_d8609c import Floseup20AstRealRefatorarSrcFloseAD8609cSolution

def test_hex_to_hsl_conversion():
    sol = Floseup20AstRealRefatorarSrcFloseAD8609cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup20AstRealRefatorarSrcFloseAD8609cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
