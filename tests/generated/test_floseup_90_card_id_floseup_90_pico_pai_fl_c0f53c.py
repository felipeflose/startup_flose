"""
Pytest unit test suite for UI Solution: floseup_90_card_id_floseup_90_pico_pai_fl_c0f53c.
"""
import pytest
from flose.solutions.floseup_90_card_id_floseup_90_pico_pai_fl_c0f53c import Floseup90CardIdFloseup90PicoPaiFlC0f53cSolution

def test_hex_to_hsl_conversion():
    sol = Floseup90CardIdFloseup90PicoPaiFlC0f53cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup90CardIdFloseup90PicoPaiFlC0f53cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
