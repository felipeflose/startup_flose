"""
Pytest unit test suite for UI Solution: floseup_84_card_id_floseup_84_pico_pai_fl_4c71ca.
"""
import pytest
from flose.solutions.floseup_84_card_id_floseup_84_pico_pai_fl_4c71ca import Floseup84CardIdFloseup84PicoPaiFl4c71caSolution

def test_hex_to_hsl_conversion():
    sol = Floseup84CardIdFloseup84PicoPaiFl4c71caSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup84CardIdFloseup84PicoPaiFl4c71caSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
