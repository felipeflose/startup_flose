"""
Pytest unit test suite for UI Solution: floseup_32_card_id_floseup_32_pico_pai_fl_ce112c.
"""
import pytest
from flose.solutions.floseup_32_card_id_floseup_32_pico_pai_fl_ce112c import Floseup32CardIdFloseup32PicoPaiFlCe112cSolution

def test_hex_to_hsl_conversion():
    sol = Floseup32CardIdFloseup32PicoPaiFlCe112cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup32CardIdFloseup32PicoPaiFlCe112cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
