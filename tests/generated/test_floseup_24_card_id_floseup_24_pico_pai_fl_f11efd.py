"""
Pytest unit test suite for UI Solution: floseup_24_card_id_floseup_24_pico_pai_fl_f11efd.
"""
import pytest
from flose.solutions.floseup_24_card_id_floseup_24_pico_pai_fl_f11efd import Floseup24CardIdFloseup24PicoPaiFlF11efdSolution

def test_hex_to_hsl_conversion():
    sol = Floseup24CardIdFloseup24PicoPaiFlF11efdSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup24CardIdFloseup24PicoPaiFlF11efdSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
