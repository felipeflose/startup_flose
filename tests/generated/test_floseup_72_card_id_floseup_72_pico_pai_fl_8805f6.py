"""
Pytest unit test suite for UI Solution: floseup_72_card_id_floseup_72_pico_pai_fl_8805f6.
"""
import pytest
from flose.solutions.floseup_72_card_id_floseup_72_pico_pai_fl_8805f6 import Floseup72CardIdFloseup72PicoPaiFl8805f6Solution

def test_hex_to_hsl_conversion():
    sol = Floseup72CardIdFloseup72PicoPaiFl8805f6Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup72CardIdFloseup72PicoPaiFl8805f6Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
