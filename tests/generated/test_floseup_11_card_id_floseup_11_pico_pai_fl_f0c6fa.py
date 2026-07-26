"""
Pytest unit test suite for UI Solution: floseup_11_card_id_floseup_11_pico_pai_fl_f0c6fa.
"""
import pytest
from flose.solutions.floseup_11_card_id_floseup_11_pico_pai_fl_f0c6fa import Floseup11CardIdFloseup11PicoPaiFlF0c6faSolution

def test_hex_to_hsl_conversion():
    sol = Floseup11CardIdFloseup11PicoPaiFlF0c6faSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup11CardIdFloseup11PicoPaiFlF0c6faSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
