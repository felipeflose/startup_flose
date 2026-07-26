"""
Pytest unit test suite for UI Solution: floseup_29_card_id_floseup_29_pico_pai_fl_1fece8.
"""
import pytest
from flose.solutions.floseup_29_card_id_floseup_29_pico_pai_fl_1fece8 import Floseup29CardIdFloseup29PicoPaiFl1fece8Solution

def test_hex_to_hsl_conversion():
    sol = Floseup29CardIdFloseup29PicoPaiFl1fece8Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup29CardIdFloseup29PicoPaiFl1fece8Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
