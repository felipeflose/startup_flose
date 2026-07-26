"""
Pytest unit test suite for UI Solution: floseup_98_card_id_floseup_98_pico_pai_fl_a70419.
"""
import pytest
from flose.solutions.floseup_98_card_id_floseup_98_pico_pai_fl_a70419 import Floseup98CardIdFloseup98PicoPaiFlA70419Solution

def test_hex_to_hsl_conversion():
    sol = Floseup98CardIdFloseup98PicoPaiFlA70419Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup98CardIdFloseup98PicoPaiFlA70419Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
