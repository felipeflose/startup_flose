"""
Pytest unit test suite for UI Solution: floseup_116_card_id_floseup_116_pico_pai_f_081ceb.
"""
import pytest
from flose.solutions.floseup_116_card_id_floseup_116_pico_pai_f_081ceb import Floseup116CardIdFloseup116PicoPaiF081cebSolution

def test_hex_to_hsl_conversion():
    sol = Floseup116CardIdFloseup116PicoPaiF081cebSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup116CardIdFloseup116PicoPaiF081cebSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
