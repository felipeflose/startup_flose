"""
Pytest unit test suite for UI Solution: floseup_113_card_id_floseup_113_pico_pai_f_4aa85d.
"""
import pytest
from flose.solutions.floseup_113_card_id_floseup_113_pico_pai_f_4aa85d import Floseup113CardIdFloseup113PicoPaiF4aa85dSolution

def test_hex_to_hsl_conversion():
    sol = Floseup113CardIdFloseup113PicoPaiF4aa85dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup113CardIdFloseup113PicoPaiF4aa85dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
