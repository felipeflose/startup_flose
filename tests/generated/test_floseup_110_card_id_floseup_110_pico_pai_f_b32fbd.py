"""
Pytest unit test suite for UI Solution: floseup_110_card_id_floseup_110_pico_pai_f_b32fbd.
"""
import pytest
from flose.solutions.floseup_110_card_id_floseup_110_pico_pai_f_b32fbd import Floseup110CardIdFloseup110PicoPaiFB32fbdSolution

def test_hex_to_hsl_conversion():
    sol = Floseup110CardIdFloseup110PicoPaiFB32fbdSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup110CardIdFloseup110PicoPaiFB32fbdSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
