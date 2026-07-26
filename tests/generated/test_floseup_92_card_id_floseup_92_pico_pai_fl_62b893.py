"""
Pytest unit test suite for UI Solution: floseup_92_card_id_floseup_92_pico_pai_fl_62b893.
"""
import pytest
from flose.solutions.floseup_92_card_id_floseup_92_pico_pai_fl_62b893 import Floseup92CardIdFloseup92PicoPaiFl62b893Solution

def test_hex_to_hsl_conversion():
    sol = Floseup92CardIdFloseup92PicoPaiFl62b893Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup92CardIdFloseup92PicoPaiFl62b893Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
