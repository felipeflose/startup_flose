"""
Pytest unit test suite for UI Solution: floseup_78_card_id_floseup_78_pico_pai_fl_395025.
"""
import pytest
from flose.solutions.floseup_78_card_id_floseup_78_pico_pai_fl_395025 import Floseup78CardIdFloseup78PicoPaiFl395025Solution

def test_hex_to_hsl_conversion():
    sol = Floseup78CardIdFloseup78PicoPaiFl395025Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup78CardIdFloseup78PicoPaiFl395025Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
