"""
Pytest unit test suite for UI Solution: floseup_58_card_id_floseup_58_pico_pai_fl_36b906.
"""
import pytest
from flose.solutions.floseup_58_card_id_floseup_58_pico_pai_fl_36b906 import Floseup58CardIdFloseup58PicoPaiFl36b906Solution

def test_hex_to_hsl_conversion():
    sol = Floseup58CardIdFloseup58PicoPaiFl36b906Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup58CardIdFloseup58PicoPaiFl36b906Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
