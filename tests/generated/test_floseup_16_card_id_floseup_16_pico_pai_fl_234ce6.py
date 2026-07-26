"""
Pytest unit test suite for UI Solution: floseup_16_card_id_floseup_16_pico_pai_fl_234ce6.
"""
import pytest
from flose.solutions.floseup_16_card_id_floseup_16_pico_pai_fl_234ce6 import Floseup16CardIdFloseup16PicoPaiFl234ce6Solution

def test_hex_to_hsl_conversion():
    sol = Floseup16CardIdFloseup16PicoPaiFl234ce6Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup16CardIdFloseup16PicoPaiFl234ce6Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
