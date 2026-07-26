"""
Pytest unit test suite for UI Solution: floseup_82_card_id_floseup_82_pico_pai_fl_d9a7c2.
"""
import pytest
from flose.solutions.floseup_82_card_id_floseup_82_pico_pai_fl_d9a7c2 import Floseup82CardIdFloseup82PicoPaiFlD9a7c2Solution

def test_hex_to_hsl_conversion():
    sol = Floseup82CardIdFloseup82PicoPaiFlD9a7c2Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup82CardIdFloseup82PicoPaiFlD9a7c2Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
