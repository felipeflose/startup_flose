"""
Pytest unit test suite for UI Solution: floseup_54_card_id_floseup_54_pico_pai_fl_d52520.
"""
import pytest
from flose.solutions.floseup_54_card_id_floseup_54_pico_pai_fl_d52520 import Floseup54CardIdFloseup54PicoPaiFlD52520Solution

def test_hex_to_hsl_conversion():
    sol = Floseup54CardIdFloseup54PicoPaiFlD52520Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup54CardIdFloseup54PicoPaiFlD52520Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
