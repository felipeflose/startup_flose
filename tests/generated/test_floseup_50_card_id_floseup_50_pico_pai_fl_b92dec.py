"""
Pytest unit test suite for UI Solution: floseup_50_card_id_floseup_50_pico_pai_fl_b92dec.
"""
import pytest
from flose.solutions.floseup_50_card_id_floseup_50_pico_pai_fl_b92dec import Floseup50CardIdFloseup50PicoPaiFlB92decSolution

def test_hex_to_hsl_conversion():
    sol = Floseup50CardIdFloseup50PicoPaiFlB92decSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup50CardIdFloseup50PicoPaiFlB92decSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
