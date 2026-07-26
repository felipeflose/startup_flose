"""
Pytest unit test suite for UI Solution: floseup_66_card_id_floseup_66_pico_pai_fl_2285f3.
"""
import pytest
from flose.solutions.floseup_66_card_id_floseup_66_pico_pai_fl_2285f3 import Floseup66CardIdFloseup66PicoPaiFl2285f3Solution

def test_hex_to_hsl_conversion():
    sol = Floseup66CardIdFloseup66PicoPaiFl2285f3Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup66CardIdFloseup66PicoPaiFl2285f3Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
