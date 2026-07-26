"""
Pytest unit test suite for UI Solution: floseup_106_card_id_floseup_106_pico_pai_f_c03e9b.
"""
import pytest
from flose.solutions.floseup_106_card_id_floseup_106_pico_pai_f_c03e9b import Floseup106CardIdFloseup106PicoPaiFC03e9bSolution

def test_hex_to_hsl_conversion():
    sol = Floseup106CardIdFloseup106PicoPaiFC03e9bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup106CardIdFloseup106PicoPaiFC03e9bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
