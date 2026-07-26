"""
Pytest unit test suite for UI Solution: floseup_12_ast_real_refatorar_src_flose_s_c6485c.
"""
import pytest
from flose.solutions.floseup_12_ast_real_refatorar_src_flose_s_c6485c import Floseup12AstRealRefatorarSrcFloseSC6485cSolution

def test_hex_to_hsl_conversion():
    sol = Floseup12AstRealRefatorarSrcFloseSC6485cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup12AstRealRefatorarSrcFloseSC6485cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
