"""
Pytest unit test suite for UI Solution: floseup_104_card_id_floseup_104_pico_pai_f_027b60.
"""
import pytest
from flose.solutions.floseup_104_card_id_floseup_104_pico_pai_f_027b60 import Floseup104CardIdFloseup104PicoPaiF027b60Solution

def test_hex_to_hsl_conversion():
    sol = Floseup104CardIdFloseup104PicoPaiF027b60Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup104CardIdFloseup104PicoPaiF027b60Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
