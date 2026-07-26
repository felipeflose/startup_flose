"""
Pytest unit test suite for UI Solution: floseup_26_card_id_floseup_26_pico_pai_fl_a46b94.
"""
import pytest
from flose.solutions.floseup_26_card_id_floseup_26_pico_pai_fl_a46b94 import Floseup26CardIdFloseup26PicoPaiFlA46b94Solution

def test_hex_to_hsl_conversion():
    sol = Floseup26CardIdFloseup26PicoPaiFlA46b94Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup26CardIdFloseup26PicoPaiFlA46b94Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
