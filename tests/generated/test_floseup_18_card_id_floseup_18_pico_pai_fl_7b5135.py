"""
Pytest unit test suite for UI Solution: floseup_18_card_id_floseup_18_pico_pai_fl_7b5135.
"""
import pytest
from flose.solutions.floseup_18_card_id_floseup_18_pico_pai_fl_7b5135 import Floseup18CardIdFloseup18PicoPaiFl7b5135Solution

def test_hex_to_hsl_conversion():
    sol = Floseup18CardIdFloseup18PicoPaiFl7b5135Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup18CardIdFloseup18PicoPaiFl7b5135Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
