"""
Pytest unit test suite for UI Solution: floseup_17_ast_real_refatorar_src_flose_w_c4b2b3.
"""
import pytest
from flose.solutions.floseup_17_ast_real_refatorar_src_flose_w_c4b2b3 import Floseup17AstRealRefatorarSrcFloseWC4b2b3Solution

def test_hex_to_hsl_conversion():
    sol = Floseup17AstRealRefatorarSrcFloseWC4b2b3Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup17AstRealRefatorarSrcFloseWC4b2b3Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
