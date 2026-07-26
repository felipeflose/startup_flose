"""
Pytest unit test suite for UI Solution: floseup_29_ast_real_refatorar_src_flose_w_21b48f.
"""
import pytest
from flose.solutions.floseup_29_ast_real_refatorar_src_flose_w_21b48f import Floseup29AstRealRefatorarSrcFloseW21b48fSolution

def test_hex_to_hsl_conversion():
    sol = Floseup29AstRealRefatorarSrcFloseW21b48fSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup29AstRealRefatorarSrcFloseW21b48fSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
