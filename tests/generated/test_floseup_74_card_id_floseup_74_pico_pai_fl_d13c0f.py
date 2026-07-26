"""
Pytest unit test suite for UI Solution: floseup_74_card_id_floseup_74_pico_pai_fl_d13c0f.
"""
import pytest
from flose.solutions.floseup_74_card_id_floseup_74_pico_pai_fl_d13c0f import Floseup74CardIdFloseup74PicoPaiFlD13c0fSolution

def test_hex_to_hsl_conversion():
    sol = Floseup74CardIdFloseup74PicoPaiFlD13c0fSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup74CardIdFloseup74PicoPaiFlD13c0fSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
