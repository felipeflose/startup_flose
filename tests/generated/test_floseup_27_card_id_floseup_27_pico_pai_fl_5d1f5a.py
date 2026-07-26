"""
Pytest unit test suite for UI Solution: floseup_27_card_id_floseup_27_pico_pai_fl_5d1f5a.
"""
import pytest
from flose.solutions.floseup_27_card_id_floseup_27_pico_pai_fl_5d1f5a import Floseup27CardIdFloseup27PicoPaiFl5d1f5aSolution

def test_hex_to_hsl_conversion():
    sol = Floseup27CardIdFloseup27PicoPaiFl5d1f5aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup27CardIdFloseup27PicoPaiFl5d1f5aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
