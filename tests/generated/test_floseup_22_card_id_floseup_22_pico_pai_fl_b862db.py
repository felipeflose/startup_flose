"""
Pytest unit test suite for UI Solution: floseup_22_card_id_floseup_22_pico_pai_fl_b862db.
"""
import pytest
from flose.solutions.floseup_22_card_id_floseup_22_pico_pai_fl_b862db import Floseup22CardIdFloseup22PicoPaiFlB862dbSolution

def test_hex_to_hsl_conversion():
    sol = Floseup22CardIdFloseup22PicoPaiFlB862dbSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup22CardIdFloseup22PicoPaiFlB862dbSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
