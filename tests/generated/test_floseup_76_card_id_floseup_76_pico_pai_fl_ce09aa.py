"""
Pytest unit test suite for UI Solution: floseup_76_card_id_floseup_76_pico_pai_fl_ce09aa.
"""
import pytest
from flose.solutions.floseup_76_card_id_floseup_76_pico_pai_fl_ce09aa import Floseup76CardIdFloseup76PicoPaiFlCe09aaSolution

def test_hex_to_hsl_conversion():
    sol = Floseup76CardIdFloseup76PicoPaiFlCe09aaSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup76CardIdFloseup76PicoPaiFlCe09aaSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
