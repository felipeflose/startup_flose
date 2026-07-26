"""
Pytest unit test suite for UI Solution: floseup_32_card_id_floseup_32_pico_pai_fl_7bf2f2.
"""
import pytest
from flose.solutions.floseup_32_card_id_floseup_32_pico_pai_fl_7bf2f2 import Floseup32CardIdFloseup32PicoPaiFl7bf2f2Solution

def test_hex_to_hsl_conversion():
    sol = Floseup32CardIdFloseup32PicoPaiFl7bf2f2Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup32CardIdFloseup32PicoPaiFl7bf2f2Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
