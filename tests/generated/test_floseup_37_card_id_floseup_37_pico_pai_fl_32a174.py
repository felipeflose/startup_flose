"""
Pytest unit test suite for UI Solution: floseup_37_card_id_floseup_37_pico_pai_fl_32a174.
"""
import pytest
from flose.solutions.floseup_37_card_id_floseup_37_pico_pai_fl_32a174 import Floseup37CardIdFloseup37PicoPaiFl32a174Solution

def test_hex_to_hsl_conversion():
    sol = Floseup37CardIdFloseup37PicoPaiFl32a174Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup37CardIdFloseup37PicoPaiFl32a174Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
