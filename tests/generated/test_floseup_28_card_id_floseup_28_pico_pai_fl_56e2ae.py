"""
Pytest unit test suite for UI Solution: floseup_28_card_id_floseup_28_pico_pai_fl_56e2ae.
"""
import pytest
from flose.solutions.floseup_28_card_id_floseup_28_pico_pai_fl_56e2ae import Floseup28CardIdFloseup28PicoPaiFl56e2aeSolution

def test_hex_to_hsl_conversion():
    sol = Floseup28CardIdFloseup28PicoPaiFl56e2aeSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup28CardIdFloseup28PicoPaiFl56e2aeSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
