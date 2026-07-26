"""
Pytest unit test suite for UI Solution: floseup_88_card_id_floseup_88_pico_pai_fl_dd2613.
"""
import pytest
from flose.solutions.floseup_88_card_id_floseup_88_pico_pai_fl_dd2613 import Floseup88CardIdFloseup88PicoPaiFlDd2613Solution

def test_hex_to_hsl_conversion():
    sol = Floseup88CardIdFloseup88PicoPaiFlDd2613Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup88CardIdFloseup88PicoPaiFlDd2613Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
