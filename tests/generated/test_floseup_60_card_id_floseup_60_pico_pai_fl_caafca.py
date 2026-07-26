"""
Pytest unit test suite for UI Solution: floseup_60_card_id_floseup_60_pico_pai_fl_caafca.
"""
import pytest
from flose.solutions.floseup_60_card_id_floseup_60_pico_pai_fl_caafca import Floseup60CardIdFloseup60PicoPaiFlCaafcaSolution

def test_hex_to_hsl_conversion():
    sol = Floseup60CardIdFloseup60PicoPaiFlCaafcaSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup60CardIdFloseup60PicoPaiFlCaafcaSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
