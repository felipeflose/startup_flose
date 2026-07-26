"""
Pytest unit test suite for UI Solution: floseup_62_card_id_floseup_62_pico_pai_fl_195c0c.
"""
import pytest
from flose.solutions.floseup_62_card_id_floseup_62_pico_pai_fl_195c0c import Floseup62CardIdFloseup62PicoPaiFl195c0cSolution

def test_hex_to_hsl_conversion():
    sol = Floseup62CardIdFloseup62PicoPaiFl195c0cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup62CardIdFloseup62PicoPaiFl195c0cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
