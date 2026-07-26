"""
Pytest unit test suite for UI Solution: floseup_86_card_id_floseup_86_pico_pai_fl_26fde3.
"""
import pytest
from flose.solutions.floseup_86_card_id_floseup_86_pico_pai_fl_26fde3 import Floseup86CardIdFloseup86PicoPaiFl26fde3Solution

def test_hex_to_hsl_conversion():
    sol = Floseup86CardIdFloseup86PicoPaiFl26fde3Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup86CardIdFloseup86PicoPaiFl26fde3Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
