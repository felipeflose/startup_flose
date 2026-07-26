"""
Pytest unit test suite for UI Solution: floseup_52_card_id_floseup_52_pico_pai_fl_52b42b.
"""
import pytest
from flose.solutions.floseup_52_card_id_floseup_52_pico_pai_fl_52b42b import Floseup52CardIdFloseup52PicoPaiFl52b42bSolution

def test_hex_to_hsl_conversion():
    sol = Floseup52CardIdFloseup52PicoPaiFl52b42bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup52CardIdFloseup52PicoPaiFl52b42bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
