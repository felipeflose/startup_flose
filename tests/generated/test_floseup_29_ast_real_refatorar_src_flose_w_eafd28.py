"""
Pytest unit test suite for UI Solution: floseup_29_ast_real_refatorar_src_flose_w_eafd28.
"""
import pytest
from flose.solutions.floseup_29_ast_real_refatorar_src_flose_w_eafd28 import Floseup29AstRealRefatorarSrcFloseWEafd28Solution

def test_hex_to_hsl_conversion():
    sol = Floseup29AstRealRefatorarSrcFloseWEafd28Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup29AstRealRefatorarSrcFloseWEafd28Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
