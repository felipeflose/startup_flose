"""
Pytest unit test suite for UI Solution: floseup_121_card_id_floseup_121_pico_pai_f_48445b.
"""
import pytest
from flose.solutions.floseup_121_card_id_floseup_121_pico_pai_f_48445b import Floseup121CardIdFloseup121PicoPaiF48445bSolution

def test_hex_to_hsl_conversion():
    sol = Floseup121CardIdFloseup121PicoPaiF48445bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup121CardIdFloseup121PicoPaiF48445bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
