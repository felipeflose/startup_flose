"""
Pytest unit test suite for UI Solution: floseup_120_card_id_floseup_120_pico_pai_f_1d0571.
"""
import pytest
from flose.solutions.floseup_120_card_id_floseup_120_pico_pai_f_1d0571 import Floseup120CardIdFloseup120PicoPaiF1d0571Solution

def test_hex_to_hsl_conversion():
    sol = Floseup120CardIdFloseup120PicoPaiF1d0571Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup120CardIdFloseup120PicoPaiF1d0571Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
