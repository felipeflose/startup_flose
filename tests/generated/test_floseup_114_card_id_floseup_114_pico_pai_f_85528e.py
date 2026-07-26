"""
Pytest unit test suite for UI Solution: floseup_114_card_id_floseup_114_pico_pai_f_85528e.
"""
import pytest
from flose.solutions.floseup_114_card_id_floseup_114_pico_pai_f_85528e import Floseup114CardIdFloseup114PicoPaiF85528eSolution

def test_hex_to_hsl_conversion():
    sol = Floseup114CardIdFloseup114PicoPaiF85528eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup114CardIdFloseup114PicoPaiF85528eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
