"""
Pytest unit test suite for UI Solution: floseup_84_card_id_floseup_84_pico_pai_fl_b74440.
"""
import pytest
from flose.solutions.floseup_84_card_id_floseup_84_pico_pai_fl_b74440 import Floseup84CardIdFloseup84PicoPaiFlB74440Solution

def test_hex_to_hsl_conversion():
    sol = Floseup84CardIdFloseup84PicoPaiFlB74440Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup84CardIdFloseup84PicoPaiFlB74440Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
