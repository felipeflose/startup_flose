"""
Pytest unit test suite for UI Solution: floseup_25_card_id_floseup_25_pico_pai_fl_756914.
"""
import pytest
from flose.solutions.floseup_25_card_id_floseup_25_pico_pai_fl_756914 import Floseup25CardIdFloseup25PicoPaiFl756914Solution

def test_hex_to_hsl_conversion():
    sol = Floseup25CardIdFloseup25PicoPaiFl756914Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup25CardIdFloseup25PicoPaiFl756914Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
