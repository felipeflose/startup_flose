"""
Pytest unit test suite for UI Solution: floseup_18_card_id_floseup_18_pico_pai_fl_aecc57.
"""
import pytest
from flose.solutions.floseup_18_card_id_floseup_18_pico_pai_fl_aecc57 import Floseup18CardIdFloseup18PicoPaiFlAecc57Solution

def test_hex_to_hsl_conversion():
    sol = Floseup18CardIdFloseup18PicoPaiFlAecc57Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup18CardIdFloseup18PicoPaiFlAecc57Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
