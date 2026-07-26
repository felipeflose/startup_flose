"""
Pytest unit test suite for UI Solution: floseup_20_card_id_floseup_20_pico_pai_fl_0067c1.
"""
import pytest
from flose.solutions.floseup_20_card_id_floseup_20_pico_pai_fl_0067c1 import Floseup20CardIdFloseup20PicoPaiFl0067c1Solution

def test_hex_to_hsl_conversion():
    sol = Floseup20CardIdFloseup20PicoPaiFl0067c1Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup20CardIdFloseup20PicoPaiFl0067c1Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
