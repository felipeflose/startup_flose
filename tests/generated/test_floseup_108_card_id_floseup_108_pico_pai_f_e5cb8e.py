"""
Pytest unit test suite for UI Solution: floseup_108_card_id_floseup_108_pico_pai_f_e5cb8e.
"""
import pytest
from flose.solutions.floseup_108_card_id_floseup_108_pico_pai_f_e5cb8e import Floseup108CardIdFloseup108PicoPaiFE5cb8eSolution

def test_hex_to_hsl_conversion():
    sol = Floseup108CardIdFloseup108PicoPaiFE5cb8eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup108CardIdFloseup108PicoPaiFE5cb8eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
