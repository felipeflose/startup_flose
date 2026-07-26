"""
Pytest unit test suite for UI Solution: floseup_96_card_id_floseup_96_pico_pai_fl_0af0d3.
"""
import pytest
from flose.solutions.floseup_96_card_id_floseup_96_pico_pai_fl_0af0d3 import Floseup96CardIdFloseup96PicoPaiFl0af0d3Solution

def test_hex_to_hsl_conversion():
    sol = Floseup96CardIdFloseup96PicoPaiFl0af0d3Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup96CardIdFloseup96PicoPaiFl0af0d3Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
