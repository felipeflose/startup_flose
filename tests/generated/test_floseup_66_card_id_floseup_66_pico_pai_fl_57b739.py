"""
Pytest unit test suite for UI Solution: floseup_66_card_id_floseup_66_pico_pai_fl_57b739.
"""
import pytest
from flose.solutions.floseup_66_card_id_floseup_66_pico_pai_fl_57b739 import Floseup66CardIdFloseup66PicoPaiFl57b739Solution

def test_hex_to_hsl_conversion():
    sol = Floseup66CardIdFloseup66PicoPaiFl57b739Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup66CardIdFloseup66PicoPaiFl57b739Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
