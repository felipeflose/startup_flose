"""
Pytest unit test suite for UI Solution: floseup_22_card_id_floseup_22_pico_pai_fl_2a76fb.
"""
import pytest
from flose.solutions.floseup_22_card_id_floseup_22_pico_pai_fl_2a76fb import Floseup22CardIdFloseup22PicoPaiFl2a76fbSolution

def test_hex_to_hsl_conversion():
    sol = Floseup22CardIdFloseup22PicoPaiFl2a76fbSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup22CardIdFloseup22PicoPaiFl2a76fbSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
