"""
Pytest unit test suite for UI Solution: floseup_41_card_id_floseup_41_pico_pai_fl_7a152e.
"""
import pytest
from flose.solutions.floseup_41_card_id_floseup_41_pico_pai_fl_7a152e import Floseup41CardIdFloseup41PicoPaiFl7a152eSolution

def test_hex_to_hsl_conversion():
    sol = Floseup41CardIdFloseup41PicoPaiFl7a152eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup41CardIdFloseup41PicoPaiFl7a152eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
