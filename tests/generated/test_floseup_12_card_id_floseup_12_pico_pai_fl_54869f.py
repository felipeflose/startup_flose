"""
Pytest unit test suite for UI Solution: floseup_12_card_id_floseup_12_pico_pai_fl_54869f.
"""
import pytest
from flose.solutions.floseup_12_card_id_floseup_12_pico_pai_fl_54869f import Floseup12CardIdFloseup12PicoPaiFl54869fSolution

def test_hex_to_hsl_conversion():
    sol = Floseup12CardIdFloseup12PicoPaiFl54869fSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup12CardIdFloseup12PicoPaiFl54869fSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
