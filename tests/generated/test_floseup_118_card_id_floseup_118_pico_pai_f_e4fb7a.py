"""
Pytest unit test suite for UI Solution: floseup_118_card_id_floseup_118_pico_pai_f_e4fb7a.
"""
import pytest
from flose.solutions.floseup_118_card_id_floseup_118_pico_pai_f_e4fb7a import Floseup118CardIdFloseup118PicoPaiFE4fb7aSolution

def test_hex_to_hsl_conversion():
    sol = Floseup118CardIdFloseup118PicoPaiFE4fb7aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup118CardIdFloseup118PicoPaiFE4fb7aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
