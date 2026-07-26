"""
Pytest unit test suite for UI Solution: floseup_94_card_id_floseup_94_pico_pai_fl_c0a019.
"""
import pytest
from flose.solutions.floseup_94_card_id_floseup_94_pico_pai_fl_c0a019 import Floseup94CardIdFloseup94PicoPaiFlC0a019Solution

def test_hex_to_hsl_conversion():
    sol = Floseup94CardIdFloseup94PicoPaiFlC0a019Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup94CardIdFloseup94PicoPaiFlC0a019Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
