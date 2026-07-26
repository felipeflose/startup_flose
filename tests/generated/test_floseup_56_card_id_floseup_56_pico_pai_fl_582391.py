"""
Pytest unit test suite for UI Solution: floseup_56_card_id_floseup_56_pico_pai_fl_582391.
"""
import pytest
from flose.solutions.floseup_56_card_id_floseup_56_pico_pai_fl_582391 import Floseup56CardIdFloseup56PicoPaiFl582391Solution

def test_hex_to_hsl_conversion():
    sol = Floseup56CardIdFloseup56PicoPaiFl582391Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup56CardIdFloseup56PicoPaiFl582391Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
