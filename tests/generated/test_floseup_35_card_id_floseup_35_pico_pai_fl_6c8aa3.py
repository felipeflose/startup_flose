"""
Pytest unit test suite for UI Solution: floseup_35_card_id_floseup_35_pico_pai_fl_6c8aa3.
"""
import pytest
from flose.solutions.floseup_35_card_id_floseup_35_pico_pai_fl_6c8aa3 import Floseup35CardIdFloseup35PicoPaiFl6c8aa3Solution

def test_hex_to_hsl_conversion():
    sol = Floseup35CardIdFloseup35PicoPaiFl6c8aa3Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup35CardIdFloseup35PicoPaiFl6c8aa3Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
