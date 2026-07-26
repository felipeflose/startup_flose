"""
Pytest unit test suite for UI Solution: floseup_13_card_id_floseup_13_pico_pai_fl_0be14b.
"""
import pytest
from flose.solutions.floseup_13_card_id_floseup_13_pico_pai_fl_0be14b import Floseup13CardIdFloseup13PicoPaiFl0be14bSolution

def test_hex_to_hsl_conversion():
    sol = Floseup13CardIdFloseup13PicoPaiFl0be14bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup13CardIdFloseup13PicoPaiFl0be14bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
