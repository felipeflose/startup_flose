"""
Pytest unit test suite for UI Solution: floseup_31_card_id_floseup_31_pico_pai_fl_c8dae9.
"""
import pytest
from flose.solutions.floseup_31_card_id_floseup_31_pico_pai_fl_c8dae9 import Floseup31CardIdFloseup31PicoPaiFlC8dae9Solution

def test_hex_to_hsl_conversion():
    sol = Floseup31CardIdFloseup31PicoPaiFlC8dae9Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup31CardIdFloseup31PicoPaiFlC8dae9Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
