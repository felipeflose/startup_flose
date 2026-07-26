"""
Pytest unit test suite for UI Solution: floseup_110_card_id_floseup_110_pico_pai_f_3390d1.
"""
import pytest
from flose.solutions.floseup_110_card_id_floseup_110_pico_pai_f_3390d1 import Floseup110CardIdFloseup110PicoPaiF3390d1Solution

def test_hex_to_hsl_conversion():
    sol = Floseup110CardIdFloseup110PicoPaiF3390d1Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup110CardIdFloseup110PicoPaiF3390d1Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
